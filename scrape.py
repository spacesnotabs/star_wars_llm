import requests
import time
import os
from bs4 import BeautifulSoup

API = "https://starwars.fandom.com/api.php"
HEADERS = {"User-Agent": "ChrisRAG/0.1 (learning; contact: you@example.com)"}

def list_members(category):
    cont = None
    while True:
        params = {
            "action":"query",
            "list":"categorymembers",
            "cmtitle":f"Category:{category}",
            "cmtype":"page",
            "cmlimit":"500",
            "format":"json"
        }

        if cont is not None: 
            params["cmcontinue"] = cont

        r = requests.get(API, params=params, headers=HEADERS)
        r = r.json()

        for m in r["query"]["categorymembers"]:
            yield m["title"]

        cont = r.get("continue", {}).get("cmcontinue")
        if not cont: 
            break

    
if __name__ == "__main__":
    print("Listing members of Category:Character stubs")

    if not os.path.exists("characters"):
        os.makedirs("characters")

    max_count = 10
    for member in list_members("Character stubs"):
        if max_count <= 0:
            break

        print("Processing Member:", member)

        # The URL from the problem description was for a specific character.
        # This is a better API call to get the page content that can be parsed.
        url = f"https://starwars.fandom.com/api.php?action=parse&page={member}&prop=text&format=json"
        r = requests.get(url, headers=HEADERS)

        if r.status_code == 200:
            try:
                data = r.json()
                if 'parse' in data and 'text' in data['parse'] and '*' in data['parse']['text']:
                    html_content = data["parse"]["text"]["*"]
                    soup = BeautifulSoup(html_content, 'html.parser')
                    text = soup.get_text()

                    # The filenames can't contain slashes or quotes, so they are replaced.
                    safe_member_name = member.replace("/", "_").replace('"', '')

                    with open(f"characters/{safe_member_name}.txt", "w", encoding="utf-8") as f:
                        f.write(text)

                    print(f"Successfully saved data for {member}")
                else:
                    print(f"Could not find content for {member} in the response.")

            except (ValueError, KeyError) as e:
                print(f"Failed to parse data for {member}: {e}")

        else:
            print(f"Failed to retrieve data for {member}, status code: {r.status_code}")

        max_count -= 1
        time.sleep(1)