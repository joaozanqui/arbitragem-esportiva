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
    'brasileirao': 'https://www.pinnacle.com/pt/soccer/brazil-serie-a/matchups/#all',
    'brasileiraob': 'https://www.pinnacle.com/pt/soccer/brazil-serie-b/matchups/#all',
    'brasileiraoc': 'https://www.pinnacle.com/pt/soccer/brazil-serie-c/matchups/#all',
    'brasileiraod': 'https://www.pinnacle.com/pt/soccer/brazil-serie-d/matchups/#all',
    'copadobrasil': 'https://www.pinnacle.com/pt/soccer/brazil-cup/matchups/#all',
    'inglaterra1': 'https://www.pinnacle.com/pt/soccer/england-premier-league/matchups/#all',
    'espanha1': 'https://www.pinnacle.com/pt/soccer/spain-la-liga/matchups/#all',
    'argentina1': 'https://www.pinnacle.com/pt/soccer/argentina-liga-pro/matchups/#all',
    'libertadores': 'https://www.pinnacle.com/pt/soccer/conmebol-copa-libertadores/matchups/#all'
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'copadobrasil'

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do Esportes da Sorte."


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
    infos = df.loc[df.aa_classList.str.contains('row-bbd1776fd58233709296 row-d92d06fbd3b09cc856bc', regex=True, na=False)].aa_innerText

    horarios = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for info in infos:
        info_split = info.splitlines()
        if is_number(info_split[1]):
            continue
        if "Partida" not in info_split[0].split(' (')[1] or "Partida" not in info_split[1].split(' (')[1]:
            continue

        horarios.append(info_split[2])
        time1.append(info_split[0].split(' (')[0])
        time2.append(info_split[1].split(' (')[0])
        odd1.append(info_split[3])
        oddX.append(info_split[4])
        odd2.append(info_split[5])


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