from dotenv import load_dotenv
import os 
load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
USERNAME = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE_NAME = os.environ.get('DB_NAME')
DATABASE_URI = f"postgresql+asyncpg://{USERNAME}:{PASSWORD}@{DB_HOST}:5432/{DATABASE_NAME}"

# URL queue type (options: 'database', 'memory', 'redis')
URL_QUEUE_TYPE = 'redis'  # Choose your preferred queue implementation

# Redis configuration (if URL_QUEUE_TYPE is set to 'redis')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

# Maximum concurrent requests
MAX_CONCURRENT_REQUESTS = 10

# Rate limit delay (seconds) between requests
RATE_LIMIT_DELAY = 1

# Mobile User-agent string for the crawler
USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36'