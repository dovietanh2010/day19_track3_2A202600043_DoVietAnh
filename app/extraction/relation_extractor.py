from typing import List
from app.extraction.schema import Triplet
from app.extraction.entity_extractor import EntityExtractor

class RelationExtractor:
    def __init__(self):
        self.extractor = EntityExtractor()

    def extract_relations(self, text: str) -> List[Triplet]:
        """
        Uses the EntityExtractor to get triplets from text.
        """
        response = self.extractor.extract(text)
        return response.triplets
