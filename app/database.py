from argon2 import PasswordHasher
from sqlmodel import SQLModel, Session, create_engine, select

from .config import settings
from .models import Role, User

engine = create_engine(settings.database_url)
ph = PasswordHasher()


def create_db():
    SQLModel.metadata.create_all(engine)


def seed_admin():
    if not settings.admin_username or not settings.admin_password:
        return
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == settings.admin_username)
        ).first()
        if not user:
            user = User(
                username=settings.admin_username,
                hashed_password=ph.hash(settings.admin_password),
                role=Role.ADMIN,
            )
            session.add(user)
        else:
            user.role = Role.ADMIN
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session
