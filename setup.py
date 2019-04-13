from setuptools import setup

version = {}
with open('genanki/version.py') as fp:
  exec(fp.read(), version)

setup(name='genanki-marccarre',
      version=version['__version__'],
      description='Generate Anki decks programmatically (fork from http://github.com/kerrickstaley/genanki)',
      url='http://github.com/marccarre/genanki',
      author='Marc Carré (fork maintainer), Kerrick Staley (original author)',
      author_email='carre.marc@gmail.com',
      license='MIT',
      packages=['genanki'],
      zip_safe=False,
      install_requires=[
        'cached-property',
        'frozendict',
        'pystache',
        'pyyaml',
      ],
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=[
          'pytest',
      ],
      keywords=[
        'anki',
        'flashcards',
        'memorization',
      ])
