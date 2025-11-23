import asyncio

# Example LLM call - replace with your agent client
async def call_llm(prompt: str) -> str:
    # simulate network call / async LLM request
    await asyncio.sleep(1)
    return f"LLM response for prompt: {prompt}"
