import queue


class ThreadCommunication:
    def __init__(self):
        self.queues = {"cont_to_gen": queue.Queue(), "anlys_to_cont": queue.Queue()}
