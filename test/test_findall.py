#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pymysql
import re
import datetime

starttime = datetime.datetime.now()
# 药路通网站变量
domain = "http://www.yaolutong.com"
start_url_count = 50024
#product_url_count = 200
product_url_count = 55000

# product_basic库
#re_product_id = 
re_product_name = '产品名称：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_approval_number = '批准文号：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_product_specifications = '产品规格：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_product_dosage = '产品剂型：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_manufacture_factory = '生产厂家：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_investment_enterprise = '招商企业：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_procuct_channels = '产品渠道：'.decode("utf8") + '</span>((?:.|\n)*?)</li>'
re_procuct_category = '产品类别：'.decode("utf8") + '.*bigkind=(.+?)"'
#re_procuct_category = '产品类别：'.decode("utf8") + '.*bigkind=(.+?)".*sKey=(.+?)"'
# product_detail库
re_brand_name = '商标名称：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_properties = '产品性能：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_usage = '用法用量：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_ingredients = '成    份：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_product_description = '产品说明：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_procuct_pack = '产品包装：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_procuct_character = '产品性状：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
re_investment_area = '招商区域：'.decode("utf8") + '.*\n.*"nei">((?:.|\n)*?) </li>'
# company_contact库
re_contact_name = '<p>联系人：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_telphone = '<p>电话：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_mobilephone = '<p>手机：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_wechat = '<p>微信：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_qq = '<p>Q Q：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_mail = '<p>邮箱：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_website = '<p>网址：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_fax = '<p>传真：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_address = '<p>地址：'.decode("utf8") + '((?:.|\n)*?)</p>'
re_postcode = '<p>邮编：'.decode("utf8") + '((?:.|\n)*?)</p>'
old_re_all = re_product_name + '(?:.|\n)*' + re_approval_number + '(?:.|\n)*' + re_product_specifications + '(?:.|\n)*' \
	+ re_product_dosage  + '(?:.|\n)*' +  re_manufacture_factory  + '(?:.|\n)*' +  re_investment_enterprise + '(?:.|\n)*' \
	+ re_procuct_channels  + '(?:.|\n)*' + re_procuct_category  + '(?:.|\n)*' + re_brand_name  + '(?:.|\n)*' \
	+ re_product_properties  + '(?:.|\n)*' + re_product_usage  + '(?:.|\n)*' + re_product_ingredients  + '(?:.|\n)*' \
	+ re_product_description  + '(?:.|\n)*' + re_procuct_pack  + '(?:.|\n)*' + re_procuct_character  + '(?:.|\n)*' \
	+ re_investment_area  + '(?:.|\n)*' + re_contact_name  + '(?:.|\n)*' +  re_telphone + '(?:.|\n)*' \
	+ re_mobilephone  + '(?:.|\n)*' + re_wechat  + '(?:.|\n)*' + re_qq  + '(?:.|\n)*' \
	+ re_mail  + '(?:.|\n)*' + re_website  + '(?:.|\n)*' + re_fax  + '(?:.|\n)*' \
	+ re_address  + '(?:.|\n)*' + re_postcode
new_re_all = re.compile(old_re_all)

#* 初始网站访问session
def request_url(page_url):
    headers = {
            'Host': 'www.yaolutong.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
            }
    session = requests.Session()
    s_page = session.get(page_url, headers=headers)
    s_page.encoding = 'utf-8'
    return s_page

s = request_url('http://www.yaolutong.com/zhaoshang/96032.html')
#result = re.findall(re_brand_name, s.text)
#result01 = re.findall(re_product_properties, s.text)
old_product_list = new_re_all.findall(s.text)
#print old_product_list
#new_product_list = [ key.encode('utf8') for key in old_product_list[0] ]
#for i in new_product_list:
#	print i
endtime = datetime.datetime.now()
print (endtime - starttime).microseconds




