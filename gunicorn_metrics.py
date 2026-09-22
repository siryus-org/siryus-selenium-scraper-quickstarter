from prometheus_client import multiprocess
from selenium_scraper_runtime.browser import close_all_drivers


def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)


def worker_abort(worker):
    close_all_drivers()


def worker_exit(server, worker):
    close_all_drivers()
