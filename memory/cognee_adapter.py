import asyncio
import cognee


async def remember(text):

    await cognee.add(text)

    await cognee.cognify()


async def recall(query):

    result = await cognee.search(query)

    return result


def save(text):

    asyncio.run(

        remember(text)

    )


def search(query):

    return asyncio.run(

        recall(query)

    )