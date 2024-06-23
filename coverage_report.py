import coverage
import unittest


cov = coverage.Coverage()
cov.start()
try:
    unittest.main(module='tests.test_localdb')
finally:
    cov.stop()
    cov.save()
    print("\nCoverage Report:")
    cov.report()
