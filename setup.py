"""
Setup file for the mtsthelens package
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

opts = dict(
    name = 'MtStHelens',
    version = '0.1',
    url = 'https://github.com/CSE583MtStHelens/CSE583_MtStHelens',
    license = 'MIT',
    author = 'guiliangz,shreeyag, yash6599, callumk, koepflma',
    author_email = 'guiliang@uw.edu, shreeyag@uw.edu, yash6599@uw.edu, callumk@uw.edu, koepflma@uw.edu',
    description = 'Analyze the seismic data of the volcanic eruption of the Mount St. Helens from 2004 to 2008',
    long_description = 'Analyze the correlation of seismic attenuation and the magma extrusion rate and the changing\
          of the climatic patterns in the region from seismic data of the Mount St. Helens',
    packages = ['mtsthelens', 'tests', 'example'],
    package_data = {'example':['example_data/*.*']},
    include_package_data = True,
    setup_requires = ['pytest-runner', 'flake8'],
    tests_requires = ['pytest'],
)

if __name__=='__main__':
    setup(**opts)
