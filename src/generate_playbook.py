import yaml


def minify_playbook(changed_roles, playbook_file, output_path):
    """
    This function takes the changed_roles and a playbook file and filters
    all roles that are not changed out of it. Then it prints it to the specified path
    @param changed_roles A list of changed roles in this merge request
    @param playbook_file The path to the playbook that should be minified
    @param output_path The path where the minified playbook should be written too
    """

    playbook = yaml.safe_load(open(playbook_file, 'r'))
    counter = 0
    for host in playbook:
        new_roles = []
        for role in host['roles']:
            if role['role'] in changed_roles:
                new_roles.append(role)
        playbook[counter]['roles'] = new_roles
        counter += counter

    yaml.safe_dump(playbook, open(output_path, 'w'))
