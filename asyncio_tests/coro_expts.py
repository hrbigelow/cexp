import sys
import inspect
import asyncio

def indent(depth):
    return '    ' * depth

# The async function
async def thing(depth, max_depth):
    print(indent(depth) + '-first')
    await asyncio.sleep(0)
    print(indent(depth) + '-second')
    await asyncio.sleep(0)
    print(indent(depth) + '-third')
    yield depth
    await asyncio.sleep(0)
    print(indent(depth) + '-recursing')
    if depth <= max_depth:
        async for val in thing(depth+1, max_depth):
            yield val
        # await thing(depth+1, max_depth)
        # thing(depth+1, max_depth)
    print(indent(depth) + '-finished')
    raise StopIteration
# return
    # return 0

async def async_gen(capacity):
    for _ in range(capacity):
        yield 0


async def async_loop():
    agen = async_gen(5)
    async for i in agen:
        print(i)

asyncio.run(async_loop())

sys.exit(0)


# coroutine object returned by the async function
coro = thing(0, 2)
assert inspect.isasyncgen(coro)

# The 'send' function 
# it = iter(coro)

while True:
    # print('Send')
    # coro.send(None)
    print(anext(coro))
    print(f'Coroutine state: {coro.ag_frame.f_locals=}')

