import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY=os.environ['GITHUB_KEY']
header = {'Authorization' : 'token '+ API_KEY}
BASE_URL='https://api.github.com'

def get_repositories():
    repositories = []
    res = requests.get(BASE_URL + '/search/repositories?q=ck_+in:name+org:wiley', headers= header)
    while 'next' in res.links.keys():
        json_response = res.json()
        for repo in json_response['items']:
            repositories.append({ 'name' : repo['name'] ,'url': repo['html_url'], 'owner': repo['owner']['login'], 'id' : repo['id']})

        res = requests.get(res.links['next']['url'], headers= header)

    json_response = res.json()
    for repo in json_response['items']:
        repositories.append({'name' : repo['name'] ,'url': repo['html_url'], 'owner': repo['owner']['login'], 'id' : repo['id']})

    return repositories

def get_teams(repo_name):
    res = requests.get(BASE_URL + '/repos/wiley/'+ repo_name +'/teams', headers= header)
    if res.status_code != 200:
        #print('WARNING: Unable to access the teams for the repo '+repo_name)
        return {}

    json_response = res.json()
    teams = {}
    while 'next' in res.links.keys():
        json_response = res.json()
    
        for team in json_response:
            teams[str(team['slug'])] = {'name' : team['name'], 'permission' : team['permission'], 'slug' : team['slug']}

        res = requests.get(res.links['next']['url'], headers= header)

    json_response = res.json()
    for team in json_response:
        teams[str(team['slug'])] = {'name' : team['name'], 'permission' : team['permission'], 'slug' : team['slug']}
    
    return teams

def get_collaborators(repo_name):
    res = requests.get(BASE_URL + '/repos/wiley/'+ repo_name +'/collaborators', headers= header)
    if res.status_code != 200:
        print('WARNING: Unable to access the collaborators for the repo '+repo_name)
        return {}

    json_response = res.json()
    collaborators = {}
    while 'next' in res.links.keys():
        json_response = res.json()
    
        for collaborator in json_response:
            collaborators[collaborator['login']] = {'name' : collaborator['login'], 'permissions' : collaborator['permissions']}

        res = requests.get(res.links['next']['url'], headers= header)

    json_response = res.json()
    for collaborator in json_response:
        collaborators[collaborator['login']] = {'name' : collaborator['login'], 'permissions' : collaborator['permissions']}
    
    return collaborators


def add_admin_to_repo(repo_name, user_login):
    
    data = {'permission': 'admin'}
    response = requests.put(BASE_URL + '/repos/wiley/'+ repo_name +'/collaborators/' + user_login, data = json.dumps(data), headers = header)
    if response.status_code != 201 and response.status_code != 204:
        print('Unable to add '+ user_login +' as Admin in '+ repo_name)

def add_team_to_repo(repo_name, team_slug, permission):
    
    data = {'permission': permission}
    response = requests.put(BASE_URL + '/orgs/wiley/teams/'+ team_slug +'/repos/wiley/' + repo_name, data = json.dumps(data), headers = header)
    if response.status_code != 201 and response.status_code != 204:
        print('Unable to add '+ team_slug +' as Admin in '+ repo_name)


if __name__ == '__main__':
     
    

    print('Get the repository list')
    repositories = get_repositories()
    print(str(len(repositories)) + ' repositories found')
    repositories_with_missing_team = {}
    for repo in repositories:
        repository_name = repo['name']
        if repository_name.startswith('ck_it') or repository_name.startswith('ck-it'):
            continue

        teams = get_teams(repository_name)
        for slug, team in teams.items():
            if team['permission'] == 'admin':
                print(team['name'] + ' is Admin on the repo: '+ repository_name)
                
        
        """
        print('Add pxotox as Admin on '+ repository_name)
        add_admin_to_repo(repository_name, 'pxotox')

        print('Add smartarello as Admin on '+ repository_name)
        add_admin_to_repo(repository_name, 'smartarello')
        """
    #collaborators = get_collaborators(repo)
    #logging.debug(collaborators)

    #add_admin_to_repo('ck_ckplayer', 'smartarello')
    #add_team_to_repo(repo, 'crossknowledge-maintainer', 'push')

