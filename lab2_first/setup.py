from setuptools import setup

setup(
    name="my_first_lib",
    version="1.0.0",
    description="Serialize and deserialize objects to Yaml, Toml, Json",
    author="Misha Grigorchuk",
    author_email='mishagrigorchu@gmail.com',
    url="https://github.com/PechenkoVkysnoe/Python/tree/lab2/lab2_first",
    install_requires=["pytomlpp"],
    packages=["lab2/",
              "."],
    entry_points={"console_scripts": "cu=console_util:main"}
)
