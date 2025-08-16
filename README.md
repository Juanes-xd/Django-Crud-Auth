# Django CRUD Auth

Este proyecto es una aplicación web construida con Django que implementa operaciones CRUD (Crear, Leer, Actualizar, Eliminar) con autenticación de usuarios.

## Características
- Registro y autenticación de usuarios (signup, signin, signout)
- Gestión de tareas (crear, ver, editar, eliminar)
- Interfaz sencilla con plantillas HTML

## Estructura del proyecto
- `djangocrud/`: Configuración principal de Django
- `tasks/`: Aplicación principal con modelos, vistas, formularios y plantillas
- `templates/`: Archivos HTML para la interfaz de usuario
- `db.sqlite3`: Base de datos SQLite por defecto
- `manage.py`: Script de gestión de Django

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/Juanes-xd/Django-Crud-Auth.git
   cd Django-Crud-Auth
   ```
2. Instala las dependencias:
   ```bash
   pip install django
   ```
3. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```
4. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```
5. Accede a la aplicación en [http://localhost:8000](http://localhost:8000)

## Uso
- Regístrate o inicia sesión para gestionar tus tareas.
- Crea, edita, elimina y visualiza tareas desde la interfaz web.

## Licencia
Este proyecto está bajo la licencia MIT.
