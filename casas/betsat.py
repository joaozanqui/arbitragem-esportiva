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
    'brasileirao': 'https://br.betsat.com/prejogo/#leagues/2417-undefined',
    'brasileiraob': 'https://br.betsat.com/prejogo/#league/2418-undefined',
    'brasileiraoc': 'https://br.betsat.com/prejogo/#league/2850-undefined',
    'inglaterra1': 'https://br.betsat.com/prejogo/#leagues/46-undefined',
    'espanha1': 'https://br.betsat.com/prejogo/#league/117-undefined',
    'argentina1': 'https://br.betsat.com/prejogo/#leagues/596-undefined',
    'libertadores': 'https://br.betsat.com/prejogo/#leagues/2572-undefined'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'libertadores'
    driver = Driver(uc=True)

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Betano."

    driver.get(url)
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

    infos = df.loc[df.aa_classList.str.contains("odds_tr", na=False, regex=True)].aa_innerText
    horarios = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for info in infos:
        info_split = info.splitlines()
        horarios.append(info_split[1])
        time1.append(info_split[3].split('-')[0])
        time2.append(info_split[3].split('-')[1])
        odd1.append(info_split[6])
        oddX.append(info_split[8])
        odd2.append(info_split[10])

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