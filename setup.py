from setuptools import setup, find_packages

version = '1.0a1'

setup(name='pystunnel',
      version=version,
      description='Python interface to stunnel',
      #long_description=open('README.rst').read() + '\n' +
      #                 open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='stunnel ssl tunnel tls',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://pypi.python.org/pypi/pystunnel',
      license='AGPLv3',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      #test_suite='pystunnel.tests',
      install_requires=[
          'setuptools',
          'six',
      ],
      entry_points={
          'console_scripts': 'pystunnel=pystunnel.pystunnel:main',
      },
)
