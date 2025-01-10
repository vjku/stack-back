from setuptools import setup, find_namespace_packages

setup(
    name="stack-back",
    url="https://github.com/lawndoc/stack-back",
    version="0.7.1",
    author="Einar Forselv",
    author_email="eforselv@gmail.com",
    packages=find_namespace_packages(include=[
        'restic_compose_backup',
        'restic_compose_backup.*',
    ]),
    install_requires=[
        'docker~=7.1.0',
    ],
    entry_points={'console_scripts': [
        'stack-back = restic_compose_backup.cli:main',
        'rcb = restic_compose_backup.cli:main',
    ]},
)
