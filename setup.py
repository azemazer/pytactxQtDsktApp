from distutils.core import setup # Need this to handle modules
import py2exe 
setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [{'script': "script.py"}],
    zipfile = None,
)