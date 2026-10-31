# Mini CRM

<p align="center">
  <img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="260" alt="Logo de Django">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&amp;logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?logo=django&amp;logoColor=white" alt="Django 5.2">
  <img src="https://img.shields.io/badge/SQLite-Base_de_datos-003B57?logo=sqlite&amp;logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Docker-Contenedores-2496ED?logo=docker&amp;logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/HTML5-E34F26?logo=html5&amp;logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?logo=css3&amp;logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&amp;logoColor=black" alt="JavaScript Vanilla">
  <img src="https://img.shields.io/badge/Lottie-Animaciones-00DDB3" alt="Animaciones Lottie">
  <img src="https://github.com/Raraulo/Mini-CRM/actions/workflows/ci.yml/badge.svg?branch=main" alt="Estado de GitHub Actions en main">
</p>

Un pequeño sistema para registrar, buscar, editar y eliminar clientes.
Incluye un dashboard, filtros por estado y gráficos de resumen.

## 1. ¿Qué necesitas tener instalado?

Solo necesitas **Docker Desktop** y un navegador.

- Abre Docker Desktop y espera a que termine de iniciar.
- Docker debe usar **contenedores Linux**.
- Descarga el proyecto completo y descomprímelo si viene en un ZIP.

**No necesitas instalar Python, Django, Node ni SQLite en tu computadora.**
Docker prepara Python y las dependencias automáticamente.
La primera vez necesitas Internet para descargar la imagen y las dependencias.

## 2. Abre una terminal en la carpeta del proyecto

Puedes abrir la carpeta con VS Code y seleccionar **Terminal > Nueva terminal**.
La terminal debe estar en la carpeta donde está este README.

Por ejemplo, en PowerShell:

```powershell
cd "C:\ruta\donde\descargaste\Mini CRM"
```

Reemplaza esa ruta por la ubicación del proyecto en tu computadora.
**Ejecuta los siguientes comandos uno por uno y en el orden indicado.**

## 3. Crea tu archivo .env

El archivo `.env` no se incluye en GitHub porque guarda una clave privada de
Django. Cada persona debe generar su propia clave.

Ejecuta este comando en PowerShell:

```powershell
docker run --rm python:3.12-slim python -c "import secrets; print('DJANGO_SECRET_KEY=' + secrets.token_urlsafe(48))" | Set-Content -Encoding ascii .env
```

El comando crea `.env` automáticamente en la carpeta del proyecto. No tienes
que inventar una clave ni instalar Python: se genera dentro de un contenedor.
`.env.example` solo muestra qué variable se necesita.

**Este paso se hace una sola vez.** Si ya tienes `.env`, consérvalo. No lo subas
a GitHub ni lo compartas; cambiar la clave cierra las sesiones existentes.

## 4. Levanta la aplicación

```powershell
docker compose --env-file .env -f docker/docker-compose.yml up --build -d --wait
```

Espera a que termine. La primera vez puede tardar unos minutos. La opción `--env-file .env` indica expresamente dónde está tu clave de configuración.
Este comando prepara el contenedor, crea las tablas de SQLite, carga los datos
de ejemplo e inicia Django.

Para comprobar que está encendido:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml ps
```

El servicio `web` debe aparecer como **Up** y **healthy**.
También puedes verlo en **Docker Desktop > Containers > minicrm**.

## 5. Crea tu usuario y contraseña

La aplicación necesita iniciar sesión. Los contactos de ejemplo **no son cuentas
de acceso**, por eso debes crear tu propio administrador:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml exec web python manage.py createsuperuser
```

La terminal te pedirá estos datos. Por ejemplo:

| Lo que te pide | Qué puedes escribir |
| --- | --- |
| Nombre de usuario / Username | `evaluador` |
| Correo / Email address | `evaluador@example.com` |
| Contraseña / Password | Una contraseña segura que tú elijas, de al menos 8 caracteres |
| Confirmar contraseña / Password again | Repite esa misma contraseña |

