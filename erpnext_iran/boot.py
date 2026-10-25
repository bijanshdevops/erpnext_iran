from erpnext_iran.utils.settings import get_settings

DEFAULT_PARTNER_LOGO = "/assets/erpnext_iran/images/greenlanco-logo.png"
DEFAULT_PARTNER_NAME = "فانوس سبز ارتباطات"


def boot_session(bootinfo):
	settings = get_settings()
	bootinfo.erpnext_iran = {
		"jalali_display": settings.get("jalali_display") or "Off",
		"persian_digits": settings.get("persian_digits") or 0,
		"persian_digits_everywhere": settings.get("persian_digits_everywhere") or 0,
	}


def update_website_context(context):
	"""Partner logo for the desk loading screen (templates/includes/splash_screen.html)."""
	settings = get_settings()
	if settings.show_partner_logo:
		context["ir_partner_logo"] = settings.partner_logo or DEFAULT_PARTNER_LOGO
		context["ir_partner_name"] = DEFAULT_PARTNER_NAME if not settings.partner_logo else ""
