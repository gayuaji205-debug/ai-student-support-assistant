import unittest
from pathlib import Path

from main import answer_query, load_documents, search_documents


class StudentSupportAssistantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = load_documents(
            Path(__file__).resolve().parent / "student_data.txt"
        )

    def test_loads_resources(self):
        self.assertIn("Exam Schedule", self.documents)
        self.assertIn("Student Guidelines", self.documents)

    def test_finds_exam_schedule(self):
        results = search_documents("What is the exam schedule?", self.documents)
        self.assertEqual(results[0][1], "Exam Schedule")

    def test_returns_helpful_answer(self):
        response = answer_query("library timings", self.documents)
        self.assertIn("Monday to Saturday", response)

    def test_handles_unknown_question(self):
        response = answer_query("campus weather tomorrow", self.documents)
        self.assertIn("could not find", response.lower())


if __name__ == "__main__":
    unittest.main()