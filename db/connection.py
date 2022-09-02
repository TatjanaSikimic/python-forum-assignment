from sqlalchemy import create_engine


# TODO: Add proper engine configuration, using dotenv or environment variables
engine = create_engine('driver://username:pass@url:port/db')


# TODO: Add session creation using the engine above
