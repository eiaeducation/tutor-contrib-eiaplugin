"""Setup script for the eiaplugin plugin for Tutor."""

import io
import os

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    """
    Load the README file.
    """
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    """
    Load the __about__.py file.
    """
    about = {}
    with io.open(
        os.path.join(HERE, "eiaplugin", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-eiaplugin",
    version=ABOUT["__version__"],
    url="https://github.com/eiaeducation/tutor-contrib-eiaplugin",
    project_urls={
        "Code": "https://github.com/eiaeducation/tutor-contrib-eiaplugin",
        "Issue tracker": "https://github.com/eiaeducation/tutor-contrib-eiaplugin/issues",
    },
    license="AGPLv3",
    author="Lawrence McDaniel",
    author_email="lpm0073@gmail.com",
    description="eiaplugin plugin for Tutor",
    long_description=load_readme(),
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["tutor>=18.0.0,<19.0.0","python-dotenv"],
    extras_require={
        "dev": [
            "tutor[dev]>=18.0.0,<19.0.0",
        ]
    },
    entry_points={
        "tutor.plugin.v1": [
            "eiaplugin = eiaplugin.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
