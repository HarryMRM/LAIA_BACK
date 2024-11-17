from cryptography.fernet import Fernet # Importacion correcta

data_1 = "niebla"
data_2 = "niebla"

# key = Fernet.generate_key()
key = b'YH00ls871JDGYoVtkxwIk4-q6TWLNDtLACWphp15olk='

fernet = Fernet(key)

encdata_1 = fernet.encrypt(data_1.encode())
encdata_2 = fernet.encrypt(data_2.encode())

decdata_1 = fernet.decrypt(encdata_1).decode()
decdata_2 = fernet.decrypt(encdata_2).decode()

print("Comparacion: ", True if decdata_1 == decdata_2 else False)