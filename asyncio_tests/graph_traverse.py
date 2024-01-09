def neighbors(node):
    time.sleep(1)
    return node.children

async def async_neighbors(node, pool):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(pool, partial(neighbors, node))

