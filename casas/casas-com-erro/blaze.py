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
import re

add_printer(True)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from renomear_times import renomear
from campeonato_vazio import casa_sem_campeonato

urls = {
    'brasileirao': 'https://sportsbet.io/pt/sports/soccer/brazil/brasileiro-serie-a/matches',
    'brasileiraob': 'https://sportsbet.io/pt/sports/soccer/brazil/brasileiro-serie-b/matches',
    'brasileiraoc': 'https://sportsbet.io/pt/sports/soccer/brazil/brasileiro-serie-c/matches'
}

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileiraoc'

    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    driver = Driver(uc=True)

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Betano."


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

    jogos = df.loc[df.aa_classList.str.contains("grid__EventListBodyWrapper-sc-l1d0h4-0 evtRDd", na=False,regex=True)].aa_innerText
    horario = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for jogo in jogos:
        jogo_split = jogo.splitlines()
        if (jogo_split[4] == "INVENTOR"):
            jogo_split.pop(4)
            jogo_split.pop(4)
        time1.append(jogo_split[0])
        time2.append(jogo_split[2])
        horario.append(jogo_split[4].split(' ')[1])
        if not is_float(jogo_split[10]) or not is_float(jogo_split[12]) or not is_float(jogo_split[14]):
            odd1.append(0)
            oddX.append(0)
            odd2.append(0)
        else:
            odd1.append(jogo_split[10])
            oddX.append(jogo_split[12])
            odd2.append(jogo_split[14])

    dftime = pd.DataFrame({'horario': horario})
    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})
    dfodds = pd.DataFrame({'odd1': odd1, 'oddX': oddX, 'odd2': odd2})

    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)

    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato