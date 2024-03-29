#! /bin/env python3
import os
import sys
import subprocess
from functools import lru_cache
import urllib3
import fire
import json
import glob
coreurl = '''
curl 'https://appzdsbtscz6568.h5.xiaoeknow.com/micro_page/xe.micro_page.h5_more/1.0.0' \
  -H 'authority: appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/json' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36' \
  -H 'token: xiaoe_open_api' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'origin: https://appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://appzdsbtscz6568.h5.xiaoeknow.com/mp_more/eyJpZCI6IjI2NzY5NiIsImNoYW5uZWxfaWQiOiIiLCJjb21wb25lbnRfaWQiOjI3MTI2OTF9' \
  -H 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,de;q=0.5,pl;q=0.4,ny;q=0.3' \
  -H 'cookie: xenbyfpfUnhLsdkZbX=0; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%2217d12cfa4a8362-0566b2d6b6b2d6-57b1a33-2073600-17d12cfa4a9e5a%22%7D; sa_jssdk_2015_appzdsbtscz6568_h5_xiaoeknow_com=%7B%22distinct_id%22%3A%22u_5e9ccfe3b3c72_cRNb8sZxMF%22%2C%22first_id%22%3A%2217d12cfa4a8362-0566b2d6b6b2d6-57b1a33-2073600-17d12cfa4a9e5a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; anony_token=2d9f5f01b6f89d88f5caaa238ec73ff1; ko_token=ca0fff4624006fa66440b7d7dc4e4315; shop_version_type=4; dataUpJssdkCookie={"wxver":"","net":"","sid":""}; h5_transport_time=2021-12-01+12%3A37%3A00; logintime=1638333440' \
  --data-raw '{"bizData":{"id":"267696","page_num":1,"page_size":10,"last_id":"","component_id":2712691,"channel_id":""}}' \
  --compressed ;
'''
microurl= '''
curl 'https://appzdsbtscz6568.h5.xiaoeknow.com/xe.micro_page.h5_more/1.0.0' \
  -H 'authority: appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,de;q=0.5,pl;q=0.4,ny;q=0.3' \
  -H 'content-type: application/json' \
  -H 'cookie: shop_version_type=4; anony_token=9262c5ece1d1c0a1339e6fa2cfec90af; xenbyfpfUnhLsdkZbX=0; dataUpJssdkCookie={"wxver":"","net":"","sid":""}; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%22183b589df7b1272-00291b6c04ab83-26021c51-3399414-183b589df7c195b%22%7D; sajssdk_2015_new_user_appzdsbtscz6568_h5_xiaoeknow_com=1; ko_token=a892ca5c5b99a2af19bfcfc7451d7b4a; sa_jssdk_2015_appzdsbtscz6568_h5_xiaoeknow_com=%7B%22distinct_id%22%3A%22u_5e9ccfe3b3c72_cRNb8sZxMF%22%2C%22first_id%22%3A%22183b589df7b1272-00291b6c04ab83-26021c51-3399414-183b589df7c195b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; logintime=1665203620' \
  -H 'origin: https://appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'referer: https://appzdsbtscz6568.h5.xiaoeknow.com/p/decorate/more/eyJpZCI6IjI2NzY5NyIsImNoYW5uZWxfaWQiOiIiLCJjb21wb25lbnRfaWQiOjI3MTI2OTF9' \
  -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'token: xiaoe_open_api' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
  --data-raw '{"app_id":"appzDSBtscz6568","user_id":"u_5e9ccfe3b3c72_cRNb8sZxMF","agent_type":1,"agent_version":1,"is_offset":1,"app_version":"0.1","agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36","buz_data":{"id":"267697","page_num":1,"page_size":900,"last_id":"","component_id":2712691,"channel_id":"","alive_type":""}}' \
  --compressed
'''
readingurl = '''
curl 'https://appzdsbtscz6568.h5.xiaoeknow.com/micro_page/xe.micro_page.h5_more/1.0.0' \
  -H 'authority: appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'content-type: application/json' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36' \
  -H 'token: xiaoe_open_api' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'origin: https://appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://appzdsbtscz6568.h5.xiaoeknow.com/mp_more/eyJpZCI6IjI2NzY4OCIsImNoYW5uZWxfaWQiOiIiLCJjb21wb25lbnRfaWQiOjI3MTI2OTF9' \
  -H 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,de;q=0.5,pl;q=0.4,ny;q=0.3' \
  -H 'cookie: xenbyfpfUnhLsdkZbX=0; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%2217d12cfa4a8362-0566b2d6b6b2d6-57b1a33-2073600-17d12cfa4a9e5a%22%7D; sa_jssdk_2015_appzdsbtscz6568_h5_xiaoeknow_com=%7B%22distinct_id%22%3A%22u_5e9ccfe3b3c72_cRNb8sZxMF%22%2C%22first_id%22%3A%2217d12cfa4a8362-0566b2d6b6b2d6-57b1a33-2073600-17d12cfa4a9e5a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; anony_token=2d9f5f01b6f89d88f5caaa238ec73ff1; ko_token=ca0fff4624006fa66440b7d7dc4e4315; shop_version_type=4; dataUpJssdkCookie={"wxver":"","net":"","sid":""}; h5_transport_time=2021-12-01+12%3A55%3A02; logintime=1638334505' \
  --data-raw '{"bizData":{"id":"267688","page_num":1,"page_size":999,"last_id":"","component_id":2712691,"channel_id":""}}' \
  --compressed ;
'''
def xx(filex):
    with open(filex,'r') as fid:
        a=fid.readlines()[0]
        b=json.loads(a)['data']['component']['list']
        for c in b:
            print(c['spu_id'])
            # print(f"https://appzdsbtscz6568.h5.xiaoeknow.com/v1/course/audio/{c['spu_id']}?type=2 --- {c['title']}")

def yy(filex):
    with open(filex,'r') as fid:
        audiolist = fid.readlines()
    a='''
curl 'https://appzdsbtscz6568.h5.xiaoeknow.com/xe.course.business.audio.info.get/2.0.0' \
  -H 'authority: appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,de;q=0.5,pl;q=0.4,ny;q=0.3' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -H 'cookie: shop_version_type=4; anony_token=9262c5ece1d1c0a1339e6fa2cfec90af; xenbyfpfUnhLsdkZbX=0; dataUpJssdkCookie={"wxver":"","net":"","sid":""}; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%22183b589df7b1272-00291b6c04ab83-26021c51-3399414-183b589df7c195b%22%7D; sajssdk_2015_new_user_appzdsbtscz6568_h5_xiaoeknow_com=1; ko_token=a892ca5c5b99a2af19bfcfc7451d7b4a; sa_jssdk_2015_appzdsbtscz6568_h5_xiaoeknow_com=%7B%22distinct_id%22%3A%22u_5e9ccfe3b3c72_cRNb8sZxMF%22%2C%22first_id%22%3A%22183b589df7b1272-00291b6c04ab83-26021c51-3399414-183b589df7c195b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; logintime=1665206068' \
  -H 'origin: https://appzdsbtscz6568.h5.xiaoeknow.com' \
  -H 'referer: https://appzdsbtscz6568.h5.xiaoeknow.com/p/course/audio/a_632ac0fae4b0eca59c336ebf?type=2' \
  -H 'req-uuid: 20221008131409000640628' \
  -H 'retry: 1' \
  -H 'sec-ch-ua: "Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36' \
  --data-raw 'bizData%5Bresource_id%5D=
  '''
    c=''' 
    '\
      --compressed -o
    '''
    with open('getmp3list.sh','w') as fid:
        for x in audiolist:
            # print(x)
            fid.write(a.strip()+x.strip()+c.strip()+" "+x.strip()+".data")
            fid.write('\n')
    subprocess.run(["chmod","+x",f"{os.path.join(os.path.abspath('.'),'getmp3list.sh')}"])

def zz():
    a=glob.glob("*.data")
    with open('mp3list_url.sh','w') as fid:
        for x in a:
            b=json.load(open(x))['data']['audio_info']
            title = b['title']
            # data = b['data']
            audiourl = b['audio_url']
            fid.write(f"curl {audiourl} -o '{title}.mp3'")
            fid.write('\n')
    subprocess.run(["chmod","+x",f"{os.path.join(os.path.abspath('.'),'mp3list_url.sh')}"])


if __name__ == '__main__':
    fire.Fire()
    # curl core >> mirco.data
    # python3 songhongbing.py xx micro.data 
    # python3 songhongbing.py xx micro.data > ids
    # python3 songhongbing.py yy ids
    # python3 songhongbing.py zz
    # nohup mp3list_url.txt &
