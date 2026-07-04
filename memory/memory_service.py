import cognee
import asyncio


async def initialize_memory():

    await cognee.prune.prune_data()

    await cognee.prune.prune_system(metadata=True)


def init_memory():

    asyncio.run(initialize_memory())