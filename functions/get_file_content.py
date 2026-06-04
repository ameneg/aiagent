import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_wd = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_target_dir = os.path.commonpath([abs_wd, target_path]) == abs_wd
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content

    except Exception as except_msg:
        return f'Error: {except_msg}'