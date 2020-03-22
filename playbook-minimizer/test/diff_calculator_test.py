import unittest

import git
import mockito

from diff_calculator import GitLabCIDiffer


class DiffCalculatorTest(unittest.TestCase):

    def test_ci_diff(self):
        mock_repo = mockito.mock(git.Repo)
        mock_commit_a = mockito.mock(git.Commit)
        mock_commit_b = mockito.mock(git.Commit)
        mock_diff_one = mockito.mock(git.Diff)
        mock_diff_two = mockito.mock(git.Diff)

        mockito.when(mock_repo).commit('this_is_a_test_commit').thenReturn(mock_commit_a)
        mockito.when(mock_repo).commit('this_is_a_second_test_commit').thenReturn(mock_commit_b)

        mock_diff_one.renamed_file = False
        mock_diff_one.a_path = 'testerino'
        mock_diff_two.renamed_file = True
        mock_diff_two.renamed_to = 'test'
        mockito.when(mock_commit_a).diff(mock_commit_b, 'test_playbook').thenReturn([mock_diff_one, mock_diff_two])
        mockito.when(git).Repo('test_repo').thenReturn(mock_repo)

        differ_under_test = GitLabCIDiffer('test_repo', 'this_is_a_test_commit', 'this_is_a_second_test_commit',
                                           'test_playbook')

        actual_changed_files = differ_under_test.get_changed_files()

        self.assertEqual(['testerino', 'test'], actual_changed_files)
