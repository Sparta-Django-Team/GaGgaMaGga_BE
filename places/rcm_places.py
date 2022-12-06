import pandas as pd
import numpy as np
import sqlite3

import random
import json

# import sys
# import os
# import django

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaggamagga.settings')
# django.setup()

conn = sqlite3.connect("./db.sqlite")
cur = conn.cursor()
cur.execute("SELECT * FROM places")
rows = cur.fetchall()
cols = [column[0] for column in cur.description]
data_df = pd.DataFrame.from_records(data=rows, columns=cols)
conn.close()
print(data_df)






# new_list = []
# for i in range(301):
#     new_data = {"model":"places.place"}
#     new_dict = {}
#     new_dict['score_taste'] = random.randint(1, 5)
#     new_dict['score_service'] = random.randint(1, 5)
#     new_dict['score_cleanliness'] = random.randint(1, 5)
#     new_data["fields"] = new_dict
#     new_list.append(new_data)

# with open('place_score.json', 'w', encoding='UTF-8') as f:
#     json.dump(new_list, f, ensure_ascii=False, indent=2)


# with open('data.json', 'r',encoding='utf-8-sig') as f:
#     place_data = json.load(f)

# new_list = []
# for data in place_data:
#     new_data = {'model': 'places.place'}
#     new_data["fields"] = data
#     new_list.append(new_data)
    
# with open('place_data_fin.json', 'w', encoding='UTF-8') as f:
#     json.dump(new_list, f, ensure_ascii=False, indent=2)


