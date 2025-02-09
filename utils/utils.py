import os
import shutil

class DirectoryManager:
    @staticmethod
    def clear_directories(directories):
        """Clear contents of specified directories"""
        for directory in directories:
            if os.path.exists(directory):
                try:
                    for filename in os.listdir(directory):
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                except Exception as e:
                    raise Exception(f"Error clearing {directory}: {e}")

    @staticmethod
    def ensure_directories_exist(directories):
        """Ensure all required directories exist"""
        for directory in directories:
            os.makedirs(directory, exist_ok=True)