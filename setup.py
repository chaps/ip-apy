from distutils.core import setup

setup(
    name="ip_apy",
    version="0.0.1",
    author="Chaps",
    author_email="drumchaps@gmail.com",
    maintainer="Chaps",
    maintainer_email="drumchaps@gmail.com",
    url="https://bitbucket.org/drumchaps/ip-apy",
    packages  = [
        "ip_apy",
    ],
    package_dir={'ip_apy': 'src/ip-apy'},
    #install_requires = ["requests",]
)


