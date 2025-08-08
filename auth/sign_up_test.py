from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string

# Thiết lập tùy chọn để hiển thị trình duyệt toàn màn hình
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Mở cửa sổ trình duyệt toàn màn hình
options.add_argument("--log-level=3")  # Giảm bớt logs

driver = webdriver.Chrome(options=options)  # Truyền tùy chọn vào driver

# Số lượng tài khoản cần test
num_accounts = 3

try:
    for i in range(num_accounts):
        # Tạo thông tin ngẫu nhiên cho mỗi tài khoản
        random_username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        random_email = f"{random_username}@example.com"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=10))
        
        print(f"\n===== Tạo tài khoản {i+1}/{num_accounts} =====")
        print(f"Username: {random_username}")
        print(f"Email: {random_email}")
        print(f"Password: {random_password}")
        
        # Mở trang đăng ký
        driver.get("http://localhost:4200/auth")
        
        # Click vào link Sign Up
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Sign Up"))
        ).click()
        
        time.sleep(1)  # Chờ form hiển thị
        
        # Điền thông tin đăng ký
        driver.find_element(By.CSS_SELECTOR, ".register-form input[name='username']").send_keys(random_username)
        time.sleep(0.4)
        driver.find_element(By.CSS_SELECTOR, ".register-form input[name='email']").send_keys(random_email)
        time.sleep(0.4)
        driver.find_element(By.CSS_SELECTOR, ".register-form input[name='password']").send_keys(random_password)
        
        # Click nút đăng ký
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign Up')]").click()
        
        time.sleep(3)  # Chờ phản hồi và có thể reload trang
        
        current_url = driver.current_url
        print(f"URL hiện tại: {current_url}")
        
        try:
            message_element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".message-container p"))
            )
            message = message_element.text
            
            if "success" in message_element.get_attribute("class"):
                print(f"Đăng ký thành công: {message}")
            else:
                print(f"Đăng ký thất bại: {message}")
                
        except:
            if "/auth" in current_url and "Sign In" in driver.page_source:
                print("Đăng ký thành công, đã quay lại trang đăng nhập")
            else:
                print("Không thể xác định kết quả đăng ký")
        
        # Lưu thông tin tài khoản vào file (để sử dụng sau này nếu cần)
        with open("accounts.txt", "a") as f:
            f.write(f"Username: {random_username}, Email: {random_email}, Password: {random_password}\n")

except Exception as e:
    print(f"Lỗi: {e}")

finally:
    # Chờ một chút trước khi đóng trình duyệt
    time.sleep(2)
    driver.quit()