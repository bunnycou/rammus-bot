import json, requests

# import our hidden keys
secret = json.load(open("secret.json"))
key = secret["api-key"]

summonerName = input("Summoner Name: ").strip().lower()

account = json.loads(requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={key}").text)

print(account["summonerLevel"])