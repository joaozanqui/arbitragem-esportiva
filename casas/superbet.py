from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
import time
import re
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
    'brasileirao': 'https://superbet.com/pt-br/sport-bets/football/brazil/brazil-brasileiro-serie-a?ti=1698',
    'brasileiraob': 'https://superbet.com/pt-br/sport-bets/football/brazil/brazil-brasileiro-serie-b?ti=1697',
    'brasileiraoc': 'https://superbet.com/pt-br/sport-bets/football/brazil/brazil-brasileiro-serie-c/all?ti=1696&cpi=1281&ct=m',
    'copadobrasil': 'https://superbet.com/pt-br/sport-bets/football/brazil/brazil-copa-do-brasil?ti=1690',
    # 'inglaterra1': 'https://superbet.com/pt-br/sport-bets/football/england/england-premier-league?ti=106',
    'argentina1': 'https://superbet.com/pt-br/sport-bets/football/argentina/argentina-liga-profesional?ti=1740',
    'libertadores': 'https://superbet.com/pt-br/sport-bets/football/international-clubs/copa-libertadores-playoff/all'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'

    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da SuperBet."

    driver = Driver(uc=True)
    driver.get(url)
    time.sleep(5)
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


    # driver_to_save = Driver(uc=True)
    # driver_to_save.get(url)
    # WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    # time.sleep(5)
    # page_source = driver_to_save.page_source
    # with open(pasta_casas + 'casas-html/superbet.html', 'w', encoding='utf-8') as file:
    #     file.write(page_source)
    # driver_to_save.quit()
    #
    # driver = Driver(uc=True)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # caminho_html = os.path.join(current_dir, 'casas-html/superbet.html')
    # driver.get(f"file://{caminho_html}")
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

    infos = df.loc[df.aa_classList.str.contains('event-card__main-content', regex=True, na=False) & ~df.aa_innerText.str.match(r'^\d', na=False) & ~df.aa_innerText.str.match(r'^HT', na=False)].aa_innerText
    horarios = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for info in infos:
        info_split = info.splitlines()
        if re.search(r'(\d+:\d\d)', info):
            horarios.append(re.search(r'(\d+:\d\d)', info).group(0))
        time1.append(info_split[2])
        time2.append(info_split[3])
        odd_split = info_split[6].split(' ')
        odd1.append(odd_split[0])
        odd_split = info_split[8].split(' ')
        oddX.append(odd_split[0])
        odd_split = info_split[10].split(' ')
        odd2.append(odd_split[0])

    dftime = pd.DataFrame({
        'horario': horarios
    })

    dfteams = pd.DataFrame({
        'time1': time1,
        'time2': time2,
    })
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