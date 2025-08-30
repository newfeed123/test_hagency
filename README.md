1. Clone repository
	+ git clone https://github.com/newfeed123/test_hagency.git
	+ cd test_hagency
2. Tạo môi trường ảo và cài đặt thư viện
	+ python -m venv venv  
	+ Nếu dùng Linux, Unbutu: source venv/bin/activate  
  + Nếu dùng Windows: venv\Scripts\activate
	+ pip install -r requirements.txt  
3. Thiết lập cơ sở dữ liệu
	+ python manage.py makemigrations  
	+ python manage.py migrate  
4. Chạy dự án
	+ python manage.py runserver  

=> Truy cập để test API trên swagger: http://127.0.0.1:8000/swagger/

=> Truy cập site admin: http://127.0.0.1:8000/admin/
	+ account: admin
	+ password: 1234
