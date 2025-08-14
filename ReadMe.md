# 🧪 SELENIUM TEST AUTOMATION

## 📋 TỔNG QUAN
Dự án test tự động cho ứng dụng Angular sử dụng Selenium WebDriver và Grid.

## 🔧 CÀI ĐẶT

### Yêu cầu
- Python 3.11+, Java 8+
- Chrome, Firefox browsers
- Angular app tại `http://localhost:4200`

### Cài đặt
```bash
pip install selenium requests
```

### Tải Selenium Grid
```bash
# Tải selenium-server-4.35.0.jar vào thư mục Grid/
```

## 📁 CẤU TRÚC
```
test_selenium/
├── auth/sign_in_test.py         # Test đăng nhập
├── profile/profile_test.py      # Test profile  
├── ranking/ranking_test.py      # Test xếp hạng
├── Grid/grid-test.py           # Test đa browser
└── ReadMe.md
```

## 🚀 CÁCH CHẠY TEST

### 1. Chuẩn bị
```bash
# Khởi động Angular
ng serve

# Đảm bảo tài khoản test tồn tại:
# Email: kimphu123@gmail.com, Password: 123
```

### 2. Test đơn lẻ
```bash
# Test đăng nhập
python auth\sign_in_test.py

# Test profile  
python profile\profile_test.py

# Test ranking
python ranking\ranking_test.py
```

### 3. Test Grid (đa browser)
```bash
# Khởi động Grid
cd Grid
java -jar selenium-server-4.35.0.jar standalone

# Kiểm tra Grid: http://localhost:4444/ui

# Chạy test
python grid-test.py
```

## 📊 KẾT QUẢ MONG ĐỢI

### Sign In Test
```
Đăng nhập thành công
```

### Profile Test  
```
👤 BẮT ĐẦU TEST PROFILE
✅ Đăng nhập thành công!
✅ Đã chỉnh sửa profile
✅ TEST HOÀN TẤT!
```

### Grid Test
```
🚀 Starting Grid Test...
✅ Chrome - Account 1 logged in!
✅ Firefox - Account 2 logged in!
🎉 Multi-browser test completed!
```

## 🔧 TROUBLESHOOTING

| Lỗi | Giải pháp |
|-----|-----------|
| Connection refused port 4444 | Khởi động Selenium Grid |
| Element not found | Kiểm tra selector, tăng wait time |
| Site can't be reached | Khởi động Angular: `ng serve` |

## ⚙️ CẤU HÌNH

### Tài khoản test
```python
# Account 1 (có sẵn)
email = "kimphu123@gmail.com"
password = "123"

# Account 2 (cần tạo)  
email = "user2@gmail.com"
password = "456"
```

### Debug mode
```python
# Bỏ comment để thấy browser
# chrome_options.add_argument('--headless')
```

## 🎯 TÍNH NĂNG

- ✅ Test đăng nhập/đăng xuất
- ✅ Test chỉnh sửa profile + upload ảnh
- ✅ Test bảng xếp hạng đa cấp độ
- ✅ Test đồng thời trên Chrome + Firefox
- ✅ Test multi-account
- ✅ Error handling & cleanup
