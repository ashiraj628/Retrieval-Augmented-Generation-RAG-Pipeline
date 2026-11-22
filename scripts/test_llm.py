from app.services.llm import LLMService
import asyncio

async def main():
    llm=LLMService()
    result=await llm.generate(
        "tell me about la maritza song. answer in 1 sentence"
    )
    print(result)


if __name__=="__main__":
    asyncio.run(main())