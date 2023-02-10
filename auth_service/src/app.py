from src.core.security import SecureFlask

# Create app
app = SecureFlask(__name__)
app.config['DEBUG'] = True
