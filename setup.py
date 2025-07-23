from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(), #  finds these directories automatically so you don’t have to type them out.
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
# packages tells Python what package directories (and the Python files they contain) to include.
# To include other files, such as the static and templates directories, include_package_data is set. Python needs another file named MANIFEST.in to tell what this other data is.



