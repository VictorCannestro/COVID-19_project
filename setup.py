from setuptools import setup

INSTALL_REQUIRES = [
    'pandas',
    'numpy',
    'scipy',
    'rtree',
    'gdal',
    'fiona',
    'shapely',
    'geopandas',
    'pysal',
    'matplotlib',
    'missingno',
    'time',
    'seaborn',
    'requests',
    'bs4'
]
TEST_REQUIRES = [
    # testing and coverage
    'pytest', 'coverage', 'pytest-cov'
    # to be able to run `python setup.py checkdocs`
    'collective.checkdocs', 'pygments',
]

setup(
    name='Covid-19 Project',
    author='Victor Cannestro',
    description='Visualizations of the 2019-2021 COVID-19 pandemic in the US',
    long_description=README,
    url='https://github.com/VictorCannestro/COVID-19_project',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'test': TEST_REQUIRES + INSTALL_REQUIRES,
    })
