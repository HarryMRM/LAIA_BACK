import resend
import os
from dotenv import load_dotenv
import random
load_dotenv()

API_KEY = os.getenv('RESEND_API_KEY')
resend.api_key = API_KEY

LENGTH = 8
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def generate_code():
    code = []
    for i in range(LENGTH):
        code.append(random.choice(CHARS))
    return ''.join(code)

def send_code(code = generate_code()):
    body = f"""
        <div style="background-color: #e1f5fe71; font-size: 30px">
            <h1>
                <span style="color: #0f9ed5"
                    >Lamentamos que perdieras tu contraseña 😢</span
                >
            </h1>
            <h2>
                <span style="color: #9c27b0; font-size: 30px">
                    Pero no te preocupes, puedes recuperar tu cuenta escribiendo
                    el siguiente código de validación y siguiendo los pasos en
                    LAIA app 😸:
                </span>
            </h2>
            <code>
                <h1>
                    <span style="color: #e91e63; font-size: 70px">{code}</span>
                </h1>
            </code>
        </div>
    """

    return resend.Emails.send({
        "from": "laia-app@resend.dev",
        "to": "a1176033@uabc.edu.mx",
        "subject": "Recuperar contraseña",
        "html": body
    })

if __name__ == '__main__':
    r = send_code(generate_code())
    print(f"""Email Sent:\n{r}""")
