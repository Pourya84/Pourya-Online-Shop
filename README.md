🛒 Pourya Online Shop

یک فروشگاه اینترنتی که با Django و Django REST Framework ساخته شده است.

این پروژه را بیشتر برای یادگیری و تجربه کار روی یک پروژه نسبتاً واقعی Django ساختم. در طول توسعه پروژه روی بخش‌هایی مثل احراز هویت، سطح دسترسی کاربران، مدیریت محصولات، سبد خرید، API، تست‌نویسی و بهینه‌سازی کوئری‌های دیتابیس کار کردم.

پروژه هنوز در حال توسعه است و بعضی قسمت‌ها جای بهبود دارند.









📌 درباره پروژه

ایده پروژه یک فروشگاه آنلاین ساده بود، اما در حین توسعه سعی کردم فقط به CRUD و نمایش چند محصول محدود نشوم.

در پروژه بخش‌هایی مثل ثبت‌نام و ورود کاربران، نقش‌های خریدار و فروشنده، مدیریت محصولات، سبد خرید، checkout، لایک و نظر، جستجو و فیلتر محصولات و همچنین یک REST API پیاده‌سازی شده است.

برای بخش API از Django REST Framework استفاده کردم و مستندات API نیز با Swagger / OpenAPI در دسترس است.

Frontend پروژه با Django Templates و Bootstrap 5 ساخته شده و برای محتوای فارسی، RTL نیز در نظر گرفته شده است.

✨ امکانات
👤 کاربران و احراز هویت

ثبت‌نام و ورود کاربران

احراز هویت Session در بخش وب

احراز هویت JWT برای API

تغییر رمز عبور

فراموشی و بازیابی رمز عبور از طریق ایمیل

نقش‌های خریدار و فروشنده

مدیریت دسترسی بر اساس نقش کاربر

🛍️ فروشگاه

ایجاد و مدیریت محصولات

مدیریت دسته‌بندی‌ها

مدیریت موجودی محصولات

پنل فروشنده

جستجوی محصولات

فیلتر و مرتب‌سازی محصولات

سبد خرید

فرایند Checkout

لایک محصولات

ثبت نظر برای محصولات

🔌 REST API

پیاده‌سازی API با Django REST Framework

احراز هویت JWT با SimpleJWT

Serializer و Permissionهای اختصاصی

مستندات API با OpenAPI

Swagger UI و ReDoc

فیلتر و دریافت اطلاعات محصولات از طریق API

⚡ بهینه‌سازی

در بعضی قسمت‌های پروژه برای کاهش کوئری‌های غیرضروری دیتابیس از موارد زیر استفاده شده است:

select_related()

prefetch_related()

only()

برای بررسی کوئری‌ها و پیدا کردن مشکلات عملکردی نیز از Django Debug Toolbar و Silk استفاده شده است.

🧪 تست

برای تست پروژه از pytest استفاده کردم.

در حال حاضر:

48 تست نوشته شده

تست‌ها با pytest و pytest-django اجرا می‌شوند

حدود 66٪ پوشش تست وجود دارد

گزارش Coverage با pytest-cov قابل تولید است

🛠️ تکنولوژی‌ها
بخش	تکنولوژی
زبان	Python 3.10+
Backend	Django 5.2
REST API	Django REST Framework 3.15
Authentication	Session / SimpleJWT
API Documentation	drf-spectacular / Swagger / OpenAPI
Database	SQLite
Frontend	Django Templates / Bootstrap 5 / jQuery
Icons	Font Awesome
Testing	pytest / pytest-django / pytest-cov
Performance	Silk / Django Debug Toolbar
Code Quality	Black / isort / flake8 / pre-commit

در حال حاضر پروژه با SQLite اجرا می‌شود و برای استفاده در محیط Production می‌توان آن را به PostgreSQL منتقل کرد.

📸 تصاویر پروژه

تصاویر بخش‌های مختلف پروژه را اینجا قرار می‌دهم.

صفحه اصلی

فروشگاه

پنل فروشنده

🚀 نصب و اجرا
پیش‌نیازها

برای اجرای پروژه به موارد زیر نیاز دارید:

Python 3.10 یا بالاتر

pip

Git

1. دریافت پروژه
git clone https://github.com/Pourya84/Pourya-Online-Shop.git
cd Pourya-Online-Shop

2. ساخت محیط مجازی

