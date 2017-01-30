from setuptools import setup, find_packages
from pythiaplotter import __version__


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="PythiaPlotter",
    version=__version__,
    description="Generate diagram of particles in the event tree from a "
                "High-Energy Physics Monte Carlo event generator.",
    long_description="SOMETHING HERE",
    author="Robin Aggleton",
    author_email="robinaggleton@gmail.com",
    url="https://github.com/raggleton/PythiaPlotter",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'PythiaPlotter=pythiaplotter.PythiaPlotter:main'
        ]
    },
    package_data={
        'pythiaplotter': ['particledata/*.tex', 'particledata/*.xml',
                          'printers/templates/vis_template.html']
    },
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
