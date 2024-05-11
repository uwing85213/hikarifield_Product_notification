import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import random

####
#flag 
step_0 = False
step_1 = False
####
#value
json_data = []
item_id = 0
API_Message =""
token = "Your_Line_Notify_Token"
#func
# 生成随机等待时间
def random_wait():
	# 设置等待时间范围，单位为秒
	min_wait = 2  # 最小等待时间
	max_wait = 6  # 最大等待时间
	# 生成随机等待时间
	wait_time = random.uniform(min_wait, max_wait)
	# 返回随机等待时间
	print("delay time: ",wait_time," sec")
	return wait_time

def message_add(str_message):
	global API_Message
	API_Message += (str_message + "\n") 
	return 0

def lineNotifyMessage(token, msg):
	headers = {
		"Authorization": "Bearer " + token,
		"Content-Type" : "application/x-www-form-urlencoded"
	}
	payload = {'message': msg }
	r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
	return r.status_code

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

url_Homepage= 'https://store.hikarifield.co.jp/goods'
HomePage = requests.get(url_Homepage, headers=headers)
if HomePage.status_code == 200:
	soup = BeautifulSoup(HomePage.text, 'html.parser')
	step_0 = True
else:
	print( "商品頁面存取失敗" )
	message_add("商品頁面存取失敗")

if (step_0 == True):
	# 找到下拉式選單
	special_div = soup.find('div', class_='dropdown-menu')

	if special_div:
		# 把dropdown-item 內的 href & text取出 
		special_div2 = special_div.find_all( 'a', class_='dropdown-item' )
		for link in special_div2:
			href_value = link.get('href')
			#print("href value:", href_value)
			print("text value：", link.text.strip())
			message_add( ("text value：" + link.text.strip() ) )
			data = {
				"id": item_id,
				"href_value": href_value,
				"href_text": link.text.strip()
			}
			json_data.append(data)
			item_id+=1
		step_1 = True
	# 将数据转换为 JSON 格式的字符串
	# json_string = json.dumps(json_data, indent=4, ensure_ascii=False)
	else:
		print("未找到具有特定 class 的 div 標籤.")
		message_add("未找到具有特定 class 的 div 標籤.")

print("========================================================")
if (step_1 == True):
	#開始爬url
	time.sleep(random_wait())
	for i in range( 1 , item_id): #0不用 最後一個數要-1 
		print( "執行中:" , json_data[i]["href_text"] )
		print( "URL:" 	, json_data[i]["href_value"] )
		message_add( "執行中:" + json_data[i]["href_text"] )
		message_add( "URL:" 	+ json_data[i]["href_value"] )

		url= json_data[i]["href_value"]
		resp = requests.get(url, headers=headers)

		if resp.status_code == 200:
			soup = BeautifulSoup(resp.text, 'html.parser')
			for link in soup.find_all('button'):
				text_condition = link.text.strip()
				if (text_condition == "加入购物车"):
					data_good_id = link.get('data-good-id')
					print( "id:" , data_good_id , "尚有存貨" )
					message_add( "id:" + data_good_id + "尚有存貨" )
				elif text_condition == "尚未开售":
					print("尚未开售")
					message_add("尚未开售")
				elif text_condition == "已售罄":
					print("已售罄")
					message_add("已售罄")
				# else:
				# 	print("非商品 or 沒找到")
		else:
			print('無法取得網頁內容。')
			message_add("無法取得網頁內容。")
		time.sleep(random_wait())
	print( "All Task Finish!" )
	message_add("All Task Finish!")
else:
	print( "什麼都沒有,停止深度搜索" )
	message_add("什麼都沒有,停止深度搜索")

print(lineNotifyMessage(token, API_Message))
