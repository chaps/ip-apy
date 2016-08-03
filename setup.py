from distutils.core import setup

setup(
    name="ip-apy",
    version="0.0.1",
    author="Chaps",
    author_email="drumchaps@gmail.com",
    maintainer="Chaps",
    maintainer_email="drumchaps@gmail.com",
    url="https://bitbucket.org/drumchaps/ip-apy",
    packages  = [
        "ip-apy",
    ],
    package_dir={'ip-apy': 'src/ip-apy'},
    #install_requires = ["requests",]
)


