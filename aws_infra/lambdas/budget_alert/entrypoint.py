from typing import Dict, Any


def handler(event: Dict[str, Any], context: Dict[str, Any]):
    print("Running ...")
    print("Event: ")
    print(event)
    print("Context:")
    print(context)