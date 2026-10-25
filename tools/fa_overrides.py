"""Persian overrides merged into erpnext_iran/translations/fa.csv by update_translations.py.

ONBOARDING: ERPNext's onboarding texts (Module Onboarding / Onboarding Step records). They
live in database records, so ERPNext's own fa.po has none of them. Keys are (record, field)
and the English source is read from the site when regenerating.

CORRECTIONS: strings ERPNext/Frappe already translate, but wrongly (wrong word, reversed word
order, missing half-space) or inconsistently - "Item" must always be «کالا».
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
