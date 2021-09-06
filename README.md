این پروژه، پروژه‌ی درس رایانش ابری است. در این سیستم سه سرویس زیر را داریم:

* Authentication

کار این سرویس احراز هویت و سطح دسترسی است. در این سیستم کاربرانی که ثبت‌نام می‌کنند یکی از دو نقش دکتر یا بیمار (کاربر) را می‌توانند داشته باشند.

این سرویس یک توکن JWT برای احراز هویت درست می‌کند.

از این توکن برای برای شناسایی در سایر سرویس‌ها می توان استفاده کرد.

* Users

این سرویس برای مدیریت اطلاعات کاربران (بیماران) است. 

* Doctors

اطلاعات مربوط به دکترها در این سرویس مدیریت می‌شوند.


#### اجرا
برای اجرا می‌توان از فایل `docker-compose.yml` استفاده کرد.

```
docker-compose up
```

به صورت پیش‌فرض بروی localhost و پورت 8000 سرویس بالا می‌آید.

بنا به نیاز می‌توان آن را در `docker-compose.yml` و سرویس kong آن را تغییر داد.

Hello!