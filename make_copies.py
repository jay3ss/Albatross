import os
import shutil


def backup_py_files(
    root_dir: str,
    file_ext: str = ".py",
    new_ext: str = "_backup.py",
    topdown: bool = True
) -> None:
    """
    Backup .py files in a directory and its immediate subdirectories.

    Args:
        root_dir (str): The root directory to start crawling from.
        file_ext (str, optional): The file extension to filter for. Defaults to
        ".py".
        new_ext (str, optional): The new file extension for the backup files.
        Defaults to "_backup.py".
        topdown (bool, optional): Whether to start from the top directory and
        descend down. Defaults to True.
    """
    # get the file name with extension
    # adapted from: https://stackoverflow.com/a/64263838
    script_path = __file__.rsplit("/", 1)[1]
    for dirpath, _, filenames in os.walk(root_dir, topdown=topdown):
        for filename in filenames:
            if filename.endswith(file_ext):
                src_path = os.path.join(dirpath, filename)
                if not script_path == src_path:
                    dst_filename = filename.replace(file_ext, new_ext)
                    dst_path = os.path.join(dirpath, dst_filename)
                    shutil.copy2(src_path, dst_path)
                    print(f'Copied {src_path} to {dst_path}')


if __name__ == "__main__":
    print(__file__.rsplit("/", 1)[1])
    # backup_py_files(root_dir=".", file_ext=".py", new_ext="_backup.py", topdown=True)
