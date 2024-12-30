import json

with open("muslim.json", "r", encoding="utf-8") as f:
    data =  json.load(f)


for i in data:
    i['id'] = f"{i['book']} {i['id']}"

with open("muslim2.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)