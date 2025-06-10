import re

def calculator(a, b, operator):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == 'x':
        return a * b
    elif operator == '/':
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError("Invalid operator")

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # Memeriksa huruf besar
        return False
    if not re.search(r"[a-z]", password):  # Memeriksa huruf kecil
        return False
    if not re.search(r"[0-9]", password):  # Memeriksa angka
        return False
    if not re.search(r"[!@#$%^&*()]", password):  # Memeriksa karakter khusus
        return False
    return True