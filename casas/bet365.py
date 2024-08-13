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

from renomear_times import renomear

urls = {
    'brasileirao': 'https://www.bet365.com/#/AC/B1/C1/D1002/E88369731/G40/',
    'brasileiraob': 'https://www.bet365.com/#/AC/B1/C1/D1002/E102584281/G40/',
    'inglaterra1': 'https://www.bet365.com/#/AC/B1/C1/D1002/E91422157/F0/G40/',
    'argentina1': 'https://www.bet365.com/#/AC/B1/C1/D1002/E98752003/G40/',
    'libertadores': 'https://www.bet365.com/#/AC/B1/C1/D1002/E101830157/G40/'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = ('brasileirao')
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

    dftime = df.loc[df.aa_classList.str.contains("rcl-ParticipantFixtureDetails_BookCloses", na=False, regex=True)].aa_innerText

    teams = df.loc[df.aa_classList.str.contains("rcl-ParticipantFixtureDetails_TeamNames", na=False, regex=True)].aa_innerText
    quantidade_jogos = teams.size
    time1 = []
    time2 = []
    for team in teams:
        team_split = team.splitlines()
        time1.append(team_split[0])
        time2.append(team_split[1])

    dfteams = pd.DataFrame({
            'time1': time1,
            'time2': time2,
        })

    odds = df.loc[df.aa_classList.str.contains("sgl-ParticipantOddsOnly80_Odds", na=False, regex=True)].aa_innerText
    odd1 = []
    oddX = []
    odd2 = []
    controle = 1
    for odd in odds:
        if controle <= quantidade_jogos:
            odd1.append(odd)
        elif controle <= 2 * quantidade_jogos:
            oddX.append(odd)
        else:
            odd2.append(odd)
        controle += 1

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