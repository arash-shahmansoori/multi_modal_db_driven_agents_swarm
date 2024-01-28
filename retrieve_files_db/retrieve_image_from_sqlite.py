import io

from PIL import Image
from sqlalchemy.orm.session import Session

from configs import GeneratedImage


def retrieve_image_sqlite(
    GenImage: GeneratedImage, session: Session, image_id: int
) -> None:
    # Query the image by its ID
    imagemodel = session.query(GenImage).filter(GenImage.id == image_id).first()
    if imagemodel:
        # Convert binary data to a bytes object and use PIL to display
        image_data = io.BytesIO(imagemodel.image_data)
        image = Image.open(image_data)
    else:
        print("Image not found.")
        image = None
    return image
