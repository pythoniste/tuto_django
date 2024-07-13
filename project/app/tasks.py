from random import choice
from itertools import repeat
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from celery import shared_task

from .models import Player


@shared_task
def create_avatar(instance_pk: int):
    # Get the Player object
    instance = Player.objects.get(pk=instance_pk)

    # Set image size
    img_size = (128, 128)
    # Set random dark background color (font is white)
    bgcolor = "#" + "".join((f() for f in repeat(lambda: choice([str(x) for x in range(8)]), 3)))

    # Get user initials
    user = instance.user
    match user.first_name, user.last_name, user.username:
        case first_name, last_name, _ if first_name and last_name:
            initials = first_name[0] + last_name[0]
        case first_name, "" | None, _ if first_name:
            initials = first_name[:2]
        case "" | None, last_name, _ if last_name:
            initials = last_name[:2]
        case _:
            initials = user.username[:2]

    # Create the image
    img = Image.new('RGB', img_size, color=bgcolor)
    draw = ImageDraw.Draw(img)

    # Set the font and boundaries
    font = ImageFont.load_default(size=64)

    # Get the text position (up left corner)
    bounding_box = font.getbbox(initials)
    text_width = bounding_box[2] - bounding_box[0]
    text_height = bounding_box[3] - bounding_box[1]
    position = ((img_size[0] - text_width) / 2, (img_size[1] - text_height) / 2)

    # Write initials
    draw.text(position, initials, fill="white", font=font)

    # Save the avatar
    with BytesIO() as image_io:
        img.save(image_io, format='PNG')
        image_io.seek(0)
        instance.avatar.save(f"generated_avatar_{initials}", image_io)
    instance.save()
