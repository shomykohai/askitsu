from setuptools import setup
import re


version = ''
with open('askitsu/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md') as f:
    readme = f.read()

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

packages = [
    'askitsu'
]

setup(
    name='askitsu',
    author='ShomyKohai',
    version=version,
    license='MIT',
    description='An async python wrapper Kitsu.io API',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=packages,
    keywords='kitsu',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed'
    ]
)
