# What does this do

This is a simple tool, that checks your ansible-playbook has any changes,
and generates a minimal playbook, that only includes changed roles including their dependencies.
For this the command git diff is used and then the files inside the playbook structure are parsed.

# Expected structure

This tool expects the playbooks to be in a certain structure. This makes detecting roles and variables much easier.

Roles are expected to be in a toplevel directory of the playbook. The directory housing these roles should also contain
the string "roles". Host variables(variables added via the vars directive in a playbook) should be housed on ia toplevel
directory with the name "vars". The structure of the directory can be flat or deep, both are resolved until all files are 
found.

Component roles(Roles that are only used as dependencies and never directly in a playbook) should be housed in a directory
called "components" in the "roles" directory. These roles are treated differently than normal roles and should be handled
with special care. 

The tool uses a cli interface to get the needed variables. Maybe in the future custom playbook structur can be defined 
a yaml file.

# Why this tool? 

Because it decreases the time to test/deploy changes of ansible code.

# Disclaimer

I do not garantuee you that this code works or is any good.
