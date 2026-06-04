import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_wd = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_wd, directory))
        valid_target_dir = os.path.commonpath([abs_wd, target_dir]) == abs_wd
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            output = ""
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir, item)
                output = (
                    output + "- " + item + ": file_size=" + str(os.path.getsize(item_path)) + " bytes, is_dir="
                    + str(os.path.isdir(item_path)) + "\n"
                )
            return output

    except Exception as except_msg:
        return f'Error: {except_msg}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

