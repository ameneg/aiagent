import os

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
            try:
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

    except Exception as except_msg:
        return f'Error: {except_msg}'
