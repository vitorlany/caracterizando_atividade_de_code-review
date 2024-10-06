import os
from utils import github, data

auth_token = os.getenv("GITHUB_TOKEN")

# REPOSITORIES_NUMBER = 200
REPOSITORIES_NUMBER = 1

if not data.is_file_exists('repositories'):
    repositories = github.get_repositories(REPOSITORIES_NUMBER, auth_token)
    data.save_data(repositories, 'repositories')
repositories = data.load_data('repositories')
github.get_pull_requests(repositories, auth_token)
print(repositories)