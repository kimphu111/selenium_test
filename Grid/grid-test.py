from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("🚀 Starting Grid Login Test with 2 different accounts...")

# Chrome configuration
chrome_options = Options()
# Bỏ headless để thấy giao diện
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--no-sandbox')

# Firefox configuration
firefox_options = FirefoxOptions()
# Bỏ headless để thấy giao diện
# firefox_options.add_argument('--headless')
firefox_options.add_argument('--width=1920')
firefox_options.add_argument('--height=1080')

# Thông tin tài khoản khác nhau
ACCOUNT_1 = {
    "email": "kimphu123@gmail.com",
    "password": "123"
}

ACCOUNT_2 = {
    "email": "user2@gmail.com",  # Thay bằng email khác
    "password": "456"            # Thay bằng password khác
}

try:
    print("Connecting to Chrome...")
    driver_chrome = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )
    
    print(" Connecting to Firefox...")
    driver_firefox = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=firefox_options
    )
    
    print("✅ Both browsers connected!")
    
    # Test đăng nhập với Chrome (Account 1)
    print("🔑 Chrome - Logging in with Account 1...")
    driver_chrome.get("http://localhost:4200/auth")
    
    # Đăng nhập Chrome với Account 1
    email_chrome = WebDriverWait(driver_chrome, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_chrome = driver_chrome.find_element(By.NAME, "password")
    
    email_chrome.send_keys(ACCOUNT_1["email"])
    password_chrome.send_keys(ACCOUNT_1["password"])
    
    login_button_chrome = driver_chrome.find_element(By.XPATH, "//button[text()='Sign In']")
    login_button_chrome.click()
    
    # Test đăng nhập với Firefox (Account 2)
    print("🔑 Firefox - Logging in with Account 2...")
    driver_firefox.get("http://localhost:4200/auth")
    
    # Đăng nhập Firefox với Account 2
    email_firefox = WebDriverWait(driver_firefox, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_firefox = driver_firefox.find_element(By.NAME, "password")
    
    email_firefox.send_keys(ACCOUNT_2["email"])
    password_firefox.send_keys(ACCOUNT_2["password"])
    
    login_button_firefox = driver_firefox.find_element(By.XPATH, "//button[text()='Sign In']")
    login_button_firefox.click()
    
    # Chờ cả 2 đăng nhập
    print("Waiting for both logins to complete...")
    
    try:
        WebDriverWait(driver_chrome, 10).until(EC.url_contains("/home"))
        print("Chrome (Account 1) logged in successfully!")
    except:
        print("Chrome (Account 1) login failed!")
    
    try:
        WebDriverWait(driver_firefox, 10).until(EC.url_contains("/home"))
        print("Firefox (Account 2) logged in successfully!")
    except:
        print("Firefox (Account 2) login failed!")
    
    # Test cả 2 account trên home page
    print("Testing both accounts on home page...")
    
    time.sleep(3)
    
    # Chrome home page
    driver_chrome.get("http://localhost:4200/home")
    time.sleep(2)
    print(f"Chrome (Account 1) Home Title: {driver_chrome.title}")
    
    # Firefox home page
    driver_firefox.get("http://localhost:4200/home")
    time.sleep(2)
    print(f"Firefox (Account 2) Home Title: {driver_firefox.title}")
    
    print("Both browsers will stay open for 15 seconds to observe...")
    print("You can see both accounts logged in simultaneously!")
    time.sleep(15)
    
    # Đóng browsers
    driver_chrome.quit()
    driver_firefox.quit()
    
    print("Multi-account test completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    try:
        driver_chrome.quit()
    except:
        pass
    try:
        driver_firefox.quit()
    except:
        pass