import unittest
from utils.recommender import load_projects, recommend_projects


class TestDevPath(unittest.TestCase):

    def setUp(self):
        # Load project data before each test
        self.projects = load_projects()

    # Test 1: Check if projects are loaded correctly
    def test_load_projects(self):
        self.assertIsInstance(self.projects, list)
        self.assertGreater(len(self.projects), 0, "Projects list should not be empty")

    # Test 2: Check recommendation logic returns valid results
    def test_recommend_projects(self):
        user_input = {
            "skill": "Python",
            "level": "Beginner",
            "interest": "General",
            "time": "Low"
        }

        results = recommend_projects(user_input, self.projects)

        # Check type
        self.assertIsInstance(results, list)

        # Should return max 3 results
        self.assertLessEqual(len(results), 3)

        # Validate structure if results exist
        if results:
            project = results[0]
            self.assertIn("title", project)
            self.assertIn("description", project)

    # Test 3: Ensure empty input returns no results
    def test_empty_input(self):
        user_input = {
            "skill": "",
            "level": "",
            "interest": "",
            "time": ""
        }

        results = recommend_projects(user_input, self.projects)

        self.assertEqual(results, [])

    # Test 4: Invalid skill should return empty list
    def test_invalid_skill(self):
        user_input = {
            "skill": "InvalidSkill",
            "level": "Beginner",
            "interest": "General",
            "time": "Low"
        }

        results = recommend_projects(user_input, self.projects)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
