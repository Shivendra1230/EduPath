import os, json, re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class GroqService:
    def __init__(self):
        self.key = os.getenv("GROQ_API_KEY","").strip()
        self.fast_model = os.getenv("GROQ_MODEL_FAST","openai/gpt-oss-20b")
        self.reasoning_model = os.getenv("GROQ_MODEL_REASONING","openai/gpt-oss-120b")
        self.client = Groq(api_key=self.key) if self.key else None

    @property
    def live(self): return self.client is not None

    def chat(self, system, user, model=None, temperature=0.25, max_tokens=1800):
        if not self.client:
            raise RuntimeError("GROQ_API_KEY is missing.")
        r = self.client.chat.completions.create(
            model=model or self.fast_model,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            temperature=temperature,
            max_completion_tokens=max_tokens
        )
        return r.choices[0].message.content or ""

    def json(self, system, user, model=None, max_tokens=3000):
        if not self.client:
            raise RuntimeError("GROQ_API_KEY is missing.")
        r = self.client.chat.completions.create(
            model=model or self.fast_model,
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            temperature=0.1,
            max_completion_tokens=max_tokens,
            response_format={"type":"json_object"}
        )
        raw = r.choices[0].message.content or "{}"
        raw = re.sub(r"^```json\s*|\s*```$", "", raw.strip())
        return json.loads(raw)

    def stream(self, messages, model=None, temperature=0.35, max_tokens=1600):
        if not self.client:
            raise RuntimeError("GROQ_API_KEY is missing.")
        return self.client.chat.completions.create(
            model=model or self.reasoning_model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens,
            stream=True
        )

groq_service = GroqService()
