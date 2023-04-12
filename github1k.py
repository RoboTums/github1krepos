import pandas as pd
import requests 

def get_github_repos()-> pd.DataFrame:

    headers = {"Authorization": "Token [token-here]"}
    # set the search query parameters to retrieve up to 1000 repos with 1000 or more stars
    params = {"q": "stars:>=1000", "sort": "stars", "order": "desc", "per_page": 100, "page": 1}
    all_repos = []
     
    # make successive API requests until we have 1000 repos or there are no more pages
    while len(all_repos) < 40300:
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()
        if 'items' not in data.keys():
            params["page"] += 1
            time.sleep(6)
            if params['page']%10 == 0:
                print(f'scraped up to {params["page"]} pages')

            continue
        else:
            for i in range(len(data['items'])):
                result = {
                    'language':data['items'][i]['language'],
                    'project':data['items'][i]['name'],
                    'description':data['items'][i]['description'],
                    'homepage':data['items'][i]['html_url'],
                    'stars':data['items'][i]['stargazers_count'],
                    'topics':" ".join(data['items'][i]['topics']),
                    'forks':data['items'][i]['forks']
                }
                all_repos.append(result)
            time.sleep(6)
            # check if there are no more results
            # add the current page of results to the list of all repos
            all_repos.extend(data["items"])
            # move to the next page of results
            params["page"] += 1
            if params['page']%10 == 0:
                print(f'scraped up to {params["page"]} pages')

    # do something with the list of 1000 repos
    print(f"Found {len(all_repos)} repos with 1000 or more stars, on page {params['page']}")
    return pd.DataFrame(all_repos)

if __name__ == "__main__":
    df = get_github_repos()
    df.to_csv('github1k.csv')