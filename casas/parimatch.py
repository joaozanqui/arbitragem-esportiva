from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from selenium.common.exceptions import NoSuchElementException, WebDriverException

from PrettyColorPrinter import add_printer
import time
import sys
import re
import os

add_printer(True)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pasta_casas = ''
else:
    pasta_casas = 'casas/'

from renomear_times import renomear
from login import conta

urls = {
    'brasileirao': 'https://br.parimatch.com/pt/football/serie-a-0f7c91bcf24e4d62a76e7d9d3fee8177/prematch',
    'brasileiraob': 'https://br.parimatch.com/pt/football/serie-b-dd8f2355b4e3459090ebbcb6db9c7854/prematch',
    'brasileiraoc': 'https://br.parimatch.com/pt/football/serie-c-ac49b9f8662d4beea16360a570b41421/prematch',
    'brasileiraod': 'https://br.parimatch.com/pt/football/serie-d-8ccb46c09f4844fc9b1b2440ef9ab501/prematch',
    'copadobrasil': 'https://br.parimatch.com/pt/football/cup-58ca48f32a8d4ae1addaf40de59f724b/prematch',
    'inglaterra1': 'https://br.parimatch.com/pt/football/premier-league-7f5506e872d14928adf0613efa509494/prematch',
    'espanha1': 'https://br.parimatch.com/pt/football/laliga-d84ce93378454b0fa61d58b2696a950b/prematch',
    'argentina1': 'https://br.parimatch.com/pt/football/primera-division-1bcb9cbd374a481faa39bd89c66bdcab/prematch',
    'libertadores': 'https://br.parimatch.com/pt/football/copa-libertadores-ddccbf1be9ef4c8195ae4645d793899f/prematch'
}


def has_only_numbers(text):
    pattern = r'^(\d+(\.\d+)?\n)*\d+(\.\d+)?$'
    return bool(re.match(pattern, str(text)))

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'inglaterra1'

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da parimatch."

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

    if(campeonato_nome == 'libertadores'):
        df.loc[df.aa_classList.str.contains('modulor_list-cell__element__1_49_0', regex=True, na=False) & df.aa_textContent.str.contains('ibertadores', regex=True, na=False)].iloc[0].se_click()
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

    dftime = df.loc[df.aa_classList.str.contains('styles_time-status__Y2C9z', regex=True, na=False)].aa_textContent.str.extract(r'(\d+:\d\d)', expand=False)

    dfteams = df.loc[df.aa_classList.str.contains('styles_competitors__UgcxV', regex=True, na=False)]
    times = dfteams['aa_innerText'].reset_index(drop=True)
    time1 = []
    time2 = []
    for each_time in times:
        time_split = each_time.splitlines()
        time1.append(time_split[0])
        time2.append(time_split[1])

    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})

    dfodds = df.loc[df.aa_outerHTML.str.contains('data-id="modulor-typography"', regex=True, na=False)]
    dfodds = dfodds[dfodds['aa_innerText'].apply(has_only_numbers) & (dfodds['aa_offsetHeight'] == 34)].aa_innerText

    if dfodds.empty:
        dfodds = df.loc[df.aa_classList.str.contains('styles_markets-wrapper__l9k-w', regex=True, na=False)].aa_innerText
        odd1 = []
        oddX = []
        odd2 = []
        for odd in dfodds:
            odd_split = odd.splitlines()
            odd1.append(odd_split[0])
            oddX.append(odd_split[2])
            odd2.append(odd_split[4])
    else:
        odds = []
        for odd in dfodds:
            odd_split = odd.splitlines()
            odds.append(odd_split[1])
        odd1 = odds[::3]
        oddX = odds[1::3]
        odd2 = odds[2::3]

    dfodds = pd.DataFrame({
        'odd1': odd1,
        'oddX': oddX,
        'odd2': odd2
    })

    for line in dfodds:
        for i, (odd) in enumerate(dfodds[line]):
            nova_odd = float(odd)*0.98397
            dfodds[line][i] = round(nova_odd, 2)


    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)

    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato