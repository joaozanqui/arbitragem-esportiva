import importlib.util
import pandas as pd
import os
import numpy as np
from multiprocessing import Pool, Manager
from tabulate import tabulate
from colorama import Fore, Back, Style, init

# Diretório onde estão os scripts
pasta_casas = 'casas'
arquivos_ignorar = []
# arquivos_ignorar = ['bet365.py', 'betano.py', 'betfair.py', 'esportesdasorte.py', 'galerabet.py', 'pmbet.py', 'portugabet.py', 'sportingbet.py', 'sportybet.py', 'apostaganha.py', 'betnacional.py', 'bwin.py', 'stake.py', 'betsson.py', 'estrelabet.py', 'superbet.py', 'pinnacle.py', 'h2bet.py']
casas_de_aposta = [casa.replace('.py', '') for casa in os.listdir(pasta_casas) if casa.endswith('.py')]

# Lista para armazenar as variáveis coletadas
jogos_casas = {}
arquivos_com_erro = []
campeonatos_disponiveis = ['brasileirao', 'brasileiraob', 'brasileiraoc', 'brasileiraod', 'copadobrasil', 'inglaterra1', 'argentina1', 'libertadores']
valor_gasto = 100.00

# Cria o dicionario para selecionar as melhores odds
melhores_odds = {}
def process_file(args):
    filename, campeonato_nome, pasta_casas = args
    try:
        script_path = os.path.join(pasta_casas, filename)
        spec = importlib.util.spec_from_file_location(filename[:-3], script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'processar_campeonato'):
            return (filename, module.processar_campeonato(campeonato_nome))
    except Exception as e:
        return (filename, e)

# def abrir_arquivos(campeonat  o_nome='brasileirao'):
#     with Pool() as pool:
#         filenames = [filename for filename in os.listdir(pasta_casas) if filename.endswith('.py') and filename not in arquivos_ignorar]
#         args = [(filename, campeonato_nome, pasta_casas) for filename in filenames]
#         results = pool.map(process_file, args)
#     quantidade_casas = len(casas_de_aposta) - len(arquivos_ignorar) - 2
#     contagem = 1
#     for filename, result in results:
#         print(filename, " - ", contagem, "/", quantidade_casas)
#         contagem += 1
#         if isinstance(result, Exception):
#             arquivos_com_erro.append(filename)
#             print(f"\n\nErro ao processar o arquivo {filename}: {result}\n")
#         else:
#             jogos_casas[os.path.splitext(filename)[0]] = result
#
#     comparar_odds()


def leitura_arquivos(campeonato_nome, filenames, quantidade_casas, reprocessando):
    contagem = 1

    with Pool() as pool:
        args = [(filename, campeonato_nome, pasta_casas) for filename in filenames]
        results = pool.map(process_file, args)

    for filename, result in results:
        if reprocessando:
            print(filename, " reprocessado...")
        else:
            print(filename, " - ", contagem, "/", quantidade_casas)
        contagem += 1
        # print(filename, result)
        if isinstance(result, Exception):
            arquivos_com_erro.append(filename)
            if reprocessando:
                print(f"\n\nErro ao reprocessar o arquivo {filename}: {result}\n")
            else:
                print(f"\n\nErro ao processar o arquivo {filename}: {result}\n")
        elif result.empty:
            arquivos_com_erro.append(filename)
            print(f"\n\nArquivo {filename} Vazio\n")
        else:
            jogos_casas[os.path.splitext(filename)[0]] = result


