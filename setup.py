from setuptools import setup

setup(
    name='ninjahelper',
    version='0.1',
    long_description=__doc__,
    packages=['ninjahelper'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-Compass',
        'pymongo',
        'pyjade>=1.0.1',
        'pyyaml',
    ],
)
