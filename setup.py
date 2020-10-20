import setuptools
from setuptools.command.install import install
from distutils.command.build_ext import build_ext
from distutils.core import Extension

import shutil
import os


def cp_libs():
    os.makedirs('lilang/lib', exist_ok=True)
    shutil.copy('lib/io.li', 'lilang/lib/io.li')


class LilangBuildExt(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        filename_parts = filename.split('.')
        return f'{filename_parts[0]}.{filename_parts[-1]}'


class LilangInstall(install):
    def run(self):
        install.run(self)
        cp_libs()


iolib = Extension(
    'lilang/lib/libio',
    sources=['lib/io.c'],
    )

setuptools.setup(
    name="lilang",
    version="0.1.0",
    author="Piotr Resztak",
    author_email="piotr.resztak@gmail.com",
    description="Lilang package",
    packages=setuptools.find_packages(),
    package_data={'lilang': ['lib/io.li']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    python_requires='>=3.8.2',
    install_requires=[
        "sly>=0.4",
        "llvmlite>=0.33.0",
        "click>=7.1.2"
    ],
    extras_require={
        "dev": [
            "isort", "flake8"
        ]
    },
    entry_points={
        'console_scripts': [
            'lilang = lilang.lilang:main'
        ],
    },
    cmdclass={
        'build_ext': LilangBuildExt,
        'install': LilangInstall
    },
    ext_modules=[iolib]
)
