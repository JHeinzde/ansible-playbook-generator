import os
import yaml
from detect_changed_roles import get_roles_from_playbook


def get_all_dependencies(playbook_dir):
    """
    This function takes a playbook path and extracts all role dependencies
    @param playbook_dir The path to the playbook (must be absolute!)
    @return
    """
    all_roles = get_roles_from_playbook(playbook_dir)
    role_deps = {}

    for role in all_roles:
        abs_path = "/".join([playbook_dir, role, "meta", "main.yml"])
        if os.path.isfile(abs_path):
            deps = yaml.safe_load(os.open(abs_path, 'r'))
            role_deps[role] = deps

    return role_deps


def filter_roles_with_dependencies(c_roles, all_deps):
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
