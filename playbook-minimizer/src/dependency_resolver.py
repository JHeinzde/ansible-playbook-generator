import os
from typing import List, Dict

import yaml

import utils


class DependencyResolver():

    def __init__(self, playbook_abs_path):
        self.playbook_abs_path = playbook_abs_path

    def get_all_dependencies(self) -> Dict[str, List[str]]:
        """
        This function takes a playbook path and extracts all role dependencies
        @param playbook_abs_path The path to the playbook (must be absolute!)
        @return A map with the role name as key and a list of its dependencies as value
        """
        all_roles = utils.get_roles_from_playbook(self.playbook_abs_path)
        role_deps = {}

        for role in all_roles:
            abs_path = utils.get_abs_path(self.playbook_abs_path, role, "meta", "main.yml")
            if os.path.isfile(abs_path):
                deps = yaml.safe_load(open(abs_path, 'r'))
                role_deps[role] = deps

        return role_deps
