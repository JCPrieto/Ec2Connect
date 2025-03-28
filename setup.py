from setuptools import setup, find_packages

from appinfo import app_name, app_version

setup(
    name=app_name,
    version=app_version,
    packages=find_packages(),
    py_modules=[app_name],
    install_requires=[
        'boto3',
        'questionary',
        'pyyaml',
        'setuptools',
        'appinfo'
    ],
    include_package_data=True,  # Asegura que los datos adicionales sean incluidos
    package_data={
        # Incluye el archivo YAML en todos los paquetes
        # 'config': ['logging_config.yml'],
    },
)
