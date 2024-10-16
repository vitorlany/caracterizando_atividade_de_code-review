import pandas as pd

from utils import data

def get_data(row):
    row = row['node']
    tamanho_arquivos = row['files']['totalCount']
    tamanho_adicionadas = row['additions']
    tamanho_removidas = row['deletions']
    tempo_analise = str(pd.to_datetime(row.get('closedAt', row.get('mergedAt'))) - pd.to_datetime(row['createdAt']))
    descricao = len(row['body'])
    num_participantes = row['participants']['totalCount']
    num_comentarios = row['comments']['totalCount']
    return tamanho_arquivos, tamanho_adicionadas, tamanho_removidas, tempo_analise, descricao, num_participantes, num_comentarios

files_name = data.list_pullrequests_json_files()
for file_name in files_name:
    file_data = data.load_data(f'pull_requests/{file_name}')
    pullrequests_number = len(file_data)
    total = []
    for row in file_data:
        res = get_data(row)
        total = total + [res]
    print(total)
    print(pullrequests_number)
