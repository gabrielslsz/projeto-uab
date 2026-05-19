from queue import Queue
from threading import Lock, Thread


_job_queue = Queue()
_start_lock = Lock()
_worker_started = False


def _worker_loop():
    while True:
        job_callable, args, kwargs = _job_queue.get()
        try:
            job_callable(*args, **kwargs)
        finally:
            _job_queue.task_done()


def _ensure_worker_started():
    global _worker_started
    if _worker_started:
        return

    with _start_lock:
        if _worker_started:
            return
        worker = Thread(target=_worker_loop, daemon=True)
        worker.start()
        _worker_started = True


def enfileirar_job(job_callable, *args, **kwargs):
    _ensure_worker_started()
    _job_queue.put((job_callable, args, kwargs))


def aguardar_jobs():
    _job_queue.join()