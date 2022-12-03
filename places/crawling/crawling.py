import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


driver = webdriver.Chrome(ChromeDriverManager().install())


# 크롬창 숨기기
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)  # 드라이버 경로

url = 'https://map.naver.com/v5/search'
driver.get(url)
key_word = '강남구 치킨'  # 검색어


# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


# css를 찾을때 까지 10초 대기
time_wait(20, 'div.input_box > input.input_search')

search = driver.find_element(
    By.CSS_SELECTOR, 'div.input_box > input.input_search')

search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(1)


# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경


# 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)


# frame 변경
switch_frame('searchIframe')
page_down(40)
sleep(5)


# 매장 리스트
store_list = driver.find_elements(By.CSS_SELECTOR, '.CHC5F')
# 페이지 리스트
next_btn = driver.find_elements(By.CSS_SELECTOR, '.zRM9F > a')

# list 생성
place_list = []
# 시작시간
start = time.time()

count=0

# 크롤링 (페이지 리스트 만큼)
for btn in range(len(next_btn))[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
    store_list
    for data in range(len(store_list)):  # 매장 리스트 만큼
        page = driver.find_elements(By.CSS_SELECTOR, '.tzwk0')
        page[data].click()
        sleep(2)
        try:
            # 상세 페이지로 이동
            switch_frame('entryIframe')
            # time_wait(5, '.zD5Nm')
            time.sleep(5)
            # 스크롤을 맨밑으로 1초간격으로 내린다.
            for down in range(3):
                sleep(1)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

            # -----매장명 가져오기-----
            store_name = driver.find_element(By.CSS_SELECTOR, '.Fc1rA').text

            # -----카테고리-----
            try:
                store_category = driver.find_element(
                    By.CSS_SELECTOR, '.DJJvD').text
            except:
                pass

            # -----평점-----
            try:
                store_rating = driver.find_element(
                    By.CSS_SELECTOR, '.PXMot > em').text
            except:
                pass

            # -----주소(위치)-----
            try:
                store_addr = driver.find_element(
                    By.CSS_SELECTOR, '.IH7VW').text
            except:
                pass
            
            
            # -----영업시간-----
            try:
                store_time = driver.find_element(
                    By.CSS_SELECTOR, '.MxgIj > time').text
            except:
                pass

            # -----전화번호 가져오기-----
            try:
                store_tel = driver.find_element(By.CSS_SELECTOR, '.dry01').text
            except:
                pass





            # -----썸네일 사진 주소-----
            try:
                thumb_list = driver.find_element(By.CSS_SELECTOR, '.K0PDV').value_of_css_property(
                    'background-image')  # css 속성명을 찾는다
                store_thumb = re.sub(
                    'url|"|\)|\(', '', thumb_list)  # url , (" ") 제거
            except:
                pass

            switch_frame('searchIframe')
            
            
            # 페이지 전환
            switch_frame('searchIframe')

            # ---- dict에 데이터 집어넣기----

            
            new_place = {"model" :"places.place"}
            new_place["fields"] = {}
            new_place["fields"]["place_name"] = store_name
            new_place["fields"]["category"] = store_category
            new_place["fields"]["place_number"] = store_name
            new_place["fields"]["rating"] = store_rating
            new_place["fields"]["place_address"] = store_addr
            new_place["fields"]["place_time"] = store_time
            new_place["fields"]["place_img"] = store_thumb
            new_place["fields"]["latitude"] = ""
            new_place["fields"]["longitude"] = ""
            new_place["fields"]["menu"] = ""



            switch_frame('searchIframe')
            sleep(1)

        except:
            print('ERROR!' * 3)

        # 다음 페이지 버튼
        if page[-1]:  # 마지막 매장일 경우 다음버튼 클릭
            next_btn[-1].click()
            sleep(2)
        else:
            print('페이지 인식 못함')
            break
        count +=1
        print(count)

print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을닫는다.

# json 파일로 저장
with open('places/crawling/store_data.json', 'w', encoding='utf-8') as f:
    json.dump(place_list, f, indent=4, ensure_ascii=False)
