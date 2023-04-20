from agent9.configs import cfg
from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(cfg.default_thread_pool_size)


def create_thread_pool(size=cfg.default_thread_pool_size):
    return ThreadPoolExecutor(size)
