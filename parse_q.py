import json

with open("quran_english_1.json", "r", encoding="utf-8") as f:
    data =  json.load(f)

with open("surahNames.json", "r", encoding="utf-8") as f:
    surahNames =  json.load(f)


final_data = []

for i, (surah, ayats) in enumerate(zip(surahNames, data)):
    for j, ayat in enumerate(ayats):
        
        record = {
            "id": f"{i+1}:{j+1}",
            "surah": surah,
            "text": ayat
        }

        final_data.append(record)

with open("quran.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)