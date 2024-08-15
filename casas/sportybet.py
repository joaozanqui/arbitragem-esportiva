import time

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

urls = {
    'brasileirao': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:325',
    'brasileiraob': 'https://www.sportybet.com/br/sport/football/sr:category:top/sr:tournament:390',
    'brasileiraoc': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:1281',
    'brasileiraod': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:15335',
    'copadobrasil': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:373',
    'inglaterra1': 'https://www.sportybet.com/br/sport/football/sr:category:1/sr:tournament:17',
    'argentina1': 'https://www.sportybet.com/br/sport/football/sr:category:48/sr:tournament:155',
    'libertadores': 'https://www.sportybet.com/br/sport/football/sr:category:top/sr:tournament:384'
}

def processar_campeonato(campeonato_nome):
    driver = Driver(uc=True)

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da SportyBet."

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

    dftime = df.loc[df.aa_classList.str.contains('clock-time', regex=True, na=False)]
    dftime = dftime.aa_innerText

    dfteams = df.loc[df.aa_classList.str.contains('teams', regex=True, na=False)]
    dfteams = dfteams.aa_innerText.str.split("\n", expand=True, regex=False)

    dfodds = df.loc[df.aa_classList.str.contains('m-market market', regex=True, na=False) & df.aa_innerHTML.str.contains('<!----> <div', regex=True, na=False)]
    dfodds = dfodds.aa_innerText.str.split("\n", expand=True, regex=False)
    # for coluna in dfodds:
    #     for i, (odd) in enumerate(dfodds[coluna]):
    #         dfodds[coluna][i] = float(dfodds[coluna].iloc[i])

    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)

    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato