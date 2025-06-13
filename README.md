# Sistema de Gestión de Biblioteca con Django

[![Django](https://img.shields.io/badge/Django-3.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

Este proyecto es un sistema de gestión de biblioteca desarrollado con Django como parte de una prueba técnica. Implementa todas las funcionalidades requeridas.

## Características principales

- ✅ Modelos para Libros, Usuarios y Registros de Préstamos
- ✅ Vistas basadas en clases para todas las operaciones
- ✅ Control de acceso por roles (Usuario regular / Administrador)
- ✅ Sistema de préstamos y devoluciones de libros
- ✅ Interfaz profesional con Bootstrap 5
- ✅ Autenticación de usuarios
- ✅ Documentación completa del código

## Requisitos del sistema

- Python 3.8+
- Django 3.2+
- pip

## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. **Clonar el repositorio**:
    git clone https://github.com/tu-usuario/library-management.git
    cd library-management


2. **Crear un entorno virtual** :
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  

3. **Instalar dependencias**:


    pip install -r requirements.txt


4. **Generar la base de datos**

    python manage.py migrate

5. **Ejecutar el servidor de desarrollo**:

    python manage.py runserver