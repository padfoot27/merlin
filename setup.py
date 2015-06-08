from setuptools import setup

setup(
        name = 'merlin',
        version = '0.1',
        py_modules = ['merlin'],
        install_requires = [
            'Click',
            'tmdbsimple',
        ],
        entry_points = '''
            [console_scripts]
            merlin=merlin:discover
        ''',
)
