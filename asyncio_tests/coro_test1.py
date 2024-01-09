import asyncio

async def thing():
    print(f'Before first sleep')
    await asyncio.sleep(1)
    print(f'After first sleep')
    await asyncio.sleep(1)
    print(f'After second sleep')
    return


coro = thing()
print('Send None')
coro.send(None)

print('Send 5')
coro.send(5)

print('Send 10')
coro.send(10)



