import time
from multiprocessing.dummy import Pool as ThreadPool 
import os
import sys
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import partial
from image_downloader import datarow, download, get_img_url
from csv_writer import create_csv, write_csv

driver = webdriver.Chrome()
driver.get("https://apps.polkcountyiowa.gov/PolkCountyInmates/CurrentInmates")
driver.minimize_window()

urls_ = []
dataset_ = []
img_scrs = []

def get_urls():
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME,"tbody")))
    except exceptions.TimeoutException as e:
        driver.close()
        sys.exit(f"COnnection TimedOut\nCheck Internet connection\n{e}")
        
    else:
        details = element.find_elements_by_link_text('Details')
        return details


def write_url(filename, urls):
    with open(filename, "a+") as txt:

        # pos = txt.tell()
        txt.seek(0)
        lines = txt.readlines()

        def _write(url):
            
            entry = url.get_attribute('href') + "\n"

            if entry not in lines:
                txt.writelines(entry)
                urls_.append(entry)
                   
        pool = ThreadPool(9)
        pool.map(_write, urls)
        pool.close()
        pool.join() 

    driver.close()
       

start_time = time.time()

write_url("urls.txt", reversed(get_urls()))

duration = time.time()- start_time

print(f"{len(urls_)} new link(s) found ({duration} seconds)\nFetching DataSet(s)....")


start_time = time.time()

pool = ThreadPool(9)
dataset_ = pool.map(datarow, urls_)
pool.close()
pool.join()

duration = time.time()- start_time

print(f"{len(dataset_)} dataset(s) found ({duration} seconds)")



start_time = time.time()

pool = ThreadPool(9)
img_scrs = pool.map(get_img_url, urls_)
pool.close()
pool.join()

duration = time.time()- start_time

print(f"{len(img_scrs)} image(s) found ({duration} seconds)")

if not os.path.isfile("Inmates.csv"):
    create_csv("Inmates.csv")
print(f"Writting {len(dataset_) } datasets to csv....")
start_time = time.time()
write_csv("Inmates.csv", dataset_)
duration = time.time()- start_time
print(f" ({duration} seconds)")

print(f"downloading {len(dataset_) } images to 'images Dir'....")
start_time = time.time()
pool = ThreadPool(4)
pool.map(download, img_scrs)
pool.close()
pool.join()

duration = time.time()- start_time
print(f"{len(img_scrs)} downloaded ({duration} seconds)")

       


