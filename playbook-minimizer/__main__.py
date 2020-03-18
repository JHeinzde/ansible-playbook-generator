import argparse
import dependency_resolver
import detect_changed_roles
import diff_calculator
import playbook_minimizer

parser = argparse.ArgumentParser(description='Playbook minimizer')
parser.add_argument("repo_path", type=str, help='Absolute path to the repository')
parser.add_argument('playbook_dir', type=str, help='The directory where the playbook is located in the repository')
parser.add_argument('branch', type=str, help='The branch on which the merge occurs')
parser.add_argument('playbook_name', type=str, help='The name of the playbook file that should be minimized')
parser.add_argument('playbook_out_path', type=str,
                    help='The path to which the minimized playbook should be written too')


def main():
    args = parser.parse_args()
    diff = diff_calculator.get_changed_files_local(args.repo_path, args.branch, args.playbook_dir)
    changed_roles = detect_changed_roles.get_changed_roles("/".join([args.repo_path, args.playbook_dir]),
                                                           diff)
    playbook_minimizer.minify_playbook(changed_roles, "/".join([args.repo_path, args.playbook_dir, args.playbook_name]),
                                       args.playbook_out_path)


if __name__ == '__main__':
    main()
