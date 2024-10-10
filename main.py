import os
from utils import github, data

auth_token = os.getenv("GITHUB_TOKEN")

# REPOSITORIES_NUMBER = 200
REPOSITORIES_NUMBER = 5

if not data.is_file_exists('repositories'):
    repositories = github.get_repositories(REPOSITORIES_NUMBER, auth_token)
    data.save_data(repositories, 'repositories')
repositories = data.load_data('repositories')
github.get_pull_requests(repositories, auth_token)

def get_pull_request_details(repo, pr_number, auth_token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"token {auth_token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pr_data = response.json()
        files_changed = pr_data['changed_files']
        additions = pr_data['additions']
        deletions = pr_data['deletions']
        
        return {
            'files_changed': files_changed,
            'additions': additions,
            'deletions': deletions
        }
    else:
        raise Exception(f"Failed to fetch PR details for PR #{pr_number} in {repo}")
    
def get_time_to_merge_or_close(pr):
    created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    closed_at = datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
    
    time_to_merge_or_close = closed_at - created_at
    return time_to_merge_or_close

def get_description_length(pr):
    return len(pr.get('body', ''))

def get_interactions(pr, repo, auth_token):
    comments_url = f"https://api.github.com/repos/{repo}/issues/{pr['number']}/comments"
    headers = {"Authorization": f"token {auth_token}"}
    
    response = requests.get(comments_url, headers=headers)
    if response.status_code == 200:
        comments = response.json()
        participants = {comment['user']['login'] for comment in comments}
        return {
            'comments_count': len(comments),
            'participants_count': len(participants)
        }
    else:
        raise Exception(f"Failed to fetch comments for PR #{pr['number']} in {repo}")

def process_pull_requests(repositories, auth_token):
    for repo in repositories:
        repo_name = repo['full_name']
        pull_requests = github.get_pull_requests(repo_name, auth_token)
        
        for pr in pull_requests:
            pr_details = get_pull_request_details(repo_name, pr['number'], auth_token)
            time_to_merge_or_close = get_time_to_merge_or_close(pr)
            description_length = get_description_length(pr)
            interactions = get_interactions(pr, repo_name, auth_token)

            print(f"Repository: {repo_name}, PR #{pr['number']}")
            print(f"Files changed: {pr_details['files_changed']}, Additions: {pr_details['additions']}, Deletions: {pr_details['deletions']}")
            print(f"Time to merge/close: {time_to_merge_or_close}")
            print(f"Description length: {description_length} characters")
            print(f"Comments count: {interactions['comments_count']}, Participants count: {interactions['participants_count']}")
            print("----------------------------------------------------------")

process_pull_requests(repositories, auth_token)