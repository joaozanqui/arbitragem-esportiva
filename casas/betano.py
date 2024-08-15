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
    'brasileirao': 'https://br.betano.com/sport/futebol/brasil/brasileirao-serie-a-betano/10016/',
    'brasileiraob': 'https://br.betano.com/sport/futebol/brasil/brasileirao-serie-b/10017/',
    'brasileiraoc': 'https://br.betano.com/sport/futebol/brasil/brasileirao-serie-c/18249/',
    'brasileiraod': 'https://br.betano.com/sport/futebol/competicoes/brasil/10004/?sl=182510',
    'copadobrasil': 'https://br.betano.com/sport/futebol/competicoes/brasil/10004/?sl=10008',
    'inglaterra1': 'https://br.betano.com/sport/futebol/competicoes/inglaterra/1/',
    'espanha1': 'https://br.betano.com/sport/futebol/espanha/laliga/5/',
    'argentina1': 'https://br.betano.com/sport/futebol/competicoes/argentina/11319/',
    'libertadores': 'https://br.betano.com/sport/futebol/competicoes/copa-libertadores/189817/'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'
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

    cookies = df.loc[df.aa_classList.str.contains("uk-button sticky-notification__cta sticky-notification__cta--secondary", na=False, regex=True)]
    popup1 = df.loc[df.aa_classList.str.contains("tw-cursor-pointer tw-uppercase tw-p-n tw-text-white-snow tw-font-bold tw-leading-xs tw-text-xs", na=False, regex=True)]
    popup2 = df.loc[df.aa_classList.str.contains("sb-modal__close__btn uk-modal-close-default uk-icon uk-close", na=False, regex=True)]
    #Fechar cookies
    if not(cookies.empty):
        cookies.iloc[0].se_click()
    #Fechar popup
    if not(popup1.empty):
        popup1.iloc[0].se_click()
    #Fechar popup2
    if not(popup2.empty):
        popup2.iloc[0].se_click()

    dfteams = df.loc[df.aa_classList.str.contains("vue-recycle-scroller__item-view", na=False, regex=True)]
    informacoes = []
    for data in dfteams.aa_innerText:
        data_split = data.splitlines()
        data_split = [item for item in data_split if item != 'SO']
        if data_split[0] == "AO VIVO":
            continue
        if not data_split[4].isdigit():
            data_split.pop(4)

        horario = data_split[1]
        team1 = data_split[2]
        team2 = data_split[3]
        odd1 = data_split[5]
        oddX = data_split[7]
        odd2 = data_split[9]
        (informacoes.append([horario, team1, team2, odd1, oddX, odd2]))

    campeonato = pd.DataFrame(informacoes, columns=['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2'])
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato