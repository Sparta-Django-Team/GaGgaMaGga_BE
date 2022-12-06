import json

with open('review_data.json', 'r',encoding='utf-8-sig') as f:
    place_data = json.load(f)

new_list = []
for data in place_data:
    new_data = {'model': 'reviews.review'}
    new_data["fields"] = data
    new_list.append(new_data)
    
with open('review_data_trans.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)