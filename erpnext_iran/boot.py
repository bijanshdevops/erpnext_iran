from erpnext_iran.utils.settings import get_settings


def boot_session(bootinfo):
	settings = get_settings()
	bootinfo.erpnext_iran = {
		"jalali_display": settings.get("jalali_display") or "Off",
		"persian_digits": settings.get("persian_digits") or 0,
	}
