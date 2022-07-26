#!/usr/bin/env python
import subprocess
import os

ROOT_DIR = os.path.dirname(__file__)

if __name__ == '__main__':
    # Export requirements.txt
    subprocess.run('cd test_project && poetry export --without-hashes -o requirements.txt', shell=True)
    # Remove old archives
    subprocess.run('rm -rf dist', shell=True)
    # Generating distribution archives
    subprocess.run('python -m build', shell=True)
    # Upload the distribution archives
    subprocess.run('twine upload dist/*', shell=True)
