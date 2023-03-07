from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

action = ActionChains(driver)

homepage_url = 'https://raritysniper.com/nft-collections/'

data = pd.DataFrame(columns=['collection_name','nft_id','rank_within_collection','rarity_score'])

def get_webpage(url):
    driver.get(url=url)
    time.sleep(5)  # Allow 2 seconds for the web page to open
    # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    scroll_pause_time = 1
    screen_height = driver.execute_script(
        "return window.screen.height;")   # get the screen height of the web
    i = 1
    while True:
        # scroll one screen height each time
        driver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script(
            "return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height)*(i*2) > scroll_height:
            break


def get_all_links(homepage_url):
    get_webpage(homepage_url)
    collections = driver.find_elements(by=By.TAG_NAME, value='a')
    links = []
    for collect in collections:
        links.append(collect.get_attribute('href'))

    #We can check manually that first 20 links are not from nft-collection
    return links[21:]


all_links = get_all_links(homepage_url)


# Go to the site and get NFT Value


def get_nft_details(link):

    get_webpage(link)

    nft_icons = driver.find_elements(by=By.XPATH,value="//*[@class='cursor-pointer']")

    collect_name = link.split('/')[-1]
    
    j=len(data)+1
    for nft in nft_icons:
        action.move_to_element(nft).click().perform()
        time.sleep(1)
        ranks = driver.find_element(by=By.XPATH,value="//*[@class='text-primary font-extrabold dark:text-dark-primary']").text
        time.sleep(2)
        nft_id = driver.find_element(by=By.XPATH,value="//*[@class='flex items-center text-blueGray-dark dark:text-dark-text']").text
        time.sleep(2)
        rarity = driver.find_element(by=By.XPATH,value=".//span[@class='text-primary dark:text-dark-primary']").text

        data.loc[j] = [collect_name,nft_id[1:],ranks.split(' ')[-1],rarity]
        j+= 1
        time.sleep(2)
        close_but = driver.find_element(by=By.XPATH,value='.//button[@class = "close-button absolute -top-8 right-2 opacity-1"]')
        action.move_to_element(close_but).click().perform()

for i in range(len(all_links[4:8])):
    get_nft_details(all_links[i])

data.to_csv('dataset.csv',index=False)


