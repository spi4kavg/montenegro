from app import app, db
from app.models import User


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    user = User('admin', 'admin', True)
    db.session.add(user)
    db.session.commit()