Al escribir la contraseña **no aparecen letras ni asteriscos**; es normal.
Si Django indica que es demasiado débil, elige una más segura.
Cuando aparezca **Superuser created successfully**, la cuenta está lista.

El usuario y correo de la tabla son ejemplos, no una cuenta ya creada.
Cada persona usa sus propias credenciales. **En el login debes escribir el
nombre de usuario que elegiste**, por ejemplo `evaluador`.
Este paso también se hace una sola vez.

## 6. Abre el CRM

- **Aplicación:** http://localhost:8000/
- **Django Admin:** http://localhost:8000/admin/

Inicia sesión con el usuario y contraseña que acabas de crear.
La misma cuenta sirve para el CRM y para Django Admin.
En el CRM puedes gestionar los contactos; en Admin también puedes gestionar
cuentas y consultar las fechas de creación y actualización.

¡Con eso ya puedes probar el proyecto!

## ¿Ya vienen datos para probar?

Sí. Al iniciar por primera vez se cargan automáticamente **10 contactos ficticios**:

- 5 clientes activos.
- 3 prospectos.
- 2 inactivos.

Están en `base_de_datos/contactos_prueba.json`. No necesitas cargar ese archivo
manualmente ni descargar una base de datos por separado.

SQLite crea su archivo y guarda los datos en un **volumen de Docker**, llamado
`minicrm_crm_data`. También guarda allí tu cuenta y los contactos que agregues.
Detener o reiniciar el contenedor no elimina los datos.
Los ejemplos se cargan una sola vez: reiniciar no los duplica ni restaura los
que hayas borrado. Los datos y contraseñas de la computadora del autor no se comparten.

## ¿Cómo lo vuelvo a abrir otro día?

Abre Docker Desktop, abre la terminal en el proyecto y ejecuta:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml up -d --wait
```

Después abre http://localhost:8000/.
**No necesitas volver a generar .env ni crear otra cuenta.**

Para apagarlo sin perder los datos:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml down
```

No agregues `-v` al comando de apagado: esa opción elimina el volumen y su base.

## ¿Qué puedes probar?

- Registrar y editar clientes desde un modal.
- Eliminar un cliente con confirmación previa.
- Buscar por nombre o empresa y filtrar por estado.
- Consultar métricas y desplegar los gráficos con **Ver más**.
- Ver mensajes de confirmación que se cierran después de cuatro segundos.
- Ver cómo se bloquea el botón mientras se envía un formulario.
- Mostrar u ocultar la contraseña en el login y cerrar sesión.
- Abrir una dirección inexistente para ver la página de error.
- Cambiar el tamaño del navegador para revisar la versión móvil y tablet.

Nombre, correo y estado son obligatorios; empresa y teléfono son opcionales.
El nombre no admite números y el teléfono, si se ingresa, no admite letras.
Las fechas se guardan automáticamente.

El gráfico de dona muestra la distribución por estado. El de líneas muestra
los contactos registrados cada día en los últimos 30 días, entre los contactos
que siguen en la base de datos.

## ¿Qué se usó y por qué?

| Tecnología | Para qué se usa |
| --- | --- |
| HTML y CSS | Estructura, diseño y adaptación a móvil, tablet y escritorio |
| JavaScript Vanilla | Modales, búsqueda dinámica, validaciones, notificaciones y gráficos, sin un framework frontend |
| Django | Backend, formularios, login, validaciones y panel de administración |
| SQLite | Guardar contactos y cuentas de forma sencilla, sin otro servidor de base de datos |
| Docker | Ejecutar el proyecto con el mismo entorno sin instalar sus dependencias en cada computadora |
| Lottie Web | Reproducir las ilustraciones e iconos animados de los archivos JSON |

**Lottie no requiere que instales nada.** Su reproductor y animaciones ya están
incluidos en `frontend/static/`, junto con la licencia del reproductor.
Los gráficos usan CSS y SVG; tampoco requieren una instalación adicional.

## ¿Cómo están organizadas las carpetas?

