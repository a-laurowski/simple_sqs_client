import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simple_sqs_client',
    author='Aleksander Laurowski',
    author_email='aleksander.laurowski191@gmail.com',
    description='Very simple SQS Client',
    keywords='simple_sqs_client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a-laurowski/simple_sqs_client',
    project_urls={
        'Documentation': 'https://github.com/a-laurowski/simple_sqs_client/blob/main/README.md',
        'Bug Reports':
        'https://github.com/a-laurowski/simple_sqs_client/issues',
        'Source Code': 'https://github.com/a-laurowski/simple_sqs_client',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=simple_sqs_client:main',
    # You can execute `run` in bash to run `main()` in src/simple_sqs_client/__init__.py
    #     ],
    # },
)
