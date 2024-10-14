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
                    edges {{
                        node {{
                            title
                            url
                            state
                            createdAt
                            mergedAt
                            closedAt
                            reviews(first: 100) {{
                                totalCount
                            }}
                            files(first: 100) {{
                              totalCount
                            }}
                            additions
                            deletions
                            body
                            participants(first: 100) {{
                                totalCount
                            }}
                            comments(first: 100) {{
                                totalCount
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

def get_pull_requests_bypass_page(owner, name, num_prs, auth_token, cursor = ''):
    pull_requests = []
    max_per_page = num_prs if num_prs < 25 else 25
    num_pages = math.ceil(num_prs / max_per_page)
    page = 1
    cursor = ""

    while page <= num_pages:
        graphql_query = build_pull_request_query(owner, name, max_per_page, cursor)
        result = run_query(graphql_query, auth_token)

        page_pull_requests = result["data"]["repository"]["pullRequests"]["edges"]
        if not page_pull_requests:
            break

        filtered_data = list(filter(lambda obj: obj['node']['reviews']['totalCount'] > 0, page_pull_requests))

        if len(filtered_data) == 0:
            break

        pull_requests.extend(filtered_data)
        cursor = result["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
        page += 1

    return pull_requests

def get_pull_requests(repositories, auth_token):

    for repository in repositories:
        owner = repository["owner"]["login"]
        name = repository["name"]
        total_count = repository["pullRequests"]["totalCount"]
        name_with_owner = repository["nameWithOwner"].replace("/", "-")
        pull_requests = get_pull_requests_bypass_page(owner, name, total_count, auth_token)
        data.save_data(pull_requests, f'pull_requests/{name_with_owner}')