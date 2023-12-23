import subprocess
import sys
import os
import shutil


def settingup_django(project_name, database):
    script_path = os.path.realpath(__file__)
    base_settings_path = script_path.replace("auto-django.py", 'settings.py')

    with open(base_settings_path, 'r') as file:
        settings = file.read()
        file.close()

    with open(os.path.join(script_path.replace("auto-django.py", 'utils/responder.py')), 'r') as file:
        responder = file.read()
        file.close()

    responder = responder.replace("django_base_architecture", project_name)

    with open(os.path.join(script_path.replace("auto-django.py", 'utils/responder.py')), 'w') as file:
        file.write(responder)
        file.close()

    shutil.move(script_path.replace("auto-django.py", 'utils'), os.path.join(script_path.replace("auto-django.py", project_name), 'utils'))
    shutil.move(script_path.replace("auto-django.py", 'middlewares'), os.path.join(script_path.replace("auto-django.py", project_name), project_name, "middlewares"))
    shutil.move(script_path.replace("auto-django.py", '.env'), os.path.join(script_path.replace("auto-django.py", project_name), project_name))
    shutil.move(script_path.replace("auto-django.py", 'exception.py'), os.path.join(script_path.replace("auto-django.py", project_name), project_name))
    shutil.move(script_path.replace("auto-django.py", 'exception_handler.py'), os.path.join(script_path.replace("auto-django.py", project_name), project_name))

    with open(os.path.join(script_path.replace("auto-django.py", project_name), project_name, "__init__.py"), 'w') as file:
        file.write("""from environ import Env

Env.read_env()
env = Env()
""")
        file.close()

    settings = settings.replace("django_base_architecture", project_name)

    db_config = ""
    db_default_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
    print("finding : ", settings.find(db_default_config))
    if database == 1:
        db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': env('DB_USER'),
        'HOST': env('DB_HOST'),
        'PASSWORD': env('DB_PASSWORD'),
        'NAME': env('DB_NAME'),
        'PORT': env('DB_PORT'),
    }
}"""
        settings = settings.replace(db_default_config.strip(), db_config.strip())
    elif database == 2:
        db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': env('DB_USER'),
        'HOST': env('DB_HOST'),
        'PASSWORD': env('DB_PASSWORD'),
        'NAME': env('DB_NAME'),
        'PORT': env('DB_PORT'),
    }
}"""
        settings = settings.replace(db_default_config, db_config)

    with open(os.path.join(script_path.replace("auto-django.py", project_name), f'{project_name}', 'settings.py'), 'w') as file:
        file.write(settings)
        file.close()


def create_django_project(project_name):
    subprocess.run(['django-admin', 'startproject', project_name])


def install_package_in_venv(database):
    # Replace 'path/to/your/venv' with the path to your virtual environment
    venv_path = os.path.realpath(__file__)
    venv_path = venv_path.replace("auto-django.py", "venv")


    # Activate the virtual environment
    activate_script = os.path.join(venv_path, 'Scripts' if sys.platform == 'win32' else 'bin', 'activate')
    activate_command = f'source {activate_script}' if sys.platform != 'win32' else activate_script
    activate_cmd = f'"{activate_command}" &&'
    activate_cmd = activate_cmd.replace('\\', '/')

    # Install the package using pip inside the virtual environment
    database_package = ""
    if database == 1:
        database_package = 'mysqlclient'
    elif database == 2:
        database_package = 'psycopg2'

    install_cmd = f'pip install django djangorestframework {database_package} django-environ loguru django-cors-headers flake8'

    cmd = f'{activate_cmd} {install_cmd}'
    # Run the activation command and then install the package
    subprocess.run(cmd, shell=True, check=True)
    # subprocess.run('pip install django', shell=True, check=True)


def create_python_venv(python_path):
    subprocess.run([python_path, '-m', 'venv', 'venv'])


def settingup_celery(project_name):
    script_path = os.path.realpath(__file__)
    celery_path = script_path.replace("auto-django.py", 'celery.py')

    with open(celery_path, 'r') as file:
        celery = file.read()
        celery = celery.replace("django_base_architecture", project_name)
        file.close()

    with open(celery_path, 'w') as file:
        celery = file.write(celery)
        file.close()

    shutil.move(celery_path, script_path.replace("auto-django.py", project_name), project_name)

    with open(os.path.join(script_path.replace("auto-django.py", project_name), project_name, "__init__.py"), 'w') as file:
        file.write("""from environ import Env
from .celery import app as celery_app


Env.read_env()
env = Env()

__all__ = ("celery_app", "env")
""")


if __name__ == "__main__":
    python_path = input("Enter python path for a specific Python version or press Enter for the default environment: ").strip()
    database = ""
    while isinstance(database, str):
        database = input("""Enter a number to select a DB:
                        0 or enter for default
                        1 for mysql
                        2 for postgres
                        3 for mongodb\n""").strip()
        try:
            if not database:
                database = '0'
            database = int(database)
            if database not in range(0, 4):
                print("please select a valid number(0 to 3)")
                database = ""
        except ValueError:
            print("Enter a valid integer or just press 'ENTER' for default DB configuration")
    project_name = input("Enter project name : ")
    python_path = python_path if python_path else "python"
    create_python_venv(python_path)
    install_package_in_venv(database)
    create_django_project(project_name)
    settingup_django(project_name, database)
    celery = input("Do you want celery, 'Y' for yes: ")
    if celery.lower == 'y':
        settingup_celery(project_name)
    os.remove("settings.py")
    os.remove(sys.argv[0])
