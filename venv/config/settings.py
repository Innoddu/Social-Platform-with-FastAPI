from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
import secrets
import string



load_dotenv()

# Generate a random string of 32 characters
JWT_SECRET_KEY = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
# print(JWT_SECRET_KEY)

# Define your OAuth2 security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define your JWT secret key
JWT_SECRET_KEY = "YER4wJcAEUIbDLCzmORvxOyXLEANvzc0"