در ویندوز:

python -m venv venv
venv\Scripts\activate


در Linux / macOS:

python3 -m venv venv
source venv/bin/activate

3. نصب وابستگی‌ها
pip install -r requirements.txt

4. اجرای Migrationها
python manage.py migrate

5. ساخت کاربر ادمین

در صورت نیاز:

python manage.py createsuperuser

6. اجرای پروژه
python manage.py runserver


بعد از اجرای سرور، پروژه از آدرس زیر در دسترس خواهد بود:

http://127.0.0.1:8000/

🔌 مستندات API

مستندات API با استفاده از drf-spectacular و استاندارد OpenAPI ساخته شده است.

بعد از اجرای پروژه، Swagger و ReDoc از مسیرهایی که در urls.py تعریف شده‌اند قابل دسترسی هستند.

برای مثال:

Swagger:
http://127.0.0.1:8000/<swagger-path>/

ReDoc:
http://127.0.0.1:8000/<redoc-path>/


مسیرهای بالا باید با URL واقعی تعریف‌شده در پروژه جایگزین شوند.

چند نمونه از APIهای پروژه:

GET /api/products/
GET /api/products/<id>/
POST /api/products/
GET /api/categories/


برای مشاهده لیست کامل endpointها، پارامترهای درخواست و نحوه احراز هویت، بهتر است از Swagger استفاده شود.

🧪 تست‌ها

برای اجرای تست‌ها:

pytest


برای اجرای تست‌ها همراه با Coverage:

pytest --cov=. --cov-report=term-missing


برای ساخت گزارش HTML:

pytest --cov=. --cov-report=html


بعد از اجرای دستور، گزارش در مسیر زیر ساخته می‌شود:

htmlcov/index.html


در حال حاضر پروژه شامل 48 تست با حدود 66٪ Coverage است.

📁 ساختار پروژه
Pourya-Online-Shop/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── forms.py
│   └── ...
│
├── store/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── forms.py
│   ├── services.py
│   ├── permissions.py
│   ├── validators.py
│   └── ...
│
├── core/
│   └── ...
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│   └── ...
│
├── tests/
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md

توضیح پوشه‌ها

accounts/

بخش مربوط به کاربران، احراز هویت، پروفایل و امکانات مرتبط با حساب کاربری.

store/

هسته اصلی فروشگاه. مدل‌ها، Viewها، Serializerها، فرم‌ها، Serviceها، Permissionها و Validatorهای مربوط به فروشگاه در این بخش قرار دارند.

core/

توابع و ابزارهای عمومی پروژه.

tests/

تست‌های خودکار پروژه.

templates/ و static/

قالب‌های HTML و فایل‌های CSS، JavaScript و تصاویر پروژه.

🔍 چیزهایی که در این پروژه تمرین کردم

در این پروژه بیشتر از اینکه فقط روی ساختن صفحات تمرکز کنم، سعی کردم با بخش‌هایی از توسعه واقعی یک پروژه Django کار کنم.

مهم‌ترین چیزهایی که روی آنها کار کردم:

طراحی Modelها و ارتباط بین آنها

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

انتقال دیتابیس از SQLite به PostgreSQL

اضافه کردن Docker

افزایش Coverage تست‌ها

اضافه کردن GitHub Actions و CI

آماده‌سازی پروژه برای Deployment

کامل‌تر کردن تست‌های API

بهبود بخش سفارش‌ها و Checkout

بررسی و بهینه‌سازی بیشتر Queryهای دیتابیس

🤝 مشارکت

این پروژه در درجه اول یک پروژه شخصی و Portfolio است، اما اگر پیشنهادی برای بهتر شدن کد یا ساختار پروژه دارید، خوشحال می‌شوم آن را ببینم.

برای تغییرات بزرگ بهتر است ابتدا یک Issue ایجاد شود و بعد از مشخص شدن تغییرات، Pull Request ارسال شود.

📄 لایسنس

این پروژه تحت MIT License منتشر شده است.

جزئیات بیشتر در فایل LICENSE قرار دارد.

📬 ارتباط با من

Pourya

GitHub: @Pourya84

Email: amirkhah1384@gmail.com

در حال حاضر به دنبال فرصت‌های شغلی Junior Django / Python Backend هستم و از فرصت‌های Remote، Full-time و Freelance استقبال می‌کنم.