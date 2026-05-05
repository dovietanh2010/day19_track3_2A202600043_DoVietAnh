import json
from typing import List
from openai import OpenAI
from app.config import Config
from app.extraction.schema import Entity, Triplet, ExtractionResponse
from app.utils.logger import setup_logger

logger = setup_logger("EntityExtractor")

class EntityExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL

    def extract(self, text: str) -> ExtractionResponse:
        prompt = f"""
        Extract entities and relationships from the following text related to tech companies.
        Return the result in JSON format.
        
        Text: {text}
        
        Required JSON Structure:
        {{
            "entities": [
                {{"name": "Entity Name", "type": "COMPANY/PERSON/YEAR/PRODUCT"}}
            ],
            "triplets": [
                {{"subject": "Entity A", "relation": "RELATION_TYPE", "object": "Entity B", "subject_type": "TYPE", "object_type": "TYPE"}}
            ]
        }}
        
        Rules:
        1. Keep entity names consistent (e.g., "OpenAI" instead of "Open AI").
        2. Use UPPERCASE for relation types (e.g., FOUNDED_BY, INVESTED_IN, RELEASED).
        3. Identify the type of each entity in the triplet.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in information extraction for knowledge graphs."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            data = json.loads(response.choices[0].message.content)
            return ExtractionResponse(**data)
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            return ExtractionResponse(entities=[], triplets=[])
