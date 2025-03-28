# Ec2Connect

## Descripción

Este script permite conectarse a instancias EC2 de AWS utilizando SSH.

Facilita la conexión al automatizar el proceso de construcción del comando SSH, lo que ahorra tiempo y reduce la
posibilidad de errores.

Cada conexión por ssh se abrirá en una nueva pestaña de terminal, lo que permite mantener múltiples conexiones abiertas
al mismo tiempo.

## Requisitos previos

- Tener una instancia EC2 en ejecución.
- Tener la clave privada (.pem) asociada a la instancia.
- Tener configurado el acceso SSH en la instancia EC2.
- Tener instalado el cliente SSH en tu máquina local.
- Tener configurado el grupo de seguridad de la instancia EC2 para permitir conexiones SSH (puerto 22) desde tu
  dirección IP.
- Tener configurada la variable de entorno `AWS_ACCESS_KEY_ID` con tu clave de acceso de AWS.

La configuración para la conexión ssh se carga desde el archivo application.yml, que debe estar en la misma carpeta que
el script. Este archivo debe contener la siguiente estructura:

Ejemplo de archivo `application.yml`:

```yaml
aws:
  profiles:
    - name: myProfile # Nombre del perfil
      description: Nombre del perfil 1
      ssh:
        credentials-file: $HOME/.ssh/myCredential.pem # Ruta a la clave privada
        user: ec2-user # Usuario por defecto
        autorun: "sudo tail -f /var/log/messages" # Comando a ejecutar al conectarse
    - name: myProfile2 # Nombre del perfil 2
      description: Nombre del perfil 2
      ssh:
        credentials-file: $HOME/.ssh/myCredential2.pem # Ruta a la clave privada
        user: admin # Usuario por defecto
        autorun: "sudo tail -f /var/log/messages" # Comando a ejecutar al conectarse
```

## Requisitos

- Python 3.6 o superior
- Instalación de las librerías necesarias:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python ec2connect.py
```

## Notas

- Asegúrate de que la clave privada tenga los permisos correctos (chmod 400).
- El nombre de la instancia debe ser el nombre público o privado de la instancia EC2.
- El nombre de usuario puede variar según el sistema operativo de la instancia. Algunos ejemplos son:
    - Amazon Linux: ec2-user
    - Ubuntu: ubuntu
    - CentOS: centos
    - RHEL: ec2-user o root
    - Debian: admin o root
    - SUSE: ec2-user o root
    - Fedora: ec2-user o root
    - Windows: Administrator
