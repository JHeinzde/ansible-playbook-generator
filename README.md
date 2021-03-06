# What is this ?

This is a minimizer for ansible playbooks, designed to make deployment runs as short as possible. Since
we run our ansible playbooks in a CI, runtimes can go up to 40-50 minutes, which is not always desired.
To combat this, I wrote a tool that analyzes a git diff and detect changed roles. With these it minimizes the given ansible
playbook to only include these changed roles.

The order of the roles in the original playbook is preserved.

# Usage

Currently this tool can only be used in GitLab CI on merge requests. It reads the environment variables
CI_PROJECT_DIR, CI_COMMIT_BEFORE_SHA and CI_COMMIT_SHA and uses them with the command line arguments you provide,
to calculate the changed roles. A sample call for this would be
```bash
./playbook-minimizer --force_roles_config_path=<path-to-a-file-including-roles-to-force-include> <directory-of-the-git-repo-that-contains-the-playbook> <playbook-name> <out_path-and-name-of-new-playbook>
```
The last argument is a path to a YAML config! It is a simple file with this structure
````yaml
- role1
- role2
- role3
````
