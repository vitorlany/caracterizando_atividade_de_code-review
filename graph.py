import pandas as pd
import matplotlib.pyplot as plt

# tamanho é a soma das colunas tamanho_adicionadas e tamanho_removidas
# feedback é a coluna state
# tempo de análise é a coluna tempo_analise (em tempo)
# descrição é descricao (número)
# interações é num_comentarios
# número de revisões é reviews

def plot_pr_size_vs_feedback(data):
    data['tamanho'] = data['tamanho_adicionadas'] + data['tamanho_removidas']
    plt.figure(figsize=(10, 6))
    data.boxplot(column='tamanho', by='state', grid=False)
    plt.title('Relationship between PR size and final feedback')
    plt.suptitle('')
    plt.xlabel('Feedback (State)')
    plt.ylabel('PR Size')
    plt.show()

def plot_analysis_time_vs_feedback(data):
    data['tempo_analise'] = pd.to_timedelta(data['tempo_analise']).dt.total_seconds()
    plt.figure(figsize=(10, 6))
    data.boxplot(column='tempo_analise', by='state', grid=False)
    plt.title('Relationship between PR analysis time and final feedback')
    plt.suptitle('')
    plt.xlabel('Feedback (State)')
    plt.ylabel('Analysis Time (seconds)')
    plt.show()

def plot_description_vs_feedback(data):
    plt.figure(figsize=(10, 6))
    data.boxplot(column='descricao', by='state', grid=False)
    plt.title('Relationship between PR description and final feedback')
    plt.suptitle('')
    plt.xlabel('Feedback (State)')
    plt.ylabel('Description (number of characters)')
    plt.show()

def plot_interactions_vs_feedback(data):
    plt.figure(figsize=(10, 6))
    data.boxplot(column='num_comentarios', by='state', grid=False)
    plt.title('Relationship between PR interactions and final feedback')
    plt.suptitle('')
    plt.xlabel('Feedback (State)')
    plt.ylabel('Interactions (number of comments)')
    plt.show()

def plot_pr_size_vs_reviews(data):
    data['tamanho'] = data['tamanho_adicionadas'] + data['tamanho_removidas']
    plt.figure(figsize=(10, 6))
    data.boxplot(column='tamanho', by='reviews', grid=False)
    plt.title('Relationship between PR size and number of reviews')
    plt.suptitle('')
    plt.xlabel('Number of Reviews')
    plt.ylabel('PR Size')
    plt.show()

def plot_description_vs_reviews(data):
    plt.figure(figsize=(10, 6))
    data.boxplot(column='descricao', by='reviews', grid=False)
    plt.title('Relationship between PR description and number of reviews')
    plt.suptitle('')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Description (number of characters)')
    plt.show()

def plot_interactions_vs_reviews(data):
    plt.figure(figsize=(10, 6))
    data.boxplot(column='num_comentarios', by='reviews', grid=False)
    plt.title('Relationship between PR interactions and number of reviews')
    plt.suptitle('')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Interactions (number of comments)')
    plt.show()

def plot_analysis_time_vs_reviews(data):
    data['tempo_analise'] = pd.to_timedelta(data['tempo_analise']).dt.total_seconds()
    plt.figure(figsize=(10, 6))
    data.boxplot(column='tempo_analise', by='reviews', grid=False)
    plt.title('Relationship between PR analysis time and number of reviews')
    plt.suptitle('')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Analysis Time (seconds)')
    plt.show()

data = pd.read_csv('./data/metrics.csv')
plot_pr_size_vs_feedback(data)
plot_analysis_time_vs_feedback(data)
plot_description_vs_feedback(data)
plot_interactions_vs_feedback(data)
plot_pr_size_vs_reviews(data)
plot_analysis_time_vs_reviews(data)
plot_description_vs_reviews(data)
plot_interactions_vs_reviews(data)