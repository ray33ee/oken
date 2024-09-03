
# Override tempfile._mkstemp_inner and tempfile.mkdtemp
# Override builtins.open
# Shutil copying looks like it works via builtins.open, so no changes needed. However from python 3.8 we have 'Platform-dependent efficient copy operations' which might mean open is not used. see 'https://docs.python.org/3/library/shutil.html'
#    So we must override copy, use the default open, and implement own inverse, then restore the modified open after
# Override shutil.move
# Override shutil.rmtree
# Add logging and debug logging to builtins.open so we can see what and when we open

import overrides


import inverses
import zipfile
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


with zipfile.ZipFile("spam3.zip", "w") as fh:
    fh.write("eggs.txt")

print(inverses.inverse_list)
