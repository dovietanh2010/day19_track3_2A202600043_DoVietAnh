import json
from openai import OpenAI
from app.config import Config

class Metrics:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def score_accuracy(self, query: str, answer: str) -> int:
        """
        Uses LLM as a judge to score accuracy from 0 to 10.
        """
        prompt = f"""
        Rate the accuracy of the following AI-generated answer to the query on a scale of 0 to 10.
        Consider if the answer is factually correct based on general knowledge of tech companies.
        
        Query: {query}
        Answer: {answer}
        
        Return ONLY a JSON object: {{"score": <int>, "reason": "<string>"}}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            return data.get("score", 0), data.get("reason", "N/A")
        except:
            return 0, "Error during scoring"
