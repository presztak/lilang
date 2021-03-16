import setuptools
from distutils.command.build_ext import build_ext
from distutils.core import Extension


class LilangBuildExt(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        filename_parts = filename.split('.')
        return f'{filename_parts[0]}.{filename_parts[-1]}'


iolib = Extension(
    'lilang.lib.libio',
    sources=['lilang/lib/io.c'],
    )

strlib = Extension(
    'lilang.lib.libstr',
    sources=['lilang/lib/str.c'],
    )

vaarglib = Extension(
    'lilang.lib.libvaarg',
    sources=['lilang/lib/vaarg.c'],
    )

setuptools.setup(
    name="lilang",
    version="0.1.0",
    author="Piotr Resztak",
    author_email="piotr.resztak@gmail.com",
    description="Lilang package",
    packages=setuptools.find_packages(),
    package_data={'lilang': ['lib/io.li', 'lib/str.li', 'lib/vaarg.li']},
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
    },
    ext_modules=[iolib, strlib, vaarglib]
)
