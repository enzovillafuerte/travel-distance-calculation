from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from time import sleep

def get_travel_info(origin_lat, origin_lng, dest_lat, dest_lng):
    driver = webdriver.Chrome()
    
    try:
        # Go to Google Maps
        driver.get('https://www.google.com/maps')
        print("Opened Google Maps")
        
        # Wait for and click the directions button
        directions_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Directions'], button[data-tooltip='Directions']"))
        )
        directions_button.click()
        print("Clicked directions button")
        
        # Wait for the origin input field and enter coordinates
        origin_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Choose starting point'], input[placeholder*='Starting']"))
        )
        origin_coords = f"{origin_lat},{origin_lng}"
        origin_input.clear()
        origin_input.send_keys(origin_coords)
        origin_input.send_keys(Keys.RETURN)
        print(f"Entered origin coordinates: {origin_coords}")
        
        sleep(3)
        
        # Wait and enter destination coordinates
        dest_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Choose destination'], input[placeholder*='Destination']"))
        )
        dest_coords = f"{dest_lat},{dest_lng}"
        dest_input.clear()
        dest_input.send_keys(dest_coords)
        dest_input.send_keys(Keys.RETURN)
        print(f"Entered destination coordinates: {dest_coords}")
        
        # Wait longer for route calculation
        sleep(8)
        
        try:
            # Try first with class names
            try:
                time_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "Fk3sm"))
                )
                distance_element = driver.find_element(By.CLASS_NAME, "ivN21e")
                
            except Exception:
                print("Class name search failed, trying XPath...")
                # If class names fail, try XPath
                time_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[1]'
                    ))
                )
                distance_element = driver.find_element(
                    By.XPATH, 
                    '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[2]/div'
                )
            
            time_text = time_element.text
            distance_text = distance_element.text
            
            info_text = f"{time_text} ({distance_text})"
            print(f"Found route information: {info_text}")
            
            # Take a success screenshot
            driver.save_screenshot("success_screenshot.png")
            
            return info_text
                
        except Exception as e:
            print(f"Failed to find route information: {e}")
            driver.save_screenshot("route_not_found.png")
            raise
            
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
        print(f"Final result: {result}")
    except Exception as e:
        print(f"Failed to retrieve travel information: {e}")

# python distance_calculator.py
