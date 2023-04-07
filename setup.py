from setuptools import setup, find_packages

setup(
    name='fullsubnet',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch>=1.7.0',
        'librosa>=0.10.0',
        'toml>=0.10.2',
        'torchaudio>=0.7.2',
        'torchvision>=0.8.2',
        'tqdm'
    ],
)
