from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import re

def extract_number(text):
    """Extract the numeric value from strings like '13 min' or '5.2 miles'"""
    if isinstance(text, str):
        number = re.findall(r'[\d.]+', text)
        return number[0] if number else 'N.A.'
    return 'N.A.'

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
            
            time_number = extract_number(time_text)
            distance_number = extract_number(distance_text)
            
            print(f"Extracted values - Time: {time_number} min, Distance: {distance_number} miles")
            
            return time_number, distance_number
                
        except Exception as e:
            print(f"Failed to find route information: {e}")
            driver.save_screenshot("route_not_found.png")
            return 'N.A.', 'N.A.'
            
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        return 'N.A.', 'N.A.'
        
    finally:
        sleep(2)
        driver.quit()

def process_coordinates_file(input_file, output_file, num_rows=2):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Take only the first num_rows
    df = df.head(num_rows)
    
    # Create new columns for results
    df['Travel Time (min)'] = 'N.A.'
    df['Total Distance (miles)'] = 'N.A.'
    
    # Process each row
    for index, row in df.iterrows():
        print(f"\nProcessing row {index + 1}/{num_rows}")
        try:
            time_value, distance_value = get_travel_info(
                # row['y1'], row['x1'],  # Note: Swapped to match lat/lng format
                #row['y2'], row['x2']
                row['x1'], row['y1'],
                row['x2'], row['y2']
            )
            
            df.at[index, 'Travel Time (min)'] = time_value
            df.at[index, 'Total Distance (miles)'] = distance_value
            
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")
            continue
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"\nProcessing complete. Results saved to {output_file}")

if __name__ == "__main__":
    input_file = 'coordinates.xlsx'
    output_file = 'coordinates_with_travel_info.csv'
    
    process_coordinates_file(input_file, output_file)

# python distance_calculator.py
