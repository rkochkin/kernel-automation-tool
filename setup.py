from setuptools import setup, find_packages

setup(
    name="kernel-builder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'PyYAML>=6.0',
        'requests>=2.25.0',
        'gitpython>=3.1.0',
    ],
    entry_points={
        'console_scripts': [
            'kernel-builder=main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for building Linux kernels with YAML configuration",
    python_requires='>=3.7',
)
