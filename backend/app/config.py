"""Application configuration."""
import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://127.0.0.1:27017/supplychain'

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not os.environ.get('MONGO_URI'):
            return False, "MONGO_URI environment variable is not set. Please configure MongoDB Atlas and set MONGO_URI in Render dashboard."
        return True, None

