from auths_domain.core import app

if __name__ == '__main__':
    app.run(debug=app.app.config.get('DEBUG', False))
