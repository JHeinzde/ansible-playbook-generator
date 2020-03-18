import os
import yaml
from detect_changed_roles import get_roles_from_playbook
from typing import List, Dict


def get_all_dependencies(playbook_abs_path: str) -> Dict[str, List[str]]:
    """
    This function takes a playbook path and extracts all role dependencies
    @param playbook_abs_path The path to the playbook (must be absolute!)
    @return A map with the role name as key and a list of its dependencies as value
    """
    all_roles = get_roles_from_playbook(playbook_abs_path)
    role_deps = {}

    for role in all_roles:
        abs_path = "/".join([playbook_abs_path, role, "meta", "main.yml"])
        if os.path.isfile(abs_path):
            deps = yaml.safe_load(open(abs_path, 'r'))
            role_deps[role] = deps

    return role_deps


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
