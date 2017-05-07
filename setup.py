from setuptools import setup

setup(name='genanki',
      version='0.3.0',
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
