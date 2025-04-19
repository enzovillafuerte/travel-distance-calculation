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
        sleep(8)  # Increased wait time
        
        # Try multiple approaches to find the route information
        try:
            # First attempt: Look for the main route card
            route_card = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main'] div[role='article']"))
            )
            
            # Look for specific elements within the route card
            time_element = route_card.find_element(By.CSS_SELECTOR, "div[class*='section-directions-trip-duration']")
            distance_element = route_card.find_element(By.CSS_SELECTOR, "div[class*='section-directions-trip-distance']")
            
            info_text = f"{time_element.text} ({distance_element.text})"
            print(f"Found route information: {info_text}")
            
        except Exception as e:
            print(f"First attempt failed: {e}")
            # Second attempt: Try to find any elements with numbers that look like times or distances
            elements = driver.find_elements(By.CSS_SELECTOR, 
                "div[class*='section-directions'] div, span[class*='section-directions']"
            )
            
            route_info = []
            for elem in elements:
                try:
                    text = elem.text.strip()
                    # Look for text that contains numbers and typical route information indicators
                    if text and any(char.isdigit() for char in text):
                        if any(indicator in text.lower() for indicator in ['min', 'hr', 'km', 'mi', 'miles']):
                            route_info.append(text)
                except StaleElementReferenceException:
                    continue
            
            if route_info:
                info_text = " | ".join(route_info)
                print(f"Found alternative route information: {info_text}")
            else:
                # Take a screenshot of the current state
                driver.save_screenshot("route_not_found.png")
                raise Exception("Could not find route information")
            
        return info_text
        
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
