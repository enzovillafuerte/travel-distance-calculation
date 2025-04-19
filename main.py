from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep


# Defining the url for the starting point
url = 'https://www.google.com/maps'  # Simplified URL

# Initializing the driver
driver = webdriver.Chrome()

# Accessing the url with the driver
driver.get(url)

def get_place():
    try:
        # Wait up to 10 seconds for the search box to be present
        # Try different possible selectors
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='q'], input[aria-label*='Search'], #searchboxinput"))
        )
        
        # Clear any existing text and send the search query
        search_box.clear()
        search_box.send_keys('Barcelona')
        
        # Try to find and click the search button
        try:
            search_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Search'], button[jsaction*='search']"))
            )
            search_button.click()
        except TimeoutException:
            # If we can't find the search button, try pressing Enter on the search box
            search_box.send_keys(Keys.RETURN)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")  # This will help debug what's on the page
        raise

get_place()

def get_direction():
    # Sleep so we don't send too many requests to the web (may raise issues)
    sleep(5)
    # define where the button is in the HTML
    direction_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/div[2]/button')
    # Automating the click on the directions button
    direction_button.click()

    # origin = 





print('Success')

# Make sure to add this at the end of your script

sleep(5)
driver.quit()

# python main.py