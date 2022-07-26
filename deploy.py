#!/usr/bin/env python
import re
import subprocess
import os

ROOT_DIR = os.path.dirname(__file__)
PYPROJECT_TOML_PATH = os.path.join(ROOT_DIR, "pyproject.toml")

if __name__ == "__main__":
    # Replace version
    p = re.compile(r"version = \"(?P<version>.*?)\"")
    toml = open(PYPROJECT_TOML_PATH).read()
    m = re.search(p, toml)
    version = m.group("version")
    split_versions = version.split(".")
    split_versions[-1] = str(int(split_versions[-1]) + 1)
    new_version = ".".join(split_versions)

    new_toml = re.sub(version, new_version, toml)
    open(PYPROJECT_TOML_PATH, "wt").write(new_toml)

    # Export requirements.txt
    subprocess.run(
        "cd test_project && poetry export --without-hashes -o requirements.txt",
        shell=True,
    )
    # Remove old archives
    subprocess.run("rm -rf dist", shell=True)
    # Generating distribution archives
    subprocess.run("python -m build", shell=True)
    # Upload the distribution archives
    subprocess.run("twine upload dist/*", shell=True)
