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
    'brasileirao': 'https://www.h2bet.com/esportes/match/Soccer/Brazil/1792/',
    'brasileiraob': 'https://www.h2bet.com/esportes/match/Soccer/Brazil/3104/',
    'brasileiraoc': 'https://www.h2bet.com/esportes/match/Soccer/Brazil/4672/25071388',
    'brasileiraod': 'https://www.h2bet.com/esportes/match/Soccer/Brazil/12156/25120617',
    'copadobrasil': 'https://www.h2bet.com/esportes/match/Soccer/Brazil/1799/25170875',
    'inglaterra1': 'https://www.h2bet.com/esportes/match/Soccer/England/538/24949853',
    'espanha1': 'https://www.h2.bet/esportes/match/Soccer/Spain/545/25121899',
    'argentina1': 'https://www.h2bet.com/esportes/match/Soccer/Argentina/1685/25052168',
    'libertadores': 'https://www.h2.bet/esportes/match/Soccer/South%20America/2988/25229209'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'copadobrasil'

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da H2Bet."

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

    #Raspagem Offline
    driver_to_save = Driver(uc=True)
    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/h2bet.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/h2bet.html')
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

    dftime = df.loc[df.aa_classList.str.contains('v3-col col_time', regex=True, na=False)].aa_innerText
    dftime = dftime.reset_index(drop=True)
    dfinfos = df.loc[df.aa_classList.str.contains('style__Wrapper-sc-vig7k4-3 guLYBN mainContentWrapper', regex=True, na=False)].aa_innerText
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    for i, (info) in enumerate(dfinfos):
        info_split = info.splitlines()
        if len(info_split) > 2:
            time1.append(info_split[0])
            time2.append(info_split[1])
            odd1.append(info_split[2])
            oddX.append(info_split[3])
            odd2.append(info_split[4])
        else:
            dftime = dftime.drop(i)


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