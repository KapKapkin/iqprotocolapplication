from django import template
import pymorphy3

register = template.Library()

morph = pymorphy3.MorphAnalyzer()


@register.simple_tag
def change_case(string, case):
    result = ' '.join(morph.parse(word)[0].inflect(
        case).word for word in string.split())
    return result
