from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Testing',
    'Programming Language :: Python :: 2.7'
]

setup(
    name="yamltests",
    version="0.0.1",
    description="""Running yaml tests from nose""",
    long_description=""" """,
    author="Viktor Pekar",
    author_email="v.pekar@gmail.com",
    url="https://github.com/vpekar/yamltests",,
    license="New BSD License",
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['nose', 'pyyaml', 'setuptools'],
    py_modules=['yamltests'],
    zip_safe = False,
    entry_points = {
        'nose.plugins.0.10': [
            'yamltests = yamltests:YamlTests'
            ]
        },
)