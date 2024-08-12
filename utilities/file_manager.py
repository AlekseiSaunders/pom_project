# file_manager.py

import os
from .utils import logger
from .config import FILE_UPLOAD_DIR


class FileManager:
    """A class for uploading files"""

    @staticmethod
    def upload_file(file_input, file_name: str) -> bool:

        """
        Uploads a file using a pre-located file input element
        :param file_input: WebElement, the file input element
        :param file_name: str, name of the file to be uploaded
        :return:
        """
        try:
            # Construct the full file path using FILE_UPLOAD_DIR and file_name
            file_path = os.path.join(FILE_UPLOAD_DIR, file_name)

            # Get the absolute path of the file you want to upload
            abs_file_path = os.path.abspath(file_path)

            # Use the send_keys() method to set the file path
            file_input.send_keys(abs_file_path)
            logger.info(f"Successfully uploaded file: {file_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to upload fle {file_name}: {str(e)}")
            return False
