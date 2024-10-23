import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with your actual API token and profile ID
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiY2E2NTk1ZTc0NjkwOWQ0NzhjNDE3YmU0MTRlN2U3OTUxNWZjZGQ3NGVlYTM0Y2RjNTlmNGVlYjU0ZmM2NWQ5NDg5MzE4NWM1OGZjYzZjM2MiLCJpYXQiOjE2OTE0NjQ2MDkuNDIxMjU1LCJuYmYiOjE2OTE0NjQ2MDkuNDIxMjU3LCJleHAiOjE2OTQwNTY2MDkuNDExODk2LCJzdWIiOiIyNTUzMjIzIiwic2NvcGVzIjpbXX0.hqT-_d5TuhjtbCuzGO3mFsDj1Yi9PXYXXn0-Xp5nAfvtMrs6I-0IlCWdrx-o84B2vedN0E4qVp_QGudyZQvl3trKt-Xor0Tc6LR2vHdGL_Qt6AzJcn37ox5zBpgdEDD45lkhfhA35lR7G9eiOzg6jPwCK_HCCn5JPQG1pMLl7_94paT22IwKrGYwjp2YrlZc1kgN25yh1D8yyVfqw0fSb5LmDrfWrCN3hDkhywvLwtJgJnSHjKzESlCeyLU0wWSEo6o__raFIlfP0HDPzPzyqjAjH1BYe9JyO0lwNrjK3ezWHLAi4GUI3eas85JNgQOC2cD5xJzGVTPisxXoz9s5uYWgK78bRYt8nx1hvBW5jdZ8Xip7r-_C-c9cgQN2mMmP1szf3P2I-S-KO8yaH-UKxsCHTNrSg3osNUB_mJbja4a6iL3qep8yJhB4TrYdAAYJhGjamhBRrfp-j7EsTOiT3PVOakXcgE5KePCPlauVa64a_JVhX2ZauQad3ucOXTRArpXCvgq9lVzB8uaDlzrEja5qHDXHchTK7yHUGApdyv3jk4WVaiXt5diRA8G3g0oXLx_lmv410GKHxi_UWez75aDudzmMmGDhAaKfiNOa42jTTvwApzdhS8ClYDsUOpKdHY8lBLwyAHsbtq1a_d32UmIAqAaYMB6s3nikfbEBNXE"

#PROFILE_ID = "128509345" #Lashvin
#PROFILE_ID = "130972772" #Test2
PROFILE_ID = "130992122" #Test3


# Step 1: Start a profile via the API
start_url = f"http://localhost:3001/v1.0/browser_profiles/{PROFILE_ID}/start?automation=1"
stop_url = f"http://localhost:3001/v1.0/browser_profiles/{PROFILE_ID}/stop"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
response = requests.get(start_url, headers=headers)
data = response.json()



def inject_script(driver, js_code):
    driver.execute_script(js_code)
if data.get("success"):
    print("Profile started successfully.")
    if __name__ == "__main__":

        # Configure Chrome WebDriver options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--remote-debugging-port={data["automation"]["port"]}')
        # Launch Chrome WebDriver with configured options
        
        chromedriver_path = 'C:/Users/javie/Desktop/chromedriver-windows-x64.exe'
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # Open the Google sign-in page
        

        # Get the handles of all open tabs/windows
        window_handles = driver.window_handles

        # Loop through the window handles and close tabs except the first one
        for handle in window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()

        # Switch back to the first tab
        driver.switch_to.window(window_handles[0])

        driver.get('https://www.google.com')
        time.sleep(10)

        requests.get(stop_url)
        
        # Close the WebDriver
        driver.quit()
else:
    print("Failed to start profile.")