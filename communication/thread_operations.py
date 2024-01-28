import queue
from queue import Queue
from typing import List


def get_all_items(q: Queue) -> List[str]:
    items = []
    while True:
        try:
            item = q.get_nowait()
        except queue.Empty:
            break
        else:
            items.append(item)
            # If you need to preserve the queue's content, requeue the items
            # Be cautious as it might not be safe in a concurrent environment
            # q.put(item)
    return items
