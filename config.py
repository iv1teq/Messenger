import dotenv
import os
dotenv.load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")