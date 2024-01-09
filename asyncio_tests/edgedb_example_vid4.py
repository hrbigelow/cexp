import sys
import asyncio

class TraceStep(asyncio.tasks._PyTask):
    def _Task__step(self, exc=None):
        print(f'<step name={self.get_name()} done={self.done()}>')
        result = super()._Task__step(exc=exc)
        print(f'</step name={self.get_name()} done={self.done()}>')

async def example(count: int) -> str:
    print(indent(count), 'Before the first await')
    await asyncio.sleep(0)
    print(indent(count), 'After the first await')

    if count == 0:
        print(indent(count), 'Returning result')
        return 'result'

    for i in range(count):
        print(indent(count), 'Before await inside loop iteration', i)
        await asyncio.sleep(i)
        print(indent(count), 'After await inside loop iteration', i)

    print(indent(count), f'Before await on example({count-1})')
    return await example(count-1)

def indent(count):
    return '    ' * (5 - count)

if __name__ == '__main__':
    count = int(sys.argv[1])
    loop = asyncio.get_event_loop()
    loop.set_task_factory(lambda loop, coro: TraceStep(coro, loop=loop))
    loop.run_until_complete(example(count))



