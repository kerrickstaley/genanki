from setuptools import setup

version = {}
with open('genanki/version.py') as fp:
  exec(fp.read(), version)

setup(name='genanki',
      version=version['__version__'],
      description='Generate Anki decks programmatically',
      url='http://github.com/kerrickstaley/genanki',
      author='Kerrick Staley',
      author_email='k@kerrickstaley.com',
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
