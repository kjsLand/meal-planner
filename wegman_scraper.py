import json
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # import this
from wegmans_enums import Paths

DELAY = 13

def setup() -> uc.Chrome:
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument('--disable-popup-blocking')
    options.set_capability("goog:loggingPrefs", {"performance":"ALL"})
    return uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def get_XHR(driver:uc.Chrome):
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
    
    with open("all_logs.txt", "w") as file:
        file.write(json.dumps(found_req))
    url = found_req["params"]["response"]["url"]

    time.sleep(DELAY)
    driver.execute_script(f"window.open('{url}','secondtab')")
    driver.switch_to.window("secondtab")
    time.sleep(DELAY)
    info = driver.find_element(By.XPATH, "/html/body").text
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()

    # Stores the request
    with open("item_req.txt", "w") as file:
        file.write(info)
    
    input()

    return None

def grab_all_products():
    driver = setup()
    driver.get("https://shop.wegmans.com/shop/categories")
    time.sleep(DELAY)
    # click the popup x before pressing enter to continue
    input("Press Enter to continue: ")
    time.sleep(DELAY)
    departments = driver.find_elements(By.XPATH, Paths.department.value)
    for dep in departments:
        dep.click()
        time.sleep(DELAY)
        products = driver.find_elements(By.XPATH, Paths.product.value)
        for item in products:
            driver.get_log("performance") # clears log
            item.click()
            time.sleep(DELAY)
            with open("logs.txt", "w") as file:
                file.write(json.dumps(get_XHR(driver)))
            return
            time.sleep(DELAY)
            driver.back()
        input()
        driver.find_element(By.XPATH, Paths.department_list.value).click()

def main(): 
    grab_all_products()

    # test = {}
    # with open("all_logs.txt", "r") as file:
    #     test = json.loads(file.readlines()[0])

    # print(json.loads(test["params"]["request"]["postData"])["properties"].keys())

if __name__ == "__main__":
    main()