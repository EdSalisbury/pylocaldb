from setuptools import setup, find_packages

setup(
    name='localdb',
    version='1.0.0',
    description='Wrapper for local databases.',
    author='Ed Salisbury',
    author_email='ed.salisbury@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/edsalisbury/pylocaldb',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
