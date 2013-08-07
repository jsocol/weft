from setuptools import setup, find_packages


setup(
    name='weft',
    version='0.0.1',
    description='Remote server state management and configuration',
    author='James Socol',
    author_email='me@jamessocol.com',
    license='Apache Software License',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.rst']},
    install_requires=[
        'PyYAML==3.10',
        'Fabric==1.7',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System',
    ],
)