```text
Mini CRM/
├── frontend/
│   ├── templates/          Páginas HTML
│   │   ├── clients/        Dashboard, listado y modales
│   │   ├── registration/   Inicio de sesión
│   │   └── errors/         Página de errores
│   └── static/
│       ├── css/            Estilos y diseño responsive
│       ├── js/             Interacciones y reproductor Lottie
│       ├── images/         Imágenes e icono de la pestaña
│       └── lotties/        Animaciones e iconos
├── backend/
│   ├── config/             Configuración de Django, sesión, rutas y errores
│   ├── clients/            Modelo, formularios, vistas, rutas, Admin y pruebas
│   │   └── migrations/     Pasos para crear y actualizar las tablas
│   ├── manage.py           Entrada de los comandos de Django
│   └── requirements.txt    Dependencias que Docker instala
├── base_de_datos/
│   ├── configuracion.py    Configuración de SQLite
│   └── contactos_prueba.json  Los 10 contactos de ejemplo
├── docker/
│   ├── Dockerfile          Instrucciones para construir la imagen
│   ├── Dockerfile.dockerignore  Archivos excluidos de la construcción
│   └── docker-compose.yml  Servicio, puerto y almacenamiento
├── .env.example            Ejemplo de la variable requerida
├── .gitignore              Archivos locales que no deben subirse
└── README.md               Esta guía
```

Los archivos `__init__.py` identifican paquetes de Python.
El `.env` que generas se queda en tu computadora. La base SQLite está en el
volumen Docker, no en una carpeta que debas subir al repositorio.

## Comprobaciones del proyecto

Durante el desarrollo se ejecutó `manage.py check` sin errores y se realizaron
pruebas automatizadas. Para comprobar la versión que descargaste, con el
contenedor encendido ejecuta:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml exec web python manage.py check
docker compose --env-file .env -f docker/docker-compose.yml exec web python manage.py test clients
```

`check` debe indicar **System check identified no issues** y las pruebas deben
terminar en **OK**. Usan una base temporal; no borran tus contactos.
Incluyen validaciones, operaciones de clientes, filtros, datos de ejemplo,
inicio y cierre de sesión y manejo de errores.

## Si algo no funciona

| Problema | Qué hacer |
| --- | --- |
| Docker no conecta | Abre Docker Desktop y espera a que inicie el motor Linux |
| Falta DJANGO_SECRET_KEY | Completa el paso 3 y ejecuta los comandos desde la raíz del proyecto |
| El puerto 8000 está ocupado | Cierra la otra aplicación que esté usando ese puerto |
| No recuerdas tu contraseña | Ejecuta el comando de cambio de contraseña de abajo |
| No ves los últimos cambios visuales | Recarga con Ctrl + F5 |

Para ver los mensajes del servidor:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml logs -f web
```

Ctrl+C sale de los mensajes sin apagar el contenedor.

Para cambiar la contraseña, reemplaza `evaluador` por tu nombre de usuario:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml exec web python manage.py changepassword evaluador
```

Si modificaste el proyecto y necesitas reconstruirlo:

```powershell
docker compose --env-file .env -f docker/docker-compose.yml up --build -d --wait
```

## Nota sobre el entorno

Esta guía prepara el proyecto para **pruebas y desarrollo local**, no para
publicarlo en Internet. Solo se expone el puerto en tu computadora.
El CRM exige sesión y usa protección CSRF. Las cuentas activas comparten el
directorio; Django Admin conserva sus permisos de administración.

## ¿Por qué tiene login y qué seguridad incluye?

El login permite comprobar quién entra al CRM. **Conocer o copiar el enlace no
es suficiente para ver ni modificar los clientes:** primero debes iniciar sesión
con una cuenta activa de Django.

Por ejemplo, si alguien abre `http://localhost:8000/clients/` sin sesión, se le
redirige al login. Si intenta enviar una solicitud directamente para crear,
editar o borrar un contacto, Django también comprueba la sesión en el servidor.
No depende solo de ocultar botones en la pantalla.

### Protecciones implementadas

- **Acceso con sesión:** el listado y las operaciones de clientes requieren
  autenticación. No hay registro público ni cuentas predeterminadas.
