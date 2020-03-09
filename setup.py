try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('LICENSE') as f:
    license = f.read()
with open('README.md') as f:
    readme = f.read()

setup(
    name='fastlangid',
    version='1.0.0',
    description='Language detection for news powered by fasttext',
    long_description=readme,
    author='Ray',
    author_email='ray@currentsapi.services',
    url='https://github.com/currentsapi/fastlangid',
    keywords='language detection library',
    packages=['fastlangid'],
    package_data={'fastlangid': ['fastlangid/*', 'models/*']},
    include_package_data=True,
    install_requires=['fasttext'],
    license=license,
    classifiers=[
        'Development Status :: 1 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)