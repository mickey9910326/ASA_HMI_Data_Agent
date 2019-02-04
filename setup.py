import os
import shutil
from setuptools import setup, find_packages

REQUIREMENTS = [
    'py-asa-loader',
    'numpy',
    'pypiwin32',
    'PyQt5',
    'pyserial',
    'pyzmq',
    'scipy',
    'sip'
]

def run():
    setup(
        name='asa-hmi-data-agent',
        version='0.5.0',
        description = 'ASA developing tools on PC.',
        long_description='',
        author = 'mickey9910326',
        author_email = 'mickey9910326@gmail.com',
        url='https://github.com/mickey9910326/ASA_HMI_Data_Agent',
        license = 'GPL v3',
        packages=find_packages(),
        package_data={ 'asa_hmi_data_agent': [ 'tools/*', 'settings/*', 'tmp/*' ] },
        zip_safe=False,
        entry_points = {
            'console_scripts': [
                'asa_hmi_data_agent = asa_hmi_data_agent.__main__:run',
                'adt = asa_hmi_data_agent.__main__:run',
                'adt-term = asa_hmi_data_agent.cli_tools.tool_term:run',
                'adt-loader = asa_hmi_data_agent.cli_tools.tool_loader:run'
            ],
        },
        install_requires=REQUIREMENTS
    )

if __name__ == '__main__':
    run()
