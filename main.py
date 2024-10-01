import os
from utils import github, data

auth_token = os.getenv("GITHUB_TOKEN")

REPOSITORIES_NUMBER = 1

repositories = github.get_repositories(REPOSITORIES_NUMBER, auth_token)
data.save_data(repositories, 'repositories')
print(repositories)