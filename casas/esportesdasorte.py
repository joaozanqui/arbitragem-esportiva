from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
import time
import sys
import os

add_printer(True)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pasta_casas = ''
else:
    pasta_casas = 'casas/'

from renomear_times import renomear
from campeonato_vazio import casa_sem_campeonato

urls = {
    'brasileirao': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/brazil',
    'brasileiraob': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/brazil/brasileiro-serie-b-2024',
    'brasileiraoc': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/brazil/brasileiro-serie-c-2024',
    'copadobrasil': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/brazil/copa-do-brasil-2024',
    'inglaterra1': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/england',
    'espanha1': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/spain',
    'argentina1': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/argentina',
    'libertadores': 'https://m.esportesdasorte.com/ptb/bet/sports/soccer/international-clubs'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'
    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do Esportes da Sorte."


    # #Raspagem online
    # driver = Driver(uc=True)
    # driver.get(url)
    # time.sleep(5)
    # df = pd.DataFrame()
    # while df.empty:
    #     df = get_df(
    #         driver,
    #         By,
    #         WebDriverWait,
    #         expected_conditions,
    #         queryselector="*",
    #         with_methods=True,
    #     )

    #Raspagem Offline
    driver_to_save = Driver(uc=True)
    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/esportes_da_sorte.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/esportes_da_sorte.html')
    driver.get(f"file://{caminho_html}")
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector="*",
            with_methods=True,
        )

    infos = df.loc[df.aa_classList.str.contains('match-content flex-container', regex=True, na=False)].aa_textContent
    retirar = -1
    for i, (jogo) in enumerate(infos):
        if 'Aposte Agora' in jogo:
            retirar = i

    dftime = df.loc[df.aa_classList.str.contains('minutes', regex=True, na=False)].aa_textContent.str.extract(r'(\d+:\d\d)', expand=False)
    dfteams = df.loc[df.aa_classList.str.contains('team-content-info', regex=True, na=False)]
    time1 = dfteams['aa_innerText'][::2].reset_index(drop=True)
    time2 = dfteams['aa_innerText'][1::2].reset_index(drop=True)

    if retirar > -1:
        dftime.pop(dftime.index[retirar])
        time1.pop(retirar)
        time2.pop(retirar)

    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})

    dfodds = df.loc[df.aa_classList.str.contains('bet-btn-odd', regex=True, na=False)]
    odd1 = dfodds['aa_innerText'][::3].reset_index(drop=True)
    oddX = dfodds['aa_innerText'][1::3].reset_index(drop=True)
    odd2 = dfodds['aa_innerText'][2::3].reset_index(drop=True)
    dfodds = pd.DataFrame({
        'odd1': odd1,
        'oddX': oddX,
        'odd2': odd2
    })

    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)

    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato