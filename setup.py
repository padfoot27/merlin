from setuptools import setup,find_packages

setup(
        name = 'movieMerlin',
        packages=find_packages(),
        version = '0.1',
        description = 'A personal movie recommender',
        author = 'Siddharth Verma',
        author_email = 'siddharthv93@gmail.com',
        url = 'https://github.com/padfoot27/merlin',
        download_url = 'https://github.com/padfoot27/merlin/tarball/0.1',
        include_package_data=True,
        install_requires = [
            'Click',
            'tmdbsimple',
        ],
        entry_points = '''
            [console_scripts]
            merlin=package.scripts.merlin:discover
        ''',
)
