def create_project_init(path, celery):
    init_content = """from environ import Env


Env.read_env()
env = Env()
"""
    if celery.lower() == 'y':
        init_content = """from environ import Env
from .celery import app as celery_app


Env.read_env()
env = Env()

__all__ = ("celery_app", "env")
"""

    with open(path, 'w') as file:
        file.write(init_content)
