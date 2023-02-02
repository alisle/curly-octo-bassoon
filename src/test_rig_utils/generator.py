import random
import os

from model import APIType

_name_generator_first_names = None
_name_generator_last_names = None
_name_generator_domains = None
_name_generator_loaded = False


def _name_generator_load_files():   
    global _name_generator_first_names
    global _name_generator_last_names
    global _name_generator_domains
    global _name_generator_loaded

    with open(os.path.join(os.path.dirname(__file__), 'first_names.txt')) as first_names:         
        _name_generator_first_names =  first_names.readlines()
    
    with open(os.path.join(os.path.dirname(__file__), 'last_names.txt')) as last_names:         
        _name_generator_last_names =  last_names.readlines()

    with open(os.path.join(os.path.dirname(__file__), 'domains.txt')) as domains:         
        _name_generator_domains =  domains.readlines()

    _name_generator_loaded = True

def create_name() -> str:
    global _name_generator_first_names
    global _name_generator_last_names
    global _name_generator_loaded

    if not _name_generator_loaded:
        _name_generator_load_files()
    

    first_name = random.choice(_name_generator_first_names).strip()
    second_name = random.choice(_name_generator_last_names).strip()

    return f"{first_name} {second_name}"

def create_email(full_name : str) -> str:
    global _name_generator_domains
    global _name_generator_loaded

    if not _name_generator_loaded:
        _name_generator_load_files()

    names = full_name.lower().split(" ", 1)
    domain = random.choice(_name_generator_domains).strip()

    return f"{names[0]}.{names[1]}@{domain}"
    

def create_name_email() -> dict:
    name = create_name()
    email = create_email(name)

    return { "display_name" : name, "email_address": email}

def get_api_name() -> APIType:
    api = random.choice(list(APIType))
    return api
