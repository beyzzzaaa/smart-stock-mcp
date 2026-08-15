import requests

class LLMService:
    def __init__(self):
        self.url = "https://engine-evidence-factor-commented.trycloudflare.com/generate"

    def generate(self, messages):
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            prompt_parts.append(f"{role}: {content}")
        
        prompt = "\n".join(prompt_parts)
        if not prompt.endswith("\nassistant:"):
            prompt += "\nassistant:"
            
        print(f"Prompt karakter sayısı: {len(prompt)}")
        print(f"Prompt token sayısı (tahmini): {len(prompt) // 4}")
        
        payload = {
            "prompt": prompt,
            "max_new_tokens": 512
        }
        
        response = requests.post(
            self.url,
            json=payload,
            timeout=(20, 300)
        )
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise RuntimeError(
                f"LLM API hatası: {response.status_code} - {response.text}"
            ) from exc
            
        data = response.json()
        return data["response"]