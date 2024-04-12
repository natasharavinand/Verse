from os import environ, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
    CORS_HEADERS = 'Content-Type, Authorization, Origin, x-csrf-token' 
    CORS_METHODS = 'GET, HEAD, POST, PATCH, DELETE, OPTIONS' 
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:5000']