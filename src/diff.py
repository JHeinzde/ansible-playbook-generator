import git as git
import tempfile as tempfile


def _get_remote_repo(remote_url):
    """
    This function creates a new tmp directory and pulls an origin to that directory.
    After that it creates a Repo object and returns it to the caller
    @param remote_url The url of the repository that should be pulled
    @returns A repo object referencing this repository
     """

    tmp_dir = tempfile.mkdtemp()
    repo = git.Repo(tmp_dir)
    origin = repo.create_remote('origin', remote_url)
    origin.pull()
    return repo


def _get_local_repo(repo_dir):
    """
    This function creates a git Repo object from the provided path
    @param repo_dir The path to the desired repository
    """
    return git.Repo(repo_dir)


def _get_branch_head(repo, branch):
    """
    This function returns the head of a branch from the given repository
    @param repo The repository which contains the branch
    @param branch The branch for which the head should be returned
    """
    return repo.heads[branch]


def _get_changed_files(repo, src_branch, target_branch, playbook_dir):
    """
    This function calculates the changed files between to branches inside the provided playbook directory
    @param repo The repository, that contains the provided branches
    @param src_branch The source branch for the calculation(the branch you intend to merge)
    @param target_branch The target branch for the diff calculation(the branch you intend to merge into)
    @param playbook_dir The directory where the playbook and its roles/vars etc. are contained.
                        The diff calculation is only done for this directory
    """

    src_head = _get_branch_head(repo, src_branch)
    target_head = _get_branch_head(repo, target_branch)

    diffs = src_head.commit.tree.diff(target_head.commit.tree, playbook_dir)
    changed_files = []
    for diff in diffs:
        if diff.renamed_file:
            changed_files.append(diff.renamed_to)
        else:
            changed_files.append(diff.a_path)
    return changed_files


def get_changed_files_local(repo_dir, src_branch, target_branch, playbook_dir):
    """
    This function calculates the changed files between to branches inside the provided playbook directory
    @param repo_dir The directory of the repository, that contains the provided branches
    @param src_branch The source branch for the calculation(the branch you intend to merge)
    @param target_branch The target branch for the diff calculation(the branch you intend to merge into)
    @param playbook_dir The directory where the playbook and its roles/vars etc. are contained.
                        The diff calculation is only done for this directory
    """

    repo = _get_local_repo(repo_dir)
    return _get_changed_files(repo, src_branch, target_branch, playbook_dir)


def get_changed_files_remote(repo_url, src_branch, target_branch, playbook_dir):
    """
    This function calculates the changed files between to branches inside the provided playbook directory
    @param repo_url The url of the repository, that contains the provided branches
    @param src_branch The source branch for the calculation(the branch you intend to merge)
    @param target_branch The target branch for the diff calculation(the branch you intend to merge into)
    @param playbook_dir The directory where the playbook and its roles/vars etc. are contained.
                        The diff calculation is only done for this directory
    """
    repo = _get_remote_repo(repo_url)
    return _get_changed_files(repo, src_branch, target_branch, playbook_dir)
