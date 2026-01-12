# Corrective RAG (CRAG) using LangChain & LangGraph

This repository implements a **Corrective Retrieval-Augmented Generation (Corrective RAG / CRAG)** system using **LangChain** and **LangGraph**.

Unlike standard RAG pipelines that assume retrieval is always sufficient, this implementation introduces a **self-correcting mechanism** that:
- Evaluates retrieved documents
- Detects low-quality or insufficient context
- Rewrites the query
- Falls back to web search when needed
- Generates a grounded final answer

The workflow is explicitly modeled as a **stateful LangGraph**, making the correction logic transparent, debuggable, and extensible.

---

## 🧠 Why Corrective RAG?

Traditional RAG pipelines:

> Retrieve → Generate → Answer

fail when:
- Retrieval returns irrelevant documents
- Queries are poorly phrased
- Knowledge is missing from the vector store

**Corrective RAG fixes this** by introducing an evaluation and correction loop:

> Retrieve → Grade → Correct → Retry → Generate

This results in **more reliable and accurate answers**.

---

## 🏗️ Architecture Overview

The system follows the graph below:


::contentReference[oaicite:0]{index=0}


### Execution Flow

```text
__start__
   ↓
 retrieve
   ↓
 grade_documents
   ├── (sufficient) ───────────────▶ generate ─▶ __end__
   └── (insufficient)
           ↓
     transform_query
           ↓
     web_search_node
           ↓
        generate ─▶ __end__


<p align="center">
  <img src="/Users/kalyanpichumani/Desktop/Code experiments/Langgraph/correctiveRag.png" width="500"/>
</p>


