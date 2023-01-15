from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='shiroplot',
    version='1.2.0',
    author='SHIRO',
    author_email='39456646+shiro46mt@users.noreply.github.com',
    license='MIT',
    description='Shiroplot is a Python visualization library inspired by seaborn.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['matplotlib', 'seaborn'],
    packages=find_packages()
)
