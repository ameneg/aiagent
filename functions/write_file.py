import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_wd = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_target_dir = os.path.commonpath([abs_wd, target_path]) == abs_wd
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as except_msg:
        return f'Error: {except_msg}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites content into file given by the filepath",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be read, relative to working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write into the file"
            )
        },
        required=["file_path", "content"]
    ),
)