from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep

def get_travel_info(origin_lat, origin_lng, dest_lat, dest_lng):
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
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Choose starting point'], input[placeholder*='Starting point']"))
        )
        origin_coords = f"{origin_lat},{origin_lng}"
        origin_input.clear()
        origin_input.send_keys(origin_coords)
        origin_input.send_keys(Keys.RETURN)
        
        sleep(2)  # Wait for origin to be processed
        
        # Wait and enter destination coordinates
        dest_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Choose destination'], input[placeholder*='Destination']"))
        )
        dest_coords = f"{dest_lat},{dest_lng}"
        dest_input.clear()
        dest_input.send_keys(dest_coords)
        dest_input.send_keys(Keys.RETURN)
        
        # Wait longer for route calculation
        sleep(5)
        
        try:
            # Try multiple possible selectors for route information
            route_info = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "div[class*='section-directions-trip-distance-time'], " +
                    "div[class*='section-directions-trip-numbers'], " +
                    "div[class*='route-bar'] div[class*='primary-text']"
                ))
            )
            
            # Take a screenshot for debugging
            driver.save_screenshot("success_screenshot.png")
            
            info_text = route_info.text
            print(f"Route information: {info_text}")
            return info_text
            
        except TimeoutException:
            # If we can't find the exact element, try to get any visible route information
            print("Attempting to find route information through alternative means...")
            driver.save_screenshot("route_search_screenshot.png")
            
            # Try to find any elements that might contain the route information
            route_elements = driver.find_elements(By.CSS_SELECTOR, 
                "div[class*='route'] span, div[class*='trip'] span, div[class*='distance'] span"
            )
            
            if route_elements:
                info_text = " ".join([elem.text for elem in route_elements if elem.text])
                print(f"Found alternative route information: {info_text}")
                return info_text
            else:
                raise Exception("Could not find route information")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        raise
        
    finally:
        sleep(2)
        driver.quit()

# Example usage
if __name__ == "__main__":
    # Example coordinates
    origin_coords = (43.07, -83.73)
    dest_coords = (43.02, -83.69)
    
    try:
        result = get_travel_info(
            origin_coords[0], 
            origin_coords[1], 
            dest_coords[0], 
            dest_coords[1]
        )
        print("Travel information retrieved successfully!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed to retrieve travel information: {e}")

# python distance_calculator.py
