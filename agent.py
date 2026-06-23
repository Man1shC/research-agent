import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage
import operator

load_dotenv()

# ── Model + Tools ────────────────────────────────────────
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", max_tokens=2000)
search_tool = TavilySearchResults(max_results=5)

# ── Agent State ──────────────────────────────────────────
class AgentState(TypedDict):
    topic: str
    search_results: list
    report: str
    messages: Annotated[list, operator.add]

# ── Nodes ────────────────────────────────────────────────
def search_node(state: AgentState):
    print(f"🔍 Searching for: {state['topic']}")
    results = search_tool.invoke(state["topic"])
    return {"search_results": results}

def synthesize_node(state: AgentState):
    print("✍️ Synthesizing report...")
    context = "\n\n".join([
        f"Source: {r['url']}\n{r['content']}"
        for r in state["search_results"]
    ])
    prompt = f"""You are a research analyst. Based on the search results below, write a comprehensive research report on: {state['topic']}

Search Results:
{context}

Write a structured report with:
1. Executive Summary (2-3 sentences)
2. Key Findings (4-5 bullet points)
3. Detailed Analysis (3-4 paragraphs)
4. Conclusion
5. Sources (list the URLs)

Be factual, cite the sources, and be thorough."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"report": response.content}

# ── Build Graph ──────────────────────────────────────────
def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("search", search_node)
    graph.add_node("synthesize", synthesize_node)
    graph.set_entry_point("search")
    graph.add_edge("search", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()

# ── Test run ─────────────────────────────────────────────
if __name__ == "__main__":
    agent = build_agent()
    result = agent.invoke({
        "topic": "latest developments in large language models 2025",
        "search_results": [],
        "report": "",
        "messages": []
    })
    print("\n📄 REPORT:\n")
    print(result["report"])