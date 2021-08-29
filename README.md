# Web Services Libros

Esta aplicación se realizó con la finalidad de crear una Web Service en Python con la API REST de Django

# **Instalación**

### **Paso 1**

**Forma 1:** Dar clic en **Code**, luego **Download Zip** y descomprimir el archivo en tu ordenador.

**Forma 2:** Abrir una terminal en tu ordenador y ejecutar el siguiente comando:

    https://github.com/CarlosAlmeida2000/ws_biblioteca.git

### **Paso 2**

Descargar e instalar [**Python**](https://www.python.org/downloads/)

### **Paso 3**

Instalar Django ejecutando el siguente comando en la consola de tu ordenador, para más información [**click aquí.**](https://docs.djangoproject.com/en/3.2/)

    pip install django==3.0.8

### **Paso 3**

Instalar la API para utilizar peticiones **REST** en Django Python, ejecutar el siguiente comando en la consola de tu ordenador y para más información [**click aquí.**](https://www.django-rest-framework.org/)

    pip install djangorestframework

### **Paso 4**

Instalar el controlador de la conexión de PostgreSQL ejecutando el siguiente comando en la consola de tu ordenador.

    pip install psycopg2 ==2.8.6

### **Paso 5**

-   **Primero:** Configurar la conexión de la base de datos en el archivo **setting.py** de la carpeta **../vw_bilioteca**

-   **Segundo:** Ejecutar el siguiente comando en consola:

          python manage.py migrate

### **Paso 6**

Instalar la libreria **requests**, ejecutando el siguente comando en consola:

    pip install requests

Consumir las aplicaciones

-   **Primero:** Ejecutar la aplicación de WebService, abriendo la terminal en la carpeta **../vw_biblioteca** y ejecutar el siguiente comando en consola:

          python manage.py runserver
