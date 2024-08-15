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
    pasta_casas = ''
else:
    pasta_casas = 'casas/'

from renomear_times import renomear
from campeonato_vazio import casa_sem_campeonato

urls = {
    'brasileirao': 'https://www.portugabet.com/home/events-area/s/CLE?group_type=LEAGUE&identifier=sr:tournament:325&name=Brasileir%C3%A3o%20S%C3%A9rie%20A',
    'brasileiraob': 'https://www.portugabet.com/home/events-area/s/CLE?group_type=LEAGUE&identifier=sr:tournament:390&name=Brasileir%C3%A3o%20S%C3%A9rie%20B',
    'brasileiraoc': 'https://www.portugabet.com/home/events-area/s/SC?country=Brasil&championship=Brasileir%C3%A3o%20S%C3%A9rie%20C&championshipId=sr:tournament:1281',
    'inglaterra1': 'https://www.portugabet.com/home/events-area/s/CLE?group_type=LEAGUE&identifier=sr:tournament:17&name=Premier%20League',
    'espanha1': 'https://www.portugabet.com/home/events-area/s/CLE?group_type=LEAGUE&identifier=sr:tournament:8&name=La%20Liga',
    'argentina1': 'https://www.portugabet.com/home/events-area/s/SC?country=Argentina&championship=Liga%20Profissional&championshipId=sr:tournament:155',
    'libertadores': 'https://www.portugabet.com/home/events-area/s/CLE?group_type=LEAGUE&identifier=sr:tournament:384&name=Copa%20Libertadores'
}

def processar_campeonato(campeonato_nome):

    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da PortugaBet."


    # #Raspagem online
    # driver = Driver(uc=True)
    # driver.get(url)
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

    #Raspagem offline
    driver_to_save = Driver(uc=True)
    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/portugabet.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/portugabet.html')
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

    # cookies = df.loc[df.aa_classList.str.contains('mat-focus-indicator cookies-button mat-button mat-button-base', regex=True, na=False)]
    # if not (cookies.empty):
    #     cookies.iloc[0].se_click()

    dfinfos = df.loc[df.aa_classList.str.contains('info-area', regex=True, na=False)].aa_innerText.iloc[:-1]

    informacoes = []
    for data in dfinfos:
        data_split = data.splitlines()
        horario = data_split[0]
        time1 = data_split[1]
        time2 = data_split[2]
        informacoes.append([horario, time1, time2])
    dfteams = pd.DataFrame(informacoes, columns=['horario', 'time1', 'time2'])

    odds = []
    dfodds = df.loc[df.aa_classList.str.contains('odds-area', regex=True, na=False)].aa_innerText
    for odd in dfodds:
        each_odd = odd.splitlines()
        odd1 = each_odd[0]
        oddX = each_odd[1]
        odd2 = each_odd[2]
        odds.append([odd1, oddX, odd2])
    dfodds = pd.DataFrame(odds, columns=['odd1', 'oddX', 'odd2'])

    while dfodds.shape[0] > dfteams.shape[0]:
        dfodds = dfodds.iloc[:-1]

    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)

    campeonato = pd.concat([dfteams, dfodds], axis=1)

    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato