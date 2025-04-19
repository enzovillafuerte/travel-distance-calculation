from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep

def get_travel_info(origin_lat, origin_lng, dest_lat, dest_lng):
    # Initialize the driver
    driver = webdriver.Chrome()
    
    try:
        # Go to Google Maps
        driver.get('https://www.google.com/maps')
        
        # Wait for and click the directions button
        directions_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Directions']"))
        )
        directions_button.click()
        
        # Wait for the origin input field and enter coordinates
        origin_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Choose starting point']"))
        )
        origin_coords = f"{origin_lat},{origin_lng}"
        origin_input.clear()
        origin_input.send_keys(origin_coords)
        origin_input.send_keys(Keys.RETURN)
        
        # Wait and enter destination coordinates
        dest_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Choose destination']"))
        )
        dest_coords = f"{dest_lat},{dest_lng}"
        dest_input.clear()
        dest_input.send_keys(dest_coords)
        dest_input.send_keys(Keys.RETURN)
        
        # Wait for the results to load
        sleep(3)  # Give time for the route to calculate
        
        # Get the first route info (distance and time)
        route_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='section-directions-trip-distance-time']"))
        )
        
        # Extract distance and time
        info_text = route_info.text
        print(f"Route information: {info_text}")
        
        return info_text
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise
        
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    # Example coordinates
    origin_coords = (43.07, -83.73)  # First location
    dest_coords = (43.02, -83.69)    # Second location
    
    result = get_travel_info(
        origin_coords[0], 
        origin_coords[1], 
        dest_coords[0], 
        dest_coords[1]
    )
    
    print("Travel information retrieved successfully!")

# python distance_calculator.py
