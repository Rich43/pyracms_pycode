import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid>=1.0.2',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'waitress'
]

setup(name='pyracms_pycode',
      version='0.0',
      description='pyracms_pycode',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pyracms_pycode",
      entry_points="""\
      [paste.app_factory]
      main = pyracms_pycode:main
      [console_scripts]
      initialize_pyracms_article_db = pyracms_article.scripts.initializedb:main
      """,
      paster_plugins=['pyramid'],
      )
