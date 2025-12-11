from setuptools import setup, find_packages


setup(
    name='genericlib',
    version='0.6.0',
    license='BSD-3-Clause',
    license_files=['LICENSE'],
    description='Generic Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tuyen Mathew Duong',
    author_email='tuyen@geekstrident.com',
    maintainer='Tuyen Mathew Duong',
    maintainer_email='tuyen@geekstrident.com',
    install_requires=[
        'pyyaml',
        'regexbuilder',
        'textfsmgenerator'
    ],
    url='https://github.com/Geeks-Trident-LLC/genericlib',
    packages=find_packages(
        exclude=(
            'tests*', 'testing*', 'examples*',
            'build*', 'dist*', 'docs*', 'venv*'
        )
    ),
    include_package_data=True,
    test_suite='tests',
    classifiers=[
        # development status
        'Development Status :: 2 - Pre-Alpha',
        # natural language
        'Natural Language :: English',
        # intended audience
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        # operating system
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        # license
        "License :: OSI Approved :: BSD License",  # BSD-3-Clause classifier
        # programming language
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        # topic
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing',
    ],
)
