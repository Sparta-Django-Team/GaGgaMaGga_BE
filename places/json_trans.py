import json

with open('users.json', 'r') as f:
    place_data = json.load(f)

new_list = []
for data in place_data:
    new_data = {'model': 'users.user'}
    new_data["fields"] = data
    new_list.append(new_data)
    
with open('users_trans.json', 'w', encoding='UTF-8') as f:
    json.dump(new_list, f, ensure_ascii=False, indent=2)