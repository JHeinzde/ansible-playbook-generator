import unittest

import diff_calculator_test
import playbook_minimizer_test
import utils_test


def main():
    test_loader = unittest.TestLoader()
    suite = test_loader.loadTestsFromTestCase(playbook_minimizer_test.PlaybookMinimizerTest)
    suite.addTests(test_loader.loadTestsFromTestCase(utils_test.UtilsTest))
    suite.addTests(test_loader.loadTestsFromTestCase(diff_calculator_test.DiffCalculatorTest))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    main()
