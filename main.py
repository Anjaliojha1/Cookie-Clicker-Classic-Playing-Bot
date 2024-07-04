from selenium import webdriver
from selenium.webdriver.common.by import By
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element(By.ID, value="cookie")

stores = driver.find_elements(By.CSS_SELECTOR, "#store div")
store_ids = [store.get_attribute("id") for store in stores]

timeout = time.time() + 5
run_time = time.time() + 60*5

while True:
    cookie.click()
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        store_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text!= "":
                cost = int(element_text.split("-")[1].strip().replace(",",""))
                store_prices.append(cost)


        cookie_upgrades = {}
        for n in range(len(store_prices)):
            cookie_upgrades[store_prices[n]] = store_ids[n]

        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(by=By.ID, value=to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5
        if time.time() > run_time:
            cookie_per_s = driver.find_element(by=By.ID, value="cps").text
            print(cookie_per_s)
            break
