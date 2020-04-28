import glob
import re
from typing import List

import yaml

import dependency_resolver
import utils


def _detect_changed_vars_files(changed_files: List[str]) -> List[str]:
    changed_var_files = []

    for file in changed_files:
        if "vars" in file:
            changed_var_files.append(file)

    return changed_var_files


def _detect_changed_config_files(changed_files: List[str]) -> List[str]:
    changed_config_files = []

    for file in changed_files:
        if "configuration/" in file:
            changed_config_files.append(file)

    return changed_config_files


def _detect_changed_service_roles_from_config_files(changed_config_files: List[str], roles: List[str]) -> List[str]:
    changed_services = []
    changed_service_roles = []
    for changed_config_file in changed_config_files:
        match = re.search("configuration/(.*?)/", changed_config_file)
        if match:
            service_name_without_prefix = match.group(1)  # get the name of the service
            service_name = "tos-" + service_name_without_prefix
            changed_services.append(service_name)

    for changed_service in changed_services:
        for role in roles:
            if changed_service in role:
                changed_service_roles.append(role)
    return changed_service_roles


def _load_vars_files(changed_vars: List[str], playbook_abs_path: str) -> List[str]:
    var_names = []
    for file in changed_vars:
        abs_path = "/".join([playbook_abs_path, file.replace("tos-install/", "")])
        l_file = yaml.safe_load(open(abs_path, 'r'))
        for key in l_file.keys():
            var_names.append(key)

    return var_names


def _compile_regexes(var_names: List[str]):
    patterns = set([])
    for var in var_names:
        patterns.add(re.compile(r".*{{.*" + var + r".*}}.*", re.DOTALL))

    return patterns


def _detect_changed_roles_from_vnames(var_names: List[str], playbook_abs_path: str):
    roles = utils.get_roles_from_playbook(playbook_abs_path)
    changed_roles = []

    patterns = _compile_regexes(var_names)

    for role in roles:
        abs_path = utils.get_abs_path(playbook_abs_path, role)
        role_files = [f for f in glob.glob(utils.get_abs_path(abs_path, "**/*.yml"), recursive=True)]
        for f in glob.glob(utils.get_abs_path(abs_path, "**/*.j2"), recursive=True):
            role_files.append(f)

        for role_file in role_files:
            f = open(role_file, 'r')
            lines = f.read()
            for pattern in patterns:
                if pattern.match(lines):
                    changed_roles.append(role)
            f.close()

    return list(set(changed_roles))


def get_changed_roles(playbook_abs_path: str, changed_files: List[str]) -> List[str]:
    """
    This function takes an absolute path to a playbook and a list of changed_files in the repository of the playbook.
    Using these parameter the function calculates the changed roles inside the playbook.
    @param playbook_abs_path The absolute path to the playbook
    @param changed_files A list of changed files from the playbook repo
    """
    roles = utils.get_roles_from_playbook(playbook_abs_path)
    changed_roles = []

    for file in changed_files:
        for role in roles:
            if role in file and role not in changed_roles:
                changed_roles.append(role)

    changed_config_files = _detect_changed_config_files(changed_files)
    changed_service_roles = _detect_changed_service_roles_from_config_files(changed_config_files, roles)

    for changed_service_role in changed_service_roles:
        if changed_service_role not in changed_roles:
            changed_roles.append(changed_service_role)

    component_roles, changed_roles = utils.get_component_roles(changed_roles)
    deps = dependency_resolver.DependencyResolver(playbook_abs_path).get_all_dependencies()
    c_changed_roles = utils.filter_roles_with_dependencies(component_roles, deps)

    for changed_role in c_changed_roles:
        changed_roles.append(changed_role)

    result_list = []
    for role in changed_roles:
        result_list.append(role.replace("roles/", ""))

    vars_files = _detect_changed_vars_files(changed_files)
    var_names = _load_vars_files(vars_files, playbook_abs_path)
    v_changed = _detect_changed_roles_from_vnames(var_names, playbook_abs_path)

    for role in v_changed:
        result_list.append(role.replace("roles/", ""))

    return list(set(result_list))
