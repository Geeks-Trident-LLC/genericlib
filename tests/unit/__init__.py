import tempfile


def get_temp_file():
    _, tmp_file_name = tempfile.mkstemp()
    return tmp_file_name


def get_temp_dir():
    tmp_dir = tempfile.mkdtemp()
    return tmp_dir

