import os
from typing import List

from diff import get_changed_files_local
from generate_playbook import minify_playbook

def _get_abs_path(playbook_dir: str, role_dir: str):
    return "/".join([playbook_dir, role_dir])


def _resolve_all_roles(playbook_dir: str, role_dir: str, roles: List[str]):
    abs_path = _get_abs_path(playbook_dir, role_dir)
    if list(filter(lambda x: "tasks" in x or 'meta' in x or 'defaults' in x,
                   os.listdir(abs_path))):
        roles.append(role_dir)
    else:
        for r_dir in os.listdir(abs_path):
            _resolve_all_roles(playbook_dir, "/".join([role_dir, r_dir]), roles)


def get_roles_from_playbook(playbook_dir: str) -> List[str]:
    role_dir = list(filter(lambda x: 'roles' in x, os.listdir(playbook_dir)))
    role_dir = role_dir[0]  # only take this first directory that matches my criteria

    roles = []
    _resolve_all_roles(playbook_dir, role_dir, roles)

    return roles


def get_changed_roles(playbook_dir: str, changed_files: List[str]) -> List[str]:
    roles = get_roles_from_playbook(playbook_dir)
    changed_roles = []

    for file in changed_files:
        for role in roles:
            if role in file and role not in changed_roles:
                changed_roles.append(role)

    result_list = []
    for role in changed_roles:
        result_list.append(role.replace("roles/", ""))

    return result_list
