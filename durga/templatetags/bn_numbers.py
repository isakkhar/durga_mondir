# durga_mondir/templatetags/bn_numbers.py

from django import template

register = template.Library()

EN_TO_BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

@register.filter
def bn_number(value):
    return str(value).translate(EN_TO_BN)
