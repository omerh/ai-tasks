from browser_use import Agent, Controller
from browser_use.llm import ChatGoogle  # , ChatOlla
from loguru import logger

from src.data.amazon import AmazonItem


async def get_item_info(prompt: str, conversation_folder: str) -> str:
    # Initialize the model
    llm = ChatGoogle(model="gemini-2.5-flash-lite")
    # Header for the agent
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,he;q=0.8",
        "upgrade-insecure-requests": 1,
    }

    # Controller
    controller = Controller(output_model=AmazonItem)
    # Create agent with the model
    agent = Agent(
        task=prompt,
        llm=llm,
        save_conversation_path=f"./{conversation_folder}/",
        header=header,
        controller=controller,
    )
    result = await agent.run()

    # Print the final result (call the method)
    logger.debug("Final Result:")
    final_result = result.final_result()
    logger.debug(final_result)
    if final_result:
        return final_result
    else:
        return "No result found"
