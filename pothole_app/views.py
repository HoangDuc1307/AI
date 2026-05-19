import uuid
from pathlib import Path

from django.conf import settings
from django.shortcuts import render

_yolo_model = None


def _resolve_model_path() -> Path:
    return Path(getattr(settings, 'POTHOLE_MODEL_PATH', settings.BASE_DIR / 'best.pt'))


def _get_yolo(model_path: Path):
    global _yolo_model
    if _yolo_model is None:
        from ultralytics import YOLO

        _yolo_model = YOLO(str(model_path))
    return _yolo_model


def _base_context():
    model_path = _resolve_model_path()
    return {
        'model_ready': model_path.is_file(),
        'model_file': model_path.name,
    }


def home(request):
    context = _base_context()

    if request.method != 'POST':
        return render(request, 'index.html', context)

    upload = request.FILES.get('image')
    if not upload:
        context['error'] = 'Vui lòng chọn một ảnh.'
        return render(request, 'index.html', context)

    ext = Path(upload.name).suffix.lower() or '.jpg'
    allowed = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    if ext not in allowed:
        context['error'] = 'Định dạng ảnh không được hỗ trợ.'
        return render(request, 'index.html', context)

    upload_dir = Path(settings.MEDIA_ROOT) / 'uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f'{uuid.uuid4().hex}{ext}'
    dest = upload_dir / stored_name

    with open(dest, 'wb') as out:
        for chunk in upload.chunks():
            out.write(chunk)

    rel_upload = f'uploads/{stored_name}'
    context['original_image'] = rel_upload

    model_path = _resolve_model_path()
    if not model_path.is_file():
        context['error'] = (
            f'Không tìm thấy file model ({model_path.name}). '
            f'Đặt weights vào: {model_path}'
        )
        context['model_ready'] = False
        return render(request, 'index.html', context)

    try:
        model = _get_yolo(model_path)
        results = model.predict(str(dest), verbose=False)
        if not results:
            context['error'] = 'Model không trả về kết quả.'
            return render(request, 'index.html', context)

        r = results[0]
        boxes = r.boxes
        context['num_potholes'] = len(boxes) if boxes is not None else 0

        result_dir = Path(settings.MEDIA_ROOT) / 'results'
        result_dir.mkdir(parents=True, exist_ok=True)
        out_name = f'det_{stored_name}'
        out_path = result_dir / out_name
        r.save(filename=str(out_path))
        context['result_image'] = f'results/{out_name}'
    except Exception as exc:
        context['error'] = f'Lỗi khi chạy model: {exc}'

    return render(request, 'index.html', context)
