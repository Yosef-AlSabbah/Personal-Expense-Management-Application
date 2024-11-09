from os.path import splitext, join
from uuid import uuid4


def get_unique_profile_pic_path(instance, filename):
    """
    Generates a unique file path for the uploaded profile picture.
    The filename will be generated based on a UUID to ensure uniqueness.
    """
    # Extract the file extension from the original filename
    ext = splitext(filename)[1]
    # Generate a unique filename using UUID
    unique_filename = f"{uuid4()}{ext}"
    # Construct the path where the file will be saved
    return join('profile_pics', unique_filename)