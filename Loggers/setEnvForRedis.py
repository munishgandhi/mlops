from dotenv import load_dotenv
import os
load_dotenv()

def set_redis_url():
    if os.environ["ENVIRONMENT"] == "dev":
        return os.environ["REDIS_URL_DEV"]
    if os.environ["ENVIRONMENT"] == "staging":
        return "redis://redis_db_staging"
    if os.environ["ENVIRONMENT"] == "prod":
        return "prod in development"
    raise ValueError("Unsupported environment")

