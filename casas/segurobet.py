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
    'brasileirao': 'https://www.segurobet.com/pre-jogo/match/Soccer/Brazil/1792',
    'brasileiraob': 'https://www.segurobet.com/pre-jogo/match/Soccer/Brazil/3104',
    'brasileiraoc': 'https://www.segurobet.com/pre-jogo/match/Soccer/Brazil/4672',
    'brasileiraod': 'https://www.segurobet.com/pre-jogo/match/Soccer/Brazil/12156',
    'copadobrasil': 'https://www.segurobet.com/pre-jogo/match/Soccer/Brazil/1799',
    'inglaterra1': 'https://www.segurobet.com/pre-jogo/match/Soccer/England/538',
    'espanha1': 'https://www.segurobet.com/pre-jogo/match/Soccer/Spain/545',
    'argentina1': 'https://www.segurobet.com/pre-jogo/match/Soccer/Argentina/1685',
    'libertadores': 'https://www.segurobet.com/pre-jogo/match/Soccer/South%20America/2988'
}

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

    jogos = df.loc[df.aa_classList.str.contains("matchCardInline__moreWagesWrapper", na=False,regex=True)].aa_innerText

    horario = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for jogo in jogos:
        jogo_split = jogo.splitlines()
        time1.append(jogo_split[0])
        time2.append(jogo_split[1])
        odd1.append(jogo_split[2])
        oddX.append(jogo_split[3])
        odd2.append(jogo_split[4])
        horario.append(jogo_split[5])

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