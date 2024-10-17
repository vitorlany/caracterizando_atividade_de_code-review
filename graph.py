import pandas as pd
import matplotlib.pyplot as plt
import os

# Tamanho é a soma das colunas 'tamanho_adicionadas' e 'tamanho_removidas'
# Feedback é a coluna 'state'
# Tempo de análise é a coluna 'tempo_analise' (em tempo)
# Descrição é a coluna 'descricao' (número de caracteres)
# Interações é a coluna 'num_comentarios'
# Número de revisões é 'reviews'


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
ensure_directory_exists('./plots')


def plot_pr_size_vs_feedback(data):
    data['tamanho'] = data['tamanho_adicionadas'] + data['tamanho_removidas']
    feedback_groups = data.groupby('state')['tamanho'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(feedback_groups['state'], feedback_groups['tamanho'], color='skyblue')
    plt.title('PR Size vs Feedback', fontsize=14)
    plt.xlabel('Feedback (State)', fontsize=12)
    plt.ylabel('PR Size (Total Lines)', fontsize=12)
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.savefig('./plots/pr_size_vs_feedback.png')
    plt.show()

def plot_analysis_time_vs_feedback(data):
    data['tempo_analise'] = pd.to_timedelta(data['tempo_analise']).dt.total_seconds()
    feedback_groups = data.groupby('state')['tempo_analise'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(feedback_groups['state'], feedback_groups['tempo_analise'], label='Analysis Time', marker='o')
    plt.title('Analysis Time vs Feedback')
    plt.xlabel('Feedback (State)')
    plt.ylabel('Analysis Time (Seconds)')
    plt.grid(True)
    plt.legend()
    plt.savefig('./plots/analysis_time_vs_feedback.png')
    plt.show()

def plot_description_vs_feedback(data):
    feedback_groups = data.groupby('state')['descricao'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(feedback_groups['state'], feedback_groups['descricao'], color='salmon')
    plt.title('Description Length vs Feedback', fontsize=14)
    plt.xlabel('Feedback (State)', fontsize=12)
    plt.ylabel('Description (Characters)', fontsize=12)
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.savefig('./plots/description_vs_feedback.png')
    plt.show()

def plot_interactions_vs_feedback(data):
    feedback_groups = data.groupby('state')['num_comentarios'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(feedback_groups['state'], feedback_groups['num_comentarios'], color='orange')
    plt.title('Interactions (Comments) vs Feedback', fontsize=14)
    plt.xlabel('Feedback (State)', fontsize=12)
    plt.ylabel('Interactions (Number of Comments)', fontsize=12)
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.savefig('./plots/interactions_vs_feedback.png')
    plt.show()

def plot_pr_size_vs_reviews(data):
    data['tamanho'] = data['tamanho_adicionadas'] + data['tamanho_removidas']
    review_groups = data.groupby('reviews')['tamanho'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(review_groups['reviews'], review_groups['tamanho'], label='PR Size', marker='o')
    plt.title('PR Size vs Number of Reviews')
    plt.xlabel('Number of Reviews')
    plt.ylabel('PR Size (Total Lines)')
    plt.grid(True)
    plt.legend()
    plt.savefig('./plots/pr_size_vs_reviews.png')
    plt.show()

def plot_description_vs_reviews(data):
    review_groups = data.groupby('reviews')['descricao'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(review_groups['reviews'], review_groups['descricao'], label='Description Length', marker='o')
    plt.title('Description Length vs Number of Reviews')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Description (Characters)')
    plt.grid(True)
    plt.legend()
    plt.savefig('./plots/description_vs_reviews.png')
    plt.show()

def plot_interactions_vs_reviews(data):
    review_groups = data.groupby('reviews')['num_comentarios'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(review_groups['reviews'], review_groups['num_comentarios'], label='Number of Comments', marker='o')
    plt.title('Interactions (Comments) vs Number of Reviews')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Interactions (Number of Comments)')
    plt.grid(True)
    plt.legend()
    plt.savefig('./plots/interactions_vs_reviews.png')
    plt.show()

def plot_analysis_time_vs_reviews(data):
    data['tempo_analise'] = pd.to_timedelta(data['tempo_analise']).dt.total_seconds()
    review_groups = data.groupby('reviews')['tempo_analise'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(review_groups['reviews'], review_groups['tempo_analise'], label='Analysis Time', marker='o')
    plt.title('Analysis Time vs Number of Reviews')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Analysis Time (Seconds)')
    plt.grid(True)
    plt.legend()
    plt.savefig('./plots/analysis_time_vs_reviews.png')
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