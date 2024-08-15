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
    'brasileirao': 'https://br.1x001.com/br/line/football/1268397-brazil-campeonato-brasileiro-serie-a',
    'brasileiraob': 'https://br.1x001.com/br/line/football/57265-brazil-campeonato-brasileiro-serie-b',
    'brasileiraoc': 'https://br.1x001.com/br/line/football/70269-brazil-campeonato-brasileiro-srie-c',
    'inglaterra1': 'https://br.1x001.com/br/line/football/88637-england-premier-league',
    'argentina1': 'https://br.1x001.com/br/line/football/119599-argentina-primera-division',
    'libertadores': 'https://br.1x001.com/br/line/football/142091-copa-libertadores'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = ('libertadores')
    driver = Driver(uc=True)

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Betano."

    driver.get(url)
    time.sleep(10)
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

    dftime = df.loc[df.aa_classList.str.contains("dashboard-game-info__item dashboard-game-info__time", na=False, regex=True)].aa_innerText

    teams = df.loc[df.aa_classList.str.contains("team-scores__teams team-scores-teams", na=False, regex=True) & (df.aa_offsetHeight == 40)].aa_innerText
    time1 = []
    time2 = []
    desconsiderar = []
    for i, (team) in enumerate(teams):
        team_split = team.splitlines()
        if team_split[0] != 'Home' and team_split[1] != 'Away':
            time1.append(team_split[0])
            time2.append(team_split[1])
        else:
            desconsiderar.append(i)

    odd1 = []
    oddX = []
    odd2 = []
    odds = df.loc[df.aa_classList.str.contains("ui-dashboard-markets-cell-group dashboard-markets__group", na=False, regex=True)].aa_innerText
    for i, (odd) in enumerate(odds):
        if i in desconsiderar:
            continue
        odd_split = odd.splitlines()
        odd1.append(odd_split[0])
        oddX.append(odd_split[1])
        odd2.append(odd_split[2])

    dftime = dftime.drop(dftime.index[desconsiderar])

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