"""
Function module.
"""
from django.http import HttpResponse


def convert_txt(shop_list):
    """
    Converts the shopping list
    to a text file and returns it
    as an HTTP response for download.
    """

    file_name = 'shopping_list.txt'
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
