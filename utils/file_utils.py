#Primero se importa base64 la cual codifica datos en base64.
import base64

#Se define la llamada de funcion y recibe como parametro la ruta del archivo.
#Se abre y se lee el archivo de forma binaria, los codifica en base64
# despues regresa la cadena de bytes mediante b64encode y esta se pasa a cadena de texto
# mediante decode(' utf-8')
def convert_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')