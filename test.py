from pathlib import Path

# print(f"Current directory: {Path.cwd()}")
# print(f"Home directory: {Path.home()}")


path = Path(__file__)
print(path)

parent = path.parent
print(parent)

home = path.parent.parent
print(home)


import os

script_path = os.path.dirname(__file__)
