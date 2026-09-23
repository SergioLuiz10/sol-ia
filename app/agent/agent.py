# monta o agente da LangChain
from langchain.agents import create_agent
# função para o agente saber qual tool usar e qual ação tomar
from langchain.tools import tool     
from langchain_openai import ChatOpenAI

# importa as tools disponíveis para o agente
from app.tools.bairros import consultar_prazo_bairro
from app.tools.pedidos import consultar_status_pedido
from app.tools.politica import consultar_politica
from app.tools.humano import transferir_humano

#para pegar o caminho do arquivo de prompt do sistema
from pathlib import Path

# tool para consultar o prazo de entrega por bairro
@tool
def prazo_por_bairro(bairro: str) -> str:
    """Consulta o prazo de entrega, em dias, para um bairro de Salvador.

    Use quando o cliente perguntar quanto tempo demora para entregar,
    quando chega no bairro dele ou se a empresa entrega em determinado bairro.

    Args:
        bairro: nome do bairro informado pelo cliente, por exemplo "Pituba".
    """
    return consultar_prazo_bairro(bairro)


# tool para consultar o status de um pedido
@tool 
def status_do_pedido(numero_pedido: str) -> str:
    """Consulta o status e a data prevista de entrega de um pedido.

    Use quando o cliente informar o número do pedido e quiser saber onde ele está,
    se já saiu para entrega, se foi entregue ou quando chega.

    Args:
        numero_pedido: número do pedido informado pelo cliente, por exemplo "001".
    """
    return consultar_status_pedido(numero_pedido)


# tool para consultar a política da empresa
@tool
def politica_da_empresa(pergunta_troca: str) -> str:
    """Consulta a política de trocas, devoluções e reembolso da Distribuidora Sol.

    Use quando o cliente perguntar sobre trocar um produto, devolver uma compra,
    prazo para desistir, produto com defeito, receber o dinheiro de volta,
    quem paga o frete da devolução ou o que pode e o que não pode ser trocado.

    Args:
        pergunta: a pergunta do cliente, com as palavras dele.
    """
    return consultar_politica(pergunta_troca)



# tool para transferir o atendimento para um humano
@tool
def transferir_para_humano(telefone: str, motivo: str) -> str:
    """Encaminha o atendimento para um atendente humano e registra a solicitação.

    Use apenas quando nenhuma das outras ferramentas resolver: o cliente pede
    para falar com uma pessoa, reclama, negocia preço ou desconto, ou pergunta
    algo fora de entregas, pedidos e política de trocas.
    Não use antes de tentar as outras ferramentas.

    Args:
        telefone: telefone do cliente que está conversando neste atendimento.
        motivo: resumo curto do que o cliente precisa, para o atendente se preparar.
    """
    return transferir_humano(telefone, motivo)



modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0)

PROMPT_SISTEMA = (Path(__file__).resolve().parents[2] / "prompt" / "sistema.md").read_text(encoding="utf-8")

# cria o agente com o modelo, as ferramentas e o prompt do sistema
agente = create_agent(
    model=modelo,
    tools=[prazo_por_bairro, status_do_pedido, politica_da_empresa, transferir_para_humano],
    system_prompt=PROMPT_SISTEMA,
)