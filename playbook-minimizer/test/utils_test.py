import os
import unittest
from mockito import mockito
import utils


class UtilsTest(unittest.TestCase):

    def test_get_abs_path(self):
        result = utils.get_abs_path('/opt/test', 'lol')

        self.assertEqual('/opt/test/lol', result)

    def test_resolve_all_roles(self):
        self.setup_mocks_for_resolve_all_roles()
        actual_roles = []
        utils.resolve_all_roles('/opt/test', 'roles', actual_roles)

        self.assertEqual(['roles/ok', 'roles/abc', 'roles/def'], actual_roles)

    def test_get_all_roles_from_playbook(self):
        mockito.when(os).listdir('/opt/test').thenReturn(['roles', 'does_not_matter', 'should_not_be_detected'])
        self.setup_mocks_for_resolve_all_roles()
        actual_roles = utils.get_roles_from_playbook('/opt/test')

        self.assertEqual(['roles/ok', 'roles/abc', 'roles/def'], actual_roles)

    @staticmethod
    def setup_mocks_for_resolve_all_roles():
        mockito.when(os).listdir('/opt/test/roles').thenReturn(['ok', 'abc', 'def', 'no_role'])
        mockito.when(os).listdir('/opt/test/roles/ok').thenReturn(['meta'])
        mockito.when(os).listdir('/opt/test/roles/abc').thenReturn(['tasks'])
        mockito.when(os).listdir('/opt/test/roles/def').thenReturn(['defaults'])
        mockito.when(os).listdir('/opt/test/roles/no_role').thenReturn(['grgrlmpf'])
        mockito.when(os).listdir('/opt/test/roles/no_role/grgrlmpf').thenReturn([])


if __name__ == '__main__':
    unittest.main()
