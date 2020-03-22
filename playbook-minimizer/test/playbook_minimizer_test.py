import unittest

import mockito
import yaml

import playbook_minimizer
import utils


class PlaybookMinimizerTest(unittest.TestCase):

    def test_minify_playbook(self):
        mock = mockito.mock(utils.File)
        mockito.when(mock).get_file_content().thenReturn('')
        mockito.when(mock).write_to_file(mockito.ANY).thenReturn('')
        mockito.when(utils).File(mockito.ANY).thenReturn(mock)
        obj_under_test = playbook_minimizer.PlaybookMinimizer(['abc', 'hij'], '/does/not/matter', '/does/not/matter')
        mockito.when(yaml).safe_load(mockito.ANY).thenReturn(
            [{'roles': [{'role': 'abc'}, {'role': "efg"}, {'role': "hij"}]}])
        mockito.when(yaml).safe_dump(mockito.ANY).thenReturn('')

        obj_under_test.minify_playbook([])
        mockito.verify(yaml).safe_dump([{'roles': [{'role': 'abc'}, {'role': 'hij'}]}])
