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
PROFILE_ID = "130972772" #Test2
#PROFILE_ID = "130992122" #Test3


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

        #driver.get('https://www.google.com')

        try:
            # Open the URL
            url = "https://democaptcha.com/demo-form-eng/hcaptcha.html"  # Replace with the actual URL
            driver.get(url)

            # Your RuCaptcha API key
            api_key = 'Aa36003fe691f6155304d1f2af049060'

            # The hCaptcha site key
            site_key = '338af34c-7bcb-4c7c-900b-acbec73d7d43'

            # Prepare the data for the POST request to solve hCaptcha
            data = {
                'key': api_key,
                'method': 'hcaptcha',
                'sitekey': site_key,
                'pageurl': url
            }

            # RuCaptcha API endpoint for submitting CAPTCHA
            api_url = 'http://rucaptcha.com/in.php'

            # Send the POST request to the RuCaptcha API
            response = requests.post(api_url, data=data)

            # Extract the captcha ID from the response
            response_data = response.text.split('|')
            if len(response_data) >= 2 and response_data[0] == 'OK':
                captcha_id = response_data[1]
            else:
                print('Error submitting hCaptcha:', response.text)
                exit()

            # Wait for a few seconds before checking the result
            time.sleep(90)

            # RuCaptcha API endpoint for getting CAPTCHA result
            result_url = f'http://rucaptcha.com/res.php?key={api_key}&action=get&id={captcha_id}'

            # Poll the RuCaptcha API until the result is available
            max_poll_attempts = 10
            poll_interval = 5  # seconds

            for _ in range(max_poll_attempts):
                result_response = requests.get(result_url)
                result_text = result_response.text
                
                if 'OK' in result_text:
                    solved_captcha_solution = result_text.split('|')[1]
                    print(f'Solved hCaptcha solution: {solved_captcha_solution}')
                    break  # Stop polling if solution is found
                
                time.sleep(poll_interval)

            # Print an error message if solution is not found
            else:
                print('CAPTCHA solution not found after polling.')
            
           
            # element_to_unhide = driver.find_element('name',"g-recaptcha-response")  # Replace with the actual element ID
            # driver.execute_script("arguments[0].style.display = 'block';", element_to_unhide)
            # print ("success")

            # Find the textbox and enter the solution
            textbox = driver.find_element('name',"g-recaptcha-response")  # Replace with the actual textbox ID
            textbox.clear()
            textbox.send_keys(solved_captcha_solution)
            textbox1 = driver.find_element('name',"h-captcha-response")  # Replace with the actual textbox ID
            textbox1.clear()
            textbox1.send_keys(solved_captcha_solution)


            #Find the submit button and click it
            submit_button = driver.find_element(By.XPATH,"/html/body/main/article/div/form/input[2]")# Replace with the actual submit button ID
            submit_button.click()


            time.sleep(90)

        except Exception as e:
            print('An error occurred:', e)
        finally:
            # Close the WebDriver
            requests.get(stop_url)
            driver.quit()

else:
    print("Failed to start profile.")