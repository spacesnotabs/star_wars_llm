import requests
import time

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

        print(r.url)
        print(r.status_code)
        r = r.json()

        print(r)
        for m in r["query"]["categorymembers"]:
            yield m["title"]

        cont = r.get("continue", {}).get("cmcontinue")
        print(cont)
        if not cont: 
            break

    
if __name__ == "__main__":
    print("Listing members of Category:Character stubs")
    # max_count = 10
    # for member in list_members("Character stubs"):
    #     if max_count <= 0:
    #         break
    #     max_count -= 1
    #     print("Member:", member)
    #     time.sleep(0.2)

    url = f"https://starwars.fandom.com/api.php/page/plain/Amsora"
    r = requests.get(url, headers=HEADERS)
    print(r.text)