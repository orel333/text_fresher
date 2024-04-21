import os

LOCAL_DIR: os.PathLike = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR: os.PathLike = os.path.join(LOCAL_DIR, 'logs')
SOURCE_DIR: os.PathLike = os.path.join(LOCAL_DIR, 'source')
RESULT_DIR: os.PathLike = os.path.join(LOCAL_DIR, 'result')


def make_dir_if_needed(dir_name: os.PathLike) -> None:
    """Добавляет папку, если её нет."""
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
