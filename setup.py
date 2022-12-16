from setuptools import setup
from pathlib import Path

version = {}
with open('genanki/version.py') as fp:
  exec(fp.read(), version)

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='genanki',
      version=version['__version__'],
      description='Generate Anki decks programmatically',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/kerrickstaley/genanki',
      author='Kerrick Staley',
      author_email='k@kerrickstaley.com',
      license='MIT',
      packages=['genanki'],
      zip_safe=False,
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
        'cached-property',
        'frozendict',
        'chevron',
        'pyyaml',
      ],
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=[
          'pytest>=6.0.2',
      ],
      keywords=[
        'anki',
        'flashcards',
        'memorization',
      ])
