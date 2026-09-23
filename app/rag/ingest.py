from pathlib import Path

#o MarkdownHeaderTextSplitter corta nos titulos
#o RecursiveCharacterTextSplitter corta nos textos longos em pedaços menores
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from app.rag.store import get_vectorstore

# Caminho para o arquivo de política de trocas
CAMINHO_POLITICA = Path(__file__).resolve().parents[2] / "data" / "politica_trocas.md"



# Função para ingerir a política de trocas no vetor de armazenamento
def ingerir_politica() -> None:
    texto = CAMINHO_POLITICA.read_text(encoding="utf-8")
    # Dividir o texto em seções com base nos títulos
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "titulo"), ("##", "secao")]
    )
    secoes = splitter.split_text(texto)
    # Dividir cada texto em trechos menores com base no tamanho
    splitter_tamanho = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    trechos = splitter_tamanho.split_documents(secoes)
    # Armazenar os trechos no vetor de armazenamento
    store = get_vectorstore()
    store.delete_collection()
    store.create_collection()
    store.add_documents(trechos)

    #mostra a quantidade de trechos ingeridos
    print(f"{len(trechos)} trechos ingeridos na colecao.")


if __name__ == "__main__":
    ingerir_politica()