import diff_calculator


def main():
    changed_files = diff_calculator.get_changed_files_local(
        "/home/jonathan/Arbeit/TASTE-OS/ansible/tos-ansible-playbooks"
        , "feature/3.15.0/grafana-basic-alarming", "3.15.2", "tos-install")
    changed_vars = detect._detect_changed_vars_files(changed_files)
    var_names = detect._load_vars_files(changed_vars, "/home/jonathan/Arbeit/TASTE-OS/ansible/tos-ansible-playbooks")
    changed_roles = detect._detect_changed_roles_from_vnames(var_names,
                                                             "/home/jonathan/Arbeit/TASTE-OS/ansible/tos-ansible-playbooks/tos-install")
    print(var_names)
    print(changed_roles)


if __name__ == '__main__':
    main()
