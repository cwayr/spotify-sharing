import os
from app import app

app.config.from_object('config.developmentConfig')

print('test database uri:', os.environ.get('TEST_DATABASE_URL'))

print('env:', app.config['ENV'])

