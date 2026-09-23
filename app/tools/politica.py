
#conexao com o banco de dados para obter o vetor de armazenamento
from app.rag.store import get_vectorstore 
# Função para consultar a política de trocas para o agente no vetor de armazenamento
# pegando as 3 respostas mais similares
def consultar_politica(pergunta_troca: str) -> str:
    conexao = get_vectorstore()
    documentos = conexao.similarity_search(pergunta_troca,k=3)
   
    if not documentos:
     return "Não encontrei essa informação na política da empresa."    
    #retorna de forma concatenada o conteúdo das páginas dos documentos encontrados
    return "\n\n".join(doc.page_content for doc in documentos)