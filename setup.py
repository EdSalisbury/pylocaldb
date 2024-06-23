from setuptools import setup, find_packages

setup(
    name='localdb',
    description='Wrapper for local databases.',
    author='Ed Salisbury',
    author_email='ed.salisbury@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/edsalisbury/pylocaldb',
    version='0.1',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
