from selenium import webdriver
from selenium.webdriver.common.keys import Keys






driver = webdriver.Chrome("/Users/aprillowry/Documents/Python_Libraries/chromedriver")
driver.get("https://www.kroger.com/")

try:
    driver.find_element_by_xpath("/html/body/div[5]/div/div/button").click()
except:
    print("wooop")

driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[4]/div[2]/div/div[3]/div/form/div[1]/div[1]/div/input").send_keys("chicken breast")
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[4]/div[2]/div/div[3]/div/form/div[1]/div[1]/div/input").send_keys(Keys.RETURN)

