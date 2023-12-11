from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mapkick-static',
    version='0.1.0',
    description='Create beautiful static maps with one line of Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ankane/mapkick-static.py',
    author='Andrew Kane',
    author_email='andrew@ankane.org',
    license='MIT',
    packages=[
        'mapkick.static',
    ],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[],
    zip_safe=False
)
