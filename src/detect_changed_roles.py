import os
from typing import List


def _get_abs_path(playbook_abs_path: str, role_dir: str) -> str:
    return "/".join([playbook_abs_path, role_dir])


def _resolve_all_roles(playbook_abs_path: str, role_dir: str, roles: List[str]):
    abs_path = _get_abs_path(playbook_abs_path, role_dir)
    if list(filter(lambda x: "tasks" in x or 'meta' in x or 'defaults' in x,
                   os.listdir(abs_path))):
        roles.append(role_dir)
    else:
        for r_dir in os.listdir(abs_path):
            _resolve_all_roles(playbook_abs_path, "/".join([role_dir, r_dir]), roles)


def get_roles_from_playbook(playbook_abs_path: str) -> List[str]:
    """
    This function takes an absolute path to a playbook and extracts all roles from the playbook
    @param playbook_abs_path The absolute path to the playbook
    @return A list containing all roles inside the roles directory in the playbook
    """
    role_dir = list(filter(lambda x: 'roles' in x, os.listdir(playbook_abs_path)))
    role_dir = role_dir[0]  # only take this first directory that matches my criteria

    roles = []
    _resolve_all_roles(playbook_abs_path, role_dir, roles)

    return roles


def get_changed_roles(playbook_abs_path: str, changed_files: List[str]) -> List[str]:
    """
    This function takes an absolute path to a playbook and a list of changed_files in the repository of the playbook.
    Using these parameter the function calculates the changed roles inside the playbook.
    @param playbook_abs_path The absolute path to the playbook
    @param changed_files A list of changed files from the playbook repo
    """
    roles = get_roles_from_playbook(playbook_abs_path)
    changed_roles = []

    for file in changed_files:
        for role in roles:
            if role in file and role not in changed_roles:
                changed_roles.append(role)

    result_list = []
    for role in changed_roles:
        result_list.append(role.replace("roles/", ""))

    return result_list
