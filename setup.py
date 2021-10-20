from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='b2c2-client',
    version='1.0.0',
    author='Ayush Tiwari',
    author_email='tiwari.ayush2412@gmail.com',
    license='MIT',
    description='B2C2 CLI Application',
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        b2c2-client=b2c2_trade:main
    '''
)
