def embed_query(query):

    # TODO: Use a pre-trained model to convert the query into an embedding vector, model suggested by dad

    return [0.1, 0.2, 0.3]

def retrieve_chunks(query):

    # TODO: Use embedded query to find relevant chunks from vector database

    return [
        {"content": "The SQL Server instance is named idqs-sqlsvr.", "source": "console.md"},
        {"content": "The public IP address is 34.174.53.148.", "source": "config.txt"},
        {"content": "Backups are performed daily at 5:00 AM UTC.", "source": "backup_log.md"},
    ]
def build_prompt(query, chunks):
    prompt = f"Answer the following question using only the numbered context below.\n"
    prompt += "If applicable, refer to specific chunk numbers in your answer.\n\n"
    prompt += "Context:\n"
    for i, chunk in enumerate(chunks, start=1):
        prompt += f"[{i}] {chunk['content']}\n"
    prompt += f"\nQuestion: {query}"
    return prompt