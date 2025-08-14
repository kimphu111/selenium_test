from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Thông tin đăng nhập Facebook để test
facebook_email = "your_facebook_email@gmail.com"  # Thay bằng email Facebook thật
facebook_password = "your_facebook_password"       # Thay bằng password Facebook thật

print("BAT DAU TEST DANG NHAP FACEBOOK")

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Tắt warning của ChromeDriver
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Tránh detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

try:
    print("Mo trang dang nhap Facebook...")
    driver.get("https://www.facebook.com")
    
    # Chờ trang load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    
    print("Nhap email...")
    email_input = driver.find_element(By.ID, "email")
    email_input.clear()
    email_input.send_keys(facebook_email)
    
    print("Nhap password...")
    password_input = driver.find_element(By.ID, "pass")
    password_input.clear()
    password_input.send_keys(facebook_password)
    
    print("Click nut dang nhap...")
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    
    # Chờ đăng nhập xong
    print("Dang cho ket qua dang nhap...")
    time.sleep(5)
    
    current_url = driver.current_url
    print(f"URL hien tai: {current_url}")
    
    # Kiểm tra đăng nhập thành công
    if "facebook.com" in current_url and "login" not in current_url:
        if "checkpoint" in current_url:
            print("Can xac thuc bao mat (2FA/Captcha)")
            print("Ban can xac thuc thu cong...")
            time.sleep(30)  # Cho thời gian xác thực
        else:
            print("Dang nhap Facebook thanh cong!")
            
            # Kiểm tra tên người dùng
            try:
                user_name_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label*='Facebook']"))
                )
                print("Da dang nhap thanh cong!")
            except:
                print("Dang nhap thanh cong nhung khong tim thay ten nguoi dung")
    else:
        print("Dang nhap that bai!")
        
        # Kiểm tra lỗi
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, "._9ay7, .error")
            error_text = error_element.text
            print(f"Loi: {error_text}")
        except:
            print("Khong xac dinh duoc loi cu the")
    
    print("Giu browser mo 10 giay de quan sat...")
    time.sleep(10)

except Exception as e:
    print(f"Test that bai: {e}")
    
    # Chụ screenshot khi lỗi
    try:
        screenshot_name = f"facebook_login_error_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        print(f"Da chup screenshot loi: {screenshot_name}")
    except:
        pass

finally:
    print("Dong browser...")
    driver.quit()
    print("Test Facebook login hoan tat!")