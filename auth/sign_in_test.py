from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Thông tin đăng nhập để test
email = "kimphu123@gmail.com"
password = "123" # pass đúng là 123

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Tắt warning của ChromeDriver
options.add_argument("--start-maximized")  


driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:4200/auth")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")

    email_input.send_keys(email)
    password_input.send_keys(password)
    login_button.click()

    try:
        # Đợi chuyển hướng thành công
        WebDriverWait(driver, 5).until(
            EC.url_contains("/home")
        )
        print("Đăng nhập thành công")
    except:
        print("Đăng nhập thất bại")

    time.sleep(2)

except Exception as e:
    print("Test thất bại:", e)

finally:
    driver.quit()