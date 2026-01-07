from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://ozh.github.io/cookieclicker/")

# Handle language selection
time.sleep(3)
driver.find_element(By.ID, "langSelect-EN").click()

# Timers
end_time = time.time() + 300       # 5 minutes
check_time = time.time() + 5       # upgrade check interval

while time.time() < end_time:
    # ALWAYS re-find the cookie (fixes stale element)
    driver.find_element(By.ID, "bigCookie").click()

    if time.time() > check_time:
        check_time = time.time() + 5

        # Get cookie count
        cookies_text = driver.find_element(By.ID, "cookies").text
        cookies_count = int(cookies_text.split(" ")[0].replace(",", ""))

        # Get store items
        items = driver.find_elements(By.CSS_SELECTOR, "#store div")
        affordable = {}

        for item in items:
            if "enabled" in item.get_attribute("class"):
                price_text = item.text.split("\n")
                if len(price_text) > 1:
                    price = int(price_text[1].replace(",", ""))
                    affordable[price] = item

        # Buy most expensive affordable upgrade
        if affordable:
            affordable[max(affordable)].click()

# Print cookies per second
cps = driver.find_element(By.ID, "cookiesPerSecond").text
print("Cookies per second:", cps)
