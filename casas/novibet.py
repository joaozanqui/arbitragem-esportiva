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
    pasta_casas = ''
else:
    pasta_casas = 'casas/'

from renomear_times import renomear
from campeonato_vazio import casa_sem_campeonato

urls = {
    'brasileirao': 'https://br.novibet.com/apostas-esportivas/brazil-football/4795946/competitions?ids=4930337',
    'brasileiraob': 'https://br.novibet.com/apostas-esportivas/brazil-football/4795946/brazil/serie-b/4930439',
    'inglaterra1': 'https://br.novibet.com/apostas-esportivas/top-league/5855201/competitions?ids=5865266',
    'espanha1': 'https://br.novibet.com/apostas-esportivas/top-league/5855201/spain/laliga/5855115',
    'argentina1': 'https://br.novibet.com/apostas-esportivas/futebol/4372606/argentina/liga-profesional/4380918',
    'libertadores': 'https://br.novibet.com/apostas-esportivas/futebol-internacional/5484280/competitions?ids=5484305'
}

def is_number(item):
    return bool(re.fullmatch(r'^[0-9:]+$', item))

def processar_campeonato(campeonato_nome):
    # campeonato_nome = 'libertadores'
    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do Esportes da Sorte."

    driver_to_save = Driver(uc=True)
    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/novibet.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/novibet.html')
    driver.get(f"file://{caminho_html}")
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

    infos = df.loc[df.aa_classList.str.contains("event u-flex", na=False, regex=True)].aa_innerText
    horarios = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for info in infos:
        info_split = info.splitlines()
        if info_split[2] == "SO":
            info_split.pop(2)
        if not is_number(info_split[3]):
            info_split.pop(3)
        time1.append(info_split[0])
        time2.append(info_split[1])
        if is_number(info_split[2]):
            horarios.append(info_split[2])
        else:
            horarios.append(info_split[2].split(' ')[1])
        odd1.append(info_split[4])
        oddX.append(info_split[6])
        odd2.append(info_split[8])

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