"""git_credit installer."""


from setuptools import setup


setup(
    name="git_credit",
    version="0.0.1",
    author="Adam Talsma",
    author_email="adam@talsma.ca",
    packages=["git_credit"],
    scripts=["bin/git_credit"],
    url="https://github.com/a-tal/git_credit",
    description="A pretty way to show committer stats for git repos",
    long_description="Uses git log to display committer stats for git repos",
    download_url="https://github.com/a-tal/git_credit",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
)
