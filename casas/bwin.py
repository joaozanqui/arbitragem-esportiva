from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
import time
import re
import sys
import os

add_printer(True)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pasta_casas = ''
else:
    pasta_casas = 'casas/'

from renomear_times import renomear
from campeonato_vazio import casa_sem_campeonato

urls = {
    'brasileirao': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/brasil-33/brasileiro-a-102838',
    'brasileiraob': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/brasil-33/brasileiro-b-102361',
    'copadobrasil': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/brasil-33/copa-do-brasil-102723',
    'inglaterra1': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/inglaterra-14/premier-league-102841',
    'espanha1': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/espanha-28/laliga-102829',
    'argentina1': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/argentina-38/campeonato-argentino-102540',
    'libertadores': 'https://sports.bwin.com/pt-br/sports/futebol-4/aposta/am%C3%A9rica-do-sul-42/conmebol-libertadores-0:15'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileiraob'
    if not campeonato_nome in urls:
        return casa_sem_campeonato()


    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do Esportes da Sorte."

    driver = Driver(uc=True)
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

    # driver_to_save = Driver(uc=True)
    # driver_to_save.get(url)
    # WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    # time.sleep(10)
    # page_source = driver_to_save.page_source
    # with open(pasta_casas + 'casas-html/bwin.html', 'w', encoding='utf-8') as file:
    #     file.write(page_source)
    # driver_to_save.quit()
    #
    # driver = Driver(uc=True)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # caminho_html = os.path.join(current_dir, 'casas-html/bwin.html')
    # driver.get(f"file://{caminho_html}")
    # df = pd.DataFrame()
    # while df.empty:
    #     df = get_df(
    #         driver,
    #         By,
    #         WebDriverWait,
    #         expected_conditions,
    #         queryselector="*",
    #         with_methods=True,
    #     )

    horarios = df.loc[df.aa_classList.str.contains('event-info-container ng-star-inserted', regex=True, na=False)].aa_innerText.str.extract(r'(\d+:\d\d)', expand=False)

    times = df.loc[df.aa_classList.str.contains('participant-wrapper ng-star-inserted', regex=True, na=False)].aa_innerText
    time1 = times[::2]
    time2 = times[1::2]
    time1 = time1.reset_index(drop=True)
    time2 = time2.reset_index(drop=True)

    odds = df.loc[df.aa_classList.str.contains('grid-option ng-star-inserted', regex=True, na=False)].aa_innerText
    odd1 = odds[::5]
    oddX = odds[1::5]
    odd2 = odds[2::5]
    odd1 = odd1.fillna(0)
    oddX = oddX.fillna(0)
    odd2 = odd2.fillna(0)
    odd1 = odd1.reset_index(drop=True)
    oddX = oddX.reset_index(drop=True)
    odd2 = odd2.reset_index(drop=True)


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