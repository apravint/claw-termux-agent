import unittest
from clawagent.scraper import extract_markdown
from clawagent.searcher import search_web
from clawagent.daemon import run_daemon_task, get_daemon_logs

class TestClawTermuxAgent(unittest.TestCase):

    def test_extract_markdown(self):
        sample_html = "<html><head><title>Test Page</title></head><body><h1>Welcome</h1><p>This is a test paragraph for scraping content verification.</p></body></html>"
        res = extract_markdown(sample_html, "https://example.com")
        self.assertEqual(res["title"], "Test Page")
        self.assertIn("Test Page", res["markdown"])
        self.assertGreater(res["character_count"], 10)

    def test_search_web_structure(self):
        results = search_web("Python Termux", max_results=2)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("title", results[0])
        self.assertIn("url", results[0])

    def test_daemon_task_logging(self):
        log = run_daemon_task("https://example.com")
        self.assertIn("status", log)
        logs = get_daemon_logs()
        self.assertGreater(len(logs), 0)

if __name__ == "__main__":
    unittest.main()
