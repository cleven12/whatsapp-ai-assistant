from app.models import User, Message
from app import db

def test_create_user_and_message(app):
    with app.app_context():
        u = User(whatsapp_number="+15551234567")
        db.session.add(u)
        db.session.commit()

        assert u.id is not None

        m = Message(user_id=u.id, role="user", content="Hello bot")
        db.session.add(m)
        db.session.commit()

        assert len(u.messages) == 1
        assert u.messages[0].content == "Hello bot"