def abrir_arquivos(campeonato_nome='brasileirao'):
    filenames = [filename for filename in os.listdir(pasta_casas) if filename.endswith('.py') and filename not in arquivos_ignorar]
    quantidade_casas = len(casas_de_aposta) - len(arquivos_ignorar)
    tentativas_maximas = 3
    tentativas = 1

    leitura_arquivos(campeonato_nome, filenames, quantidade_casas, False)

    # Reprocessar arquivos com erro até tentativas máximas
    while arquivos_com_erro and tentativas <= tentativas_maximas:
        print(f"\nTentativa {tentativas} de reprocessamento dos arquivos com erro...")
        print(f"Arquivos com erro: {arquivos_com_erro}\n")
        arquivos_com_erro_atual = arquivos_com_erro[:]
        arquivos_com_erro.clear()

        leitura_arquivos(campeonato_nome, arquivos_com_erro_atual, quantidade_casas, True)
        tentativas += 1

    if arquivos_com_erro:
        print("\nArquivos que ainda geraram erro após múltiplas tentativas:")
        for filename in arquivos_com_erro:
            print(filename)

    comparar_odds()


# def abrir_arquivos(campeonato_nome='brasileirao'):
#     # Loop através de cada arquivo no diretório
#     quantidade_casas = len(casas_de_aposta) - len(arquivos_ignorar) - 2
#     contagem = 1
#     for filename in os.listdir(pasta_casas):
#         if filename.endswith('.py'):
#             if filename in arquivos_ignorar:
#                 continue
#             try:
#                 script_path = os.path.join(pasta_casas, filename)
#                 # Carregar o módulo dinamicamente
#                 spec = importlib.util.spec_from_file_location(filename[:-3], script_path)
#                 module = importlib.util.module_from_spec(spec)
#                 spec.loader.exec_module(module)
#                 # Coletar a variável desejada
#                 if hasattr(module, 'processar_campeonato'):
#                     print(filename, " - ", contagem, "/", quantidade_casas)
#                     contagem += 1
#                     jogos_casas[os.path.splitext(filename)[0]] = module.processar_campeonato(campeonato_nome)
#             except Exception as e:
#                 # Adicionar o nome do arquivo à lista de arquivos com erro
#                 arquivos_com_erro.append(filename)
#                 # Opcional: imprimir ou registrar o erro para depuração
#                 print(f"\n\nErro ao processar o arquivo {filename}: {e}\n")
#     comparar_odds()

# Função para garantir que os valores sejam floats e substituam vírgulas por pontos
def to_float(value):
    if pd.isna(value):
        return float('0')
    if isinstance(value, str):
        try:
            new_value = float(value.replace(',', '.'))
        except ValueError:
            new_value = 1
        return new_value
    return float(value)

def encontrar_indices(lista, valor):
    return [i for i, x in enumerate(lista) if x == valor]

def comparar_odds():
    #Colocando a casa que capturou o maior numero de jogos no inicio da lista
    maior = 0
    maior_casa = ""
    for i, (casa) in enumerate(jogos_casas):
        if len(casa) > len(maior_casa):
            maior = i
            maior_casa = casa

    itens = list(jogos_casas.items())
    itens[0], itens[maior] = itens[maior], itens[0]
    jogos_casas_reordenados = dict(itens)

    for i, (casa, jogos) in enumerate(jogos_casas_reordenados.items()):
        if(jogos.empty):
            print(casa, " - DataFrame Vazio")
            continue
        # Preenche o dicionario com a primeira iteracao
        if i == 0:
            numero_de_itens = len(jogos['time1'])
            for coluna in melhores_odds.keys():
                if coluna in ['casa1', 'casaX', 'casa2', 'valor1', 'valorX', 'valor2', 'valor_ganho', 'lucro', 'valor_gasto']:
                    add = 0
                    if (coluna in ['casa1', 'casaX', 'casa2']):
                        add = casa
                    elif coluna == 'valor_gasto':
                        add = valor_gasto

                    for item in range(numero_de_itens):
                        melhores_odds[coluna].append(add)
                else:
                    melhores_odds[coluna].extend(jogos[coluna])
        # Compara as odds das outras casas de aposta com as da primeira iteracao
        else:
            for j, time1 in enumerate(jogos['time1']):
                # print(time1)
                if time1 in melhores_odds['time1']:
                    indices_mo = encontrar_indices(melhores_odds['time1'], time1)
                    for i_mo in indices_mo:
                        # print(jogos['time2'][j], melhores_odds['time2'][i_mo])
                        if jogos['time2'][j] == melhores_odds['time2'][i_mo]:
                            odd1_jogo = to_float(jogos['odd1'][j])
                            oddX_jogo = to_float(jogos['oddX'][j])
                            odd2_jogo = to_float(jogos['odd2'][j])
                            odd1_mo = to_float(melhores_odds['odd1'][i_mo])
                            oddX_mo = to_float(melhores_odds['oddX'][i_mo])
                            odd2_mo = to_float(melhores_odds['odd2'][i_mo])
                            # print(time1, jogos['time2'][j], odd1_mo, odd1_jogo, oddX_mo, oddX_jogo, odd2_mo, odd2_jogo)
                            # comando = input("Pause: ").strip()
                            if odd1_jogo > odd1_mo:
                                melhores_odds['odd1'][i_mo] = jogos['odd1'][j]
                                melhores_odds['casa1'][i_mo] = casa
                            if oddX_jogo > oddX_mo:
                                melhores_odds['oddX'][i_mo] = jogos['oddX'][j]
                                melhores_odds['casaX'][i_mo] = casa
                            if odd2_jogo > odd2_mo:
                                melhores_odds['odd2'][i_mo] = jogos['odd2'][j]
                                melhores_odds['casa2'][i_mo] = casa
                            break

        recalcular_lucro()

