import re

numbers_to_words = {
    '0': 'cero', '1': 'uno', '2': 'dos', '3': 'tres', '4': 'cuatro',
    '5': 'cinco', '6': 'seis', '7': 'siete', '8': 'ocho', '9': 'nueve'
}

special_characters = {
    '@': 'arroba', '#': 'numeral', '$': 'dólar', '%': 'por ciento',
    '&': 'y', '*': 'asterisco'
}

def convert_text(text):
    result = []
    pattern = re.compile(r'[0-9@#$%&*]')
    for char in text:
        if char in numbers_to_words:
            result.append(numbers_to_words[char])
        elif char in special_characters:
            result.append(special_characters[char])
        else:
            result.append(char)
    return ''.join(result)