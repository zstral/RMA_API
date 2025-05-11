- Documentación del proyecto -

**** Se usó un entorno virtual por lo que se deben instalar los siguientes paquetes ****

-Django 5.1.7
-djangorestframework 3.16.0
-oracledb 3.1.0

1- Antes de iniciar el proyecto se debe configurar correctamente el settings.py con las credeciales correspondientes en un archivo .env
(Se usó Oracle "Thick Mode" para la conexión a la base de datos usando un wallet.)
2- Crear las migraciones.
3- Una vez hecha las migraciones se debe usar el "sql script.sql" para el poblado de las tablas utilizando el gestor de base de datos de tu preferencia.
4- Terminado los pasos anteriores se puede proceder a correr el servidor.

A - Dentro de la página no podrás acceder a la función Dashboard y API al menos que crees una cuenta de usuario.
(Las cuentas de usuario creadas se asocian a la tabla UserProfile con un rol por defecto de User)

A.1 - Para consumir la API debes tener un usuario (user) y usar una herramienta de preferencia para las solicitudes GET y POST.
Al crear la solicitud debes hacerlo en formato JSON indicando tus credenciales para obtenr un token que expira en 5 min, luego al obtener tu token puedes usar las solicitudes GET ingresando un Header Name(Authorization) y un Header Value("Token").

B - Si deseas acceder al Dashboard Admin debes crear una cuenta con rol Admin siguiendo estos pasos.
(Esta función no está pensada para el usuario final.)

1- Abre la consola y ejecuta py manage.py shell
2- Importa estos módulos 
    from django.contrib.auth.models import User
    from core.models import UserProfile
3- Finalmente escribe este código y cambia los valores con # a tu preferencia.

    user = User.objects.create_user(
    username='...', #Nombre de usuario
    email='admin@ejemplo.com', #Correo
    password='Admin1234!' #Contraseña
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()
    UserProfile.objects.create(
        user=user,
        nombre='Administrador', #Nombre
        rol='admin'
    )
    exit()
4 - Ahora puedes acceder al menú especial de administradores en RPM accediendo con las credenciales creadas.