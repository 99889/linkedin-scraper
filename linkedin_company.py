from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-features=BlockInsecurePrivateNetworkRequests")
chrome_options.add_argument("--disable-webgl")
chrome_options.add_argument("--disable-webrtc")

# Set up the Selenium WebDriver using WebDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    try:
        # Wait until the login form is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        
        # Wait for the login to complete by checking for the presence of the search bar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )
        
        print("Login successful.")
        
    except Exception as e:
        print(f"Error during login: {e}")

def scrape_profile(driver, profile_url):
    driver.get(profile_url)
    try:
        # Wait until the profile page is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pv-top-card"))
        )
        
        # Extract profile name
        profile_name = driver.find_element(By.CLASS_NAME, "pv-top-card--list li").text
        print(f"Profile Name: {profile_name}")
        
        # Add scraping logic for experience
        experience_section = driver.find_element(By.ID, "experience-section")
        experiences = experience_section.find_elements(By.CLASS_NAME, "pv-profile-section__card-item")
        print("Experience:")
        for experience in experiences:
            title = experience.find_element(By.CLASS_NAME, "pv-entity__summary-info h3").text
            company = experience.find_element(By.CLASS_NAME, "pv-entity__secondary-title").text
            duration = experience.find_element(By.CLASS_NAME, "pv-entity__date-range").text
            print(f"\t{title} at {company} ({duration})")
        
        # Add scraping logic for education
        education_section = driver.find_element(By.ID, "education-section")
        educations = education_section.find_elements(By.CLASS_NAME, "pv-profile-section__card-item")
        print("Education:")
        for education in educations:
            degree = education.find_element(By.CLASS_NAME, "pv-entity__degree-name").text
            school = education.find_element(By.CLASS_NAME, "pv-entity__school-name").text
            duration = education.find_element(By.CLASS_NAME, "pv-entity__dates").text
            print(f"\t{degree} at {school} ({duration})")
        
        
        
    except Exception as e:
        print(f"Error during profile scraping: {e}")


def main():
    username = "moininshaal7@gmail.com"
    password = "Inshaal@67890//"
    profile_url = "https://www.linkedin.com/in/akinfosec"
    
    linkedin_login(driver, username, password)
    scrape_profile(driver, profile_url)
    
    # Close the driver
    driver.quit()

if __name__ == "__main__":
    main()
