import os
import time
from dotenv import load_dotenv
from utils import github, data

load_dotenv()
auth_token = os.getenv("GITHUB_TOKEN")

REPOSITORIES_NUMBER = 200

start_time = time.time()
print("rodando")
if not data.is_file_exists('repositories'):
    repositories = github.get_repositories(REPOSITORIES_NUMBER, auth_token)
    data.save_data(repositories, 'repositories')
repositories = data.load_data('repositories')
github.get_pull_requests(repositories, auth_token)

end_time = time.time()
run_time = end_time - start_time
print(f"Tempo de execução: {run_time:.2f} segundos")