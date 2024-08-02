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
    'brasileirao': 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/brasil-33/brasileiro-a-102838',
    'brasileiraob': 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/brasil-33/brasileiro-b-102361',
    'brasileiraoc': 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/brasil-33/brasileiro-c-102155',
    'copadobrasil': 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/brasil-33/copa-do-brasil-102723',
    'inglaterra1': 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/inglaterra-14/premier-league-102841',
    'argentina1': 'https://sports.sportingbet.com/pt-br/sports/futebol-4/aposta/argentina-38/campeonato-argentino-102540'
}

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'

    if not campeonato_nome in urls:
        return casa_sem_campeonato()


    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Betano."

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

    infos = df.loc[df.aa_classList.str.contains('event-group collapsible ng-star-inserted', regex=True, na=False)].aa_innerText

    horario = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for dia in infos:
        if pd.isna(dia):
            continue
        dia_split = dia.splitlines()
        dia_split = dia_split[7:]
        while dia_split:
            if len(dia_split) > 10 and dia_split[10].replace('.', '', 1).isdigit():
                dia_split.pop(4)
            if not dia_split[4].replace('.', '', 1).isdigit():
                dia_split = dia_split[4:]
            if not is_number(dia_split[8]):
                dia_split = dia_split[8:]
                continue
            time1.append(dia_split[0])
            time2.append(dia_split[1])
            horario.append(re.findall(r'(\d+:\d\d)', dia_split[2]))
            if not re.search(r'\d', dia_split[3]):
                dia_split.pop(3)
            odd1.append(dia_split[3])
            oddX.append(dia_split[4])
            odd2.append(dia_split[5])
            dia_split = dia_split[9:]

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