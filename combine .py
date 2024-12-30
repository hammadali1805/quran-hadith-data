import json

with open("quran.json", "r", encoding="utf-8") as f:
    quran =  json.load(f)

with open("bukhari2.json", "r", encoding="utf-8") as f:
    bukhari =  json.load(f)

with open("muslim2.json", "r", encoding="utf-8") as f:
    muslim =  json.load(f)


data = []

for i in quran+bukhari+muslim:
    record = {
        "refrence": i['id'],
        "text": i['text']
    }

    data.append(record)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)