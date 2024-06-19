from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

# Đường dẫn đến ChromeDriver của bạn
driver_path = 'E:/crawl-data/chromedriver.exe'

# Khởi tạo dịch vụ cho ChromeDriver
service = Service(driver_path)

# Tùy chọn cho ChromeDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  # Chạy Chrome ở chế độ headless (không hiện giao diện)
chrome_options.add_argument('--disable-gpu')  # Tắt GPU để chạy headless mượt hơn
chrome_options.add_argument('--no-sandbox')  # Tùy chọn bảo mật (đặc biệt hữu ích trên Linux)

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=service, options=chrome_options)

# Tải trang HTML (thay thế URL bằng URL thật của bạn)
base_url = 'https://s.cafef.vn/bao-cao-tai-chinh/mwg/incsta/2024/0/0/0/0/ket-qua-hoat-dong-kinh-doanh-.chn'

# Danh sách lưu trữ dữ liệu từ các id
data_dict_list = []

for i in range(1, 72):  # Dùng range từ 1 đến 71 để lặp qua các id từ 1 đến 70
    url = f'{base_url}?id={i}'
    driver.get(url)
    time.sleep(0)  # Chờ trang tải hoàn toàn (thay đổi nếu cần)

    try:
        # Tìm hàng với id tương ứng
        row = driver.find_element(By.ID, f'{i:02}')  # Format lại id để đảm bảo 2 chữ số

        # Thu thập dữ liệu từ các cột
        data = row.find_elements(By.TAG_NAME, 'td')

        # Lấy nội dung văn bản từ các cột
        columns = [col.text for col in data]

        # Tạo dictionary để lưu dữ liệu
        data_dict = {
            "Danh mục": columns[0],
            "2021": columns[1],
            "2022": columns[2],
            "2023": columns[3]
            # "2024": columns[4]
        }

        # Thêm dictionary vào danh sách
        data_dict_list.append(data_dict)

    except Exception as e:
        print(f"Lỗi khi xử lý id {i}: {str(e)}")

# Đóng trình duyệt
driver.quit()

# Xuất ra file JSON
with open('mwg.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_dict_list, json_file, ensure_ascii=False, indent=4)

print("Đã hoàn thành việc crawl dữ liệu và lưu vào file JSON.")
