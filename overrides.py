# This file contains a set of functions that replace other library functions like open, copy, etc.

import os
import builtins
import io
import inverses
import logging

logger = logging.getLogger(__name__)

_created_tmp_paths = {}

def _new_mkdtemp(suffix=None, prefix=None, dir=None):
    pass

def _new_mkstemp_inner(dir, pre, suf, flags, output_type):
    pass
def _is_temp_path(path):
    # Returns if the path is in a temporary folder. If true, no inverses are used to destroy any created files in the target machine

    # First we see if the entry is in _created_tmp_paths

    # Then we see if the entry is in a few other locations that can contain temporary folders under windows (see _candidate_tempdir_list in tempfile for a list of locations) :

    # If all attempts fail, we assume the path is not in a temporary location

    return False

_open = builtins.open

def _new_open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, openr=None):
    print("Overide open")

    logger.debug(f"Override Open({repr(file)}, {repr(mode)})")

    # Check if the path is a temp path (use _is_temp_path)
    # Check if the mode is read only (use is not writable())
    # Check if the mode creates a new file or not (see if the file existed before open is called)
    already_exists = os.path.isfile(file)

    fh = _open(file, mode, buffering, encoding, errors, newline, closefd, openr)

    writable = fh.writable()

    is_temp = _is_temp_path(file)

    # If the file is writable and not temporary, produce an inverse
    if writable and not is_temp:
        if already_exists:
            # If the file already exists then the inverse is to restore the version before the changes
            fh.close()

            with _open(file, "rb") as bfh:
                contents = bfh.read()
                inverses.inverse_list.append(inverses.RestoreFile(file, contents))

            fh = _open(file, mode, buffering, encoding, errors, newline, closefd, openr)
        else:
            # If a new file is created, the inverse is to delete
            inverses.inverse_list.append(inverses.Delete(file))

    return fh

builtins.open = _new_open
io.open = _new_open