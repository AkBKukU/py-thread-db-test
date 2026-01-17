# py-thread-db-test
How can I write multi-threaded python applications that access the same DB?





## Concepts as I understand them

### task = asyncio.create_task(async_func())
Adds a callback function call to `async_func()` the event loop to execute at an indeterminate point in the future. The task is not immediately run.

**NOTE**, asyncio.create_task will create a `task` object that you *must* capture in a variable. It is needed later but the task the callback points to could be garbage collected if not.

### await task
If `task` hasn't been run yet, hold execution here until it has.

Also has some funky interaction with `yield` where it can create a callback to the point `yield` was run rather than the entire task ending.

### asyncio.run(async_func())
Immediately runs `async_func()` with a new event loop. Tasks created inside `async_func()` are added to this event loop and will be called before `async_func()` is returned.



## multiprocessing Process as asyncio

~~~python
import asyncio
from multiprocessing import Process

class YieldToEventLoop:
    def __await__(self):
        yield

def process_do_big_stuff(stuff_to_do):
        stuff_to_do="big"

async start_big_stuff(stuff_to_do):
    p = Process(target=process_do_big_stuff, args=(*stuff_to_do))
    p.start()
    while p.is_alive():
        await YieldToEventLoop()

    p.join()


async def main():

    big_stuff = asyncio.create_task(start_big_stuff())

    # Other stuff

    await big_stuff

asyncio.run(main())
~~~



## PyDiscRip Architecture Change

Each drive rip should have its own event loop. Tasks will be generated for working on each data type derived from the media sample. This will allow for each rip to run fully independent of others but also have internally managed logic flow.

Controllers should also have an event loop where each drive rip is started as a task. tasks starting and ending will be used to control aspects like drive availability and loading/unloading. Controllers are based on a physical element and are likely linear in nature and well suited to asyncio tasks.




```python


# Pseudo code !!!!!!



class Controller:

        def __init__(drive_count):
                # https://docs.python.org/3/library/asyncio-queue.html
                self.sample_queue = asyncio.Queue()
                self.drive_tasks = []
                for i in range(len(drive_count)):
                        task = asyncio.create_task(start_rip(f'start_rip-{i}', queue))
                        self.drive_tasks.append(task)



        async def check_samples():
                while running:
                        samples = sql_get_queue()
                        for sample in samples:
                                if sample is new:
                                        self.sample_queue.put(sample)

                        asyncio.sleep(1)



        def start_rip(queue):

                sample=queue.get()

                drive = load()

                sql_update_sample(sample_id, {"drive":drive})


                p = Process(target=rip_cd, args=(*stuff_to_do))
                p.start()
                while p.is_alive()
                        asyncio.sleep(1)

                unload(drive)


        def controller_start(sample_id):
                task_update = asyncio.create_task(check_samples())
                asyncio.run(task_update)




```

