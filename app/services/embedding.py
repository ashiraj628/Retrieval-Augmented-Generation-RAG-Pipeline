from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.model_name = settings.embedding_model
        self.model = SentenceTransformer(self.model_name)

    def generate(self, text: str) -> list[float]:
        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )
        return vector.tolist()

    def generate_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )
        return vectors.tolist()