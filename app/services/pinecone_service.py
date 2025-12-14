from pinecone import Pinecone
from app.config.settings import settings


class PineconeService:
    def __init__(self):
        self.index_name = "first-index"
        self.pc = Pinecone(api_key=settings.pinecone_api_key)

        if not self.pc.has_index(self.index_name):
            self.pc.create_index_for_model(
                name=self.index_name,
                cloud="aws",
                region="us-east-1",
                embed={
                    "model": "llama-text-embed-v2",
                    "field_map": {"text": "chunk_text"},
                } # type: ignore
            )

        self.index = self.pc.Index(self.index_name)

    def upsert_records(self, records):
        self.index.upsert_records(namespace="__default", records=records)

    def search(self, dataset_ids: list[int], query: str, top_k: int = 5):
        chunk_texts: list[str] = []

        for dataset_id in dataset_ids:
            res = self.index.search(
                namespace="__default", 
                query={
                    "inputs": {"text": query}, 
                    "top_k": top_k,
                    "filter": {"dataset_id": dataset_id},
                }, # type: ignore
            )
            print(res)

            for hit in res.result.hits:
                print(hit)
                chunk_text = hit.fields.get("chunk_text")
                chunk_texts.append(chunk_text)

        return chunk_texts

    def build_context(self, chunks: list[str]) -> str:
        return "\n\n".join(chunks)
