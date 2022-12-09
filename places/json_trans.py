import json

with open('convert2.json', 'r', encoding='UTF-8') as f:
    place_data = json.load(f)

new_list = []
for data in place_data:
    new_data = {'model': 'places.place'}
    new_data["fields"] = data
    new_list.append(new_data)
    
with open('place_data_jeju2.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)