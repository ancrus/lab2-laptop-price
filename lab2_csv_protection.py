import pandas as pd
import re
from cryptography.fernet import Fernet

# Загружаем CSV
df = pd.read_csv("Laptop_price.csv")

# Проверка на CSV-инъекции 
def check_csv_injection(value):
    if isinstance(value, str):
        return bool(re.match(r'^\s*[=+\-@]', value))
    return False

df['csv_injection'] = df.apply(lambda row: any(check_csv_injection(str(cell)) for cell in row), axis=1)

# Проверка на SQL-инъекции 
def check_sql_injection(value):
    if isinstance(value, str):
        return bool(re.search(r"(--|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bDROP\b)", value, re.IGNORECASE))
    return False

df['sql_injection'] = df.apply(lambda row: any(check_sql_injection(str(cell)) for cell in row), axis=1)

#  Шифрование RAM_Size 
key = Fernet.generate_key()
fernet = Fernet(key)

def encrypt_ram(value):
    try:
        return fernet.encrypt(str(value).encode()).decode()
    except Exception:
        return None

df['Encrypted_RAM'] = df['RAM_Size'].apply(encrypt_ram)

#  Расшифровка RAM 
def decrypt_ram(encrypted_value):
    try:
        return fernet.decrypt(encrypted_value.encode()).decode()
    except Exception:
        return None

print("Первые 5 расшифрованных значений RAM:")
for val in df['Encrypted_RAM'].head(5):
    print(decrypt_ram(val))

#  Сохраняем результат 
df.to_csv("output_protected.csv", index=False)
