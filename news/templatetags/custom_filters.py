# shukach_social/templatetags/custom_filters.py
from django import template


register = template.Library()


@register.filter
def first_sentence(text):
    # text = text.replace('\n', '.')
    sentences = text.split('\n')
    if sentences:
        return sentences[0] # + '.'
    return ''


@register.filter
def news_trunkated(text):
    if len(text) > 512:
        return " ".join(text[:512].split(" ")[0:-1]) + "..."
    else:
        return text


@register.filter
def news_paragraphed(text):
    return text.replace('\n', '<br>')


@register.filter
def number_splitted(number):
    reversed_str = str(number)[::-1]
    return " ".join([reversed_str[i:i + 3] for i in range(0, len(reversed_str), 3)])[::-1]


@register.filter
def replace(value, arg):
    try:
        old_value, new_value = arg.split(',')
        return value.replace(old_value, new_value)
    except ValueError:
        return value  # або поверніть значення за замовчуванням, якщо потрібно
