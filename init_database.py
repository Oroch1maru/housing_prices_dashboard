from app.services.database_service import init_db, SessionLocal, User
from app.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_demo_user()->None:
    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(User.username == "demo_user").first()

        if existing_user:
            logger.info("Demo user already exists")
            return

        demo_user = User(
            username="demo_user",
            hashed_password=get_password_hash("demo_password"),
            is_active=True
        )

        db.add(demo_user)
        db.commit()

        logger.info("Demo user created successfully")
        logger.info("Username: demo_user")
        logger.info("Password: demo_password")

    except Exception as e:
        logger.error(f"Error creating demo user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized")

    logger.info("Creating demo user...")
    create_demo_user()

    logger.info("Setup complete!")