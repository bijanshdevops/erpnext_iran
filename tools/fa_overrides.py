"""Persian overrides merged into erpnext_iran/translations/fa.csv by update_translations.py.

ONBOARDING: ERPNext's onboarding texts (Module Onboarding / Onboarding Step records). They
live in database records, so ERPNext's own fa.po has none of them. Keys are (record, field)
and the English source is read from the site when regenerating.

CORRECTIONS: strings ERPNext/Frappe already translate, but wrongly (wrong word, reversed word
order, missing half-space) or inconsistently - "Item" must always be «کالا».

FORM_TOURS: help texts of ERPNext's form tours (Form Tour Step records, also untranslated in
fa.po). The desk passes them to __() as-is, so the English text is the key.
"""

CORRECTIONS = {
	"Item": "کالا",
	"Items": "کالاها",
	"Item Group": "گروه کالا",
	"Item Code": "کد کالا",
	"Item Name": "نام کالا",
	"Item Price": "قیمت کالا",
	"Item Tax Template": "الگوی مالیات کالا",
	"Total Active Items": "تعداد کالاهای فعال",
	"Stock": "انبار",
	"Manufacturing": "تولید",
	"Assets": "دارایی‌ها",
	"Projects": "پروژه‌ها",
	"Supplier": "تأمین‌کننده",
	"Selling Settings": "تنظیمات فروش",
	"Accounts Settings": "تنظیمات حسابداری",
	"Setup Taxes": "تنظیم مالیات‌ها",
	"Purchase Order Trends": "روند سفارش خرید",
	"Sales Order Trends": "روند سفارش فروش",
	"Purchase Receipt Trends": "روند رسید خرید",
	"Delivery Trends": "روند تحویل",
	"Opportunity Trends": "روند فرصت‌ها",
	"Payables": "حساب‌های پرداختنی",
	"Receivables": "حساب‌های دریافتنی",
	"Accounts Payable": "حساب‌های پرداختنی",
	"Accounts Receivable": "حساب‌های دریافتنی",
	"Financial Reports": "گزارش‌های مالی",
	"Financial Statements": "صورت‌های مالی",
	"Warehouse wise Stock Value": "ارزش موجودی به تفکیک انبار",
	"Asset Value Analytics": "تحلیل ارزش دارایی‌ها",
	"Reports & Masters": "گزارش‌ها و اطلاعات پایه",
	"Integrations": "یکپارچه‌سازی‌ها",
	"ERPNext Integrations": "یکپارچه‌سازی‌های ERPNext",
	"Last synced {0}": "آخرین همگام‌سازی {0}",
	"Show {0} List": "نمایش فهرست {0}",
	"Skip": "رد شدن",
	"Dismiss": "بستن",
	# (source, context) for strings Frappe translates with a context
	("Dismiss", "Stop showing the onboarding widget."): "بستن",
	"Help": "راهنما",
	"Setting up Taxes": "تنظیم مالیات‌ها",
	# Workspace headings (stored as HTML in the workspace content)
	'<span class="h4"><b>Reports &amp; Masters</b></span>': '<span class="h4"><b>گزارش‌ها و اطلاعات پایه</b></span>',
	'<span class="h4"><b>Reports & Masters</b></span>': '<span class="h4"><b>گزارش‌ها و اطلاعات پایه</b></span>',
	'<span class="h4"><b>Masters &amp; Reports</b></span>': '<span class="h4"><b>اطلاعات پایه و گزارش‌ها</b></span>',
	# Accounting
	"Chart of Accounts": "سرفصل حساب‌ها",
	"Chart of Accounts Importer": "ورود سرفصل حساب‌ها",
	"Chart of Cost Centers": "درخت مراکز هزینه",
	"Cost Center and Budgeting": "مرکز هزینه و بودجه‌بندی",
	"Accounting Dimension": "بُعد حسابداری",
	"Accounting Masters": "اطلاعات پایه حسابداری",
	"Accounting Period": "دوره حسابداری",
	"Opening and Closing": "افتتاحیه و اختتامیه",
	"Period Closing Voucher": "سند اختتامیه دوره",
	"Opening Invoice Creation Tool": "ابزار ایجاد فاکتورهای افتتاحیه",
	"Journal Entry": "سند حسابداری",
	"Journal Entry Template": "الگوی سند حسابداری",
	"Payment Entry": "ثبت پرداخت",
	"Payments": "پرداخت‌ها",
	"Payment Term": "شرط پرداخت",
	"Mode of Payment": "روش پرداخت",
	"General Ledger": "دفتر کل",
	"Trial Balance": "تراز آزمایشی",
	"Profit and Loss": "سود و زیان",
	"Purchase Invoice": "فاکتور خرید",
	"Finance Book": "دفتر مالی",
	"Learn Accounting": "آموزش حسابداری",
	"Multi Currency": "چندارزی",
	"Currency Exchange": "نرخ تبدیل ارز",
	"Exchange Rate Revaluation": "تسعیر ارز",
	"Share Management": "مدیریت سهام",
	"Shareholder": "سهامدار",
	"Share Transfer": "انتقال سهام",
	"Share Ledger": "دفتر سهام",
	"Share Balance": "مانده سهام",
	"Bank Clearance": "تسویه بانکی",
	"Bank Reconciliation Tool": "ابزار مغایرت‌گیری بانکی",
	"Bank Reconciliation Statement": "صورت مغایرت بانکی",
	"Tax Masters": "اطلاعات پایه مالیاتی",
	"Sales Taxes and Charges Template": "الگوی مالیات و هزینه‌های فروش",
	"Purchase Taxes and Charges Template": "الگوی مالیات و هزینه‌های خرید",
	"Tax Category": "دسته‌بندی مالیاتی",
	"Tax Rule": "قاعده مالیاتی",
	"Tax Withholding Category": "دسته‌بندی مالیات تکلیفی",
	"Total Outgoing Bills": "جمع صورتحساب‌های صادره",
	"Total Incoming Bills": "جمع صورتحساب‌های دریافتی",
	"Total Incoming Payment": "جمع دریافت‌ها",
	"Total Outgoing Payment": "جمع پرداخت‌ها",
	# Buying
	"Material Request": "درخواست کالا",
	"Request for Quotation": "درخواست استعلام قیمت",
	"Supplier Quotation": "استعلام قیمت تأمین‌کننده",
	"Supplier Group": "گروه تأمین‌کننده",
	"Supplier Scorecard": "کارنامه تأمین‌کننده",
	"Supplier Scorecard Variable": "متغیر کارنامه تأمین‌کننده",
	"Supplier Scorecard Criteria": "معیارهای کارنامه تأمین‌کننده",
	"Supplier Scorecard Standing": "رتبه کارنامه تأمین‌کننده",
	"Items & Pricing": "کالاها و قیمت‌گذاری",
	"Items and Pricing": "کالاها و قیمت‌گذاری",
	"Price List": "فهرست قیمت",
	"Product Bundle": "بسته محصول",
	"Pricing Rule": "قاعده قیمت‌گذاری",
	"Terms and Conditions Template": "الگوی شرایط و ضوابط",
	"Address": "نشانی",
	"Key Reports": "گزارش‌های کلیدی",
	"Other Reports": "سایر گزارش‌ها",
	"Purchase Analytics": "تحلیل خرید",
	"Purchase Order Analysis": "تحلیل سفارش خرید",
	"Purchase Invoice Trends": "روند فاکتور خرید",
	"Supplier-Wise Sales Analytics": "تحلیل فروش به تفکیک تأمین‌کننده",
	"Items to Order and Receive": "کالاهای قابل سفارش و دریافت",
	"Items To Be Requested": "کالاهای نیازمند درخواست",
	"Item-wise Purchase History": "سابقه خرید به تفکیک کالا",
	"Procurement Tracker": "پیگیری تدارکات",
	"Subcontracted Raw Materials To Be Transferred": "مواد اولیه پیمانکاری قابل انتقال",
	"Subcontracted Item To Be Received": "کالای پیمانکاری قابل دریافت",
	"Supplier Quotation Comparison": "مقایسه استعلام‌های قیمت تأمین‌کنندگان",
	"Material Requests for which Supplier Quotations are not created": "درخواست‌های کالای بدون استعلام قیمت تأمین‌کننده",
	"Supplier Addresses And Contacts": "نشانی و مخاطبان تأمین‌کنندگان",
	"Regional": "منطقه‌ای",
	"Import Supplier Invoice": "ورود فاکتور تأمین‌کننده",
	"Learn Procurement": "آموزش تدارکات",
	# Selling / CRM
	"Lead": "سرنخ",
	"Lead Source": "منبع سرنخ",
	"Quotation": "پیش‌فاکتور",
	"Quotation Trends": "روند پیش‌فاکتور",
	"Blanket Order": "سفارش کلی",
	"Sales Person": "کارشناس فروش",
	"Shipping Rule": "قاعده حمل‌ونقل",
	"Point of Sale": "صندوق فروش (POS)",
	"Point-of-Sale Profile": "پروفایل صندوق فروش",
	"POS Opening Entry": "ثبت افتتاح صندوق",
	"POS Closing Entry": "ثبت بستن صندوق",
	"Loyalty Point Entry": "ثبت امتیاز وفاداری",
	"Sales Analytics": "تحلیل فروش",
	"Sales Order Analysis": "تحلیل سفارش فروش",
	"Sales Invoice Trends": "روند فاکتور فروش",
	"Delivery Note Trends": "روند حواله خروج",
	"Customer Acquisition and Loyalty": "جذب و وفاداری مشتری",
	"Inactive Customers": "مشتریان غیرفعال",
	"Customer Credit Balance": "مانده اعتبار مشتری",
	"Customers Without Any Sales Transactions": "مشتریان بدون معامله فروش",
	"Customer Addresses And Contacts": "نشانی و مخاطبان مشتریان",
	"Sales Person-wise Transaction Summary": "خلاصه معاملات به تفکیک کارشناس فروش",
	"Item-wise Sales History": "سابقه فروش به تفکیک کالا",
	"Available Stock for Packing Items": "موجودی در دسترس کالاهای بسته‌بندی",
	"Pending SO Items For Purchase Request": "کالاهای سفارش فروش در انتظار درخواست خرید",
	"Sales Partners Commission": "کمیسیون شرکای فروش",
	"Territory Target Variance Based On Item Group": "انحراف از هدف منطقه بر اساس گروه کالا",
	"Sales Person Target Variance Based On Item Group": "انحراف از هدف کارشناس فروش بر اساس گروه کالا",
	"Sales Partner Target Variance Based On Item Group": "انحراف از هدف شریک فروش بر اساس گروه کالا",
	"Learn Sales Management": "آموزش مدیریت فروش",
	# Stock
	"Unit of Measure (UOM)": "واحد اندازه‌گیری (UOM)",
	"UOM Conversion Factor": "ضریب تبدیل واحد",
	"Stock Reconciliation": "انبارگردانی",
	"Update Stock": "به‌روزرسانی موجودی انبار",
	"Stock Settings": "تنظیمات انبار",
	"Stock Transactions": "تراکنش‌های انبار",
	"Stock Entry": "سند انبار",
	"Delivery Note": "حواله خروج",
	"Pick List": "فهرست برداشت",
	"Landed Cost Voucher": "سند هزینه‌های جانبی خرید",
	"Packing Slip": "برگه بسته‌بندی",
	"Installation Note": "یادداشت نصب",
	"Item Alternative": "کالای جایگزین",
	"Item Manufacturer": "سازنده کالا",
	"Item Attribute": "ویژگی کالا",
	"Item Variant Settings": "تنظیمات گونه کالا",
	"Item Variant Details": "جزئیات گونه‌های کالا",
	"Item Prices": "قیمت‌های کالا",
	"Item Price Stock": "قیمت و موجودی کالا",
	"Item Shortage Report": "گزارش کمبود کالا",
	"Items Catalogue": "کاتالوگ کالاها",
	"Itemwise Recommended Reorder Level": "نقطه سفارش پیشنهادی به تفکیک کالا",
	"Customs Tariff Number": "شماره تعرفه گمرکی",
	"Serial No and Batch": "شماره سریال و بچ",
	"Batch": "بچ",
	"Serial No Status": "وضعیت شماره سریال",
	"Serial No Warranty Expiry": "انقضای گارانتی شماره سریال",
	"Serial No Service Contract Expiry": "انقضای قرارداد خدمات شماره سریال",
	"Batch Item Expiry Status": "وضعیت انقضای کالاهای بچ‌دار",
	"Batch-Wise Balance History": "سابقه موجودی به تفکیک بچ",
	"Quality Inspection Template": "الگوی بازرسی کیفیت",
	"Quick Stock Balance": "موجودی سریع انبار",
	"Requested Items To Be Transferred": "کالاهای درخواستی قابل انتقال",
	"Stock Reports": "گزارش‌های انبار",
	"Stock Ledger": "دفتر انبار",
	"Stock Balance": "موجودی انبار",
	"Stock Projected Qty": "مقدار پیش‌بینی‌شده موجودی",
	"Stock Summary": "خلاصه موجودی",
	"Stock Ageing": "سن موجودی",
	"Stock Analytics": "تحلیل موجودی",
	"Warehouse Wise Stock Balance": "موجودی به تفکیک انبار",
	"Learn Inventory Management": "آموزش مدیریت موجودی",
	# Assets
	"Asset Category": "گروه دارایی",
	"Asset Movement": "جابه‌جایی دارایی",
	"Asset Maintenance": "نگهداری دارایی",
	"Asset Maintenance Team": "تیم نگهداری دارایی",
	"Asset Maintenance Log": "سابقه نگهداری دارایی",
	"Asset Repair": "تعمیر دارایی",
	"Asset Capitalization": "سرمایه‌ای کردن دارایی",
	"Asset Depreciation Ledger": "دفتر استهلاک دارایی",
	"Asset Depreciations and Balances": "استهلاک و مانده دارایی‌ها",
	"Fixed Asset Register": "دفتر دارایی‌های ثابت",
	# Home / setup
	"Data Import and Settings": "ورود داده‌ها و تنظیمات",
	"Import Data": "ورود داده‌ها",
	"Email Account": "حساب ایمیل",
	# Buying Settings
	"Naming Series and Price Defaults": "سری شماره‌گذاری و پیش‌فرض‌های قیمت",
	"Supplier Naming By": "نام‌گذاری تأمین‌کننده بر اساس",
	"Supplier Name": "نام تأمین‌کننده",
	"Naming Series": "سری شماره‌گذاری",
	"Series": "سری شماره‌گذاری",
	"Default Supplier Group": "گروه پیش‌فرض تأمین‌کننده",
	"Default Buying Price List": "فهرست قیمت پیش‌فرض خرید",
	"Default Selling Price List": "فهرست قیمت پیش‌فرض فروش",
	"Action If Same Rate is Not Maintained": "اقدام در صورت حفظ نشدن نرخ یکسان",
	"Stop": "توقف",
	"Warn": "هشدار",
	"Role Allowed to Override Stop Action": "نقش مجاز به نادیده گرفتن توقف",
	"Is Purchase Order Required for Purchase Invoice & Receipt Creation?": "آیا برای ایجاد فاکتور و رسید خرید، سفارش خرید لازم است؟",
	"Is Purchase Receipt Required for Purchase Invoice Creation?": "آیا برای ایجاد فاکتور خرید، رسید خرید لازم است؟",
	"Purchase Order Required": "سفارش خرید الزامی است",
	"Purchase Receipt Required": "رسید خرید الزامی است",
	"Blanket Order Allowance (%)": "حد مجاز بیش از سفارش کلی (٪)",
	"Update frequency of Project": "تناوب به‌روزرسانی پروژه",
	"How often should Project be updated of Total Purchase Cost ?": "بهای کل خرید پروژه هر چند وقت یک‌بار به‌روز شود؟",
	"Each Transaction": "با هر تراکنش",
	"Manual": "دستی",
	"Set Landed Cost Based on Purchase Invoice Rate": "محاسبه بهای تمام‌شده بر اساس نرخ فاکتور خرید",
	"Use Transaction Date Exchange Rate": "استفاده از نرخ ارز تاریخ تراکنش",
	"While making a Purchase Receipt or Purchase Invoice from a Purchase Order, use the exchange rate on its posting date rather than inheriting it from the Purchase Order.": "هنگام ایجاد رسید یا فاکتور خرید از روی سفارش خرید، نرخ ارز تاریخ همان سند به کار رود نه نرخ سفارش خرید.",
	"Allow Supplier Quotation with Zero Quantity": "اجازه ثبت استعلام قیمت تأمین‌کننده با مقدار صفر",
	"Allows users to submit Supplier Quotations with zero quantity. Useful when rates are fixed but the quantities are not. Eg. Rate Contracts.": "کاربران می‌توانند استعلام قیمت تأمین‌کننده را با مقدار صفر ثبت کنند. برای وقتی که نرخ ثابت است اما مقدار هنوز معلوم نیست، مانند قراردادهای نرخ ثابت.",
	"Allow Request for Quotation with Zero Quantity": "اجازه درخواست استعلام قیمت با مقدار صفر",
	"Allows users to submit Request for Quotations with zero quantity. Useful when rates are fixed but the quantities are not. Eg. Rate Contracts.": "کاربران می‌توانند درخواست استعلام قیمت را با مقدار صفر ثبت کنند. برای وقتی که نرخ ثابت است اما مقدار هنوز معلوم نیست، مانند قراردادهای نرخ ثابت.",
	"Maintain Same Rate Throughout the Purchase Cycle": "حفظ نرخ یکسان در کل چرخه خرید",
	"Allow Item To Be Added Multiple Times in a Transaction": "اجازه افزودن یک کالا در چند ردیف یک تراکنش",
	"Disable Last Purchase Rate": "غیرفعال کردن نرخ آخرین خرید",
	"Subcontracting Settings": "تنظیمات پیمانکاری",
	"Backflush Raw Materials of Subcontract Based On": "کسر خودکار مواد اولیه پیمانکاری بر اساس",
	"Material Transferred for Subcontract": "مواد انتقال‌یافته برای پیمانکاری",
	"Over Transfer Allowance (%)": "حد مجاز انتقال بیش از سفارش (٪)",
	"Percentage you are allowed to transfer more against the quantity ordered. For example: If you have ordered 100 units. and your Allowance is 10% then you are allowed to transfer 110 units.": "درصدی که می‌توانید بیش از مقدار سفارش انتقال دهید. مثلاً اگر ۱۰۰ واحد سفارش داده‌اید و حد مجاز ۱۰٪ است، تا ۱۱۰ واحد قابل انتقال است.",
	"Auto Create Subcontracting Order": "ایجاد خودکار سفارش پیمانکاری",
	# Material Request
	"Purpose": "هدف",
	"Material Transfer": "انتقال کالا",
	"Material Issue": "صدور کالا",
	"Manufacture": "تولید",
	"Customer Provided": "تأمین‌شده توسط مشتری",
	"Required By": "تاریخ نیاز",
	"Get Items From": "دریافت کالاها از",
	"Set Warehouse": "انبار همه ردیف‌ها",
	"Set Source Warehouse": "انبار مبدأ همه ردیف‌ها",
	"Set Target Warehouse": "انبار مقصد همه ردیف‌ها",
	"Source Warehouse": "انبار مبدأ",
	"Target Warehouse": "انبار مقصد",
	"Terms and Conditions Content": "متن شرایط و ضوابط",
	"Reference": "مرجع",
	"Submitted": "ثبت‌شده",
	"Pending": "در انتظار",
	"Ordered": "سفارش داده شده",
	"Issued": "صادر شده",
	"Partially Ordered": "بخشی سفارش داده شده",
	"Partially Received": "بخشی دریافت شده",
	"% Ordered": "٪ سفارش داده شده",
	"% Received": "٪ دریافت شده",
	"Work Order": "دستور تولید",
	"UOM": "واحد",
	"Stock UOM": "واحد انبار",
	"Stock Qty": "مقدار به واحد انبار",
	"Min Order Qty": "حداقل مقدار سفارش",
	"Projected Qty": "مقدار پیش‌بینی‌شده",
	"Actual Qty": "مقدار واقعی",
	"Completed Qty": "مقدار تکمیل‌شده",
	"Received Qty": "مقدار دریافت‌شده",
	"Price List Rate": "نرخ فهرست قیمت",
	"Amount": "مبلغ",
	"Cost Center": "مرکز هزینه",
	"Manufacturer Part Number": "شماره قطعه سازنده",
	"BOM No": "شماره فهرست مواد",
	"Lead Time Date": "تاریخ تأمین",
	"Sales Order Item": "ردیف سفارش فروش",
	"Material Request Plan Item": "ردیف برنامه درخواست کالا",
	"Job Card Item": "ردیف کارت کار",
	"Page Break": "صفحه جدید",
	"Is Purchase Item": "کالای خریدنی",
	"Is Group": "گروهی",
	"All Supplier Groups": "همه گروه‌های تأمین‌کننده",
	"Pharmaceutical": "دارویی",
	# Projects
	"Task": "وظیفه",
	"Project Update": "گزارش پیشرفت پروژه",
	"Timesheet": "برگه زمان کارکرد",
	"Daily Timesheet Summary": "خلاصه روزانه برگه‌های زمان",
	"Project wise Stock Tracking": "پیگیری موجودی به تفکیک پروژه",
	"Delayed Tasks Summary": "خلاصه وظایف معوق",
	"Learn Project Management": "آموزش مدیریت پروژه",
	"Open Projects": "پروژه‌های باز",
	"Projects Settings": "تنظیمات پروژه‌ها",
	"Overdue": "سررسید گذشته",
	# Quality / Support
	"Tree of Procedures": "درخت رویه‌ها",
	"Quality Action": "اقدام کیفی",
	"Issues": "درخواست‌های پشتیبانی",
	"Issue": "درخواست پشتیبانی",
	"Issue Type": "نوع درخواست پشتیبانی",
	"Issue Priority": "اولویت درخواست پشتیبانی",
	"Maintenance Schedule": "برنامه نگهداری",
	"Maintenance Visit": "بازدید نگهداری",
	"Service Level Agreement": "توافق‌نامه سطح خدمات",
	"First Response Time for Issues": "زمان اولین پاسخ به درخواست‌های پشتیبانی",
	# CRM
	"Lead Details": "مشخصات سرنخ",
	"Sales Pipeline Analytics": "تحلیل خط لوله فروش",
	"Prospects Engaged But Not Converted": "مشتریان بالقوه درگیر اما تبدیل‌نشده",
	"First Response Time for Opportunity": "زمان اولین پاسخ به فرصت",
	"Campaign Efficiency": "کارایی کمپین",
	"Lead Owner Efficiency": "کارایی مسئول سرنخ",
	"Masters": "اطلاعات پایه",
	"Appointment": "قرار ملاقات",
	"SMS Center": "مرکز پیامک",
	"SMS Log": "سابقه پیامک",
	"Territory Wise Sales": "فروش به تفکیک منطقه",
	# Manufacturing
	"Downtime Entry": "ثبت توقف تولید",
	"Downtime Analysis": "تحلیل توقف تولید",
	"BOM": "فهرست مواد",
	"Bill of Materials": "فهرست مواد (BOM)",
	"BOM Update Tool": "ابزار به‌روزرسانی فهرست مواد",
	"BOM Comparison Tool": "ابزار مقایسه فهرست مواد",
	"BOM Search": "جستجوی فهرست مواد",
	"BOM Stock Report": "گزارش موجودی فهرست مواد",
	"BOM Operations Time": "زمان عملیات فهرست مواد",
	"BOM Creator": "سازنده فهرست مواد",
	"Manufacturing Settings": "تنظیمات تولید",
	"Workstation": "ایستگاه کاری",
	"Routing": "مسیر تولید",
	"Production Planning Report": "گزارش برنامه‌ریزی تولید",
	"Work Order Summary": "خلاصه دستورهای تولید",
	"Job Card Summary": "خلاصه کارت‌های کار",
	"Production Analytics": "تحلیل تولید",
	"Work Order Consumed Materials": "مواد مصرفی دستور تولید",
	"Learn Manufacturing": "آموزش تولید",
	"Plant Floor": "سالن تولید",
	"Forecasting": "پیش‌بینی",
	# Users / Website / Tools / Settings / Integrations / Build
	"Role Profile": "پروفایل نقش",
	"Module Profile": "پروفایل ماژول",
	"Website Settings": "تنظیمات وب‌سایت",
	"Website Theme": "پوسته وب‌سایت",
	"Website Script": "اسکریپت وب‌سایت",
	"Website Sidebar": "نوار کناری وب‌سایت",
	"Website Slideshow": "اسلایدشوی وب‌سایت",
	"Website Route Meta": "متادیتای مسیر وب‌سایت",
	"Knowledge Base": "پایگاه دانش",
	"Blogger": "نویسنده وبلاگ",
	"Assignment Rule": "قاعده تخصیص",
	"To Do": "کارها",
	"ToDo": "کارها",
	"Files": "فایل‌ها",
	"Export Data": "خروجی داده‌ها",
	"Print Format Builder": "سازنده قالب چاپ",
	"Print Format Builder (New)": "سازنده قالب چاپ (جدید)",
	"Alerts and Notifications": "هشدارها و اعلان‌ها",
	"Auto Email Report": "گزارش ایمیلی خودکار",
	"Email / Notifications": "ایمیل / اعلان‌ها",
	"Workflow Action": "اقدام گردش کار",
	"Global Defaults": "پیش‌فرض‌های عمومی",
	"Backup": "پشتیبان‌گیری",
	"Dropbox Settings": "تنظیمات Dropbox",
	"S3 Backup Settings": "تنظیمات پشتیبان‌گیری S3",
	"Slack Webhook URL": "نشانی Webhook برای Slack",
	"Webhook": "Webhook",
	"Social Login Key": "کلید ورود با شبکه‌های اجتماعی",
	"OAuth Client": "کلاینت OAuth",
	"OAuth Provider Settings": "تنظیمات ارائه‌دهنده OAuth",
	"Views": "نماها",
	"Workspace": "صفحه کار",
	"Packages": "بسته‌ها",
	# Payables / Receivables / Financial Reports
	"Invoicing": "صدور صورتحساب",
	"Payment Reconciliation": "تطبیق پرداخت",
	"Accounts Payable Summary": "خلاصه حساب‌های پرداختنی",
	"Accounts Receivable Summary": "خلاصه حساب‌های دریافتنی",
	"Purchase Register": "دفتر خرید",
	"Item-wise Purchase Register": "دفتر خرید به تفکیک کالا",
	"Sales Register": "دفتر فروش",
	"Item-wise Sales Register": "دفتر فروش به تفکیک کالا",
	"Received Items To Be Billed": "کالاهای دریافتی صورتحساب‌نشده",
	"Delivered Items To Be Billed": "کالاهای تحویلی صورتحساب‌نشده",
	"Supplier Ledger Summary": "خلاصه دفتر تأمین‌کنندگان",
	"Customer Ledger Summary": "خلاصه دفتر مشتریان",
	"Payment Gateway Account": "حساب درگاه پرداخت",
	"Dunning": "مطالبه بدهی",
	"Dunning Type": "نوع مطالبه بدهی",
	"POS Invoice": "فاکتور صندوق فروش",
	"Profit and Loss Statement": "صورت سود و زیان",
	"Consolidated Financial Statement": "صورت‌های مالی تلفیقی",
	"Ledgers": "دفاتر",
	"Trial Balance for Party": "تراز آزمایشی طرف حساب‌ها",
	"Payment Period Based On Invoice Date": "دوره وصول بر اساس تاریخ فاکتور",
	"Sales Payment Summary": "خلاصه دریافت‌های فروش",
	"Address And Contacts": "نشانی و مخاطبان",
}

