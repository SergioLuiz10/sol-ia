from fastapi import APIRouter

# funcao que calcula a taxa de resolucao das conversas
from app.repositories.conversas import calcular_taxa_resolucao

router = APIRouter()

# meta definida no PRD: 60% das conversas resolvidas sem transferir
META = 0.6


# Endpoint para obter a taxa de resolucao das conversas.
@router.get("/metricas")
def taxa_resolucao():
    # Calcula a taxa de resolucao das conversas.
    taxa = calcular_taxa_resolucao()
    # Arredonda a taxa para duas casas decimais.
    return {
        "taxa_resolucao": round(taxa, 2),
        "meta": META,
        "atingiu_meta": taxa >= META,
    }
