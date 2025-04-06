import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable, Dict
from aimakerspace.openai_utils.embedding import EmbeddingModel
import asyncio
from keybert import KeyBERT


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return dot_product / (norm_a * norm_b)


class VectorDatabase:
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.vectors = defaultdict(dict)  # Store dictionaries
        self.embedding_model = embedding_model or EmbeddingModel()
        self.keybert_model = KeyBERT()  # Initialize KeyBERT

    def insert(self, key: str, data: Dict) -> None:
        """Inserts data with metadata."""
        self.vectors[key] = data


    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
        keyword_filter: List[str] = None
    ) -> List[Tuple[str, float]]:
        scores = []
        for key, data in self.vectors.items():

          meets_criteria = True #Set initial status as true

          if keyword_filter:
              doc_keywords = data["keywords"] #The existing keywords
              # Check if ANY of the filter keywords are in the document keywords
              meets_criteria = any(keyword in doc_keywords for keyword in keyword_filter)

          if not meets_criteria: #Skip if it doesn't meet the status
              continue #Skip to the next section

          score = distance_measure(query_vector, data["embedding"])
          scores.append((key, score)) #Run similarity

        return sorted(scores, key=lambda x: x[1], reverse=True)[:k]


    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        return_as_text: bool = False,
        keyword_filter: List[str] = None #Add this filter for keyword arguments
    ) -> List[Tuple[str, float]]:
        query_vector = self.embedding_model.get_embedding(query_text)
        results = self.search(query_vector, k, distance_measure, keyword_filter) #Call this with all search parameters, now including keyword_filter
        return [result[0] for result in results] if return_as_text else results

    def retrieve_from_key(self, key: str) -> np.array:
        return self.vectors.get(key, {}).get("embedding", None)

    async def abuild_from_list(self, list_of_text: List[str]) -> "VectorDatabase":
        embeddings = await self.embedding_model.async_get_embeddings(list_of_text)
        for text, embedding in zip(list_of_text, embeddings):
            #Extract Keywords with KeyBERT
            keywords = [keyword[0] for keyword in self.keybert_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', highlight=False)] #This step actually puts the extracted data in there


            data = { #Data object
                "embedding": np.array(embedding),
                "keywords": keywords,
                "text": text
            }
            self.insert(text, data) #Pass data

        return self


if __name__ == "__main__":
    import time
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    vector_db = VectorDatabase()
    start_time = time.time()
    vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text))
    end_time = time.time()
    print(f"Time to build vector database: {end_time - start_time:.4f} seconds")
    k = 2

    #Example using search with keywords
    searched_vector = vector_db.search_by_text("I think fruit is awesome!", k=k, keyword_filter=['fruit', 'smoothie'])
    print(f"Closest {k} vector(s) (filtered by fruit/smoothie keywords):", searched_vector)

    retrieved_vector = vector_db.retrieve_from_key(
        "I like to eat broccoli and bananas."
    )
    print("Retrieved vector:", retrieved_vector)

    relevant_texts = vector_db.search_by_text(
        "I think fruit is awesome!", k=k, return_as_text=True, keyword_filter=['kittens']
    )
    print(f"Closest {k} text(s) (filtered by kittens):", relevant_texts)