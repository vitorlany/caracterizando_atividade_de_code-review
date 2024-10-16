import pandas as pd

from utils import data

def get_data(row):
    row = row['node']
    tamanho_arquivos = row['files']['totalCount']
    tamanho_adicionadas = row['additions']
    tamanho_removidas = row['deletions']
    tempo_analise = pd.to_datetime(row.get('closedAt', row.get('mergedAt'))) - pd.to_datetime(row['createdAt'])
    descricao = len(row['body'])
    num_participantes = row['participants']['totalCount']
    num_comentarios = row['comments']['totalCount']
    return tamanho_arquivos, tamanho_adicionadas, tamanho_removidas, tempo_analise, descricao, num_participantes, num_comentarios

files_name = data.list_pullrequests_json_files()
metrics_per_repository = []
for file_name in files_name:
    file_data = data.load_data(f'pull_requests/{file_name}')
    total = []
    for row in file_data:
        res = get_data(row)
        total = total + [res]
    if not total:
        continue
    data_frame = pd.DataFrame(total, columns=['tamanho_arquivos', 'tamanho_adicionadas', 'tamanho_removidas', 'tempo_analise', 'descricao', 'num_participantes', 'num_comentarios'])
    final_data = data_frame.mean().to_dict()
    final_data['repository'] = file_name
    metrics_per_repository = metrics_per_repository + [final_data]
pd.DataFrame(metrics_per_repository).to_csv('./data/metrics.csv', index=False)