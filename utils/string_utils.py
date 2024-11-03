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
    '@': 'arroba', '%': 'por ciento', '&': 'y', '(': '', ')': ''
}

common_terms = {
    'M.I.': 'Maestra en Ingeniería',
    'Dr.': 'Doctor',
    'Ext.': 'Extensión',
    'teléfono': 'teléfono',
    'correo': 'correo electrónico',
}

domain_terms = {
    'uabc.edu.mx': 'u a b c punto e d u punto m x'
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
    # Eliminar símbolos de Markdown
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Eliminar **texto**
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Eliminar *texto*
    
    # Patrón para buscar números, caracteres especiales y términos comunes
    pattern = re.compile(r'uabc\.edu\.mx|[0-9@%&]|M\.I\.|Dr\.|Ext\.|¡|!')

    # Función para reemplazar con base en los diccionarios
    def replace_match(match):
        match_str = match.group()
        if match_str in domain_terms:
            return domain_terms[match_str]
        elif match_str in numbers_to_words:
            return numbers_to_words[match_str]
        elif match_str in special_characters:
            return special_characters[match_str]
        elif match_str in common_terms:
            return common_terms[match_str]
        else:
            return match_str  # Devolver el símbolo si no está en los diccionarios

    # Reemplazo usando sub
    result = pattern.sub(replace_match, text)

    # Eliminar los símbolos no deseados directamente del texto
    result = result.replace('#', '').replace('+', '').replace('-', '').replace('*', '').replace('$', '')

    # Retornar el texto procesado
    return result