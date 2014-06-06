import contextlib
import hashlib
import logging
import os
import shutil
import sys
import tempfile
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from datetime import datetime


def get_project_base_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

log = logging.getLogger("scratchtobat")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

fh = logging.FileHandler(os.path.join(tempfile.gettempdir(), "scratchtobat-{}.log".format(datetime.now().isoformat().replace(":", "_"))))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)

log.debug("Logging initialized")

APPLICATION_NAME = "Scratch to Catrobat Converter"


def isList(obj):
    return isinstance(obj, list)


def get_test_resources_path():
    return os.path.join(get_project_base_path(), "test", "res")


def get_test_project_path(project_folder):
    return os.path.join(get_test_resources_path(), "sb2", project_folder)


def get_test_project_unpacked_file(sb2_file):
    return os.path.join(get_test_resources_path(), "sb2_unpacked", sb2_file)


def get_testoutput_path(output_path):
    output_path = os.path.join(get_project_base_path(), "testoutput", "catrobat", output_path)
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    return output_path


class Data(object):
    pass


@contextlib.contextmanager
def capture_stdout():
    old = sys.stdout
    capturer = StringIO()
    sys.stdout = capturer
    data = Data()
    yield data
    sys.stdout = old
    data.result = capturer.getvalue()


class ScratchtobatError(Exception):
    pass


def md5_hash(input_path):
    with open(input_path, "rb") as fp:
        return hashlib.md5(fp.read()).hexdigest()


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


# WORKAROUND: as shutil.rmtree fails on Windows with Jython for unknown reason with OSError (unlink())
def rmtree(path):
    assert os.path.exists(path)
    retry_count = 0
    while True:
        try:
            shutil.rmtree(path)
            if retry_count != 0:
                log.warning("Number of retries until path delete success: %d", retry_count)
            break
        except OSError:
            retry_count += 1
