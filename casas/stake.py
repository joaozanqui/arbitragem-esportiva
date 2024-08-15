from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
from datetime import datetime, timedelta
import time
import re
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
    'brasileirao': 'https://stake.com/pt/sports/soccer/brazil/brasileiro-serie-a',
    'brasileiraob': 'https://stake.com/pt/sports/soccer/brazil/brasileiro-serie-b',
    'brasileiraoc': 'https://stake.com/pt/sports/soccer/brazil/brasileiro-serie-c',
    'copadobrasil': 'https://stake.com/pt/sports/soccer/brazil/copa-do-brasil',
    'inglaterra1': 'https://stake.com/pt/sports/soccer/england/premier-league',
    'espanha1': 'https://stake.com/pt/sports/soccer/spain/la-liga',
    'argentina1': 'https://stake.com/pt/sports/soccer/argentina/superliga',
    'libertadores': 'https://stake.com/pt/sports/soccer/international-clubs/copa-libertadores'
}

def ajustar_horario(horario_str, horas_subtrair=3):
    horario = datetime.strptime(horario_str, '%H:%M')
    novo_horario = horario - timedelta(hours=horas_subtrair)
    novo_horario_str = novo_horario.strftime('%H:%M')
    return novo_horario_str

def is_text(text):
    return bool(re.search(r'[a-zA-Z]', text))

def processar_campeonato(campeonato_nome):
# campeonato_nome = 'espanha1'
    if not campeonato_nome in urls:
        return casa_sem_campeonato()

    try:
        url = urls[campeonato_nome]
    except KeyError:
        return "Erro: Campeonato não encontrado na base de dados do Esportes da Sorte."
# url = urls[campeonato_nome]

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
    with open(pasta_casas + 'casas-html/stake.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    driver_to_save.quit()

    driver = Driver(uc=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_html = os.path.join(current_dir, 'casas-html/stake.html')
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

    infos = df.loc[df.aa_classList.str.contains('fixture-preview svelte-9txh06', regex=True, na=False)].aa_innerText
    #
    horarios = []
    time1 = []
    time2 = []
    odd1 = []
    oddX = []
    odd2 = []
    captcha = False
    for info in infos:
        info_split = info.splitlines()
        if not re.search(r'\d', info_split[6]):
            captcha = True
            break
        if is_text(info_split[0]):
            continue
        if not re.search(r'\d', info_split[0]):
            continue
        horarios.append(info_split[0])
        time1.append(info_split[2])
        time2.append(info_split[3])
        odd1.append(info_split[6])
        oddX.append(info_split[8])
        odd2.append(info_split[10])

    if captcha:
        horarios = []
        time1 = []
        time2 = []
        odd1 = []
        oddX = []
        odd2 = []
        for info in infos:
            info_split = info.splitlines()
            if is_text(info_split[0]):
                continue
            if not re.search(r'\d', info_split[0]):
                continue
            horarios.append(ajustar_horario(info_split[0]))
            times = info_split[2].split(' - ')
            time1.append(times[0])
            time2.append(times[1])
            odd1.append(info_split[5])
            oddX.append(info_split[7])
            odd2.append(info_split[9])

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
    #
    dftime = dftime.reset_index(drop=True)
    dfteams = dfteams.reset_index(drop=True)
    dfodds = dfodds.reset_index(drop=True)
    #
    campeonato = pd.concat([dftime, dfteams, dfodds], axis=1)
    campeonato.columns = ['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2']
    renomear(campeonato_nome, campeonato.time1, campeonato.time2)

    driver.quit()
    return campeonato