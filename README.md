# Phát hiện ổ gà (Pothole Detection)

Ứng dụng web **Django + YOLO (Ultralytics)** để tải ảnh lên và phát hiện ổ gà trên đường.

Repository: [https://github.com/HoangDuc1307/AI](https://github.com/HoangDuc1307/AI)

## Yêu cầu

- Python 3.10+
- File weights `best.pt` (không có trong repo — tự đặt vào thư mục gốc project)

## Cài đặt

```bash
git clone https://github.com/HoangDuc1307/AI.git
cd AI

python -m venv venv
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Đặt file model `best.pt` cùng thư mục với `manage.py` (hoặc chỉnh `POTHOLE_MODEL_PATH` trong `pothole_project/settings.py`).

## Chạy ứng dụng

```bash
python manage.py migrate
python manage.py runserver
```

Mở trình duyệt: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Cấu trúc thư mục

```
├── manage.py
├── pothole_project/     # Cấu hình Django
├── pothole_app/         # View, template phát hiện
├── media/               # Ảnh upload & kết quả (tạo khi chạy, không commit)
├── best.pt              # Weights YOLO (tự thêm, không commit)
└── requirements.txt
```

## Ghi chú

- Thư mục `media/` và `venv/` không được đưa lên Git.
- Lần detect đầu có thể chậm do load model YOLO/PyTorch.
- Chỉ dùng `runserver` cho môi trường phát triển.

## Tác giả

HoangDuc1307
