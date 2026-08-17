import unittest
from unittest.mock import patch

from llm import LLMService


class LLMServiceTest(unittest.TestCase):
    @patch("llm.requests.post")
    def test_generate_uses_non_streaming_ollama_request(self, post):
        response = post.return_value
        response.json.return_value = {"response": "done"}

        service = LLMService()
        result = service.generate([{"role": "user", "content": "hello"}])

        self.assertEqual(result, "done")
        response.raise_for_status.assert_called_once_with()
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "qwen3:8b")
        self.assertEqual(payload["prompt"], "user: hello\nassistant:")
        self.assertFalse(payload["stream"])
        self.assertFalse(payload["think"])
        self.assertEqual(payload["options"]["num_predict"], 512)


if __name__ == "__main__":
    unittest.main()
