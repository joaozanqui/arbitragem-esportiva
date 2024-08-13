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
    'brasileirao': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/Brazil/1792/brasileir%C3%A3o-s%C3%A9rie-a/',
    'brasileiraob': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/Brazil/3104/brasileir%C3%A3o-s%C3%A9rie-b',
    'brasileiraoc': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/Brazil/4672/brasileirão-série-c',
    'brasileiraod': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/Brazil/12156/brasileir%C3%A3o-s%C3%A9rie-d',
    'copadobrasil': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/Brazil/1799/copa-do-brasil',
    'inglaterra1': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/England/538/premier-league',
    'argentina1': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/Argentina/1685/liga-profesional',
    'libertadores': 'https://www.playpix.com/pb/sports/pre-match/event-view/Soccer/South%20America/2988/copa-libertadores'
}

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'brasileirao'
    driver_to_save = Driver(uc=True)

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do playpix."

    driver_to_save.get(url)
    WebDriverWait(driver_to_save, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    page_source = driver_to_save.page_source
    with open(pasta_casas + 'casas-html/playpix.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/playpix.html')
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
    #

    dfgames = df.loc[df.aa_classList.str.contains('multi-column-content  multi-column-show-type-undefined', regex=True, na=False)].aa_innerText
    time1 = []
    time2 = []
    horario = []
    odd1 = []
    oddX = []
    odd2 = []
    for i, (jogo) in enumerate(dfgames):
        jogo_list = [jogo_list for jogo_list in jogo.strip().split('\n') if jogo_list.strip()]
        horario.append(jogo_list[2])
        time1.append(jogo_list[0])
        time2.append(jogo_list[1])
        odd1.append(jogo_list[3])
        oddX.append(jogo_list[4])
        odd2.append(jogo_list[5])

    for i, (odd) in enumerate(odd1):
        odd1[i] = odd.split(' ')[0]
    for i, (odd) in enumerate(oddX):
        oddX[i] = odd.split(' ')[0]
    for i, (odd) in enumerate(odd2):
        odd2[i] = odd.split(' ')[0]

    dftime = pd.DataFrame({'horario': horario})
    dfteams = pd.DataFrame({'time1': time1, 'time2': time2})
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