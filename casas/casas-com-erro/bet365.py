from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer

import sys
import os

add_printer(True)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from renomear_times import renomear


def processar_campeonato(campeonato_nome):
    # campeonato_nome = 'brasileirao'
    driver = Driver(uc=True)

    caminho_html = 'file://' + os.path.expanduser('~/Downloads/bet365 - Apostas Desportivas Online.html')
    driver.get(caminho_html)

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
        
    dftime = df.loc[df.aa_classList.str.contains('rcl-ParticipantFixtureDetails_BookCloses', regex=True, na=False)].aa_innerText

    num_jogos = dftime.shape[0]

    jogos = df.loc[df.aa_classList.str.contains('rcl-ParticipantFixtureDetails_TeamNames', regex=True, na=False)].aa_innerText
    time1 = []
    time2 = []
    for jogo in jogos:
        jogo_split = jogo.splitlines()
        time1.append(jogo_split[0])
        time2.append(jogo_split[1])
        
    dfteams = pd.DataFrame({
        'time1': time1,
        'time2': time2,
    })

    odds = df.loc[df.aa_classList.str.contains('sgl-ParticipantOddsOnly80_Odds', regex=True, na=False)].aa_innerText
    odd1 = odds.head(num_jogos).reset_index(drop=True)
    odds = odds[num_jogos::]
    oddX = odds.head(num_jogos).reset_index(drop=True)
    odds = odds[num_jogos::]
    odd2 = odds.head(num_jogos).reset_index(drop=True)

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