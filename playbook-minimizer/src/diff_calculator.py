from abc import ABC
from abc import abstractmethod
from typing import List

import git as git


class Differ(ABC):

    @abstractmethod
    def _get_repo(self, repo_url):
        pass

    @abstractmethod
    def get_changed_files(self):
        pass


class GitLabCIDiffer(Differ):

    def __init__(self, repo_dir: str, before_commit: str, after_commit: str, playbook_dir: str):
        self._repo = self._get_repo(repo_dir)
        self._before_commit = before_commit
        self._after_commit = after_commit
        self._playbook_dir = playbook_dir

    def _get_repo(self, repo_url: str) -> git.Repo:
        return git.Repo(repo_url)

    def get_changed_files(self) -> List[str]:
        before = self._repo.commit(self._before_commit)
        after = self._repo.commit(self._after_commit)

        diffs = before.diff(after, self._playbook_dir)
        changed_files = []
        for diff in diffs:
            if diff.renamed_file:
                changed_files.append(diff.renamed_to)
            else:
                changed_files.append(diff.a_path)
        return changed_files
