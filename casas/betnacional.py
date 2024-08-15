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
    'brasileirao': 'https://betnacional.com/events/1/0/325',
    'brasileiraob': 'https://betnacional.com/events/1/0/390',
    'brasileiraoc': 'https://betnacional.com/events/1/0/1281',
    'brasileiraod': 'https://betnacional.com/events/1/0/15335',
    'copadobrasil': 'https://betnacional.com/events/1/0/373',
    'inglaterra1': 'https://betnacional.com/events/1/0/17',
    'espanha1': 'https://betnacional.com/events/1/0/8',
    'argentina1': 'https://betnacional.com/events/1/0/155',
    'libertadores': 'https://betnacional.com/events/1/0/384'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'
    driver = Driver(uc=True)

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Betnacional."

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

    dfinfos = df.loc[df.aa_outerHTML.str.contains('data-testid="preMatchOdds"', regex=True, na=False) & df['aa_innerText'].str.contains(r'^\d{2}:\d{2}', regex=True)].aa_innerText

    horario = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for info in dfinfos:
        info_split = info.splitlines()
        horario.append(info_split[0])
        times = info_split[1].split(' x ')
        time1.append(times[0])
        time2.append(times[1])
        odd1.append(info_split[2])
        oddX.append(info_split[3])
        odd2.append(info_split[4])

    dftime = pd.DataFrame({
        'horario': horario,
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