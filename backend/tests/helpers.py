import string
import random
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile


def generate_channel_name() -> str:
    """Returns a new channel name for test purposes"""
    return f"specific.inmemory!{''.join(random.choice(string.ascii_letters) for i in range(12))}"


def temporary_image_file() -> SimpleUploadedFile:
    file = tempfile.NamedTemporaryFile(suffix=".jpg")
    return SimpleUploadedFile(name=file.name, content=file.read())
