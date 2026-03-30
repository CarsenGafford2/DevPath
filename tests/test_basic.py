import unittest
from utils.recommender import load_projects, recommend_projects

class TestDevPath(unittest.TestCase):

    # Test if JSON loads correctly
    def test_load_projects(self):
        projects = load_projects()
        self.assertIsInstance(projects, list)
        self.assertTrue(len(projects) > 0)

    # Test recommendation logic
    def test_recommend_projects(self):
        projects = load_projects()

        user_input = {
            "skill": "Python",
            "level": "Beginner",
            "interest": "General",
            "time": "Low"
        }

        results = recommend_projects(user_input, projects)

        self.assertIsInstance(results, list)
        self.assertTrue(len(results) <= 3)

        if results:
            self.assertIn("title", results[0])

    # Test empty input handling
    def test_empty_input(self):
        projects = load_projects()

        user_input = {
            "skill": "",
            "level": "",
            "interest": "",
            "time": ""
        }

        results = recommend_projects(user_input, projects)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
