# Sistema de Gestión de Recursos Humanos

Aplicación individual desarrollada con Django y PostgreSQL para administrar departamentos, cargos, empleados y capacitaciones. Tema: Sistema de Gestión de Recursos Humanos.

## Modelo de datos
- **Departamento** tiene muchos empleados (ForeignKey desde Empleado).
- **Cargo** tiene muchos empleados (ForeignKey desde Empleado).
- **Empleado** pertenece a un departamento y un cargo, registra quién lo creó y puede asociarse a varias capacitaciones.
- **Capacitacion** puede estar asociada a varios empleados mediante ManyToMany.

## Requisitos
Python, PostgreSQL, Django y las dependencias indicadas por el entorno de desarrollo (`python-dotenv` y el adaptador PostgreSQL).

## Instalación
1. Clonar el repositorio y entrar a la carpeta del proyecto.
2. Crear y activar un entorno virtual.
3. Instalar dependencias: `pip install -r requirements.txt`. En el entorno virtual de desarrollo, actualizar el archivo con `pip freeze > requirements.txt` antes de publicar para registrar exactamente las versiones instaladas.
4. Copiar `.env.example` como `.env` y completar los datos de PostgreSQL.
5. Crear la base de datos indicada en `DB_NAME`.
6. Ejecutar `python manage.py migrate`.
7. Crear roles y datos de prueba: `python manage.py preparar_datos_demo`.
8. Ejecutar `python manage.py runserver`.

## Usuarios de demostración
Estas credenciales son únicamente para desarrollo y evaluación local. Cámbielas si se publica el proyecto en un servidor.

| Usuario | Contraseña | Grupo | Capacidades |
|---|---|---|---|
| `admin_demo` | `AdminDemo123!` | Administrador | Superusuario para administrar todo el sitio |
| `administrador_demo` | `AdministradorDemo123!` | Administrador | CRUD completo de los cuatro módulos |
| `consultor_demo` | `ConsultorDemo123!` | Consultor | Ver y crear; editar solo empleados propios; no eliminar |

El comando `preparar_datos_demo` es repetible y crea cinco registros de cada modelo sin duplicarlos. El comando `configurar_roles` también puede ejecutarse por separado para actualizar permisos.

## Pruebas
Ejecutar `python manage.py check` y `python manage.py test personal`.

## Autenticación
- Registro: `/registro/` (los nuevos usuarios se incorporan al grupo Consultor).
- Inicio de sesión: `/accounts/login/`.
- Cierre de sesión: botón que envía POST a `/accounts/logout/`.
- La ruta `/` redirige al listado de empleados.
