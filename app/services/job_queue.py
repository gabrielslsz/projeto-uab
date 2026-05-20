import queue
import threading
import time

class JobQueue:
    _queue = queue.Queue()
    _worker_thread = None
    _stop_event = threading.Event()

    @classmethod
    def start_worker(cls):
        if cls._worker_thread is None:
            cls._worker_thread = threading.Thread(target=cls._worker, daemon=True)
            cls._worker_thread.start()

    @classmethod
    def _worker(cls):
        while not cls._stop_event.is_set():
            try:
                func, args, kwargs = cls._queue.get(timeout=1)
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"JobQueue Error: {e}")
                finally:
                    cls._queue.task_done()
            except queue.Empty:
                continue

    @classmethod
    def enqueue(cls, func, *args, **kwargs):
        cls.start_worker()
        cls._queue.put((func, args, kwargs))

    @staticmethod
    def simulate_notification(atendimento_id, mensagem):
        # Simula um delay de rede
        time.sleep(2)
        print(f"Notification Sent to Atendimento {atendimento_id}: {mensagem}")
