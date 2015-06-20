from setuptools import setup,find_packages

setup(
        name = 'movieMerlin',
        packages=find_packages(),
        version = '0.2',
        description = 'A command line tool that finds you movies',
        author = 'Siddharth Verma',
        author_email = 'siddharthv93@gmail.com',
        url = 'https://github.com/padfoot27/merlin',
        download_url = 'https://github.com/padfoot27/merlin/tarball/0.2',
        include_package_data=True,
        license = 'MIT License',
        install_requires = [
            'Click',
            'tmdbsimple',
        ],
        entry_points = '''
            [console_scripts]
            merlin=package.scripts.merlin:discover
        ''',
)
