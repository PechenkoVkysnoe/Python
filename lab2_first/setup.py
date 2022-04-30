from setuptools import setup, find_packages

setup(
    name="myfirstlib",
    version="1.0.0",
    description="Serialize and deserialize objects to Yaml, Toml, Json",
    url="https://github.com/PechenkoVkysnoe/Python/tree/lab2/lab2_first",
    author="Misha Grigorchuk",
    author_email='mishagrigorchu@gmail.com',
    install_requires=["pytomlpp", 'pyyaml'],
    packages=find_packages(),
)
