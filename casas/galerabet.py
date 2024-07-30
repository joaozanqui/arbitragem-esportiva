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
    'brasileirao': 'https://www.galera.bet/sportsbook/sports/soccer/competitions/11431',
    'brasileiraob': 'https://www.galera.bet/sportsbook/sports/soccer/competitions/11427',
    'brasileiraoc': 'https://www.galera.bet/sportsbook/sports/soccer/competitions/12913',
    'brasileiraod': 'https://www.galera.bet/sportsbook/sports/soccer/competitions/13036',
    'inglaterra1': 'https://www.galera.bet/sportsbook/sports/soccer/competitions/10104',
    'argentina1': 'https://www.galera.bet/sportsbook/sports/soccer/competitions/10051'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileiraob'
    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Galerabet."
    driver_to_save = Driver(uc=True)
    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/galerabet.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/galerabet.html')
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

    dftime = df.loc[df.aa_classList.str.contains('ta-Button', regex=True, na=False) & (df.aa_offsetHeight == 24)].aa_innerText.str.extract(r'(\d+:\d\d)', expand=False)

    dfteams = df.loc[df.aa_classList.str.contains('ta-FlexPane ta-Participants', regex=True, na=False)].aa_innerText
    time1 = []
    time2 = []
    for i, (jogo) in enumerate(dfteams):
        time1.append(jogo.splitlines()[0])
        time2.append(jogo.splitlines()[1])
    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})

    # odds_relevantes = [True, True, True, False, False]
    # indices = [odds_relevantes[i % len(odds_relevantes)] for i in range(len(dfodds))]
    # dfodds = dfodds.iloc[indices]
    # odd1 = dfodds[::3].reset_index(drop=True)
    # oddX = dfodds[1::3].reset_index(drop=True)
    # odd2 = dfodds[2::3].reset_index(drop=True)
    dfodds = df.loc[df.aa_classList.str.contains('ta-FlexPane ta-Market', regex=True, na=False)].aa_innerText[::4]
    odd1 = []
    oddX = []
    odd2 = []
    for odds in dfodds:
        odd_split = odds.splitlines()
        for i in [0, 1, 2]:
            if not re.search(r'\d', odd_split[i]):
                odd_split[i] = 0
        odd1.append(odd_split[0])
        oddX.append(odd_split[1])
        odd2.append(odd_split[2])
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