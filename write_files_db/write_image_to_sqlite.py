from typing import NoReturn

from sqlalchemy.orm.session import Session

from db_tables import GeneratedImage


def write_image_sqlite(session: Session, image: GeneratedImage | None) -> NoReturn:
    if image:
        # Save image to the database
        session.add(image)
        session.commit()
        print(f"Image saved to SQLAlchemy database with ID: {image.id}")
