""" Runs the project tests. This does path related tomfoolery, and is designed to be run 
from the project root folder. """
import os
import pathlib
import sys
import pytest

sys.path.append(os.path.join(pathlib.Path.cwd(), 'src'))
os.chdir( pathlib.Path.cwd() / 'Tests' )


pytest.main()
