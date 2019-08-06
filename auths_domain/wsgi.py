from app import current_app

application = current_app

if __name__ == '__main__':
    application.run(debug=current_app.app.config.get('DEBUG', False))
