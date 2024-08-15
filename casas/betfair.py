from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from selenium.common.exceptions import NoSuchElementException, WebDriverException

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
from login import conta

urls = {
    'brasileirao': 'https://www.betfair.com/apostas/br/futebol/brasileiro-s%C3%A9rie-a/c-13',
    'brasileiraob': 'https://www.betfair.com/apostas/br/futebol/brasileiro-s%C3%A9rie-b/c-321319',
    'brasileiraoc': 'https://www.betfair.com/apostas/br/futebol/brasil-s%C3%A9rie-c/c-3172302',
    'brasileiraod': 'https://www.betfair.com/apostas/br/futebol/brasil-s%C3%A9rie-d/c-7980087',
    'copadobrasil': 'https://www.betfair.com/apostas/br/futebol/copa-do-brasil/c-89219',
    'inglaterra1': 'https://www.betfair.com/apostas/br/futebol/inglaterra-premier-league/c-10932509',
    'espanha1': 'https://www.betfair.com/apostas/br/futebol/espanha-la-liga/c-117',
    'argentina1': 'https://www.betfair.com/apostas/br/futebol/primeira-divis%C3%A3o-da-argentina/c-67387',
    'libertadores': 'https://www.betfair.com/apostas/br/futebol/libertadores/c-12147796'
}


def to_float_or_zero(value):
    if pd.isna(value):
        return 0
    try:
        return float(value)
    except ValueError:
        return 0

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados da Betfair."

    driver_to_save = Driver(uc=True)
    driver_to_save.get(url)
    time.sleep(5)
    df_to_save = pd.DataFrame()
    while df_to_save.empty:
        df_to_save = get_df(
            driver_to_save,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector="*",
            with_methods=True,
        )

    #Copia o arquivo depois de se logar
    df_to_save.loc[df_to_save.aa_id.str.contains('onetrust-reject-all-handler', regex=True, na=False)].iloc[0].se_click()
    # login = df_to_save.loc[df_to_save.aa_classList.str.contains('ssc-itx', regex=True, na=False)]
    # login_id = login.iloc[0]['aa_id']
    # login_element = driver_to_save.find_element(By.ID, login_id)
    # login_element.send_keys(conta['email'])
    # login_id = login.iloc[1]['aa_id']
    # login_element = driver_to_save.find_element(By.ID, login_id)
    # login_element.send_keys(conta['senha'])
    # df_to_save.loc[df_to_save.aa_id.str.contains('ssc-lis', regex=True, na=False)].iloc[0].se_click()


    try:
        time.sleep(5)
        button_to_click = driver_to_save.find_element(By.CLASS_NAME, "_3a-NW")
        button_to_click.uc_click()
        button_to_click.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        button_to_click.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        button_to_click.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)
    except (NoSuchElementException, WebDriverException) as e:
        print(f"Erro ao interagir com o botão ou rolar a página - betfair")
        driver_to_save.quit()  # Fecha o navegador em caso de erro
        exit(1)  # Sai do programa com um código de erro

    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/betfair.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    #Abre o html
    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/betfair.html')
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


    dftime = df.loc[df.aa_classList.str.contains('_3Rfp0 h0Ll2', regex=True, na=False)].aa_innerText.str.extract(r'(\d+:\d\d)', expand=False)
    dfteams = df.loc[df.aa_classList.str.contains('_3btQY', regex=True, na=False)].aa_innerText
    time1 = []
    time2 = []
    for i, (jogo) in enumerate(dfteams):
        time1.append(jogo.splitlines()[0])
        time2.append(jogo.splitlines()[2])
    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})

    odds = df.loc[df.aa_classList.str.contains('_13ZSg _19r8S', regex=True, na=False)]
    odd1 = odds['aa_innerText'][::3].apply(to_float_or_zero).reset_index(drop=True)
    oddX = odds['aa_innerText'][1::3].apply(to_float_or_zero).reset_index(drop=True)
    odd2 = odds['aa_innerText'][2::3].apply(to_float_or_zero).reset_index(drop=True)

    dfodds = pd.DataFrame({
        'odd1': odd1,
        'oddX': oddX,
        'odd2': odd2
    })

    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)
    #
    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato