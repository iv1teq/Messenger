import dotenv 
import os

dotenv.load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

#APP_PASSWORD

APP_PASSWORD = os.getenv("APP_PASSWORD")