import re
"""El primer diccionario mapea números (del '0' al '9') a sus equivalentes 
en palabras en español (por ejemplo, '1' se convierte en "uno").
El siguiente mapea ciertos caracteres especiales (como @, #, &, etc.) a 
palabras en español que describen esos símbolos (por ejemplo, @ se convierte en "arroba")."""
numbers_to_words = {
    '0': 'cero', '1': 'uno', '2': 'dos', '3': 'tres', '4': 'cuatro',
    '5': 'cinco', '6': 'seis', '7': 'siete', '8': 'ocho', '9': 'nueve'
}

special_characters = {
    '@': 'arroba', '#': 'numeral', '$': 'dólar', '%': 'por ciento',
    '&': 'y', '*': 'asterisco'
}

"""La siguiente función toma un texto como entrada y lo recorre, 
caracter por caracter, buscando números o caracteres especiales.
Primero define un patrón usando expresiones regulares (re), 
para buscar números y los caracteres especiales definidos en los diccionarios.
El bucle se encarga de reemplazar los caracteres y números, por las palabras
definidas en los diccionarios. 
Finalmente une todo y lo retorna como una cadena de texto.
"""

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