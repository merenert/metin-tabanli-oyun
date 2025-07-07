import yaml
import os

BASE_DIR = os.path.dirname(__file__)

def load_items():
    with open(os.path.join(BASE_DIR, "ITEMS.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_races():
    with open(os.path.join(BASE_DIR, "RACES.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_classes():
    with open(os.path.join(BASE_DIR, "CLASSES.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)