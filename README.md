# 🛒 Pourya Online Shop

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)

> یک فروشگاه اینترنتی ساخته‌شده با **Django** و **Django REST Framework**

این پروژه را بیشتر برای یادگیری و تجربه کار روی یک پروژه نسبتاً واقعی Django ساختم. در طول توسعه، روی بخش‌هایی مثل احراز هویت، سطح دسترسی کاربران، مدیریت محصولات، سبد خرید، API، تست‌نویسی و بهینه‌سازی کوئری‌های دیتابیس کار کردم.

پروژه هنوز در حال توسعه است و بعضی قسمت‌ها جای بهبود دارند.

---

## 📌 درباره پروژه

ایده پروژه یک فروشگاه آنلاین ساده بود، اما در حین توسعه سعی کردم فقط به CRUD و نمایش چند محصول محدود نشوم.

در پروژه بخش‌هایی مثل ثبت‌نام و ورود کاربران، نقش‌های خریدار و فروشنده، مدیریت محصولات، سبد خرید، Checkout، لایک و نظر، جستجو و فیلتر محصولات و همچنین یک REST API پیاده‌سازی شده است.

برای بخش API از **Django REST Framework** استفاده کردم و مستندات API نیز با **Swagger / OpenAPI** در دسترس است.

Frontend پروژه با **Django Templates** و **Bootstrap 5** ساخته شده و برای محتوای فارسی، **RTL** نیز در نظر گرفته شده است.

---

## ✨ امکانات

### 👤 کاربران و احراز هویت
- ثبت‌نام و ورود کاربران
- احراز هویت Session در بخش وب
- احراز هویت JWT برای API
- تغییر رمز عبور
- فراموشی و بازیابی رمز عبور از طریق ایمیل
- نقش‌های خریدار و فروشنده
- مدیریت دسترسی بر اساس نقش کاربر

### 🛍️ فروشگاه
- ایجاد و مدیریت محصولات
- مدیریت دسته‌بندی‌ها
- مدیریت موجودی محصولات
- پنل فروشنده
- جستجوی محصولات
- فیلتر و مرتب‌سازی محصولات
- سبد خرید
- فرایند Checkout
- لایک محصولات
- ثبت نظر برای محصولات

### 🔌 REST API
- پیاده‌سازی API با Django REST Framework
- احراز هویت JWT با SimpleJWT
- Serializer و Permissionهای اختصاصی
- مستندات API با OpenAPI
- Swagger UI و ReDoc
- فیلتر و دریافت اطلاعات محصولات از طریق API

### ⚡ بهینه‌سازی
در بعضی قسمت‌های پروژه برای کاهش کوئری‌های غیرضروری دیتابیس از موارد زیر استفاده شده است:

- `select_related()`
- `prefetch_related()`
- `only()`

برای بررسی کوئری‌ها و پیدا کردن مشکلات عملکردی نیز از **Django Debug Toolbar** و **Silk** استفاده شده است.

### 🧪 تست
برای تست پروژه از **pytest** استفاده کردم.

- ۴۸ تست نوشته شده
- تست‌ها با `pytest` و `pytest-django` اجرا می‌شوند
- حدود **۶۶٪** پوشش تست وجود دارد
- گزارش Coverage با `pytest-cov` قابل تولید است

---

## 🛠️ تکنولوژی‌ها

| بخش | تکنولوژی |
|------|----------|
| زبان | Python 3.10+ |
| Backend | Django 5.2 |
| REST API | Django REST Framework 3.15 |
| Authentication | Session / SimpleJWT |
| API Documentation | drf-spectacular / Swagger / OpenAPI |
| Database | SQLite |
| Frontend | Django Templates / Bootstrap 5 / jQuery |
| Icons | Font Awesome |
| Testing | pytest / pytest-django / pytest-cov |
| Performance | Silk / Django Debug Toolbar |
| Code Quality | Black / isort / flake8 / pre-commit |

> در حال حاضر پروژه با **SQLite** اجرا می‌شود و برای استفاده در محیط Production می‌توان آن را به **PostgreSQL** منتقل کرد.

---

## 📸 تصاویر پروژه

| صفحه اصلی | فروشگاه | پنل فروشنده |
|:---:|:---:|:---:|
| ![Homepage](screenshots/homepage.png) | ![Store](screenshots/store.png) | ![Seller Panel](screenshots/seller-panel.png) |

| Swagger UI |
|:---:|
| ![Swagger](screenshots/swagger.png) |

---

## 🚀 نصب و اجرا

### پیش‌نیازها
- Python 3.10 یا بالاتر
- pip
- Git

