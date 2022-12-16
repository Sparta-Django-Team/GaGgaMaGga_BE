import requests, json


place_list = []
url_keyword = []        # 찾고자 하는 키워드 입력

for k in range(len(url_keyword)):
    for j in range(1, 7):
        url = f"https://map.naver.com/v5/api/search?caller=pcweb&query={url_keyword[k]}&type=all&page={j}&displayCount=40&lang=ko"
        response = requests.get(url, headers={'user-agent': 'Chrome/106.0.5249.119'})
        result = json.loads(response.content)
        numbers = result['result']['place']['list']
        
        for i in range(0,len(numbers)):
            new_data = {'model': 'places.place'}
            inner_dict = {}

            inner_dict["place_name"] = numbers[i]['name'] if numbers[i]['name'] != [] else ""
            inner_dict["category"] = numbers[i]['category'][0] if numbers[i]['category'][0] != [] else ""
            inner_dict["place_address"] = numbers[i]['roadAddress'] if numbers[i]['roadAddress'] != [] else ""
            inner_dict["place_number"] = numbers[i]['tel'] if numbers[i]['tel'] != [] else ""
            inner_dict["place_time"] = numbers[i]['businessStatus']['lastOrder'] if numbers[i]['businessStatus']['lastOrder'] != [] else ""
            inner_dict["place_img"] = numbers[i]['thumUrl'] if numbers[i]['thumUrl'] != [] else ""
            inner_dict["menu"] = numbers[i]['menuInfo'] if numbers[i]['menuInfo'] != [] else ""
            inner_dict["place_desc"] = numbers[i]['microReview'][0] if numbers[i]['microReview'] != [] else ""
            inner_dict["latitude"] = numbers[i]['y'] if numbers[i]['y'] != [] else ""
            inner_dict["longitude"] = numbers[i]['x'] if numbers[i]['x'] != [] else ""

            new_data["fields"] = inner_dict
            place_list.append(new_data)

with open('./file_name.json', 'w', encoding='UTF-8') as f:
    json.dump(place_list, f, ensure_ascii=False, indent=2)