def recalcular_lucro():
    for i, (odd1) in enumerate(melhores_odds['odd1']):
        oddX = melhores_odds['oddX'][i]
        odd2 = melhores_odds['odd2'][i]
        calcula_lucro(odd1, oddX, odd2, i)

def calcula_lucro(odd1_str, oddX_str, odd2_str, n):
    # Substituindo vírgulas por pontos antes de converter para float
    odd1 = to_float(odd1_str)
    oddX = to_float(oddX_str)
    odd2 = to_float(odd2_str)
    #
    # if odd1 == 0:
    #     odd1 = 1
    # if oddX == 0:
    #     oddX = 1
    # if odd2 == 0:
    #     odd2 = 1

    valor_inicial = round(valor_gasto, 2)
    gasto_atual = round(valor_gasto, 2)
    qtd_entradas = 3
    valores_operacao = [gasto_atual/odd1, gasto_atual/oddX, gasto_atual/odd2]
    ganho_potencial = gasto_atual
    total_gasto = sum(valores_operacao)
    trava_seguranca = 0

    while int(total_gasto * 100) != int(valor_inicial * 100):
        if (total_gasto < valor_inicial):
            sinal = 1
        elif (total_gasto > valor_inicial):
            sinal = -1

        gasto_atual += 0.01 * sinal
        valores_operacao = [gasto_atual / odd1, gasto_atual / oddX, gasto_atual / odd2]
        ganho_potencial = gasto_atual
        total_gasto = sum(valores_operacao)

        if (int(total_gasto * 100) == int(valor_inicial * 100) + 1 or int(total_gasto * 100) == int(
                valor_inicial * 100) - 1):
            trava_seguranca += 1
        if (trava_seguranca > 4):
            break

    porcentagem = str(round(100 * ((ganho_potencial - total_gasto) / total_gasto), 2))

    melhores_odds['valor1'][n] = round(valores_operacao[0], 2)
    melhores_odds['valorX'][n] = round(valores_operacao[1], 2)
    melhores_odds['valor2'][n] = round(valores_operacao[2], 2)

    melhores_odds['valor_ganho'][n] = round(ganho_potencial, 2)
    melhores_odds['valor_gasto'][n] = round(total_gasto, 2)

    melhores_odds['lucro'][n] = porcentagem + "%"

