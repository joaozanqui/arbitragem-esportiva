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

urls = {
    'brasileirao': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:325',
    'brasileiraob': 'https://www.sportybet.com/br/sport/football/sr:category:top/sr:tournament:390',
    'brasileiraoc': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:1281',
    'brasileiraod': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:15335',
    'copadobrasil': 'https://www.sportybet.com/br/sport/football/sr:category:13/sr:tournament:373',
    'inglaterra1': 'https://www.sportybet.com/br/sport/football/sr:category:1/sr:tournament:17',
    'espanha1': 'https://www.sportybet.com/br/sport/football/sr:category:32/sr:tournament:8',
    'argentina1': 'https://www.sportybet.com/br/sport/football/sr:category:48/sr:tournament:155',
    'libertadores': 'https://www.sportybet.com/br/sport/football/sr:category:top/sr:tournament:384'
}

def processar_campeonato(campeonato_nome):

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da SportyBet."

    # #Raspagem online
    # driver = Driver(uc=True)
    # driver.get(url)
    # time.sleep(10)
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
    with open(pasta_casas + 'casas-html/sportybet.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/sportybet.html')
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

    dftime = df.loc[df.aa_classList.str.contains('clock-time', regex=True, na=False)]
    dftime = dftime.aa_innerText

    dfteams = df.loc[df.aa_classList.str.contains('teams', regex=True, na=False)]
    dfteams = dfteams.aa_innerText.str.split("\n", expand=True, regex=False)

    dfodds = df.loc[df.aa_classList.str.contains('m-market market', regex=True, na=False) & df.aa_innerHTML.str.contains('<!----> <div', regex=True, na=False)]
    dfodds = dfodds.aa_innerText.str.split("\n", expand=True, regex=False)
    # for coluna in dfodds:
    #     for i, (odd) in enumerate(dfodds[coluna]):
    #         dfodds[coluna][i] = float(dfodds[coluna].iloc[i])

    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)

    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato