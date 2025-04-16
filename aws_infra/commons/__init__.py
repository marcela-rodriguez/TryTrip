import importlib
import os
import inspect
from injector import Injector, singleton


_APP_INJECTOR = Injector()


def auto_inject_dependencies_from_directory(directory: str) -> Injector:

    # Recorrer el directorio para importar todos los módulos
    print(f"Buscando dentro del directorio ------------------- [{directory}]")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                print(file)
                # Generar el nombre del módulo basado en la ruta
                module_name = os.path.splitext(file)[0]
                module_path = f'{root.replace(os.sep, ".")}.{module_name}'

                try:
                    # Importar dinámicamente el módulo
                    module = importlib.import_module(module_path)

                    # Buscar todas las clases decoradas con @singleton e inyectarlas
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and hasattr(obj, "__scope__"):
                            print(f"::::{name}")
                            _APP_INJECTOR.get(obj)

                except Exception as e:
                    raise e

    print("Finish ..............")

    return _APP_INJECTOR

