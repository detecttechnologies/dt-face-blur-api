from setuptools import setup, find_packages

setup(
    name="dt-face-blur-api",
    version="0.2.0",
    description="Face Blur API Client",
    url="https://detecttechnologies.com/",
    author="Detect Technologies Pvt. Ltd.",
    author_email="support@detecttechnologies.com",
    license="BSD 3-clause",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["opencv-python>=4.2.0.32", "requests>=2.23.0", "logzero>=1.7.0"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
    ],
)