FORM_TOURS = {
	# Accounts Settings
	"Over Billing Allowance Percentage": "درصد مجاز صورتحساب بیش از سفارش",
	"The percentage by which you can overbill transactions. For example, if the order value is $100 for an Item and percentage here is set as 10% then you are allowed to bill for $110.": "درصدی که می‌توانید بیش از مبلغ سفارش صورتحساب صادر کنید. مثلاً اگر مبلغ سفارش یک کالا ۱۰۰ و این درصد ۱۰ باشد، تا ۱۱۰ قابل صورتحساب است.",
	"Role Allowed to Over Bill": "نقش مجاز به صورتحساب بیش از سفارش",
	"Select the role that is allowed to overbill a transactions.": "نقشی را انتخاب کنید که مجاز است بیش از مبلغ سفارش صورتحساب صادر کند.",
	"If checked, system will unlink the payment against the respective invoice.": "در صورت انتخاب، با لغو فاکتور، پرداخت ثبت‌شده از آن جدا می‌شود.",
	"Similar to the previous option, this unlinks any advance payments made against Purchase/Sales Orders.": "مانند گزینه قبل، پیش‌پرداخت‌های ثبت‌شده برای سفارش‌های خرید و فروش را جدا می‌کند.",
	"Tax category can be set on Addresses. An address can be Shipping or Billing address. Set which addres to select when applying Tax Category.": "دسته‌بندی مالیاتی را می‌توان روی نشانی تعیین کرد. نشانی می‌تواند نشانی ارسال یا صورتحساب باشد؛ مشخص کنید هنگام اعمال دسته‌بندی مالیاتی کدام به کار رود.",
	"Accounts Frozen Upto": "حساب‌ها مسدود تا تاریخ",
	"Freeze accounting transactions up to specified date, nobody can make/modify entry except the specified Role.": "اسناد حسابداری تا این تاریخ مسدود می‌شوند و جز نقش تعیین‌شده، کسی نمی‌تواند سندی ثبت یا ویرایش کند.",
	"Role Allowed to Set Frozen Accounts & Edit Frozen Entries": "نقش مجاز به مسدود کردن حساب‌ها و ویرایش اسناد مسدود",
	"Users with this Role are allowed to set frozen accounts and create/modify accounting entries against frozen accounts.": "کاربران این نقش می‌توانند حساب‌ها را مسدود کنند و روی حساب‌های مسدود سند ثبت یا ویرایش کنند.",
	"Credit Controller": "کنترل‌کننده اعتبار",
	"Select the role that is allowed to submit transactions that exceed credit limits set. The credit limit can be set in the Customer form.": "نقشی را انتخاب کنید که مجاز است تراکنش‌های بیش از سقف اعتبار را ثبت کند. سقف اعتبار در فرم مشتری تعیین می‌شود.",
	# Asset / Asset Category
	"Select Naming Series based on which Asset ID will be generated": "سری شماره‌گذاری را که شناسه دارایی بر اساس آن ساخته می‌شود انتخاب کنید",
	"Select an Asset Item": "کالای دارایی را انتخاب کنید",
	"Select a Location": "مکان را انتخاب کنید",
	"Is Existing Asset?": "دارایی موجود است؟",
	"Check Is Existing Asset": "گزینه «دارایی موجود» را انتخاب کنید",
	"Set Available for use date": "تاریخ آماده بهره‌برداری را وارد کنید",
	"Set Gross purchase amount": "مبلغ ناخالص خرید را وارد کنید",
	"Set Purchase Date": "تاریخ خرید را وارد کنید",
	"Check Calculate Depreciation": "گزینه «محاسبه استهلاک» را انتخاب کنید",
	"Enter depreciation which has already been booked for this asset": "استهلاکی را که تاکنون برای این دارایی ثبت شده وارد کنید",
	"Name Asset category. You can create categories based on Asset Types like Furniture, Property, Electronics etc.": "نام گروه دارایی را وارد کنید. گروه‌ها را بر اساس نوع دارایی بسازید، مانند اثاثه، ساختمان یا تجهیزات الکترونیکی.",
	"Enable CWIP Accounting": "فعال‌سازی حسابداری دارایی در جریان تکمیل",
	"Check to enable Capital Work in Progress accounting": "برای فعال‌سازی حسابداری دارایی در جریان تکمیل انتخاب کنید",
	"Add a row to define Depreciation Method and other details. Note that you can leave Finance Book blank to have it's accounting done in the primary books of accounts.": "یک ردیف برای تعیین روش استهلاک و سایر جزئیات اضافه کنید. اگر دفتر مالی را خالی بگذارید، حسابداری در دفاتر اصلی انجام می‌شود.",
	"Select the Fixed Asset and Depreciation accounts applicable for this Asset Category type": "حساب‌های دارایی ثابت و استهلاک این گروه دارایی را انتخاب کنید",
	# Buying Settings
	"When a Supplier is saved, system generates a unique identity or name for that Supplier which can be used to refer the Supplier in various Buying transactions.": "با ذخیره تأمین‌کننده، سیستم یک شناسه یا نام یکتا برای او می‌سازد که در معاملات خرید به آن ارجاع داده می‌شود.",
	"Configure what should be the default value of Supplier Group when creating a new Supplier.": "گروهی را که هنگام ایجاد تأمین‌کننده جدید به‌طور پیش‌فرض انتخاب می‌شود تعیین کنید.",
	"Item prices will be fetched from this Price List.": "قیمت کالاها از این فهرست قیمت خوانده می‌شود.",
	'If this option is configured "Yes", ERPNext will prevent you from creating a Purchase Invoice or a Purchase Receipt directly without creating a Purchase Order first.': "اگر «بله» باشد، بدون سفارش خرید نمی‌توان فاکتور خرید یا رسید خرید ایجاد کرد.",
	'If this option is configured "Yes", ERPNext will prevent you from creating a Purchase Invoice without creating a Purchase Receipt first.': "اگر «بله» باشد، بدون رسید خرید نمی‌توان فاکتور خرید ایجاد کرد.",
	# Company
	"This is the default currency for this company.": "این ارز پیش‌فرض این شرکت است.",
	"Here, you can add multiple addresses of the company": "در این بخش می‌توانید چند نشانی برای شرکت اضافه کنید",
	"Here, you can set default Accounts, which will ease the creation of accounting entries.": "در این بخش حساب‌های پیش‌فرض را تعیین کنید تا ثبت اسناد حسابداری ساده‌تر شود.",
	"This setting is recommended if you wish to track the real-time stock balance in your books of account. This will allow the creation of a General Ledger entry for every stock transaction.": "اگر می‌خواهید موجودی انبار به‌صورت لحظه‌ای در دفاتر منعکس شود، این تنظیم توصیه می‌شود؛ برای هر تراکنش انبار یک ثبت در دفتر کل ایجاد می‌شود.",
	# Custom Field / DocType
	"Select a Document for which you want the Custom Field": "سندی را که فیلد سفارشی برای آن است انتخاب کنید",
	"Enter a Label for this field": "برچسب این فیلد را وارد کنید",
	"Select an appropriate Field Type that suits your requirements": "نوع فیلد مناسب نیاز خود را انتخاب کنید",
	"Check this to make it a mandatory field": "برای اجباری کردن این فیلد انتخاب کنید",
	"Enter the Full Name of the Customer": "نام کامل مشتری را وارد کنید",
	"Select a Module to which this DocType would belong": "ماژولی را که این نوع سند به آن تعلق دارد انتخاب کنید",
	"Check this to make the DocType as Custom": "برای سفارشی کردن این نوع سند انتخاب کنید",
	"A Field (or a docfield) defines a property of a DocType. You can define the column name, label, datatype and more for DocFields. For instance, a ToDo doctype has fields description, status and priority. These ultimately become columns in the database table tabToDo.": "هر فیلد یکی از ویژگی‌های نوع سند است و نام ستون، برچسب، نوع داده و موارد دیگر آن قابل تعریف است. مثلاً نوع سند «کار» فیلدهای شرح، وضعیت و اولویت دارد که ستون‌های جدول tabToDo در پایگاه داده می‌شوند.",
	# Item
	"Asset Item Code": "کد کالای دارایی",
	"Enter code for Asset Item": "کد کالای دارایی را وارد کنید",
	"Asset Item Name": "نام کالای دارایی",
	"Enter name for Asset Item": "نام کالای دارایی را وارد کنید",
	"Select an Item Group": "گروه کالا را انتخاب کنید",
	"Is this a Fixed Asset?": "دارایی ثابت است؟",
	"Check this field to make this an Asset Item": "برای تبدیل این کالا به کالای دارایی انتخاب کنید",
	"Auto Create Asset on Purchase": "ایجاد خودکار دارایی هنگام خرید",
	"On checking it, the system will create an Asset automatically on purchase": "در صورت انتخاب، با خرید این کالا دارایی به‌طور خودکار ایجاد می‌شود",
	"Select an Asset Category for this Asset Item": "گروه دارایی این کالا را انتخاب کنید",
	"Select a naming series which will be used to create an Asset automatically": "سری شماره‌گذاری دارایی‌هایی را که خودکار ایجاد می‌شوند انتخاب کنید",
	"Enter code for the Item": "کد کالا را وارد کنید",
	"Enter name for the Item": "نام کالا را وارد کنید",
	"Default Unit of Measurement": "واحد اندازه‌گیری پیش‌فرض",
	"This is the default measuring unit that you will use for your product. It could be Nos, Kgs, Meters, etc.": "واحد اندازه‌گیری اصلی کالا، مانند عدد، کیلوگرم یا متر.",
	"When creating an Item, entering a value for this field will automatically create an Item Price at the backend. Entering a value after the Item has been saved will not work. In this case, the Item Price is created from any transactions with the Item.": "اگر هنگام ایجاد کالا این فیلد را پر کنید، قیمت کالا خودکار ساخته می‌شود. پر کردن آن پس از ذخیره کالا اثری ندارد؛ در آن حالت قیمت از تراکنش‌های کالا ساخته می‌شود.",
	# Letter Head
	"Let's name your first Letter Head with your company's name": "نام اولین سربرگ را همان نام شرکت بگذارید",
	"Select the image containing only header part of your letter Head.": "تصویری را انتخاب کنید که فقط بخش بالای سربرگ را دارد.",
	"You can mark the Letter Head as default": "می‌توانید این سربرگ را پیش‌فرض کنید",
	# Material Request
	'The purpose of the material request can be selected here. For now select "Purchase" as the purpose.': "هدف درخواست کالا را اینجا انتخاب کنید. فعلاً «خرید» را انتخاب کنید.",
	'Set the "Required By" date for the materials. This sets the "Required By" date for all the items.': "«تاریخ نیاز» را وارد کنید؛ برای همه ردیف‌های کالا اعمال می‌شود.",
	"Setting the target warehouse sets it for all the items.": "انبار مقصد انتخاب‌شده برای همه ردیف‌های کالا اعمال می‌شود.",
	"Items table": "جدول کالاها",
	"Select an Item code. Item details will be fetched automatically.": "کد کالا را انتخاب کنید؛ مشخصات کالا خودکار پر می‌شود.",
	"Enter the required quantity for the material.": "مقدار مورد نیاز را وارد کنید.",
	# Print Format
	"Doctype": "نوع سند",
	"Select a Doctype for which you want to create a Print Format": "نوع سندی را که قالب چاپ برای آن است انتخاب کنید",
	"You can modify the style of the Print Format from this section": "ظاهر قالب چاپ را در این بخش تغییر دهید",
	"You can add custom css for your Print Format from this section": "CSS سفارشی قالب چاپ را در این بخش وارد کنید",
	"Check this if you want to add custom Jinja Code or JavaScript to your Print Format": "اگر می‌خواهید در قالب چاپ کد Jinja یا JavaScript بنویسید انتخاب کنید",
	"Select the type of Print Format": "نوع قالب چاپ را انتخاب کنید",
	"Enter the code based on the Print Format Type you selected above": "کد را متناسب با نوع قالب چاپ انتخاب‌شده وارد کنید",
	# Purchase Invoice / Purchase Order / Purchase Receipt
	"Select Supplier": "انتخاب تأمین‌کننده",
	"List of Items": "فهرست کالاها",
	"Add items in the table": "کالاها را در جدول اضافه کنید",
	"Select Item": "انتخاب کالا",
	"Select an item": "یک کالا انتخاب کنید",
	"Enter Quantity": "ورود مقدار",
	"Enter the quantity": "مقدار را وارد کنید",
	"Enter Rate": "ورود نرخ",
	"Enter rate of the item": "نرخ کالا را وارد کنید",
	"Select taxes": "انتخاب مالیات‌ها",
	"You can add taxes here": "مالیات‌ها را اینجا اضافه کنید",
	"Items Table": "جدول کالاها",
	"Items to be purchased can be added here.": "کالاهای مورد خرید را اینجا اضافه کنید.",
	"Enter the Item Code.": "کد کالا را وارد کنید.",
	"Select Asset Supplier": "تأمین‌کننده دارایی را انتخاب کنید",
	"Select an Asset Item, Enter rate and quantity": "کالای دارایی را انتخاب و نرخ و مقدار را وارد کنید",
	# Quotation / Sales Invoice / Sales Order
	"Select a customer or lead for whom this quotation is being prepared. Let's select a Customer.": "مشتری یا سرنخی را که پیش‌فاکتور برای اوست انتخاب کنید؛ فعلاً «مشتری» را انتخاب کنید.",
	"Select a specific Customer to whom this quotation will be sent.": "مشتری‌ای را که پیش‌فاکتور برای او ارسال می‌شود انتخاب کنید.",
	"Select an item for which you will be quoting a price.": "کالایی را که برای آن قیمت می‌دهید انتخاب کنید.",
	"You can select pre-populated Sales Taxes and Charges from here.": "الگوی آماده مالیات و هزینه‌های فروش را اینجا انتخاب کنید.",
	"Select Customer": "انتخاب مشتری",
	"Select a customer for whom this invoice is being prepared.": "مشتری‌ای را که فاکتور برای اوست انتخاب کنید.",
	"Select item that you have sold along with quantity and rate.": "کالای فروخته‌شده را همراه با مقدار و نرخ انتخاب کنید.",
	"Select a customer.": "مشتری را انتخاب کنید.",
	"List of items": "فهرست کالاها",
	"You can add items here.": "کالاها را اینجا اضافه کنید.",
	"Select an item.": "یک کالا انتخاب کنید.",
	"Enter quantity.": "مقدار را وارد کنید.",
	"Enter rate of the item.": "نرخ کالا را وارد کنید.",
	"Add Sales Taxes and Charges": "افزودن مالیات و هزینه‌های فروش",
	"You can add sales taxes and charges here.": "مالیات و هزینه‌های فروش را اینجا اضافه کنید.",
	# Sales Taxes and Charges Template
	"A name by which you will identify this template. You can change this later.": "نامی برای شناسایی این الگو؛ بعداً قابل تغییر است.",
	"Company for which this tax template will be applicable": "شرکتی که این الگوی مالیاتی برای آن است",
	"Is this Default Tax Template?": "الگوی مالیاتی پیش‌فرض است؟",
	"Set this template as the default for all sales transactions": "این الگو را برای همه معاملات فروش پیش‌فرض کنید",
	"Taxes Table": "جدول مالیات‌ها",
	"You can add a row for a tax rule here. These rules can be applied on the net total, or can be a flat amount.": "برای هر قاعده مالیاتی یک ردیف اضافه کنید؛ مالیات می‌تواند درصدی از جمع خالص یا مبلغی ثابت باشد.",
	# Selling Settings
	"By default, the Customer Name is set as per the Full Name entered. If you want Customers to be named by a <a href=\"https://docs.erpnext.com/docs/user/manual/en/setting-up/settings/naming-series\" target=\"_blank\">Naming Series</a>. Choose the 'Naming Series' option.": "به‌طور پیش‌فرض نام مشتری همان نام کاملی است که وارد می‌کنید. اگر می‌خواهید مشتریان با <a href=\"https://docs.erpnext.com/docs/user/manual/en/setting-up/settings/naming-series\" target=\"_blank\">سری شماره‌گذاری</a> نام‌گذاری شوند، گزینه «سری شماره‌گذاری» را انتخاب کنید.",
	"Sales Order Required for Sales Invoice & Delivery Note Creation": "الزام سفارش فروش برای ایجاد فاکتور فروش و حواله خروج",
	"If this option is configured 'Yes', ERPNext will prevent you from creating a Sales Invoice or Delivery Note without creating a Sales Order first. This configuration can be overridden for a particular Customer by enabling the 'Allow Sales Invoice Creation Without Sales Order' checkbox in the Customer master.": "اگر «بله» باشد، بدون سفارش فروش نمی‌توان فاکتور فروش یا حواله خروج ایجاد کرد. برای یک مشتری خاص می‌توانید با فعال کردن «اجازه ایجاد فاکتور فروش بدون سفارش فروش» در فرم مشتری، این محدودیت را بردارید.",
	"Delivery Note Required for Sales Invoice Creation": "الزام حواله خروج برای ایجاد فاکتور فروش",
	"If this option is configured 'Yes', ERPNext will prevent you from creating a Sales Invoice without creating a Delivery Note first. This configuration can be overridden for a particular Customer by enabling the 'Allow Sales Invoice Creation Without Delivery Note' checkbox in the Customer master.": "اگر «بله» باشد، بدون حواله خروج نمی‌توان فاکتور فروش ایجاد کرد. برای یک مشتری خاص می‌توانید با فعال کردن «اجازه ایجاد فاکتور فروش بدون حواله خروج» در فرم مشتری، این محدودیت را بردارید.",
	"Configure the default Price List when creating a new Sales transaction. Item prices will be fetched from this Price List.": "فهرست قیمت پیش‌فرض معاملات فروش جدید را تعیین کنید؛ قیمت کالاها از این فهرست خوانده می‌شود.",
	# Stock Entry / Stock Reconciliation / Stock Settings / Warehouse
	"Select the type of Stock Entry to be made. For now, to receive stock into a warehouses select <a href=\"https://docs.erpnext.com/docs/v13/user/manual/en/stock/articles/stock-entry-purpose#2purpose-material-receipt\" target=\"_blank\">Material Receipt.</a>": "نوع سند انبار را انتخاب کنید. فعلاً برای ورود کالا به انبار، <a href=\"https://docs.erpnext.com/docs/v13/user/manual/en/stock/articles/stock-entry-purpose#2purpose-material-receipt\" target=\"_blank\">دریافت کالا</a> را انتخاب کنید.",
	"Select a target warehouse where the stock will be received.": "انبار مقصدی را که کالا به آن وارد می‌شود انتخاب کنید.",
	"Select an item and entry quantity to be delivered.": "کالا و مقدار را انتخاب کنید.",
	"Set Purpose to Opening Stock to set the stock opening balance.": "برای ثبت موجودی افتتاحیه، هدف را «موجودی افتتاحیه» قرار دهید.",
	"Edit the Posting Date by clicking on the Edit Posting Date and Time checkbox below.": "برای تغییر تاریخ ثبت، گزینه «ویرایش تاریخ و زمان ثبت» را در پایین انتخاب کنید.",
	"Select the items for which the opening stock has to be set.": "کالاهایی را که موجودی افتتاحیه دارند انتخاب کنید.",
	"By default, the Item Name is set as per the Item Code entered. If you want Items to be named by a Naming Series choose the 'Naming Series' option.": "به‌طور پیش‌فرض نام کالا همان کد کالاست. اگر می‌خواهید کالاها با سری شماره‌گذاری نام‌گذاری شوند، گزینه «سری شماره‌گذاری» را انتخاب کنید.",
	"Set a Default Warehouse for Inventory Transactions. This will be fetched into the Default Warehouse in the Item master.": "انبار پیش‌فرض تراکنش‌های انبار را تعیین کنید؛ در فرم کالا به‌عنوان انبار پیش‌فرض پر می‌شود.",
	"Choose between FIFO and Moving Average Valuation Methods. Click <a href=\"https://docs.erpnext.com/docs/user/manual/en/stock/articles/item-valuation-fifo-and-moving-average\" target=\"_blank\">here</a> to know more about them.": "روش ارزش‌گذاری FIFO یا میانگین متحرک را انتخاب کنید. برای توضیح بیشتر <a href=\"https://docs.erpnext.com/docs/user/manual/en/stock/articles/item-valuation-fifo-and-moving-average\" target=\"_blank\">اینجا</a> را ببینید.",
	"Select a name for the warehouse. This should reflect its location or purpose.": "نامی برای انبار انتخاب کنید که محل یا کاربرد آن را نشان دهد.",
	"Select an account to set a default account for all transactions with this warehouse.": "حساب پیش‌فرض همه تراکنش‌های این انبار را انتخاب کنید.",
}

