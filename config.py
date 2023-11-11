import os


# For a production app, you should use a secret key set in the environment
# The recommended way to generate a 64char secret key is to run:
# python -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

# When deploying, set in the environment to the PostgreSQL URL
# SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')

# Render external connection string
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://projectmanager2_user:JDqT7lQELj86YnVQj1iyQgZBetg4cbaV@dpg-cl7r15n6e7vc739vuu70-a.frankfurt-postgres.render.com/projectmanager2')

# # local connection string
# SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:N1c0laM3365@localhost/projectmanager2')
