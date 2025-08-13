from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)

try:
    print("BẮT ĐẦU TEST PROFILE")
    
    # 1. Đăng nhập
    driver.get("http://localhost:4200/auth")
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    email_input.send_keys("kimphu123@gmail.com")
    password_input.send_keys("123")
    
    login_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")
    login_button.click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("/home"))
    print("Đăng nhập thành công!")

    # 2. Mở trang profile
    driver.get("http://localhost:4200/profile")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-container"))
    )
    print("Đã mở trang profile")
    
    # 3. Mở form chỉnh sửa
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        try:
            if "Chỉnh sửa" in button.text or "edit" in button.text.lower():
                driver.execute_script("arguments[0].click();", button)
                print("Đã mở form chỉnh sửa")
                break
        except:
            continue
    
    time.sleep(2)
    
    # 4. Điền thông tin
    fields = {
        "firstName": "Kim",
        "lastName": "Phu",
        "birthday": "01/01/2000",
        "phone": "0123456789",
        "location": "Ho Chi Minh City"
    }
    
    for field_id, value in fields.items():
        try:
            element = driver.find_element(By.ID, field_id)
            element.clear()
            element.send_keys(value)
            print(f"Đã điền {field_id}")
        except:
            print(f"Không tìm thấy {field_id}")
    
        # 5. Upload ảnh (nếu có)
    image_path = r"C:\Users\Admin\Pictures\Screenshots\z6565935812881_69ca1b0c865063c52be39aeb43ef1b5a.jpg"
    if os.path.exists(image_path):
        try:
            # Click nút upload
            upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload new pictures')]")
            driver.execute_script("arguments[0].click();", upload_button)
            
            # Tạo và sử dụng input file
            driver.execute_script(f"""
                var input = document.createElement('input');
                input.type = 'file';
                input.style.display = 'none';
                document.body.appendChild(input);
                
                input.addEventListener('change', function() {{
                    var file = this.files[0];
                    if (file) {{
                        var reader = new FileReader();
                        reader.onload = function(e) {{
                            document.querySelector('.avatar').src = e.target.result;
                        }};
                        reader.readAsDataURL(file);
                    }}
                }});
            """)
            
            # Upload file
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(image_path)
            print("Đã thay đổi avatar")
            
        except:
            print(" Không thể upload ảnh")
    
    # 6. Lưu thông tin
    save_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Save')]")
    if save_buttons:
        driver.execute_script("arguments[0].click();", save_buttons[0])
        print("Đã lưu thông tin")
    else:
        print("Không tìm thấy nút Save")
    
    time.sleep(3)
    print("TEST HOÀN TẤT!")

except Exception as e:
    print(f"Lỗi: {e}")

finally:
    time.sleep(2)
    driver.quit()