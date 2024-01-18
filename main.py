import selenium
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from csv import writer


while True:
    comp_type = str(input("Komponentes veids - (CPU, VIDEO): ").upper())
    types = ["CPU", "VIDEO"]
    if comp_type in types:
        break
    else:
        print("Ievadi komponentes veidu no piedāvātajiem!")

header = ["komponentes veids", "modelis", "links", "cena", "ietaupijums"]
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    file.close()


service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)
actions = ActionChains(driver)

url_ss = "https://www.ss.com/lv/electronics/computers/completing-pc/" + comp_type.lower() + "/sell"
driver.get(url_ss)
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div[6]/div/div/table/tbody/tr/td[2]/button").click()

def cpu_finder():
    current_cpu_url = driver.current_url
    cpu_pattern = re.compile(r'\b(?:i[3579]|Pentium|Amd FX|Ryzen|i[3579]\s?[a-zA-Z0-9]+)[\s-]?\d{4,5}[a-zA-Z]?[fk]?|Ryzen [1-9] \d{3,4}[xX]?\b', re.IGNORECASE)
    cpu_find = driver.find_element(By.ID, "msg_div_msg")
    cpu_model = cpu_pattern.findall(cpu_find.get_attribute("innerHTML"))
    price_find = driver.find_element(By.CLASS_NAME, "ads_price").get_attribute("textContent").replace(" ", "").replace("€", "")
    row = []
    if cpu_model:
        row.extend((comp_type, cpu_model[0].replace(" ", "-"), current_cpu_url, price_find))
        with open('results.csv', 'a', newline='') as file:
             writer = csv.writer(file)
             writer.writerow(row)
             file.close()
    
def gpu_finder():
    current_gpu_url = driver.current_url
    gpu_pattern = re.compile(r'\b(?:Rtx|Gtx|rx|Rx)\s?\d{3,4}(?:Ti|xt|super)?\b', re.IGNORECASE)
    gpu_find = driver.find_element(By.ID, "msg_div_msg")
    gpu_model = gpu_pattern.findall(gpu_find.get_attribute("innerHTML"))
    price_find = driver.find_element(By.CLASS_NAME, "ads_price").get_attribute("textContent").replace(" ", "").replace("€", "")
    row = []
    if gpu_model:
        row.extend((comp_type, gpu_model[0].replace("-", " "), current_gpu_url, price_find))
        with open('results.csv', 'a', newline='') as file:
             writer = csv.writer(file)
             writer.writerow(row)
             file.close()


pages = len(driver.find_elements(By.XPATH,
    "/html[1]/body[1]/div[4]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[2]/a"))
for n in range (2, pages+1):
    rows = len(driver.find_elements(By.XPATH, 
    "/html[1]/body[1]/div[4]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/table[2]/tbody[1]/tr/td[3]/div[1]/a[1]"))
    for i in range(2, rows+2):
        elem = (driver.find_element(By.XPATH, 
        "/html[1]/body[1]/div[4]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/table[2]/tbody[1]/tr["+str(i)+"]/td[3]"))
        actions.scroll_to_element(elem)
        elem.click()
        match comp_type:
            case "CPU":
                cpu_finder()
            case "VIDEO":
                gpu_finder()
        driver.back()
    page = (driver.find_element(By.XPATH, 
            "/html[1]/body[1]/div[4]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[2]/a["+str(n)+"]"))
    actions.scroll_to_element(page)
    page.click()


def cpu_pricecheck():
    with open("results.csv", "r") as file:
        next(file)
        for row in file:
            find = driver.find_element(By.ID, "CPUinput")
            find.clear()
            find.send_keys(row.split(",")[1])
            find = driver.find_element(By.CLASS_NAME, "componentList").click()
            find = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[2]/span[3]/div[2]")
            saved_price.append(int(find.get_attribute("textContent").strip().replace("$", "").replace("Price", ""))*0.9 - int(row.split(",")[3]))
            


def gpu_pricecheck():
    driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[1]/div[2]").click()
    with open("results.csv", "r") as file:
        next(file)
        for row in file:
            find = driver.find_element(By.ID, "GPUinput")
            find.clear()
            find.send_keys(row.split(",")[1])
            find = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div[1]/nav/ul").click()
            find = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[2]/span[3]/div[2]")
            saved_price.append(int(find.get_attribute("textContent").strip().replace("$", "").replace("Price", ""))*0.9 - int(row.split(",")[3]))
            
saved_price = []
url_pcp = "https://pcpricer.net/"
driver.get(url_pcp)
time.sleep(1)
match comp_type:
            case "CPU":
                cpu_pricecheck()
            case "VIDEO":
                gpu_pricecheck()

with open('results.csv', 'r') as f:
    next(f)
    reader = csv.reader(f)
    rows = list(reader)

for i, row in enumerate(rows):
    row.append(round(saved_price[i], 1))

with open('results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)
    f.close()
