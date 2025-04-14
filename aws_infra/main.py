import injector
import commons
import apps

def build_hadar_app() -> injector.Injector:
    return commons.auto_inject_dependencies_from_directory(directory="apps")

injector = build_hadar_app()
app = injector.get(apps.SBApp)
app.synth()
