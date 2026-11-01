import asyncio
import threading
import sys

def thread_func():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("Loop type:", type(loop))
    
    async def run_sub():
        proc = await asyncio.create_subprocess_exec('cmd', '/c', 'echo hello', stdout=asyncio.subprocess.PIPE)
        out, _ = await proc.communicate()
        print(out.decode())
        
    loop.run_until_complete(run_sub())

t = threading.Thread(target=thread_func)
t.start()
t.join()
