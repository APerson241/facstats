import os
import sys
sys.path.append('./facstats' + '.' if 'tests/' not in __file__ else '')
import app
import unittest

class IndexTestCase(unittest.TestCase):
	def setUp(self):
		self.app = app.app.test_client()

	def testRoot(self):
		response = self.app.get('/')
		assert len(response.data) > 0

if __name__ == '__main__':
    unittest.main()
