import os
from typing import List


def get_abs_path(playbook_abs_path: str, role_dir: str) -> str:
    return "/".join([playbook_abs_path, role_dir])


def resolve_all_roles(playbook_abs_path: str, role_dir: str, roles: List[str]):
    abs_path = get_abs_path(playbook_abs_path, role_dir)
    if list(filter(lambda x: "tasks" in x or 'meta' in x or 'defaults' in x,
                   os.listdir(abs_path))):
        roles.append(role_dir)
    else:
        for r_dir in os.listdir(abs_path):
            resolve_all_roles(playbook_abs_path, "/".join([role_dir, r_dir]), roles)


def get_roles_from_playbook(playbook_abs_path: str) -> List[str]:
    """
    This function takes an absolute path to a playbook and extracts all roles from the playbook
    @param playbook_abs_path The absolute path to the playbook
    @return A list containing all roles inside the roles directory in the playbook
    """
    role_dir = list(filter(lambda x: 'roles' in x, os.listdir(playbook_abs_path)))
    role_dir = role_dir[0]  # only take the first directory that matches my criteria

    roles = []
    resolve_all_roles(playbook_abs_path, role_dir, roles)

    return roles


class File:
    def __init__(self, file_name):
        self.file = open(file_name, 'r+')

    def __del__(self):
        self.file.close()

    def get_file_content(self):
        return self.file.read()

    def write_to_file(self, content):
        self.file.write(content)
