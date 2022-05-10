'''
setup.py - a setup script
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Authors:
    Ray : ray@currentsapi.services
'''
from setuptools import setup, Extension

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LICENSE', 'r') as f:
    license_ = f.read()

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='fastlangid',
    version='1.0.9',
    description='Language detection for news powered by fasttext',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Ray',
    author_email='ray@currentsapi.services',
    url='https://github.com/currentsapi/fastlangid',
    keywords='language detection library',
    packages=['fastlangid'],
    package_data={'fastlangid': ['fastlangid/*', 'models/*']},
    include_package_data=True,
    install_requires=['fasttext'],
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
