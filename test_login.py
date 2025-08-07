import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

try:
    driver.get("http://localhost:4200/auth")
    print("🔍 Đang truy cập trang login...")

    # Chờ input email xuất hiện
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    print("✅ Đã tìm thấy input email")

    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")

    email_input.send_keys("test@gmail.com")
    password_input.send_keys("123456")
    login_button.click()

    # Đợi chuyển trang hoặc thành công
    WebDriverWait(driver, 10).until(
        EC.url_contains("/quiz")  # hoặc "/home", tùy bạn định tuyến
    )
    print("🎉 Đăng nhập thành công!")

    time.sleep(5)  # cho bạn thấy kết quả xong rồi mới quit

except Exception as e:
    print("❌ Lỗi:", e)

finally:
    print("⛔ Đóng trình duyệt...")
    driver.quit()
