import requests
import math
from utils import data

GITHUB_API_URL = "https://api.github.com/graphql"
MINIMUM_PR_COUNT = 100

def run_query(query, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(GITHUB_API_URL, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch repositories: {response.status_code} {response.json()}")
    
def build_repository_query(number, cursor):
    return f"""
    {{
        search(query: "stars:>0", type: REPOSITORY, first: {number}, after: "{cursor}") {{
            pageInfo {{
                endCursor
            }}
            edges {{
                node {{
                    ... on Repository {{
                        name
                        owner {{
                            login
                        }}
                        createdAt
                        stargazerCount
                        pullRequests(states: [MERGED, CLOSED]) {{
                            totalCount
                        }}
                        nameWithOwner
                        url
                    }}
                }}
            }}
        }}
    }}
    """

def build_pull_request_query(owner, name, number, cursor):
    return f"""
        {{
            repository(owner: "{owner}", name: "{name}") {{
                pullRequests(states: [MERGED, CLOSED], first: {number}, after: "{cursor}") {{
                    pageInfo {{
                        endCursor
                    }}
                    nodes {{
                        title
                        url
                        createdAt
                        author {{
                            login
                        }}
                        mergedAt
                        closedAt
                        labels(first: 10) {{
                            nodes {{
                                name
                            }}
                        }}
                    }}
                }}
            }}
        }}
    """

def get_repositories_bypass_page(num_repos, auth_token, cursor = ''):
    repos = []
    max_per_page = num_repos if num_repos < 25 else 25
    num_pages = math.ceil(num_repos / max_per_page)
    page = 1
    cursor = ""

    while page <= num_pages:
        graphql_query = build_repository_query(max_per_page, cursor)
        result = run_query(graphql_query, auth_token)
        
        page_repos = result["data"]["search"]["edges"]
        if not page_repos:
            break

        repos.extend(map(lambda x: x["node"], page_repos))
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        page += 1

    return repos, cursor

def get_repositories(num_repos, auth_token):
    cursor = ''
    repositories = []
    size = 0
    while size < num_repos:
        repositories, cursor = get_repositories_bypass_page(num_repos, auth_token, cursor)
        pr_repos = list(filter(lambda x: x["pullRequests"]["totalCount"] >= MINIMUM_PR_COUNT, repositories))
        size += len(pr_repos)
        repositories.extend(pr_repos)
    return repositories[:num_repos]

def get_pull_requests(repositories, auth_token):
    pull_requests_list = []
    repository = repositories[0]
    owner = repository["owner"]["login"]
    name = repository["name"]
    name_with_owner = repository["nameWithOwner"].replace("/", "-")
    cursor = ""

    graphql_query = build_pull_request_query(owner, name, 100, cursor)
    result = run_query(graphql_query, auth_token)
    result_data = result['data']['repository']['pullRequests']['nodes']
    pull_requests_list.extend(result_data)
    data.save_data(pull_requests_list, f'pull_requests/{name_with_owner}')

