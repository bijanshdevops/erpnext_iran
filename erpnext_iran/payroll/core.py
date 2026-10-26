"""Iranian payroll arithmetic. Pure Python; amounts in rial, rounded to whole rials.

Social security (تأمین اجتماعی): the employee pays 7% and the employer 23% (20% + 3% unemployment)
of the insurable wage, capped at a ceiling of a multiple of the daily minimum wage per day.
Salary tax (مالیات حقوق) is progressive over monthly brackets, on taxable pay less the exempt
2/7 of the employee's insurance share.
"""

import datetime


def rial(value):
	return int(round(float(value or 0)))


def insurance(insurable, ceiling, employee_rate, employer_rate):
	"""(base, employee share, employer share) for an insurable wage under the ceiling."""
	base = min(rial(insurable), rial(ceiling)) if ceiling else rial(insurable)
	return base, rial(base * float(employee_rate) / 100), rial(base * float(employer_rate) / 100)


def salary_tax(taxable, brackets):
	"""Progressive tax. brackets: [(from amount, rate %)], the first usually (0, 0) for the
	exempt part; each rate applies to the part of taxable above its "from" up to the next one."""
	taxable = rial(taxable)
	ordered = sorted((rial(start), float(rate)) for start, rate in brackets)
	tax = 0.0
	for i, (start, rate) in enumerate(ordered):
		end = ordered[i + 1][0] if i + 1 < len(ordered) else None
		if taxable <= start:
			break
		tax += (min(taxable, end) - start if end is not None else taxable - start) * rate / 100
	return rial(tax)


def taxable_income(taxable_earnings, employee_insurance, exempt_insurance_fraction):
	"""Taxable pay less the exempt part (usually 2/7) of the employee's insurance."""
	return max(rial(taxable_earnings) - rial(employee_insurance * float(exempt_insurance_fraction)), 0)


def years_of_service(joining_date, on_date):
	"""Full years worked at the workplace on on_date (for the seniority increment)."""
	if not joining_date:
		return 0
	joining = joining_date if isinstance(joining_date, datetime.date) else datetime.date.fromisoformat(str(joining_date))
	on = on_date if isinstance(on_date, datetime.date) else datetime.date.fromisoformat(str(on_date))
	years = on.year - joining.year - ((on.month, on.day) < (joining.month, joining.day))
	return max(years, 0)
