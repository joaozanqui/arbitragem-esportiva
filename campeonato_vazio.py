import pandas as pd

def casa_sem_campeonato():
    df_vazio = pd.DataFrame(columns=['horario', 'time1', 'time2', 'odd1', 'oddX', 'odd2'])
    df_vazio.loc[0] = [0, 0, 0, 0, 0, 0]
    return df_vazio