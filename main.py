import os
from utils import github

auth_token = os.getenv("GITHUB_TOKEN")

data = github.get_repositories(5, auth_token)
print(data)