def get_melhores_odds():
    apostas_df = pd.DataFrame(melhores_odds)
    apostas = apostas_df.copy()

    def color_lucro(val):
        val = float(val.replace('%', ''))
        if val > 0:
            return Fore.GREEN + str(val) + "%" + Style.RESET_ALL
        else:
            return Fore.RED + str(val) + "%" + Style.RESET_ALL

    def color_ganho(val):
        val = float(val)
        if val > valor_gasto:
            return Fore.GREEN + str(val) + Style.RESET_ALL
        else:
            return Fore.RED + str(val) + Style.RESET_ALL

    def color_white(val):
        return Fore.BLACK + Back.WHITE + str(val) + Style.RESET_ALL
    def color_blue(val):
        return Fore.BLUE + str(val) + Style.RESET_ALL
    def color_yellow(val):
        return Fore.YELLOW + str(val) + Style.RESET_ALL
    def color_magneta(val):
        return Fore.MAGENTA + str(val) + Style.RESET_ALL


    apostas['lucro'] = apostas_df['lucro'].apply(color_lucro)
    apostas['valor_ganho'] = apostas_df['valor_ganho'].apply(color_ganho)
    for coluna in ['horario', 'time1', 'time2', 'valor_gasto']:
        apostas[coluna] = apostas_df[coluna].apply(color_white)
    for i in range(1, 4):
        for coluna in ['casa', 'odd', 'valor']:
            coluna_atual = coluna + str(i)
            if (i == 1):
                apostas[coluna_atual] = apostas_df[coluna_atual].apply(color_blue)
            elif (i == 2):
                apostas[coluna_atual] = apostas_df[coluna_atual].apply(color_magneta)
            else:
                coluna_atual = coluna + 'X'
                apostas[coluna_atual] = apostas_df[coluna_atual].apply(color_yellow)

    colored_columns = list(apostas.columns)

    print(tabulate(apostas, headers=colored_columns, tablefmt='grid'))


def set_valor_gasto():
    global valor_gasto
    novo_valor = input("Digite o valor Gasto: ")
    valor_gasto = float(novo_valor)
    recalcular_lucro()

primeira_vez = True
def set_campeonato():
    global primeira_vez
    global jogos_casas
    global melhores_odds
    print("Campeonatos Disponiveis: ", campeonatos_disponiveis)
    voltar = False
    if primeira_vez:
        campeonato = input("Digite o nome do campeonato: ").lower()
    else:
        campeonato = input("Digite o nome do campeonato (/voltar para voltar): ").lower()

    while (campeonato not in campeonatos_disponiveis):
        if campeonato == '/voltar' and not primeira_vez:
            voltar = True
            break
        print("Campeonato ", campeonato, " nao disponivel")
        campeonato = input("Digite o nome do campeonato: ").lower()

    if not voltar:
        jogos_casas = {}
        melhores_odds = {
            'horario': [],
            'time1': [],
            'time2': [],
            'lucro': [],
            'casa1': [],
            'odd1': [],
            'valor1': [],
            'casaX': [],
            'oddX': [],
            'valorX': [],
            'casa2': [],
            'odd2': [],
            'valor2': [],
            'valor_gasto': [],
            'valor_ganho': []
        }
        abrir_arquivos(campeonato)
        recalcular_lucro()
        primeira_vez = False

set_campeonato()

comandos = {
    '/campeonato': set_campeonato,
    '/valor': set_valor_gasto,
    '/odds': get_melhores_odds,
}
comando_errado = False

while True:
    if not comando_errado:
        print("\nComo utilizar:")
        print("/campeonato - Alterar o campeonato")
        print("/valor - Alterar o valor apostado")
        print("/odds - Ver as melhores odds do campeonato escolhido")
        print("/sair - Fechar o programa")


    comando = input("Digite um comando: ").strip()

    if comando in comandos:
        comando_errado = False
        comandos[comando]()
    elif comando == '/sair':
        print("Encerrando o programa.")
        break
    else:
        comando_errado = True
        print("Comando não reconhecido. Tente novamente.")