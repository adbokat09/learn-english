from app import create_app

# if __name__ == '__main__':
#     from app.config.db import db
#     from app.word.models import *
#     app = create_app()
#     with app.app_context():
#         db.create_all()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)