import yaml
import utils


class PlaybookMinimizer:

    def __init__(self, changed_roles, playbook_file, output_path):
        self.changed_roles = changed_roles
        self.playbook_file = utils.File(playbook_file)
        self.output_file = utils.File(output_path)

    def minify_playbook(self, roles_to_always_include):
        """
        This function takes the changed_roles and a playbook file and filters
        all roles that are not changed out of it. Then it prints it to the specified path
        """

        file_content = self.playbook_file.get_file_content()
        playbook = yaml.safe_load(file_content)

        counter = 0
        for host in playbook:
            new_roles = []
            if host['roles']:
                for role in host['roles']:
                    if role['role'] in self.changed_roles or role['role'] in roles_to_always_include:
                        new_roles.append(role)
                playbook[counter]['roles'] = new_roles
            counter += 1

        self.output_file.write_to_file(yaml.safe_dump(playbook))
