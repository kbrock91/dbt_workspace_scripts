import requests

# Configuration
NEW_GIT_ORG_REPO= 'sam-dbt-labs/medstar_demo'
API_BASE_URL = 'https://cloud.getdbt.com/api/v3'
DBT_CLOUD_ACCOUNT_ID = ''
DBT_CLOUD_PROJECT_ID = ''
DBT_CLOUD_API_TOKEN = ''
GITHUB_INSTALLATION_ID = '' 
#In order to find the github_installation_id, you can log in to dbt Cloud, replace <dbt_cloud_url> by your dbt Cloud URL and run the following commands in the Google Chrome console:
# dbt_cloud_api_result = await (fetch('https://<dbt_cloud_url>/api/v2/integrations/github/installations/').then(res => res.json()));
# console.log("github_application_id: " + dbt_cloud_api_result.filter(res => res["access_tokens_url"].includes("github"))[0]["id"]);
# Copy
# Alternatively, you can go to the page https://<dbt_cloud_url>/api/v2/integrations/github/installations/ and read the value of id or use the http provider to retrieve it automatically like in the example below.


REMOTE_URL = f'git://github.com/{NEW_GIT_ORG_REPO}.git'

HEADERS = {
    'Authorization': f'Token {DBT_CLOUD_API_TOKEN}',
    'Content-Type': 'application/json'
}

# === Functions ===

def get_current_project_info(dbt_cloud_project_id):
    url = f"{API_BASE_URL}/accounts/{DBT_CLOUD_ACCOUNT_ID}/projects/{dbt_cloud_project_id}/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code in (200, 201):
        print(f"✅ Project fetched successfully. name: {response.json()['data']['name']}, repo_id: {response.json()['data'].get('repository_id')}")
        return response.json()['data']['name'], response.json()['data'].get('repository_id')
    else:
        raise Exception(f"❌ Error fetching project: {response.status_code} - {response.text}")
        
def delete_repo(current_repo_id):
    url = f'{API_BASE_URL}/accounts/{DBT_CLOUD_ACCOUNT_ID}/projects/{DBT_CLOUD_PROJECT_ID}/repositories/{current_repo_id}/'
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 200:
        print("✅ Successfully unlinked (deleted) the repository.")
    else:
        raise Exception(f"❌ Failed to unlink the repository: {response.status_code} - {response.text}")  
        
def create_repository():
    payload = {
        'account_id': DBT_CLOUD_ACCOUNT_ID,
        'project_id': DBT_CLOUD_PROJECT_ID,
        'remote_url': REMOTE_URL,
        'git_clone_strategy': 'github_app',
        'github_installation_id': GITHUB_INSTALLATION_ID,
        'pull_request_url_template': f'https://github.com/{NEW_GIT_ORG_REPO}/compare/{{source}}...{{destination}}'
    }
    url = f"{API_BASE_URL}/accounts/{DBT_CLOUD_ACCOUNT_ID}/projects/{DBT_CLOUD_PROJECT_ID}/repositories/"
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code in (200, 201):
        print(f"✅ Repository { response.json()['data']['id']} created successfully.")
        return response.json()['data']['id']
    else:
        raise Exception(f"❌ Error creating repository: {response.status_code} - {response.text}")


def link_repository_to_project(project_name, repo_id):
    url = f"{API_BASE_URL}/accounts/{DBT_CLOUD_ACCOUNT_ID}/projects/{DBT_CLOUD_PROJECT_ID}/"
    payload = {
        'name': project_name,
        'repository_id': repo_id
    }
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print("✅ Successfully linked repository to project.")
    else:
        raise Exception(f"❌ Failed to link repository: {response.status_code} - {response.text}")


# === Main ===
if __name__ == "__main__":
    try:
        project_name, current_repo_id = get_current_project_info(DBT_CLOUD_PROJECT_ID)
        delete_repo(current_repo_id)
        repo_id = create_repository()
        link_repository_to_project(project_name, repo_id)
    except Exception as e:
        print(str(e))