ONBOARDING = {
	# ---- Home ----
	("MO:Home", "title"): "سفر خود را با ERPNext آغاز کنید",
	("MO:Home", "subtitle"): "کالا، مشتری، تأمین‌کننده و پیش‌فاکتور",
	("MO:Home", "success_message"): "آماده‌اید که کار با ERPNext را شروع کنید",
	("OS:Create an Item", "title"): "ایجاد کالا",
	("OS:Create an Item", "description"): (
		"# ایجاد کالا\n\n"
		"کالا محصول یا خدمتی است که شرکت شما ارائه می‌کند، یا چیزی که به‌عنوان بخشی از ملزومات یا مواد اولیه می‌خرید.\n\n"
		"کالاها در همه کارهای ERPNext نقش اصلی دارند؛ از صدور صورتحساب و خرید تا مدیریت موجودی. "
		"هر چیزی که می‌خرید یا می‌فروشید، چه محصول فیزیکی و چه خدمت، یک کالاست. "
		"کالا می‌تواند انبارشی، غیرانبارشی، دارای گونه، سریال‌دار، بچ‌دار، دارایی و ... باشد.\n"
	),
	("OS:Create an Item", "action_label"): "ایجاد کالای جدید",
	("OS:Create a Customer", "title"): "ایجاد مشتری",
	("OS:Create a Customer", "description"): (
		"# ایجاد مشتری\n\n"
		"اطلاعات پایه مشتری قلب معاملات فروش شماست. مشتریان در پیش‌فاکتور، سفارش فروش، فاکتور و دریافت‌ها به کار می‌روند. "
		"مشتریان را می‌توان با شماره یا با نام شناسایی کرد (معمولاً بسته به تعداد مشتریان).\n\n"
		"با اطلاعات پایه مشتری می‌توانید موارد زیر را پیگیری کنید:\n"
		" - نشانی‌ها و مخاطبان متعدد مشتری\n"
		" - حساب‌های دریافتنی\n"
		" - سقف و مهلت اعتبار\n"
	),
	("OS:Create a Customer", "action_label"): "ایجاد اولین مشتری",
	("OS:Create Your First Sales Invoice", "title"): "ایجاد اولین فاکتور فروش",
	("OS:Create Your First Sales Invoice", "description"): (
		"# درباره فاکتور فروش\n\n"
		"فاکتور فروش صورتحسابی است که برای مشتری می‌فرستید و مشتری بر اساس آن پرداخت می‌کند. "
		"فاکتور فروش یک سند حسابداری است؛ با ثبت آن، سیستم حساب دریافتنی را به‌روز و درآمد را به حساب مشتری ثبت می‌کند."
	),
	# ---- Accounting ----
	("MO:Accounts", "title"): "حساب‌ها و مالیات‌ها را راه‌اندازی کنیم.",
	("MO:Accounts", "subtitle"): "حساب‌ها، فاکتورها، مالیات و بیشتر.",
	("MO:Accounts", "success_message"): "ماژول حسابداری آماده است!",
	("OS:Chart of Accounts", "title"): "بررسی سرفصل حساب‌ها",
	("OS:Chart of Accounts", "description"): (
		"# سرفصل حساب‌ها\n\n"
		"ERPNext برای هر شرکتی که ایجاد می‌کنید یک سرفصل حساب ساده می‌سازد، اما می‌توانید آن را مطابق نیاز کسب‌وکار و الزامات قانونی تغییر دهید."
	),
	("OS:Chart of Accounts", "action_label"): "آشنایی بیشتر با سرفصل حساب‌ها",
	("OS:Setup Taxes", "description"): (
		"# تنظیم مالیات‌ها\n\n"
		"در ERPNext می‌توانید مالیات‌ها را طوری تنظیم کنید که به‌طور خودکار در معاملات خرید و فروش اعمال شوند. "
		"می‌توانید آن‌ها را به‌صورت کلی یا حتی روی هر کالا تنظیم کنید. مالیات‌های بیشتر کشورها از پیش تنظیم شده‌اند."
	),
	("OS:Setup Taxes", "action_label"): "مدیریت الگوهای مالیات فروش",
	("OS:Accounts Settings", "description"): (
		"# تنظیمات حسابداری\n\n"
		"امکانات حسابداری ERPNext مطابق نیاز کسب‌وکار شما قابل تنظیم است. در تنظیمات حسابداری برخی ترجیحات خود را تعیین می‌کنید، مانند:\n\n"
		" - سقف اعتبار و صدور صورتحساب بیش از سفارش\n"
		" - ترجیحات مالیاتی\n"
		" - ترجیحات حسابداری معوق\n"
	),
	("OS:Accounts Settings", "action_label"): "مرور سریع تنظیمات حسابداری",
	("OS:Cost Centers for Report and Budgeting", "title"): "مراکز هزینه برای بودجه‌بندی و تحلیل",
	("OS:Cost Centers for Report and Budgeting", "description"): (
		"# مراکز هزینه برای بودجه‌بندی و تحلیل\n\n"
		"دفاتر حسابداری شما بر اساس الزامات قانونی تنظیم می‌شوند، اما برای نیازهای گزارش‌گیری و بودجه‌بندی شرکت می‌توانید مرکز هزینه و ابعاد حسابداری تعریف کنید.\n\n"
		"برای آشنایی با اینکه <b>[مرکز هزینه](https://docs.erpnext.com/docs/v13/user/manual/en/accounts/cost-center)</b> و "
		"<b>[ابعاد حسابداری](https://docs.erpnext.com/docs/v13/user/manual/en/accounts/accounting-dimensions)</b> "
		"چگونه گزارش‌های تحلیلی پیشرفته مالی در اختیارتان می‌گذارند، اینجا را ببینید."
	),
	("OS:Cost Centers for Report and Budgeting", "action_label"): "نمایش درخت مراکز هزینه",
	("OS:Create Your First Purchase Invoice", "title"): "ایجاد اولین فاکتور خرید",
	("OS:Create Your First Purchase Invoice", "description"): (
		"# ایجاد اولین فاکتور خرید\n\n"
		"فاکتور خرید صورتحسابی است که از تأمین‌کننده برای کالا یا خدمات تحویل‌شده به شرکت شما دریافت می‌شود. "
		"با فاکتور خرید، حساب‌های پرداختنی را پیگیری و پرداخت‌ها را در برابر آن ثبت می‌کنید.\n\n"
		"فاکتور خرید را می‌توان از روی سفارش خرید یا رسید خرید هم ایجاد کرد."
	),
	("OS:Create Your First Purchase Invoice", "action_label"): "ایجاد اولین فاکتور خرید",
	("OS:Updating Opening Balances", "title"): "ثبت مانده‌های افتتاحیه",
	("OS:Updating Opening Balances", "description"): (
		"# ثبت مانده‌های افتتاحیه\n\n"
		"پس از بستن حساب‌ها در نرم‌افزار حسابداری قبلی، همان مانده‌ها را به‌عنوان افتتاحیه در حساب‌های ترازنامه ERPNext ثبت کنید. "
		"به این ترتیب صورت‌های مالی کامل سال‌های آینده را از ERPNext می‌گیرید و می‌توانید فوراً سیستم حسابداری موازی را کنار بگذارید."
	),
	("OS:Updating Opening Balances", "action_label"): "آموزش ثبت مانده‌های افتتاحیه",
	("OS:Financial Statements", "description"): (
		"# صورت‌های مالی\n\n"
		"در ERPNext گزارش‌های مالی مهمی مانند [ترازنامه] و [سود و زیان] را با یک کلیک دریافت می‌کنید. "
		"می‌توانید گزارش را برای دوره‌های مختلف اجرا کنید و نمودارهای تحلیلی بر اساس داده‌های آن رسم کنید. "
		"برای گزارش‌های بیشتر، بخش‌های صورت‌های مالی، دفتر کل و گزارش‌های سودآوری را ببینید.\n\n"
		"<b>[گزارش‌های حسابداری](https://docs.erpnext.com/docs/v13/user/manual/en/accounts/accounting-reports)</b>"
	),
	# ---- Buying ----
	("MO:Buying", "title"): "ماژول خرید را راه‌اندازی کنیم.",
	("MO:Buying", "subtitle"): "محصولات، خریدها، تحلیل و بیشتر.",
	("MO:Buying", "success_message"): "ماژول خرید آماده است!",
	("OS:Introduction to Buying", "description"): (
		"# تنظیمات خرید\n\n\n"
		"امکانات ماژول خرید کاملاً مطابق نیاز کسب‌وکار شما قابل تنظیم است. در تنظیمات خرید ترجیحات زیر را تعیین می‌کنید:\n\n"
		"- نام‌گذاری تأمین‌کنندگان و مقادیر پیش‌فرض\n"
		"- ترجیحات صورتحساب و ارسال در معاملات خرید\n\n\n"
	),
	("OS:Introduction to Buying", "action_label"): "مرور چند تنظیم خرید",
	("OS:Create a Material Request", "title"): "پیگیری درخواست کالا",
	("OS:Create a Material Request", "description"): (
		"# پیگیری درخواست کالا\n\n\n"
		"درخواست کالا (درخواست خرید) سندی است که نیاز به مجموعه‌ای از کالاها یا خدمات را برای اهدافی مانند تهیه، انتقال، صدور یا تولید مشخص می‌کند. "
		"پس از تأیید درخواست، مدیر خرید می‌تواند اقدام بعدی را انجام دهد؛ مثلاً از تأمین‌کننده استعلام قیمت بگیرد یا مستقیماً به تأمین‌کننده مشخصی سفارش دهد.\n\n"
	),
	("OS:Create a Material Request", "action_label"): "ایجاد اولین درخواست کالا",
	("OS:Create your first Purchase Order", "title"): "ایجاد اولین سفارش خرید",
	("OS:Create your first Purchase Order", "description"): (
		"# ایجاد اولین سفارش خرید\n\n"
		"سفارش خرید قلب معاملات خرید شماست. در ERPNext سفارش خرید را می‌توان از روی درخواست کالا و استعلام قیمت تأمین‌کننده نیز ایجاد کرد. "
		"سفارش خرید به رسید خرید و فاکتور خرید متصل است و دید کاملی از معاملات خرید به شما می‌دهد.\n\n"
	),
	("OS:Create your first Purchase Order", "action_label"): "ایجاد اولین سفارش خرید",
	# ---- Selling ----
	("MO:Selling", "title"): "ماژول فروش را راه‌اندازی کنیم.",
	("MO:Selling", "subtitle"): "محصولات، فروش، تحلیل و بیشتر.",
	("MO:Selling", "success_message"): "ماژول فروش آماده است!",
	("OS:Selling Settings", "description"): (
		"# تنظیمات فروش\n\n"
		"امکانات ماژول‌های CRM و فروش مطابق نیاز کسب‌وکار شما قابل تنظیم است. در تنظیمات فروش ترجیحات زیر را تعیین می‌کنید:\n"
		" - نام‌گذاری مشتریان و مقادیر پیش‌فرض\n"
		" - ترجیحات صورتحساب و ارسال در معاملات فروش\n"
	),
	("OS:Selling Settings", "action_label"): "مرور تنظیمات فروش",
	("OS:Sales Order", "description"): (
		"# سفارش فروش\n\n"
		"سفارش فروش تأیید سفارش مشتری است و به آن پیش‌فاکتور هم گفته می‌شود.\n\n"
		"سفارش فروش قلب معاملات فروش و خرید شماست و به حواله خروج، فاکتور فروش، درخواست کالا و معاملات نگهداری متصل است. "
		"با سفارش فروش می‌توانید انجام کامل معامله با مشتری را پیگیری کنید."
	),
	("OS:Sales Order", "action_label"): "تبدیل اولین پیش‌فاکتور به سفارش فروش",
	# ---- CRM ----
	("MO:CRM", "title"): "CRM را راه‌اندازی کنیم.",
	("MO:CRM", "subtitle"): "سرنخ، فرصت، مشتری و بیشتر.",
	("MO:CRM", "success_message"): "ماژول CRM آماده است!",
	("OS:Create and Send Quotation", "title"): "ایجاد و ارسال پیش‌فاکتور",
	("OS:CRM Settings", "description"): (
		"# تنظیمات CRM\n\n"
		"امکانات ماژول CRM مطابق نیاز کسب‌وکار شما قابل تنظیم است. در تنظیمات CRM ترجیحات زیر را تعیین می‌کنید:\n"
		"- کمپین\n"
		"- سرنخ\n"
		"- فرصت\n"
		"- پیش‌فاکتور"
	),
	("OS:Introduction to CRM", "title"): "آشنایی با CRM",
	# ---- Stock ----
	("MO:Stock", "title"): "ماژول انبار را راه‌اندازی کنیم.",
	("MO:Stock", "subtitle"): "موجودی، انبارها، تحلیل و بیشتر.",
	("MO:Stock", "success_message"): "ماژول انبار آماده است!",
	("OS:Stock Settings", "title"): "بررسی تنظیمات انبار",
	("OS:Stock Settings", "description"): (
		"# بررسی تنظیمات انبار\n\n"
		"امکانات ماژول انبار ERPNext مطابق نیاز کسب‌وکار شما قابل تنظیم است. در تنظیمات انبار ترجیحات زیر را تعیین می‌کنید:\n"
		"- مقادیر پیش‌فرض کالا و قیمت‌گذاری\n"
		"- روش پیش‌فرض ارزش‌گذاری موجودی\n"
		"- ترجیحات سریال و بچ کالا\n"
		"- حد مجاز دریافت و تحویل بیش از سفارش"
	),
	("OS:Stock Settings", "action_label"): "مرور تنظیمات انبار",
	("OS:Create a Warehouse", "title"): "ایجاد انبار",
	("OS:Create a Warehouse", "description"): (
		"# ایجاد انبار\n"
		"انبار محل یا فروشگاهی است که موجودی کالا را در آن نگهداری می‌کنید و از آنجا کالا را از اشخاص مختلف دریافت یا به آن‌ها تحویل می‌دهید.\n\n"
		"در ERPNext انبارها به‌صورت درختی تعریف می‌شوند تا محل و زیرمحل کالا قابل پیگیری باشد. "
		"همچنین می‌توانید هر انبار را به یک حساب حسابداری متصل کنید تا ارزش لحظه‌ای موجودی آن انبار در حساب منعکس شود."
	),
	("OS:Create a Warehouse", "action_label"): "ایجاد اولین انبار",
	("OS:Create a Stock Entry", "title"): "مدیریت جابه‌جایی موجودی",
	("OS:Create a Stock Entry", "description"): (
		"# مدیریت جابه‌جایی موجودی\n"
		"با ثبت انبار، جابه‌جایی موجودی را برای اهدافی مانند انتقال، دریافت، صدور، بسته‌بندی مجدد و ... ثبت می‌کنید. "
		"برای جلوگیری از سرقت و کسری، می‌توانید مطمئن شوید که هر جابه‌جایی کالا با یک سند ثبت انبار در ERPNext انجام می‌شود.\n\n"
		"برای آشنایی سریع با حالت‌های مختلف ثبت انبار، [*این ویدیو*](https://www.youtube.com/watch?v=Njt107hlY3I) را ببینید."
	),
	("OS:Create a Stock Entry", "action_label"): "ایجاد سند انتقال کالا",
	("OS:Check Stock Ledger Report", "title"): "بررسی دفتر انبار",
	("OS:Check Stock Ledger Report", "description"): (
		"# بررسی گزارش‌های انبار\n"
		"بر اساس تراکنش‌های انبار، ERPNext گزارش‌های آماده بسیاری مانند دفتر انبار، موجودی انبار، مقدار پیش‌بینی‌شده و تحلیل سن موجودی در اختیارتان می‌گذارد."
	),
	("OS:Stock Opening Balance", "title"): "ثبت موجودی افتتاحیه",
	("OS:Stock Opening Balance", "description"): (
		"# ثبت موجودی افتتاحیه\n"
		"سندی برای ثبت موجودی هر کالا در هر انبار در تاریخ و ساعتی است که کار با ERPNext را آغاز می‌کنید.\n\n"
		"پس از ثبت موجودی افتتاحیه، می‌توانید تراکنش‌هایی مانند تولید و تحویل کالا را ثبت کنید که از این موجودی مصرف می‌کنند."
	),
	("OS:Stock Opening Balance", "action_label"): "ایجاد سند موجودی افتتاحیه",
	# ---- Assets ----
	("MO:Assets", "title"): "ماژول دارایی‌ها را راه‌اندازی کنیم.",
	("MO:Assets", "subtitle"): "دارایی‌ها، استهلاک، تعمیرات و بیشتر.",
	("MO:Assets", "success_message"): "ماژول دارایی‌ها آماده است!",
	("OS:Fixed Asset Accounts", "title"): "بررسی حساب‌های دارایی ثابت",
	("OS:Fixed Asset Accounts", "description"): (
		"# حساب‌های دارایی ثابت\n\n"
		"همراه با شرکت، مجموعه‌ای از حساب‌های دارایی ثابت از پیش تنظیم می‌شود. برای اینکه تراکنش‌های دارایی اسناد حسابداری درستی ایجاد کنند، "
		"حساب‌های زیر را مطابق نیاز کسب‌وکار خود بررسی و تنظیم کنید.\n"
		" - حساب‌های دارایی ثابت\n"
		" - استهلاک انباشته\n"
		" - حساب دارایی در جریان تکمیل\n"
		" - حساب هزینه استهلاک"
	),
	("OS:Fixed Asset Accounts", "action_label"): "مرور سرفصل حساب‌ها برای بررسی تنظیمات",
	("OS:Asset Category", "title"): "تعریف گروه دارایی",
	("OS:Asset Category", "description"): (
		"# گروه دارایی\n\n"
		"گروه دارایی، دارایی‌های مختلف شرکت را دسته‌بندی می‌کند.\n\n"
		"گروه‌ها را بر اساس نوع دارایی بسازید. برای مثال، همه رایانه‌ها و لپ‌تاپ‌ها می‌توانند در گروهی به نام «تجهیزات الکترونیکی» باشند "
		"و برای اثاثه هم گروه جداگانه‌ای بسازید. برای هر گروه می‌توانید ویژگی‌های پیش‌فرض را تعیین کنید، مانند:\n"
		" - روش و مدت استهلاک\n"
		" - حساب دارایی ثابت\n"
		" - حساب استهلاک\n"
	),
	("OS:Asset Category", "action_label"): "بررسی گروه‌های دارایی موجود",
	("OS:Asset Item", "title"): "ایجاد کالای دارایی",
	("OS:Asset Item", "description"): (
		"# کالای دارایی\n\n"
		"کالاهای دارایی بر اساس گروه دارایی ایجاد می‌شوند و برای هر گروه می‌توانید یک یا چند کالا بسازید. "
		"خرید و فروش دارایی از طریق کالای دارایی انجام می‌شود. "
	),
	("OS:Asset Item", "action_label"): "ایجاد کالای دارایی جدید",
	("OS:Asset Purchase", "title"): "خرید دارایی",
	("OS:Asset Purchase", "description"): (
		"# خرید دارایی\n\n"
		"خرید دارایی با چرخه استاندارد خرید انجام می‌شود. اگر «دارایی در جریان تکمیل» در گروه دارایی فعال باشد، "
		"دارایی به محض ایجاد رسید خرید ساخته می‌شود. می‌توانید سریعاً یک رسید خرید برای دارایی بسازید و اثر آن را در دفاتر ببینید."
	),
	("OS:Asset Purchase", "action_label"): "ایجاد رسید خرید",
	("OS:Existing Asset", "title"): "افزودن دارایی موجود",
	("OS:Existing Asset", "description"): (
		"# افزودن دارایی موجود\n\n"
		"اگر تازه کار با ERPNext را آغاز کرده‌اید، باید دارایی‌هایی را که از قبل دارید وارد کنید. "
		"آن‌ها را به‌عنوان دارایی ثابت موجود اضافه کنید. توجه کنید که باید جداگانه یک سند حسابداری برای ثبت مانده افتتاحیه حساب دارایی ثابت ثبت کنید."
	),
	("OS:Existing Asset", "action_label"): "افزودن دارایی موجود",
	# ---- Manufacturing ----
	("MO:Manufacturing", "title"): "ماژول تولید را راه‌اندازی کنیم.",
	("MO:Manufacturing", "subtitle"): "محصولات، مواد اولیه، فهرست مواد، دستور تولید و بیشتر.",
	("MO:Manufacturing", "success_message"): "ماژول تولید آماده است!",
	("OS:Create Product", "title"): "کالاهای ساخته‌شده",
	("OS:Create Product", "description"): (
		"# ایجاد کالا برای فهرست مواد\n\n"
		"یکی از پیش‌نیازهای فهرست مواد (BOM)، تعریف مواد اولیه، قطعات نیمه‌ساخته و کالاهای ساخته‌شده است. "
		"پس از تعریف این کالاها می‌توانید به فهرست مواد بروید که از کالاها و مسیر تولید تشکیل می‌شود.\n"
	),
	("OS:Create BOM", "description"): (
		"# ایجاد فهرست مواد\n\n"
		"فهرست مواد (BOM) فهرستی از کالاها و قطعات نیمه‌ساخته به همراه مقادیر لازم برای تولید یک کالاست.\n\n"
		"فهرست مواد برآورد بهای تولید را نیز ارائه می‌دهد: هزینه مواد اولیه بر اساس ارزش‌گذاری و هزینه عملیات بر اساس مسیر تولید محاسبه می‌شود و بهای کل به دست می‌آید."
	),
	("OS:Create BOM", "action_label"): "ایجاد اولین فهرست مواد",
	("OS:Work Order", "description"): (
		"# ایجاد دستور تولید\n\n"
		"دستور تولید را مدیر تولید به کارگاه می‌دهد تا تولید مقدار مشخصی از یک کالا آغاز شود. "
		"دستور تولید شامل کالای تولیدی، فهرست مواد آن، مقدار تولید و عملیات است.\n\n"
		"با دستور تولید وضعیت‌های مختلف تولید را پیگیری می‌کنید، مانند:\n\n"
		"- صدور مواد اولیه به کارگاه\n"
		"- پیشرفت هر ایستگاه کاری با کارت کار\n"
		"- مقدار تولیدشده در برابر دستور تولید\n"
	),
	("OS:Work Order", "action_label"): "ایجاد اولین دستور تولید",
	("OS:Workstation", "description"): (
		"# ایجاد ایستگاه کاری\n\n"
		"ایستگاه کاری اطلاعات محلی را که عملیات در آن انجام می‌شود نگه می‌دارد. برای مثال، اگر ده چرخ خیاطی دارید، هر چرخ یک ایستگاه کاری است."
	),
	("OS:Workstation", "action_label"): "ایجاد ایستگاه کاری",
	("OS:Routing", "description"): (
		"# تنظیم مسیر تولید\n\n"
		"مسیر تولید همه عملیات را به همراه شرح، نرخ ساعتی، زمان عملیات، اندازه بچ و ... نگه می‌دارد. "
		"در ادامه ببینید چگونه الگوی مسیر تولید را برای انتخاب سریع در فهرست مواد بسازید."
	),
	("OS:Routing", "action_label"): "راهنمای تنظیم مسیر تولید",
	("OS:Operation", "description"): (
		"# ایجاد عملیات\n\n"
		"عملیات هر کار تولیدی است که روی مواد اولیه انجام می‌شود تا در مسیر تولید پیش برود. "
		"برای مثال در تولید پوشاک، عملیاتی مانند برش پارچه، دوخت و شستشو تعریف می‌کنید."
	),
	("OS:Operation", "action_label"): "ایجاد عملیات",
	("OS:Explore Manufacturing Settings", "description"): (
		"# بررسی تنظیمات تولید\n\n"
		"امکانات ماژول تولید ERPNext مطابق نیاز کسب‌وکار شما قابل تنظیم است. در تنظیمات تولید ترجیحات زیر را تعیین می‌کنید:\n\n"
		"- برنامه‌ریزی ظرفیت برای تخصیص کارها به ایستگاه‌ها\n"
		"- مصرف مواد اولیه بر اساس فهرست مواد یا مصرف واقعی\n"
		"- مقادیر پیش‌فرض و حد مجاز تولید بیش از سفارش\n"
	),
	("OS:Explore Manufacturing Settings", "action_label"): "مرور تنظیمات تولید",
	("OS:Production Planning", "title"): "برنامه‌ریزی تولید",
	("OS:Production Planning", "description"): (
		"# برنامه‌ریزی تولید چگونه کار می‌کند\n\n"
		"برنامه تولید به برنامه‌ریزی تولید و مواد برای کالاهای در دست تولید کمک می‌کند. "
		"این کالاها می‌توانند از طریق سفارش فروش (برای مشتری) یا درخواست کالا (داخلی) تعهد شوند.\n"
	),
	("OS:Production Planning", "action_label"): "آشنایی بیشتر با برنامه‌ریزی تولید",
	# ---- Settings / Tools / Website ----
	("OS:Role Permissions", "title"): "دسترسی محدود برای کاربر",
	("OS:Role Permissions", "description"): (
		"در ERPNext می‌توانید کارکنان را به‌عنوان کاربر اضافه کنید و دسترسی محدود به آن‌ها بدهید. "
		"ابزارهای مجوز نقش و مجوز کاربر امکان تعریف قواعدی را می‌دهند که دسترسی کاربر به اطلاعات پایه و تراکنش‌ها را محدود می‌کنند."
	),
	("OS:Custom Field", "description"): (
		"هر فرم در ERPNext مجموعه‌ای از فیلدهای استاندارد دارد. اگر باید اطلاعاتی را ثبت کنید که فیلد استانداردی برای آن نیست، فیلد سفارشی اضافه کنید.\n\n"
		"پس از افزودن فیلدهای سفارشی، می‌توانید از آن‌ها در گزارش‌ها و نمودارهای تحلیلی هم استفاده کنید.\n"
	),
	("OS:Naming Series", "title"): "تنظیم سری شماره‌گذاری",
	("OS:Naming Series", "description"): (
		"هر سند در ERPNext می‌تواند شناسه یکتایی با پیشوند تعریف‌شده داشته باشد. "
		"هر سند پیشوند پیش‌فرضی دارد، اما می‌توانید با ابزار سری شماره‌گذاری و قاعده نام‌گذاری اسناد آن را تغییر دهید.\n"
	),
	("OS:Report Builder", "description"): (
		"در هر ماژول گزارش‌های آماده بسیاری وجود دارد؛ از صورت‌های مالی تا تحلیل فروش و خرید و گزارش‌های انبار. "
		"اگر گزارشی که لازم دارید آماده نیست، می‌توانید با گرفتن داده از جدول‌های مختلف ERPNext گزارش سفارشی بسازید.\n"
	),
	("OS:Workflows", "title"): "تنظیم گردش کار تأیید",
	("OS:Create Blogger", "title"): "ایجاد نویسنده وبلاگ",
}
