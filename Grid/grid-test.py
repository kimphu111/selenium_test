from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# # Thêm một dòng print để kiểm tra nếu mã thực sự chạy
# print("Starting test...")

# # Tạo đối tượng Options cho Chrome
# chrome_options = Options()
# # Thêm các tùy chọn nếu cần, ví dụ:
# # chrome_options.add_argument('--headless')  # Nếu muốn chạy không hiển thị giao diện

# # Kết nối với Hub qua Remote WebDriver
# driver = webdriver.Remote(
#     command_executor='http://localhost:4444/wd/hub',  # URL của Hub
#     options=chrome_options  # Thay desired_capabilities bằng options
# )

# # Mở trang web
# driver.get("http://www.google.com")

# # In tiêu đề trang
# print("Page title is:", driver.title)

# # Đóng trình duyệt
# driver.quit()

# # Thêm một dòng print để kết thúc kiểm thử
# print("Test completed.")



# Node 1 (Chrome) configuration
chrome_options = Options()
chrome_options.add_argument('--headless')  # Chạy không giao diện người dùng (tùy chọn)

# Node 2 (Firefox) configuration
firefox_options = FirefoxOptions()
firefox_options.add_argument('--headless')  # Chạy không giao diện người dùng (tùy chọn)

# Kết nối đến Node 1 (Chrome) thông qua Selenium Grid
driver_chrome = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',  # URL của Hub
    options=chrome_options
)

# Kết nối đến Node 2 (Firefox) thông qua Selenium Grid
driver_firefox = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',  # URL của Hub
    options=firefox_options
)

# Mở trang web trên Node 1 (Chrome)
driver_chrome.get("http://localhost:4200")
print("Chrome Title:", driver_chrome.title)

# Mở trang web trên Node 2 (Firefox)
driver_firefox.get("http://localhost:4200")
print("Firefox Title:", driver_firefox.title)

# Đóng trình duyệt sau khi kiểm thử
driver_chrome.quit()
driver_firefox.quit()

print("Test completed.")

