from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options)

try:
    print("\nBẮT ĐẦU TEST BẢNG XẾP HẠNG\n")
    
    # 1. Đăng nhập
    driver.get("http://localhost:4200/auth")
    
    print("🔑 Đang đăng nhập...")
    
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    email_input.send_keys("kimphu123@gmail.com")
    password_input.send_keys("123")
    
    login_button = driver.find_element(By.XPATH, "//button[text()='Sign In']")
    login_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("/home")
    )
    print("Đăng nhập thành công!")

    # 2. Chuyển sang trang ranking
    driver.get("http://localhost:4200/ranking")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "rankings-container"))
    )
    print(" Đã mở trang xếp hạng")
    
    # 3. Kiểm tra xếp hạng ở các level
    levels = ["mix", "easy", "medium", "hard"]
    
    for level in levels:
        print(f"\n======== KIỂM TRA MỨC ĐỘ: {level.upper()} ========")
        
        # Click vào nút mức độ
        level_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{level.capitalize()}')]"))
        )
        level_button.click()
        print(f" Đã chọn mức độ: {level}")
        
        # Kiểm tra hiển thị loading
        try:
            loading_text = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Đang tải xếp hạng...')]"))
            )
            print(" Hiển thị loading khi chuyển mức độ")
        except:
            print("Không thấy hiển thị loading")
        
        # Đợi dữ liệu tải xong
        try:
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.CLASS_NAME, "loading"))
            )
            print("Đã tải dữ liệu xếp hạng")
        except:
            print("Không thấy trạng thái loading biến mất")
        
        # Kiểm tra có dữ liệu xếp hạng không
        ranking_items = driver.find_elements(By.CLASS_NAME, "ranking-item")
        print(f"👥 Số người chơi ở level {level}: {len(ranking_items)}")

        if len(ranking_items) > 0:
            # Kiểm tra huy chương
            print("\n--- Kiểm tra huy chương ---")
            medal_types = [
                {"position": 0, "name": "Vàng", "alt": "gold medal"},
                {"position": 1, "name": "Bạc", "alt": "silver medal"},
                {"position": 2, "name": "Đồng", "alt": "bronze medal"},
                {"position": 3, "name": "Khuyến khích", "alt": "encouragement medal"},
                {"position": 4, "name": "Tinh thần", "alt": "spirit medal"}
            ]
            
            for medal in medal_types:
                position = medal["position"]
                if position < len(ranking_items):
                    try:
                        medal_img = ranking_items[position].find_element(By.XPATH, f".//img[@alt='{medal['alt']}']")
                        print(f" Huy chương {medal['name']} hiển thị cho hạng {position+1}")
                    except:
                        print(f" Không tìm thấy huy chương {medal['name']} cho hạng {position+1}")
            
            # Hiển thị top 5 người chơi (hoặc ít hơn nếu không đủ)
            print("\n--- Top người chơi ---")
            top_count = min(5, len(ranking_items))
            
            for i in range(top_count):
                try:
                    player_name = ranking_items[i].find_element(By.CLASS_NAME, "player-name").text
                    score = ranking_items[i].find_element(By.CLASS_NAME, "score").text
                    duration = ranking_items[i].find_element(By.CLASS_NAME, "duration").text
                    print(f"#{i+1}: {player_name} - Điểm: {score} - Thời gian: {duration}")
                except:
                    print(f"Không thể lấy đầy đủ thông tin người chơi hạng {i+1}")
            
            # Kiểm tra sắp xếp theo điểm
            if len(ranking_items) >= 2:
                print("\n--- Kiểm tra thứ tự xếp hạng ---")
                scores = []
                durations = []
                
                for item in ranking_items:
                    try:
                        score_text = item.find_element(By.CLASS_NAME, "score").text
                        duration_text = item.find_element(By.CLASS_NAME, "duration").text
                        scores.append(int(score_text))
                        durations.append(duration_text)
                    except:
                        continue
                
                is_sorted_by_score = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
                
                if is_sorted_by_score:
                    print(" Xếp hạng được sắp xếp đúng theo điểm số giảm dần")
                    
                    # Kiểm tra các trường hợp điểm bằng nhau
                    equal_score_positions = []
                    for i in range(len(scores)-1):
                        if scores[i] == scores[i+1]:
                            equal_score_positions.append((i, i+1))
                    
                    if equal_score_positions:
                        print(f"Phát hiện {len(equal_score_positions)} trường hợp điểm bằng nhau")
                        for pos in equal_score_positions:
                            i, j = pos
                            print(f"Vị trí {i+1} và {j+1} có cùng điểm {scores[i]}")
                            print(f"Thời gian: {durations[i]} vs {durations[j]}")
                else:
                    print(" Xếp hạng KHÔNG được sắp xếp đúng theo điểm số giảm dần")
                    print("Chi tiết điểm số:")
                    for i, score in enumerate(scores):
                        print(f"Hạng {i+1}: {score} điểm")
        else:
            print(" Không có dữ liệu xếp hạng để kiểm tra")
        
        time.sleep(1)

    print("\nTEST BẢNG XẾP HẠNG HOÀN TẤT! ")

except Exception as e:
    print(f" Lỗi: {e}")

finally:
    time.sleep(2)
    driver.quit()