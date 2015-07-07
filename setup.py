import setuptools

setuptools.setup(
    install_requires=open('requirements.txt').readlines(),
    version='0.1.0',
    name='st7565',
    packages=['st7565'],
    entry_points={
        'console_scripts': [
            'stleds = st7565.cmd.stleds:main',
        ],
    }
)
