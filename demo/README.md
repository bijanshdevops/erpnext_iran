# دموی عمومی ERPNext Iran

دموی زندهٔ این اپ روی `erp.greenlanco.ir`: ERPNext، Frappe HR و erpnext_iran از روی image آمادهٔ
`ghcr.io/bijanshdevops/erpnext_iran`، با شرکت و اسناد نمونه و یک کاربر مهمان.

- **داده‌ها:** شرکت «شرکت نمونه فانوس» با کدینگ حساب‌های ایرانی، الگوهای ارزش افزوده، سال مالی شمسی و
  تعطیلات؛ کالا، مشتری و تأمین‌کننده؛ فاکتور خرید و فروش، دریافت وجه، چک صیادی؛ دو کارمند با فیش حقوق.
  ساخت آن‌ها در `erpnext_iran/demo_site.py` است.
- **ورود:** نام کاربری و رمز کاربر دمو روی صفحهٔ ورود نوشته شده است. این کاربر نقش‌های حسابداری، فروش،
  خرید، انبار و منابع انسانی را دارد، نه مدیر سیستم؛ رمز و مشخصات خودش را نمی‌تواند عوض کند.
- **بازنشانی:** سرویس `demo-reset` بار اول سایت را می‌سازد و از آن پشتیبان می‌گیرد، و هر `RESET_HOURS`
  ساعت همان پشتیبان را برمی‌گرداند و فایل‌های بارگذاری‌شده را پاک می‌کند.
- **خاموش:** ارسال ایمیل (`mute_emails`)، ارسال به سامانهٔ مؤدیان، زمان‌بند و ثبت‌نام عمومی.

## راه‌اندازی روی سرور

stack سایت greenlanco.ir باید بالا باشد (شبکهٔ `greenlanco_internal`)، چون nginx آن `erp.greenlanco.ir` را به
`erpnext-demo-frontend:8080` می‌فرستد.

```bash
git clone https://github.com/bijanshdevops/erpnext_iran.git ~/erpnext-demo && cd ~/erpnext-demo
cp demo/demo.env.example demo/demo.env && nano demo/demo.env   # DB_ROOT_PASSWORD و ADMIN_PASSWORD: openssl rand -hex 24
docker compose -p erpnext-demo -f demo/compose.demo.yml --env-file demo/demo.env up -d
docker compose -p erpnext-demo -f demo/compose.demo.yml --env-file demo/demo.env logs -f demo-reset   # تا «Demo site ready»، حدود ۱۰ دقیقه
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:3400/login                                  # 200
```

سپس در Cloudflare Zero Trust ← Networks ← Tunnels ← `greenlanco-server` ← Published application routes،
میزبان `erp.greenlanco.ir` را با سرویس `http://localhost:8081` اضافه کنید.

## به‌روزرسانی و ساخت دوباره

داده‌های نمونه فقط بار اول ساخته می‌شوند. برای رفتن به نسخهٔ تازهٔ image، stack را با volumeهایش پاک و
دوباره بالا بیاورید:

```bash
docker compose -p erpnext-demo -f demo/compose.demo.yml --env-file demo/demo.env pull
docker compose -p erpnext-demo -f demo/compose.demo.yml --env-file demo/demo.env down -v
docker compose -p erpnext-demo -f demo/compose.demo.yml --env-file demo/demo.env up -d
```

## منابع

حدود ۱٫۵ تا ۲ گیگابایت حافظه و ۶ گیگابایت دیسک (بیشترش image).
