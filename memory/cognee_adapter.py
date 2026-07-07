import asyncio
import cognee
import logging

logger = logging.getLogger("cognee_adapter")

def safe_async_run(coro):
    """Safely run async coroutines in Streamlit or other running event loops."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        return loop.run_until_complete(coro)

async def remember(text):
    await cognee.add(text)
    await cognee.cognify()

async def recall(query):
    # Retrieve relations and entities from Cognee search
    result = await cognee.search(query)
    return result

def save(text):
    """Save text data to Cognee memory graph."""
    try:
        safe_async_run(remember(text))
        return True
    except Exception as e:
        logger.error(f"Failed to save to Cognee memory: {e}")
        return False

def search(query):
    """Retrieve formatted query matches from Cognee memory graph."""
    try:
        raw_results = safe_async_run(recall(query))
        
        # Format the search result as a readable string
        if not raw_results:
            return ""
            
        formatted = []
        # Cognee search results can be lists of dicts, nodes, or string responses
        if isinstance(raw_results, list):
            for item in raw_results:
                if isinstance(item, dict):
                    formatted.append(str(item))
                elif hasattr(item, "dict"):
                    formatted.append(str(item.dict()))
                else:
                    formatted.append(str(item))
        else:
            formatted.append(str(raw_results))
            
        return "\n".join(formatted)
    except Exception as e:
        logger.error(f"Failed to search Cognee memory: {e}")
        return ""