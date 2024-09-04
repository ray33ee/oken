# This file contains a set of functions that replace other library functions like open, copy, etc.

import os
import builtins
import io
import shutil

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
    logger.debug(f"Override Open({repr(file)}, {repr(mode)})...")

    # Check if the path is a temp path (use _is_temp_path)
    # Check if the mode is read only (use is not writable())
    # Check if the mode creates a new file or not (see if the file existed before open is called)
    already_exists = os.path.isfile(file)

    fh = _open(file, mode, buffering, encoding, errors, newline, closefd, openr)

    logger.debug(f"Success.")

    writable = fh.writable()

    is_temp = _is_temp_path(file)

    # If the file is writable and not temporary, produce an inverse
    if writable and not is_temp:
        if already_exists:
            # If the file already exists then the inverse is to restore the version before the changes
            fh.close()

            inverses.inverse_list.append(inverses.RestoreFile(file))

            fh = _open(file, mode, buffering, encoding, errors, newline, closefd, openr)
        else:
            # If a new file is created, the inverse is to delete
            inverses.inverse_list.append(inverses.Remove(file))

    return fh

builtins.open = _new_open
io.open = _new_open


_mkdir = os.mkdir

def _new_mkdir(path, mode=0o777, dir_fd=None):
    logger.debug(f"Override mkdir({repr(path)})...")

    r = _mkdir(path, mode, dir_fd=dir_fd)

    logger.debug(f"Success.")

    inverses.inverse_list.append(inverses.Rmdir(path))

    return r

os.mkdir = _new_mkdir

_remove = os.remove

def _new_remove(path, dir_fd=None):
    logger.debug(f"Override remove({repr(path)})...")

    restore = inverses.RestoreFile(path)

    r = _remove(path, dir_fd=dir_fd)

    logger.debug(f"Success.")

    inverses.inverse_list.append(restore)

    return r

os.remove = _new_remove
os.unlink = _new_remove

_rmdir = os.rmdir

def _new_rmdir(path, dir_fd=None):
    logger.debug(f"Override rmdir({repr(path)})...")

    r = _rmdir(path, dir_fd=dir_fd)

    logger.debug(f"Success.")

    inverses.inverse_list.append(inverses.Mkdir(path))

    return r

os.rmdir = _new_rmdir

_copyfile = shutil.copyfile

# We have to use our own implementation for copy and cannot rely on builtins.open as shutils may not always
# use builtins.open and may use another platform dependent function instead
def _new_copyfile(src, dst, follow_symlinks=True):
    logger.debug(f"Override copyfile({repr(src)}, {repr(dst)})...")

    # We suspend replace builtins.open with the original then restore later
    builtins.open = _open
    io.open = _open

    already_exists = os.path.isfile(dst)

    is_temp = _is_temp_path(dst)

    r = _copyfile(src, dst, follow_symlinks=follow_symlinks)

    logger.debug(f"Success.")

    if not is_temp:
        if already_exists:
            inverses.inverse_list.append(inverses.RestoreFile(dst))
        else:
            inverses.inverse_list.append(inverses.Remove(dst))

    builtins.open = _new_open
    io.open = _new_open

    return r

shutil.copyfile = _new_copyfile

_copy2 = shutil.copy2

# We have to use our own implementation for copy and cannot rely on builtins.open as shutils may not always
# use builtins.open and may use another platform dependent function instead
def _new_copy2(src, dst, follow_symlinks=True):
    logger.debug(f"Override copy2({repr(src)}, {repr(dst)})...")

    already_exists = os.path.isfile(dst)

    is_temp = _is_temp_path(dst)

    r = _copy2(src, dst, follow_symlinks=follow_symlinks)

    logger.debug(f"Success.")

    if not is_temp:
        if already_exists:
            inverses.inverse_list.append(inverses.RestoreFile(dst))
        else:
            inverses.inverse_list.append(inverses.Remove(dst))

    return r

shutil.copy2 = _new_copy2

_rename = os.rename

def _new_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
    logger.debug(f"Override rename({repr(src)}, {repr(dst)})...")

    r = _rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

    logger.debug(f"Success.")

    print("noe")

    inverses.inverse_list.append(inverses.Move(dst, src))

    return r

os.rename = _new_rename



# The following functions defined in shutil take copy2 as a default arg. However this is the old copy2, so we reimplement here

_move = shutil.move

def _new_move(src, dst, copy_function=shutil.copy2):
    return _move(src, dst, copy_function)

shutil.move = _new_move

_copytree = shutil.copytree

def _new_copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False):
    return _copytree(src, dst, symlinks=symlinks, ignore=ignore, copy_function=copy_function, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)

shutil.move = _new_move

