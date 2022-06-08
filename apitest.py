import json, requests, os

# import our hidden keys
secret = json.load(open("secret.json"))
key = secret["api-key"]


# get json file of all champs from DataDragon
# first check if we already have the most recent version by getting the version list and checking if we have the most recent one
ddVersions = json.loads(requests.get("https://ddragon.leagueoflegends.com/api/versions.json").text)
ddFName = f"dd{ddVersions[0]}.json"
# when it does not exist we check if an old version exists and delete it and then create a new one
if not os.path.exists(ddFName):
    if os.path.exists(f"dd{ddVersions[1]}.json"): os.remove(f"dd{ddVersions[1]}.json")
    ddFile = open(ddFName, "w")
    ddFile.write(requests.get(f"http://ddragon.leagueoflegends.com/cdn/{ddVersions[0]}/data/en_US/champion.json").text)

# now that we have that file, load it so we can use it
ddragon = json.load(open(ddFName))

# create a new dict to convert champion ids to actual champions
ddChamps = dict()
for x in ddragon["data"]:
    ddChamps[ddragon["data"][x]["key"]] = x

# get summoner name
#summonerName = input("Summoner Name: ").strip().lower()
summonerName = "bunnycou"

# get account from summoner name
account = json.loads(requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={key}").text)

# get their champ mastery list
masteryList = json.loads(requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{account['id']}?api_key={key}").text)

# iterate through the list and create a new dict of champs without chests
# sort it by 'champion points' or mastery score, descending
chestList = dict()
for x in masteryList:
    if not x["chestGranted"]:
        chestList[x["championId"]] = x["championPoints"]
chestList = dict(sorted(chestList.items(), key=lambda item: item[1], reverse=True))

#convert chestList to a champList
champList = list()
for x in chestList:
    champList.append(x)

# go through the top 5, resolve the id, and display them
finalList = list()
for x in range(0,5):
    finalList.append(ddChamps[f"{champList[x]}"])

print(finalList)