- **Contraseñas protegidas:** Django guarda un hash de la contraseña, no su
  texto original. Cada evaluador crea sus propias credenciales.
- **Cambios mediante POST:** escribir una URL en el navegador no ejecuta una
  creación, edición o eliminación. Esas acciones requieren enviar un formulario.
- **Protección CSRF:** los formularios incluyen un token que Django comprueba
  para ayudar a evitar solicitudes enviadas desde otro sitio sin autorización.
- **Validación en el servidor:** aunque alguien desactive JavaScript o altere el
  formulario, Django vuelve a revisar los campos antes de guardar.
- **Consultas con el ORM de Django:** las búsquedas y operaciones usan consultas
  parametrizadas, sin construir SQL con los textos ingresados por el usuario.
- **Escape de contenido:** las plantillas muestran los datos como texto para
  ayudar a evitar que contenido ingresado se ejecute como HTML o JavaScript.
- **Cierre de sesión:** invalida la sesión actual. Las páginas privadas evitan
  caché y se vuelve a comprobar el acceso al regresar desde la caché del navegador.
- **Cookie de sesión HTTP-only y SameSite:** limita su acceso desde JavaScript
  y su envío en solicitudes entre sitios. La sesión se configura para terminar
  al cerrar el navegador, aunque algunos navegadores pueden restaurarla.
- **Secretos fuera del código:** la clave de Django se configura en `.env`,
  excluido de Git, junto con la exclusión de los archivos SQLite locales.
- **Errores comprensibles:** las direcciones inexistentes y solicitudes
  rechazadas muestran una página propia, sin presentar detalles técnicos al usuario.

La confirmación de borrado y el bloqueo temporal de botones ayudan a evitar
acciones accidentales y dobles clics. **La seguridad real la aplican las
comprobaciones de Django en el servidor.**

Estas medidas no significan que el sistema tenga seguridad completa para
Internet. Actualmente cualquier cuenta activa puede gestionar todos los
contactos del CRM; no hay permisos por propietario. Django Admin sí exige sus
permisos propios. Para producción faltarían, entre otros ajustes, HTTPS,
desactivar DEBUG, un servidor de producción y limitar los intentos de login.

## Validación automática en GitHub (CI)

El repositorio tiene las ramas `main` (entrega integrada) y `desarrollo`.
Los cambios se guardan con commits descriptivos en español y se integran después
conservando su historial.

Cada push o pull request ejecuta el flujo **Validar Mini CRM**, definido en
`.github/workflows/ci.yml`. Descarga el código, prepara Python, instala las
dependencias, comprueba Django y las migraciones, ejecuta las pruebas y construye
la imagen Docker. También comprueba Django dentro de la imagen construida.
No necesitas subir `.env`: el flujo genera una clave temporal y usa una base
SQLite de pruebas independiente.

Puedes ver el resultado en la pestaña **Actions** del repositorio de GitHub.
Un resultado verde indica que terminaron correctamente las comprobaciones de
ese commit. El flujo valida la entrega; no publica la aplicación en un servidor.
El desafío no requiere despliegue a producción.

## Comprobación de instalación desde cero

El 30 de octubre de 2026 se verificó una copia limpia del repositorio, con clave,
volumen SQLite y administrador de prueba propios. Se utilizó el puerto 8001 para
no interferir con la instalación habitual del autor en 8000; la guía mantiene 8000.

- `manage.py check`: sin errores.
- Migraciones: sin cambios pendientes.
- 17 pruebas automatizadas: resultado OK.
- Pruebas HTTP: login, acceso protegido, Admin, alta, edición, búsqueda, filtro,
  rechazo de datos inválidos, eliminación, notificación y cierre de sesión correctos.
- Archivos CSS, JavaScript y animaciones disponibles por HTTP.

El CSS está organizado por componentes, con las adaptaciones de pantalla
agrupadas al final. La revisión visual de escritorio, tablet y móvil fue realizada
por el autor; la comprobación HTTP no sustituye esa revisión visual.
