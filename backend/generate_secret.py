import os
from django.core.management.utils import get_random_secret_key

# Generate a new secret key
secret_key = get_random_secret_key()

# Update or create .env file
with open('.env', 'w') as f:
    f.write(f"SECRET_KEY={secret_key}\n")
    f.write("DEBUG=True\n")

print(f"✅ Generated new secret key and updated .env file")
print(f"Key: {secret_key}")