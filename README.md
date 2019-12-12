# What does this do

This is a simple tool, that checks your ansible-playbook has any changes,
and generates a minimal playbook, that only includes changed roles including their dependencies.
For this the command git diff is used and then the files inside the playbook structure are parsed.

# Why this tool? 

Because it decreases the time to test ansible code. 


# Disclaimer

I do not garantuee you that this code works or is any good.