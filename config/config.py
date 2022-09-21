import os

APP_ENV = os.getenv('APP_ENV', 'development')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'python-forum-assignment')
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'python-forum-assignment-test')
RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
PUBLISH_QUEUE = os.getenv('PUBLISH_QUEUE', 'test_publish_queue')
CONSUME_QUEUE = os.getenv('CONSUME_QUEUE', 'test_consume_queue')

