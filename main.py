from langgraph.graph import StateGraph, MessagesState,END

from nodes import run_agent_reasoning, tool_node

ACT = "act"
REASONING = "reasoning"
LAST = -1


def should_continue(state: MessagesState) -> str:
    """Determine whether to continue reasoning or act."""
    last_message = state["messages"][LAST].tool_calls
    if not last_message:
        return END
    return ACT


flow = StateGraph(MessagesState)

flow.add_node(REASONING, run_agent_reasoning)

#define onde ação começa
#preciso adicionar o add_node para o nó de ferramentas, caso contrário, o fluxo
# não sabe para onde ir após a decisão do should_continue.
#e tagbem adiconar o REASONING antes porque se não da erro no set_entry_point
flow.set_entry_point(REASONING)
flow.add_node(ACT,tool_node)

#condicional para decidir se continua ou termina
#Se should_continue retornar ACT, o fluxo vai para o nó de ferramentas.
# Se retornar END, o fluxo é encerrado e a resposta final é entregue ao usuário.
#O LangGraph pega esse retorno e busca no dicionário:

# Se o retorno for "act", o dicionário mapeia para a chave ACT, levando o fluxo para o nó de ferramentas (tool_node).
#
# Se o retorno for "__end__", o dicionário mapeia para a chave END, finalizando a execução.
# Como should_continue retorna exatamente ACT ("act") ou END ("__end__"),
# isso funciona exatamente igual ou seja redudante , agora se eu reotrnasse
# "continue" ou "stop" ai sim seria necessário o dicionário para mapear para ACT ou END.
flow.add_conditional_edges(REASONING, should_continue)
flow.add_conditional_edges(REASONING,should_continue,{
    END:END,
    ACT:ACT
})

#flow.add_edge(ACT, REASONING): Cria uma ponte direta (sem condição).
# Após executar a ferramenta no nó ACT, o controle sempre volta para o
# REASONING para que o LLM avalie o resultado da ferramenta.
flow.add_edge(ACT,REASONING)

app = flow.compile()

app.get_graph().draw_mermaid_png(output_file_path="flow.png")




if __name__ == "__main__":
    print("Hello, World!")