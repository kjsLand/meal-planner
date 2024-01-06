import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # import this
from wegmans_enums import Paths
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException

DELAY = 13
DB = "wegmans_products"

def setup() -> uc.Chrome:
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument('--disable-popup-blocking')
    options.set_capability("goog:loggingPrefs", {"performance":"ALL"})
    return uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def grab_prod_req(driver:uc.Chrome, url:str, department:str):
    time.sleep(DELAY)
    driver.execute_script(f"window.open('{url}','secondtab')")
    driver.switch_to.window("secondtab")
    time.sleep(DELAY)
    info = driver.find_element(By.XPATH, "/html/body").text
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    
    # Stores the request
    with open(f"{DB}/{department}", "a") as file:
        file.write(info + "\n")

def get_XHR(driver:uc.Chrome, department:str):
    original_logs = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in original_logs]
    
    found_req = {}
    for j_obj in logs:
        if len(str(j_obj).split("?require_storeproduct=true")) > 1:
            found_req = j_obj
    
    # Error out if no response had aisle
    if found_req == {}:
        print("not found")
        return 
    url = found_req["params"]["response"]["url"]

    grab_prod_req(driver, url, department)

def load_full_page(driver:uc.Chrome):
    for i in range(1, 5):
        driver.execute_script(f"window.scrollTo(0,document.body.scrollHeight/5*{i})")
        time.sleep(5)

def grab_all_products():
    driver = setup()
    driver.get("https://shop.wegmans.com/shop/categories")
    time.sleep(DELAY)
    # click the popup x before pressing enter to continue
    input("Press Enter to continue: ")
    time.sleep(DELAY)
    dep_length = len(driver.find_elements(By.XPATH, Paths.department.value))
    print(dep_length)
    for i in range(5, dep_length):
        # Gets departments again because of stale reference error
        all_deps = driver.find_elements(By.XPATH, Paths.department.value)
        dep_name = all_deps[i].text
        all_deps[i].click()
        time.sleep(DELAY)

        next_color = "rgba(206, 63, 36, 1)"
        while next_color == "rgba(206, 63, 36, 1)": # red (not last page)
            load_full_page(driver)
            products = driver.find_elements(By.XPATH, Paths.product.value)
            print(len(products))
            for item in products:
                driver.get_log("performance") # clears log
                driver.execute_script("arguments[0].scrollIntoView();", item)
                item.click()
                time.sleep(DELAY)
                get_XHR(driver, dep_name)
                time.sleep(DELAY)
                driver.switch_to.window(driver.window_handles[0])
                driver.back()
                time.sleep(DELAY)
            try:
                next_page = driver.find_element(By.XPATH, Paths.next_page_button.value)
            except NoSuchElementException: 
                break # Breaks while if all products are on one page
            next_color = next_page.value_of_css_property('background-color')
            print(next_color)
            if next_color == "rgba(206, 63, 36, 1)":
                next_page.click()
                time.sleep(DELAY)
        
        dep_link = driver.find_element(By.XPATH, Paths.department_list.value)
        driver.execute_script("arguments[0].scrollIntoView();", dep_link)
        dep_link.click()
        time.sleep(DELAY)

def main(): 
    grab_all_products()

if __name__ == "__main__":
    main()