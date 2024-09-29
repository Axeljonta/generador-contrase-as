# Generador de Contraseñas en Python

Este proyecto consiste en un generador de contraseñas seguro y personalizable escrito en Python. Permite a los usuarios crear y almacenar contraseñas de forma segura, garantizando así una mayor protección de la información.

## Características

- **Generador de Contraseñas**: Crea contraseñas con diferentes características, como el uso de mayúsculas, números y caracteres especiales.
- **Longitud Personalizable**: Permite especificar la longitud mínima de la contraseña (mínimo 8 caracteres).
- **Opciones de Inclusión**: Opción para incluir:
  - Mayúsculas
  - Números
  - Caracteres especiales
- **Almacenamiento Seguro**: Utiliza bcrypt para hashear las contraseñas antes de almacenarlas en una base de datos SQLite, asegurando que las contraseñas no sean legibles en caso de acceso no autorizado.
- **Registro y Verificación de Usuarios**: Los usuarios pueden registrarse con un correo electrónico único y una contraseña. La verificación de inicio de sesión se realiza mediante comparación de hashes.
- **Interfaz Interactiva**: Una sencilla interfaz de línea de comandos que guía al usuario a través del proceso de creación de contraseñas y gestión de usuarios.

## Requisitos

- Python 3.x
- Módulos: `random`, `string`, `sqlite3`, `bcrypt`, `pandas`

