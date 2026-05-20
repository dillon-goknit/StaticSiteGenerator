import os
import shutil


def copy_directory(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    _copy_contents(source, destination)


def _copy_contents(source: str, destination: str) -> None:
    for entry in os.listdir(source):
        src_path = os.path.join(source, entry)
        dst_path = os.path.join(destination, entry)
        if os.path.isfile(src_path):
            print(f"copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            _copy_contents(src_path, dst_path)
