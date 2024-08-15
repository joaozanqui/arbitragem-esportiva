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
    'brasileirao': 'https://pmbet.co.tz/en/sports/prematch/Football/Brazil/Serie%20A/',
    'brasileiraob': 'https://pmbet.co.tz/en/sports/prematch/Football/Brazil/Serie%20B/',
    'brasileiraoc': 'https://pmbet.co.tz/en/sports/prematch/Football/Brazil/Serie%20C/',
    'brasileiraod': 'https://pmbet.co.tz/en/sports/prematch/Football/Brazil/Campeonato%20Brasileiro%20Serie%20D',
    'copadobrasil': 'https://pmbet.co.tz/en/sports/prematch/Football/Brazil/Copa%20do%20Brasil',
    'inglaterra1': 'https://pmbet.co.tz/en/sports/prematch/Football/England/Premier%20League',
    'espanha1': 'https://pmbet.co.tz/en/sports/prematch/Football/Spain/La%20Liga',
    'argentina1': 'https://pmbet.co.tz/en/sports/prematch/Football/Argentina/Liga%20Profesional/',
    'libertadores': 'https://pmbet.co.tz/en/sports/prematch/Football/South%20America/Copa%20Libertadores/'
}

def to_float_or_zero(value):
    try:
        return float(value)
    except ValueError:
        return 0

def processar_campeonato(campeonato_nome):

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da PmBet."

    # #Raspagem online
    # driver = Driver(uc=True)
    # driver.get(url)
    # time.sleep(5)
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
    with open(pasta_casas + 'casas-html/pmbet.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/pmbet.html')
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


    # popup = df.loc[df.aa_classList.str.contains('royal-win-close__button', regex=True, na=False)]
    # if not (popup.empty):
    #     popup.iloc[0].se_click()

    dftime = df.loc[df.aa_classList.str.contains('ev_game__date', regex=True, na=False)].aa_innerText[1::2]

    dfteams = df.loc[df.aa_classList.str.contains('ev_game__teams', regex=True, na=False)].aa_innerText
    time1 = []
    time2 = []
    for i, (jogo) in enumerate(dfteams):
        time1.append(jogo.splitlines()[0])
        time2.append(jogo.splitlines()[1])
    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})

    dfodds = df.loc[df.aa_classList.str.contains('bet_coef', regex=True, na=False)]
    odd1 = dfodds['aa_innerText'][::3].apply(to_float_or_zero).reset_index(drop=True)
    oddX = dfodds['aa_innerText'][1::3].apply(to_float_or_zero).reset_index(drop=True)
    odd2 = dfodds['aa_innerText'][2::3].apply(to_float_or_zero).reset_index(drop=True)
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