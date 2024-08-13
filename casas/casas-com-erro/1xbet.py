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
    'brasileirao': 'https://br.1x001.com/br/line/football/1268397-brazil-campeonato-brasileiro-serie-a',
    'brasileiraob': 'https://br.betano.com/sport/futebol/brasil/brasileirao-serie-b/10017/',
    'brasileiraoc': 'https://br.betano.com/sport/futebol/brasil/brasileirao-serie-c/18249/',
    'brasileiraod': 'https://br.betano.com/sport/futebol/competicoes/brasil/10004/?sl=182510',
    'inglaterra1': 'https://br.betano.com/sport/futebol/competicoes/inglaterra/1/',
    'argentina1': 'https://br.betano.com/sport/futebol/competicoes/argentina/11319/'
}

# def processar_campeonato(campeonato_nome):
campeonato_nome = 'brasileirao'

# try:
url = urls[campeonato_nome]
# except KeyError:
#     return "Erro: Campeonato não encontrado na base de dados da Betano."

driver_to_save = Driver(uc=True)
driver_to_save.get(url)
WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(10)
page_source = driver_to_save.page_source
with open(pasta_casas + 'casas-html/1xbet.html', 'w', encoding='utf-8') as file:
    file.write(page_source)
driver_to_save.quit()

driver = Driver(uc=True)
current_dir = os.path.dirname(os.path.abspath(__file__))
caminho_html = os.path.join(current_dir, 'casas-html/1xbet.html')
driver.get(f"file://{caminho_html}")
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

# dfteams = df.loc[df.aa_classList.str.contains("team-scores__top", na=False, regex=True)].aa_innerText
# time1 = []
# time2 = []
# for times in dfteams:
#     times_split = times.splitlines()
#     time1.append(times_split[0])
#     time2.append(times_split[1])

# campeonato = pd.DataFrame(informacoes, columns=['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2'])
# renomear(campeonato_nome, campeonato.time1, campeonato.time2)

# driver.quit()
# return campeonato