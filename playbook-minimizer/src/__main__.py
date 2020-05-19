import argparse
import os

import yaml

import detect_changed_roles
import diff_calculator
import playbook_minimizer

parser = argparse.ArgumentParser(description='Playbook minimizer')
parser.add_argument('playbook_dir', type=str, help='The directory where the playbook is located in the repository')
parser.add_argument('playbook_name', type=str, help='The name of the playbook file that should be minimized')
parser.add_argument('playbook_out_path', type=str,
                    help='The path to which the minimized playbook should be written too')
parser.add_argument('--force_roles_config_path', help='These roles will be force included in the minimized playbook',
                    type=str, required=False)


def main():
    args = parser.parse_args()
    repo_path = os.environ['CI_PROJECT_DIR']
    before_sha = os.environ['CI_COMMIT_BEFORE_SHA']
    after_sha = os.environ['CI_COMMIT_SHA']
    environment_name = os.environ['CI_ENVIRONMENT_NAME']

    if args.force_roles_config_path is not None:
        with open(args.force_roles_config_path) as f:
            force_roles = yaml.safe_load(f.read())
    else:
        force_roles = []

    diff = diff_calculator \
        .GitLabCIDiffer(repo_path, before_sha, after_sha, args.playbook_dir) \
        .get_changed_files()

    changed_roles = detect_changed_roles.get_changed_roles("/".join([repo_path, args.playbook_dir]), diff, environment_name)
    minimizer = playbook_minimizer.PlaybookMinimizer(changed_roles, "/".join(
        [repo_path, args.playbook_dir, args.playbook_name]),
                                                     args.playbook_out_path)
    minimizer.minify_playbook(force_roles)


if __name__ == '__main__':
    main()
