---
title: "Spring AI: Practical Usage Notes & Architecture"
date: 2025-01-05T09:30:00+05:30
author: "Saravana"
author_role: "Principal Java Architect & TNJUG Speaker"
category: "Learning"
tags:
  - "Spring AI"
  - "Spring Boot"
  - "Generative AI"
excerpt: "Learn how to integrate artificial intelligence capabilities into enterprise Spring applications with practical architectural patterns."
featured_image: "/tamil_jug.jpeg"
---

### Why Spring AI?

Spring AI provides an idiomatic Java framework for incorporating artificial intelligence into Spring applications without requiring Python microservice glue. It abstracts model providers behind clean Spring interfaces.

### Key Capabilities

1. **Multi-Model Support**: Seamlessly swap between OpenAI, Azure OpenAI, Anthropic Claude, Ollama (local LLMs), and Hugging Face.
2. **Vector Store Integration**: Built-in support for PgVector, Chroma, Pinecone, and Milvus.
3. **Structured Outputs**: Map unstructured LLM completions directly into Java Records and strongly-typed objects.
4. **Function & Tool Calling**: Expose standard Java methods to LLM agents for retrieval-augmented generation (RAG).

### Code Example: Creating a Chat Client

```java
@RestController
public class AssistantController {

    private final ChatClient chatClient;

    public AssistantController(ChatClient.Builder builder) {
        this.chatClient = builder.build();
    }

    @GetMapping("/api/ask")
    public String ask(@RequestParam String question) {
        return chatClient.prompt()
            .user(question)
            .call()
            .content();
    }
}
```

### Best Practices for Enterprise Rollouts

- Always set timeouts and fallback strategies with Resilience4j.
- Cache embeddings aggressively to control operational costs.
- Never feed raw user prompts directly into database tools without strict authorization filters.
