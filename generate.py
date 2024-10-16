import pandas as pd

from utils import data

def get_data(row, repository):
    row = row['node']
    tamanho_arquivos = row['files']['totalCount']
    tamanho_adicionadas = row['additions']
    tamanho_removidas = row['deletions']
    tempo_analise = pd.to_datetime(row.get('closedAt', row.get('mergedAt'))) - pd.to_datetime(row['createdAt'])
    descricao = len(row['body'])
    num_participantes = row['participants']['totalCount']
    num_comentarios = row['comments']['totalCount']
    state = row['state']
    reviews = row['reviews']['totalCount']
    return repository, tamanho_arquivos, tamanho_adicionadas, tamanho_removidas, tempo_analise, descricao, num_participantes, num_comentarios, state, reviews

files_name = data.list_pullrequests_json_files()
metrics_per_repository = []
for file_name in files_name:
    file_data = data.load_data(f'pull_requests/{file_name}')
    total = []
    for row in file_data:
        res = get_data(row, file_name)
        total = total + [res]
    if not total:
        continue
    metrics_per_repository = metrics_per_repository + total
columns = ['repository', 'tamanho_arquivos', 'tamanho_adicionadas', 'tamanho_removidas', 'tempo_analise', 'descricao',
               'num_participantes', 'num_comentarios', 'state', 'reviews']
pd.DataFrame(metrics_per_repository, columns=columns).to_csv('./data/metrics.csv', index=False)