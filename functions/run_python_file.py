import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_wd = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_wd, file_path))
        
        valid_target_path = os.path.commonpath([abs_wd, target_path]) == abs_wd
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_path.endswith(".py"):
           return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_path]
        
        # FIX 1: Only extend the command list if args is actually a list
        if args:
            command.extend(args)
            
        output = subprocess.run(command, text=True, timeout=30, cwd=working_directory, capture_output=True)
        output_str = ""
        
        if output.returncode != 0:
            output_str = f'{output_str}Process exited with code {output.returncode}\n'
            
        # FIX 2: Check if the strings are empty, not if they are None (and fixed the typo)
        if not output.stdout and not output.stderr:
            output_str = f'{output_str}No output produced\n'
        else:
            output_str = f'{output_str}STDOUT: {output.stdout}\nSTDERR: {output.stderr}'

        return output_str

    except Exception as except_msg:
        return f'Error: {except_msg}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs python file(script) with optional arguments given",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to be read, relative to working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="arguments to be given to python file(script)",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    ),
)