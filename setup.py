from setuptools import setup, find_packages

version = '1.0a1'

setup(name='pystunnel',
      version=version,
      description='Python interface to stunnel',
      #long_description=open('README.rst').read() + '\n' +
      #                 open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
      #    'Programming Language :: Python :: 3',
      ],
      keywords='stunnel ssl tunnel tls',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://pypi.python.org/pypi/pystunnel',
      license='BSD',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pystunnel.tests',
      install_requires=[
          'setuptools',
      ],
      entry_points={
          'console_scripts': 'pystunnel=pystunnel.pystunnel:main',
      },
)
