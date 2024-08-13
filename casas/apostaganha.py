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

urls = {
    'brasileirao': 'https://www.apostaganha.bet/esportes/futebol/brasil/liga/16478',
    'brasileiraob': 'https://www.apostaganha.bet/esportes/futebol/brasil/liga/16493',
    'brasileiraoc': 'https://www.apostaganha.bet/esportes/futebol/brasil/liga/16724',
    'brasileiraod': 'https://www.apostaganha.bet/esportes/futebol/brasil/liga/16905',
    'copadobrasil': 'https://www.apostaganha.bet/esportes/futebol/brasil/liga/16491',
    'inglaterra1': 'https://www.apostaganha.bet/esportes/futebol/inglaterra/liga/16305',
    'argentina1': 'https://www.apostaganha.bet/esportes/futebol/argentina/liga/20031',
    'libertadores': 'https://apostaganha.bet/esportes/futebol/internacional-clubes/liga/16492'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileiraob'
    driver_to_save = Driver(uc=True)

    try:
       url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do Esportes da Sorte."

    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/apostaganha.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/apostaganha.html')
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
    infos = df.loc[df.aa_classList.str.contains('game-league-content', regex=True, na=False)].aa_innerText[::9]

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
        time1.append(info_split[1])
        time2.append(info_split[2])
        odd1.append(info_split[4])
        oddX.append(info_split[6])
        odd2.append(info_split[8])

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