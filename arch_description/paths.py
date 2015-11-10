import os
import sys

if getattr(sys, 'frozen', False):
    # The application is frozen
    maindir = os.path.dirname(sys.executable)
    templdir = maindir
    datadir = maindir
    os.environ['PYPANDOC_PANDOC'] = os.path.join(maindir, 'pandoc.exe')
else:
    # The application is not frozen
    maindir = os.path.dirname(__file__)
    templdir = os.path.join(maindir, 'templates')

datadir = os.path.join(maindir, 'data')

if not os.path.exists(datadir):
    os.makedirs(datadir)
