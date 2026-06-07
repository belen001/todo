# 📝 App de Tareas Minimalista (Flask)

Esta es una aplicación web minimalista de lista de tareas (Todo App) construida con **Python** y **Flask** (en el backend) y **HTML/CSS/JS** moderno y responsivo (en el frontend).

Está diseñada específicamente para ser **autocontenida, simple de entender y fácil de desplegar** en cualquier plataforma de nube.

---

## 🚀 Cómo ejecutarla localmente

### Opción A: Ejecutar con Python directamente

1. **Clonar o descargar** este repositorio.
2. **Crear un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows para activarlo:
   .\venv\Scripts\activate
   # En macOS/Linux para activarlo:
   source venv/bin/activate
   ```
3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```
5. Abre en tu navegador: [http://localhost:5000](http://localhost:5000)

---

### Opción B: Ejecutar con Docker

Si tienes Docker instalado en tu máquina, puedes construir y correr la aplicación en un contenedor aislado:

1. **Construir la imagen de Docker**:
   ```bash
   docker build -t todo-flask .
   ```
2. **Correr el contenedor**:
   ```bash
   docker run -d -p 5000:5000 --name todo-app todo-flask
   ```
3. Abre en tu navegador: [http://localhost:5000](http://localhost:5000)

---

## ☁️ Guía de Despliegue en la Nube

Aquí tienes tres opciones sumamente sencillas (y con planes gratuitos o de bajo costo) para publicar tu aplicación en Internet:

### Opción 1: Render (Recomendado y muy sencillo)
[Render](https://render.com/) es una plataforma excelente para desplegar aplicaciones web directamente desde GitHub.

1. Sube tu código a un repositorio público o privado en **GitHub**.
2. Regístrate en Render y haz clic en **New +** > **Web Service**.
3. Conecta tu cuenta de GitHub y selecciona el repositorio de esta app.
4. Configura los siguientes campos:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py` (o `gunicorn main:app` si instalas gunicorn)
5. Haz clic en **Deploy Web Service** ¡y listo! Render te dará una URL pública tipo `https://tu-app.onrender.com`.

### Opción 2: Railway
[Railway](https://railway.app/) detectará automáticamente tu `Dockerfile` y desplegará la app sin configuraciones complejas.

1. Sube el código a **GitHub**.
2. Inicia sesión en Railway, haz clic en **New Project** y selecciona **Deploy from GitHub repo**.
3. Selecciona tu repositorio.
4. Railway leerá el `Dockerfile` automáticamente, compilará la imagen y desplegará tu app en un par de minutos.

### Opción 3: PythonAnywhere
[PythonAnywhere](https://www.pythonanywhere.com/) está especializado en Python y es ideal si quieres un entorno tradicional sin depender de Docker.

1. Regístrate en PythonAnywhere (cuenta gratuita).
2. Ve a la pestaña **Files** y sube tu `main.py` y `requirements.txt`.
3. Abre una consola (**Consola Bash**) en su panel e instala las dependencias: `pip install --user -r requirements.txt`.
4. Ve a la pestaña **Web**, crea una nueva app web de tipo **Manual Configuration** eligiendo la versión de Python que usaste.
5. Configura el archivo WSGI (te dan un enlace para editarlo) para que apunte a tu app:
   ```python
   import sys
   path = '/home/tu_usuario/todo' # Reemplaza con la ruta de tu proyecto
   if path not in sys.path:
       sys.path.append(path)
   from main import app as application
   ```
6. Recarga la app web desde el panel ¡y visita tu sitio!