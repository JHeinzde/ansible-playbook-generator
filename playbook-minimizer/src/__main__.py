import argparse
import os

import detect_changed_roles
import diff_calculator
import playbook_minimizer

parser = argparse.ArgumentParser(description='Playbook minimizer')
parser.add_argument('playbook_dir', type=str, help='The directory where the playbook is located in the repository')
parser.add_argument('playbook_name', type=str, help='The name of the playbook file that should be minimized')
parser.add_argument('playbook_out_path', type=str,
                    help='The path to which the minimized playbook should be written too')


def main():
    args = parser.parse_args()
    repo_path = os.environ['CI_PROJECT_DIR']
    before_sha = os.environ['CI_COMMIT_BEFORE_SHA']
    after_sha = os.environ['CI_COMMIT_SHA']

    diff = diff_calculator \
        .GitLabCIDiffer(repo_path, before_sha, after_sha, args.playbook_dir) \
        .get_changed_files()

    changed_roles = detect_changed_roles.get_changed_roles("/".join([repo_path, args.playbook_dir]), diff)
    minimizer = playbook_minimizer.PlaybookMinimizer(changed_roles, "/".join(
        [repo_path, args.playbook_dir, args.playbook_name]),
                                                     args.playbook_out_path)
    minimizer.minify_playbook()


if __name__ == '__main__':
    main()
