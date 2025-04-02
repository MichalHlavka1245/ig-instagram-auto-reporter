from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import os
import glob 

# Function for reporting a profile
def report_profile(username, password, target_profile, num_reports=1):
    # Chrome settings
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    # Add this to reduce automation detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Path to chromedriver - modify according to your actual path
    service = Service(executable_path="../chromedriver.exe")  #set path to chromedriver.exe
    
    # Driver initialization
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Add User-Agent for more realistic behavior
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    })
    
    try:
        # Login to Instagram
        driver.get("https://www.instagram.com")
        print("Loading Instagram...")
        time.sleep(random.uniform(3, 5))
        
        # Decline cookies if prompted
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Odmietnuť') or contains(text(), 'Decline') or contains(text(), 'Reject')]"))
            )
            cookie_button.click()
            print("Cookies declined")
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Cookie dialog not shown or could not be processed: {e}")
        
        # Fill in login credentials
        try:
            print("Filling in login credentials...")
            username_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            
            # Click login button
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            ).click()
            
            print("Logging in...")
            time.sleep(random.uniform(6, 8))
        except Exception as e:
            print(f"Error during login: {e}")
            driver.save_screenshot("login_error.png")
            return
        
        # Try to skip "Save login info" and notifications if shown
        try:
            not_now_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Teraz nie') or contains(text(), 'Not Now') or contains(text(), 'Skip')]")
            if len(not_now_buttons) > 0:
                not_now_buttons[0].click()
                print("'Save login info' dialog skipped")
                time.sleep(random.uniform(2, 3))
        except Exception as e:
            print(f"Save login dialog not shown or could not be skipped: {e}")
        
        # Second dialog for notifications
        try:
            not_now_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Teraz nie') or contains(text(), 'Not Now') or contains(text(), 'Skip')]")
            if len(not_now_buttons) > 0:
                not_now_buttons[0].click()
                print("'Notifications' dialog skipped")
                time.sleep(random.uniform(2, 3))
        except:
            print("Notifications dialog not shown or could not be skipped")
        
        # Counter for successful reports
        successful_reports = 0
        
        # Loop for repeated reporting
        for i in range(num_reports):
            try:
                # Navigate to the Instagram profile
                print(f"Attempt #{i+1}: Going to profile {target_profile}...")
                driver.get(f'https://www.instagram.com/{target_profile}/')
                time.sleep(random.uniform(4, 6))
                
                # Check if we're on the correct page
                current_url = driver.current_url
                if target_profile.lower() not in current_url.lower():
                    print(f"Failed to navigate to profile {target_profile}, current URL: {current_url}")
                    driver.save_screenshot(f"profile_navigation_error_{i+1}.png")
                    continue
                
                print("Profile successfully loaded")
                driver.save_screenshot(f"profile_loaded_{i+1}.png")
                
                # STEP 1: Click on the three dots button
                print("Looking for the three dots button...")
                
                # Try multiple selectors for the three dots
                three_dots_selectors = [
                    "//div[contains(@role, 'button')]/*[name()='svg']/..",
                    "//button[contains(@aria-label, 'Možnosti') or contains(@aria-label, 'Options') or contains(@aria-label, 'More')]",
                    "//section//div[contains(@role, 'button')]",
                    "//section//button[not(contains(text(), 'Sledovať') or contains(text(), 'Follow'))]",
                    "//header//button[not(contains(text(), 'Sledovať') or contains(text(), 'Follow'))]",
                    # Adding new selector for the three dots button
                    "//header//div[contains(@role, 'button')]"
                ]
                
                three_dots_button = None
                for selector in three_dots_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        if elements:
                            for element in elements:
                                try:
                                    # Try to check if the element has an SVG child
                                    if element.find_elements(By.TAG_NAME, "svg"):
                                        three_dots_button = element
                                        break
                                except:
                                    pass
                        if three_dots_button:
                            break
                    except:
                        continue
                
                if not three_dots_button:
                    print("Cannot find the three dots button!")
                    driver.save_screenshot(f"no_three_dots_{i+1}.png")
                    continue
                
                # Click the three dots button
                try:
                    action = ActionChains(driver)
                    action.move_to_element(three_dots_button).click().perform()
                    print("Clicked on the three dots button")
                    driver.save_screenshot(f"three_dots_clicked_{i+1}.png")
                    time.sleep(random.uniform(2, 3))
                except Exception as e:
                    print(f"Error clicking on three dots: {e}")
                    driver.save_screenshot(f"three_dots_click_error_{i+1}.png")
                    continue
                
                # STEP 2: Click on "Report"
                print("Looking for 'Report' button...")
                try:
                    report_button = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Nahlásiť') or contains(text(), 'Report')]"))
                    )
                    report_button.click()
                    print("Clicked on 'Report'")
                    driver.save_screenshot(f"report_clicked_{i+1}.png")
                    time.sleep(random.uniform(2, 3))
                except Exception as e:
                    print(f"Error clicking on 'Report': {e}")
                    driver.save_screenshot(f"report_click_error_{i+1}.png")
                    continue
                
                # STEP 3: Click on "Report account" - UPDATED to match the menu in the screenshot
                print("Looking for 'Report account' option...")
                try:
                    # Updated with more specific selectors that match the Slovak UI in the screenshot
                    report_account_selectors = [
                        "//button[contains(text(), 'Nahlásiť účet')]",
                        "//div[contains(text(), 'Nahlásiť účet')]",
                        "//span[contains(text(), 'Nahlásiť účet')]",
                        "//div[contains(@role, 'button')]//*[contains(text(), 'Nahlásiť účet')]",
                        "//div[@role='button']//div[text()='Nahlásiť účet']",
                        "//div[contains(@role, 'menuitem')]//div[contains(text(), 'Nahlásiť účet')]"
                    ]
                    
                    report_account = None
                    for selector in report_account_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements and len(elements) > 0:
                                report_account = elements[0]
                                break
                        except:
                            continue
                    
                    if report_account:
                        report_account.click()
                        print("Clicked on 'Report account'")
                        driver.save_screenshot(f"report_account_clicked_{i+1}.png")
                        time.sleep(random.uniform(2, 3))
                    else:
                        raise Exception("Report account option not found")
                        
                except Exception as e:
                    print(f"Error clicking on 'Report account': {e}")
                    driver.save_screenshot(f"report_account_error_{i+1}.png")
                    continue
                
                # STEP 4: Select "Posts inappropriate content"
                print("Selecting reason 'Posts inappropriate content'...")
                try:
                    inappropriate_content_selectors = [
                        "//button[contains(text(), 'Zverejňuje obsah') or contains(text(), 'nepatrí')]",
                        "//div[contains(text(), 'Zverejňuje obsah') or contains(text(), 'nepatrí')]",
                        "//span[contains(text(), 'Zverejňuje obsah') or contains(text(), 'nepatrí')]",
                        "//div[contains(@role, 'button')]//*[contains(text(), 'Zverejňuje obsah')]",
                        "//button[contains(text(), 'inappropriate') or contains(text(), 'shouldn')]"
                    ]
                    
                    inappropriate_content = None
                    for selector in inappropriate_content_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements and len(elements) > 0:
                                inappropriate_content = elements[0]
                                break
                        except:
                            continue
                    
                    if inappropriate_content:
                        inappropriate_content.click()
                        print("Selected reason 'Posts inappropriate content'")
                        driver.save_screenshot(f"inappropriate_content_clicked_{i+1}.png")
                        time.sleep(random.uniform(2, 3))
                    else:
                        raise Exception("'Posts inappropriate content' option not found")
                        
                except Exception as e:
                    print(f"Error selecting 'Posts inappropriate content': {e}")
                    driver.save_screenshot(f"inappropriate_content_error_{i+1}.png")
                    continue
                
                # STEP 5: Select "Nudity or sexual activity"
                print("Selecting category 'Nudity or sexual activity'...")
                try:
                    nudity_selectors = [
                        "//button[contains(text(), 'Nahota') or contains(text(), 'sexuálna')]",
                        "//div[contains(text(), 'Nahota') or contains(text(), 'sexuálna')]",
                        "//span[contains(text(), 'Nahota') or contains(text(), 'sexuálna')]",
                        "//div[contains(@role, 'button')]//*[contains(text(), 'Nahota')]",
                        "//button[contains(text(), 'Nudity') or contains(text(), 'sexual')]"
                    ]
                    
                    nudity_option = None
                    for selector in nudity_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements and len(elements) > 0:
                                nudity_option = elements[0]
                                break
                        except:
                            continue
                    
                    if nudity_option:
                        nudity_option.click()
                        print("Selected category 'Nudity or sexual activity'")
                        driver.save_screenshot(f"nudity_clicked_{i+1}.png")
                        time.sleep(random.uniform(2, 3))
                    else:
                        raise Exception("'Nudity or sexual activity' option not found")
                        
                except Exception as e:
                    print(f"Error selecting 'Nudity or sexual activity': {e}")
                    driver.save_screenshot(f"nudity_error_{i+1}.png")
                    continue
                
                # STEP 6: Select "Nudity or pornography"
                print("Selecting specific category 'Nudity or pornography'...")
                try:
                    pornography_selectors = [
                        "//button[contains(text(), 'Nahota alebo pornografia')]",
                        "//div[contains(text(), 'Nahota alebo pornografia')]",
                        "//span[contains(text(), 'Nahota alebo pornografia')]",
                        "//div[contains(@role, 'button')]//*[contains(text(), 'Nahota alebo pornografia')]",
                        "//button[contains(text(), 'Nudity or pornography')]"
                    ]
                    
                    pornography_option = None
                    for selector in pornography_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements and len(elements) > 0:
                                pornography_option = elements[0]
                                break
                        except:
                            continue
                    
                    if pornography_option:
                        pornography_option.click()
                        print("Selected 'Nudity or pornography'")
                        driver.save_screenshot(f"pornography_clicked_{i+1}.png")
                        time.sleep(random.uniform(2, 3))
                    else:
                        raise Exception("'Nudity or pornography' option not found")
                        
                except Exception as e:
                    print(f"Error selecting 'Nudity or pornography': {e}")
                    driver.save_screenshot(f"pornography_error_{i+1}.png")
                    continue
                
                # STEP 7: Submit the report
                print("Looking for submit button...")
                try:
                    submit_selectors = [
                        "//button[contains(text(), 'Odoslať')]",
                        "//button[contains(text(), 'Submit')]",
                        "//button[contains(text(), 'Send')]",
                        "//div[contains(@role, 'button')]//*[contains(text(), 'Odoslať')]"
                    ]
                    
                    submit_button = None
                    for selector in submit_selectors:
                        try:
                            elements = driver.find_elements(By.XPATH, selector)
                            if elements and len(elements) > 0:
                                submit_button = elements[0]
                                break
                        except:
                            continue
                    
                    if submit_button:
                        submit_button.click()
                        print("Clicked submit button")
                        driver.save_screenshot(f"submit_clicked_{i+1}.png")
                        time.sleep(random.uniform(2, 3))
                        
                        # Increase successful reports counter
                        successful_reports += 1
                        print(f"Successful report #{successful_reports} of profile {target_profile}")
                        print(">> SUCCESSFULLY REPORTED: Profile was reported for nudity/pornography content <<")
                    else:
                        raise Exception("Submit button not found")
                        
                except Exception as e:
                    print(f"Error submitting the report: {e}")
                    driver.save_screenshot(f"submit_error_{i+1}.png")
                    continue
                
            except Exception as e:
                print(f"General error during reporting attempt #{i+1}: {e}")
                driver.save_screenshot(f"general_error_{i+1}.png")
            
            # Wait before next attempt
            wait_time = 0.5
            print(f"Waiting {wait_time:.1f} seconds before next attempt...")
            time.sleep(wait_time)
        
        print(f"SUMMARY: Successfully reported {successful_reports} out of {num_reports} attempts.")
        if successful_reports > 0:
            print("At least one report was successful!")
        else:
            print("No reports were successful. Check screenshots for more information.")
            
            
        
    except Exception as e:
        print(f"Critical error: {e}")
        driver.save_screenshot("critical_error.png")
    
    finally:
        # Logout (optional)
        try:
            print("Logging out...")
            driver.get("https://www.instagram.com/accounts/logout/")
            time.sleep(3)
        except:
            print("Error during logout")
        
        # Close browser
        print("Closing browser...")
        driver.quit()
        
def delete_screenshots():
    """
    Delete all screenshot files in the current directory
    that match specific naming patterns
    """
    screenshot_patterns = [
        '*_loaded_*.png',
        '*_clicked_*.png',
        '*_error_*.png',
        'three_dots_*.png',
        'report_*.png',
        'inappropriate_*.png',
        'nudity_*.png',
        'pornography_*.png',
        'submit_*.png',
        'critical_error.png',
        'login_error.png'
    ]
    
    # Iterate through all screenshot patterns
    for pattern in screenshot_patterns:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Could not delete {file}: {e}")


    
# Run the script with number of attempts
if __name__ == "__main__":
    # Set your login credentials and target profile
    username = "username"  # set Your username here
    password = "password"  # set Your password here
    target_profile = "ahrinka_1211"  # Profile you want to report
    num_reports = 1 # Number of reporting attempts
    
    print("=== STARTING INSTAGRAM PROFILE REPORTING SCRIPT ===")
    print(f"Profile to report: {target_profile}")
    print(f"Number of attempts: {num_reports}")
    print("================================================")
    
    report_profile(username, password, target_profile, num_reports)
    delete_screenshots()