"""
Auxiliary function module.
"""
from django.conf import settings
from django.http import HttpResponse


def convert_txt(shop_list):
    """
    Gреобразует список покупок `shop_list`
    в текстовый файл и возвращает его
     в виде HTTP-ответа для скачивания.
    """

    file_name = settings.SHOPPING_CART_FILE_NAME
    lines = []
    for ing in shop_list:
        name = ing['ingredient__name']
        measurement_unit = ing['ingredient__measurement_unit']
        amount = ing['ingredient_total']
        lines.append(f'{name} ({measurement_unit}) - {amount}')
    lines.append('\nFoodGram Service')
    lines.append('   (＠＾◡＾)')
    content = '\n'.join(lines)
    content_type = 'text/plain,charset=utf8'
    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response
