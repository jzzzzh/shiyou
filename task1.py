from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import argparse
from bs4 import BeautifulSoup
import re

def validate_date(date):
    pattern = r'^\d{8}$'  # 8位数字格式，例如20211231
    if not re.match(pattern, date):
        raise ValueError("Invalid date format. Please use the format YYYYMMDD.")


def get_option(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    options = soup.find_all('option')
    money_dict = {}
    for i, option in enumerate(options):
        text = option.text
        money_dict[text] = i+1
    return money_dict

def money_en2cn():
    driver = webdriver.Edge()
    driver.get(r'https://www.11meigui.com/tools/currency')
    sleep(2)
    element = driver.find_element(By.XPATH, '/html/body/main/div/table/tbody')
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tr')
    currency_data = []
    for row in rows:
        columns = row.select('td')
        if len(columns) >= 5:
            currency_name = columns[1].get_text(strip=True)
            currency_abbreviation = columns[4].get_text(strip=True)
            currency_data.append((currency_name, currency_abbreviation))
    money_en2cn_list = {}
    for currency in currency_data:
        money_en2cn_list[currency[1]] = currency[0]
    return money_en2cn_list

def get_option_num(money, money_dict):
    # money_dict = {'选择货币': 1, '英镑': 2, '港币': 3, '美元': 4, '瑞士法郎': 5, '德国马克': 6, '法国法郎': 7, '新加坡元': 8, '瑞典克朗': 9, '丹麦克朗': 10, '挪威克朗': 11, '日元': 12, '加拿大元': 13, '澳大利亚元': 14, '欧元': 15, '澳门元': 16, '菲律宾比索': 17, '泰国铢': 18, '新西兰元': 19, '韩元': 20, '卢布': 21, '林吉特': 22, '新台币': 23, '西班牙比塞塔': 24, '意大利里拉': 25, '荷兰盾': 26, '比利时法郎': 27, '芬兰马克': 28, '印度卢比': 33, '印尼卢比': 30, '巴西里亚尔': 31, '阿联酋迪拉姆': 32, '南非兰特': 34, '沙特里亚尔': 35, '土耳其里拉': 36}
    num = money_dict[money]
    return num



def open_website(date, money):
    
    driver = webdriver.Edge()
    driver.get(r'https://www.boc.cn/sourcedb/whpj/')
    money_dict = get_option(driver)
    sleep(1)
    date_input = driver.find_element(By.XPATH,'//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input')
    date_input.send_keys(date)
    sleep(1)
    select_num = get_option_num(money, money_dict)
    money_select = driver.find_element(By.XPATH, f"//*[@id='pjname']/option[{select_num}]")
    money_select.click()
    sleep(1)
    search = driver.find_element(By.XPATH,'//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')
    search.click()
    sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tr_elements = soup.find_all('tr')
    money_list = []
    for tr in tr_elements:
        money_ans = tr.select('td:nth-of-type(5)')
        if money_ans:
            money_ans_text = money_ans[0].get_text(strip=True)
            money_list.append(money_ans_text)

    driver.close()
    return money_list

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('date', type=str, help='date(20211231)')
    parser.add_argument('money', type=str, help='money(USD)')

    args = parser.parse_args()
    date = args.date
    validate_date(date)
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    money = args.money
    money_en2cn_list =  money_en2cn()
    money_cn = money_en2cn_list[money]
    money_list = open_website(date, money=money_cn)
    output = f"{money}  {date} : {money_list[1]}"
    with open("result.txt", "w") as f:
        f.write(output)
    


    