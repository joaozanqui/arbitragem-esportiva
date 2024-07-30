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
    'brasileirao': 'https://www.kto.com/pt/esportes/?page=championship&championshipIds=11318&sportId=66',
    'brasileiraob': 'https://www.kto.com/pt/esportes/?page=championship&championshipIds=11005&sportId=66'
}

# def processar_campeonato(campeonato_nome):
campeonato_nome = 'brasileirao'
driver_to_save = Driver(uc=True)

# try:
url = urls[campeonato_nome]
# except KeyError:
#     return "Erro: Campeonato não encontrado na base de dados da Galerabet."

driver_to_save.get(url)
WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(10)
page_source = driver_to_save.page_source
with open(pasta_casas + 'casas-html/kto.html', 'w', encoding='utf-8') as file:
    file.write(page_source)
driver_to_save.quit()

driver = Driver(uc=True)
current_dir = os.path.dirname(os.path.abspath(__file__))
caminho_html = os.path.join(current_dir, 'casas-html/kto.html')
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

# dfinfos = df.loc[df.aa_outerHTML.str.contains('data-testid="preMatchOdds"', regex=True, na=False) & df['aa_innerText'].str.contains(r'^\d{2}:\d{2}', regex=True)].aa_innerText
#
# horario = []
# time1 = []
# time2 = []
# odd1 = []
# oddX = []
# odd2 = []
# for info in dfinfos:
#     info_split = info.splitlines()
#     horario.append(info_split[0])
#     times = info_split[1].split(' x ')
#     time1.append(times[0])
#     time2.append(times[1])
#     odd1.append(info_split[2])
#     oddX.append(info_split[3])
#     odd2.append(info_split[4])
#
# dftime = pd.DataFrame({
#     'horario': horario,
# })
# dfteams = pd.DataFrame({
#     'time1': time1,
#     'time2': time2,
# })
# dfodds = pd.DataFrame({
#     'odd1': odd1,
#     'oddX': oddX,
#     'odd2': odd2
# })
#
# dftime = dftime.reset_index(drop=True)
# dfteams = dfteams.reset_index(drop=True)
# dfodds = dfodds.reset_index(drop=True)
#
# campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
# campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
# renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    # driver.quit()
    # return campeonato