### ۱. دریافت پروژه
```bash
git clone https://github.com/Pourya84/Pourya-Online-Shop.git
cd Pourya-Online-Shop
۲. ساخت محیط مجازی
ویندوز:

bash
python -m venv venv
venv\Scripts\activate
Linux / macOS:

bash
python3 -m venv venv
source venv/bin/activate
۳. نصب وابستگی‌ها
bash
pip install -r requirements.txt
۴. اجرای Migrationها
bash
python manage.py migrate
۵. ساخت کاربر ادمین (در صورت نیاز)
bash
python manage.py createsuperuser
۶. اجرای پروژه
bash
python manage.py runserver
بعد از اجرای سرور، پروژه از آدرس زیر در دسترس خواهد بود:

text
http://127.0.0.1:8000/
🔌 مستندات API
مستندات API با استفاده از drf-spectacular و استاندارد OpenAPI ساخته شده است.

بعد از اجرای پروژه، Swagger و ReDoc از مسیرهایی که در urls.py تعریف شده‌اند قابل دسترسی هستند:

سرویس	آدرس
Swagger	http://127.0.0.1:8000/api/schema/swagger-ui/
ReDoc	http://127.0.0.1:8000/api/schema/redoc/
چند نمونه از APIهای پروژه:

text
GET  /api/products/
GET  /api/products/<id>/
POST /api/products/
GET  /api/categories/
برای مشاهده لیست کامل endpointها، پارامترهای درخواست و نحوه احراز هویت، بهتر است از Swagger استفاده شود.

🧪 تست‌ها
اجرای تست‌ها:

bash
pytest
اجرای تست‌ها همراه با Coverage:

bash
pytest --cov=. --cov-report=term-missing
ساخت گزارش HTML:

bash
pytest --cov=. --cov-report=html
بعد از اجرا، گزارش در مسیر htmlcov/index.html ساخته می‌شود.

در حال حاضر پروژه شامل ۴۸ تست با حدود ۶۶٪ Coverage است.

📁 ساختار پروژه
text
Pourya-Online-Shop/
│
├── accounts/          # کاربران، احراز هویت، پروفایل
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── forms.py
│   └── ...
│
├── store/             # هسته اصلی فروشگاه
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── forms.py
│   ├── services.py
│   ├── permissions.py
│   ├── validators.py
│   └── ...
│
├── core/              # توابع و ابزارهای عمومی
│
├── templates/         # قالب‌های HTML
│
├── static/            # CSS, JS, Images
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/             # فایل‌های آپلودی
│
├── tests/             # تست‌های خودکار
│
├── manage.py
├── requirements.txt
└── README.md
توضیح پوشه‌ها
پوشه	توضیح
accounts/	بخش مربوط به کاربران، احراز هویت، پروفایل و امکانات مرتبط با حساب کاربری.
store/	هسته اصلی فروشگاه. مدل‌ها، Viewها، Serializerها، فرم‌ها، Serviceها، Permissionها و Validatorها.
core/	توابع و ابزارهای عمومی پروژه.
tests/	تست‌های خودکار پروژه.
templates/ و static/	قالب‌های HTML و فایل‌های CSS، JavaScript و تصاویر پروژه.
🔍 چیزهایی که در این پروژه تمرین کردم
در این پروژه بیشتر از اینکه فقط روی ساختن صفحات تمرکز کنم، سعی کردم با بخش‌هایی از توسعه واقعی یک پروژه Django کار کنم:

طراحی Modelها و ارتباط بین آن‌ها

Authentication و Permission

طراحی REST API

نوشتن Serializer و Validator

جدا کردن بخشی از منطق برنامه از Viewها

بهینه‌سازی Queryهای دیتابیس

تست‌نویسی با pytest

مستندسازی API

بررسی Queryها با Debug Toolbar و Silk

رعایت ساختار مناسب‌تر برای پروژه

🔮 برنامه‌های بعدی
چند موردی که قصد دارم در ادامه روی پروژه انجام بدهم:

□ انتقال دیتابیس از SQLite به PostgreSQL
□ اضافه کردن Docker
□ افزایش Coverage تست‌ها
□ اضافه کردن GitHub Actions و CI
□ آماده‌سازی پروژه برای Deployment
□ کامل‌تر کردن تست‌های API
□ بهبود بخش سفارش‌ها و Checkout
□ بررسی و بهینه‌سازی بیشتر Queryهای دیتابیس
🤝 مشارکت
این پروژه در درجه اول یک پروژه شخصی و Portfolio است، اما اگر پیشنهادی برای بهتر شدن کد یا ساختار پروژه دارید، خوشحال می‌شوم آن را ببینم.

📬 ارتباط با من
📧 Email: amirkhah1384@gmail.com

در حال حاضر به دنبال فرصت‌های شغلی Junior Django / Python Backend هستم و از فرصت‌های Remote، Full-time و Freelance استقبال می‌کنم.