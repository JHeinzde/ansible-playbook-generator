import os
from typing import List, Dict


def get_abs_path(playbook_abs_path: str, *sub_dirs) -> str:
    return "/".join([playbook_abs_path, *sub_dirs])


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


def get_component_roles(changed_roles: List[str]) -> (List[str], List[str]):
    """
    Takes a list of changed roles and returns all the component roles contained.
    @param changed_roles All changed roles.
    """
    result = []
    for role in changed_roles:
        if 'component' in role:
            result.append(role)

    for role in result:
        changed_roles.remove(role)

    return result, changed_roles


def filter_roles_with_dependencies(c_roles: List[str], all_deps: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    If there are changes in roles that are never used directly by a playbook, but only other roles,
    this method can get the list of roles that depend on these "component" roles.
    @param c_roles A list of component roles that are only used by other roles
    @param all_deps A map of every role and its dependencies
    """
    dependent_roles = {}

    for c_role in c_roles:
        for role, deps in all_deps:
            for dep in deps:
                if dep["role"] in c_role:
                    dependent_roles.setdefault(c_role, [])
                    dependent_roles[c_role].append(dep["role"])

    return dependent_roles


class File:
    def __init__(self, file_name):
        if os.path.exists(file_name):
            self.file = open(file_name, 'r+')
        else:
            self.file = open(file_name, 'w+')

    def get_file_content(self):
        return self.file.read()

    def write_to_file(self, content):
        self.file.write(content)
