import re

# Чистит строку от спец. символов
def clear_text(text, modes):
    # Аргумент modes получает режим работы функции. modes - список, можно передовать несколько режимов
    # strip - обрезать лишние пробелы
    # specials - удалить спецсимволы
    # line breaks - удалить лишние переводы строк
    # full - применить все режимы
    text_cl = ''

    if any(mode == 'line breaks' or mode == 'full' for mode in modes):
        for char in text:
            if char=='\n':
                pass
            else:
                text_cl += char

    if any(mode == 'strip' or mode == 'full' for mode in modes):
        if text_cl:
            text_cl.strip()
        else:
            text_cl = text.strip()

    if any(mode == 'specials' or mode == 'full' for mode in modes):
        if text_cl:
            text_cl = re.sub('\W+',' ', text_cl)
        else:
            text_cl = re.sub('\W+',' ', text)

    return text_cl