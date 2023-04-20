import os
import time
import uuid
import configparser
import multiprocessing

from typing import Optional
from dataclasses import dataclass

default_cf_base_url = "https://api.cloudflare.com/client/v4"
default_selected_key = "default"
cpu_count = multiprocessing.cpu_count()
max_thread_pool_size = 8
min_thread_pool_size = 2
default_thread_pool_size = min(max(cpu_count, min_thread_pool_size),
                               max_thread_pool_size)

stop_container_timeout_in_seconds = 3 * 60


@dataclass
class Cfg:
    bind: str = "127.0.0.1"
    port: int = 2090
    agent9_id: Optional[str] = ""
    agent9_access_token: Optional[str] = ""
    cloudflare_email: Optional[str] = ""
    cloudflare_access_token: Optional[str] = ""
    cloudflare_zone_id: Optional[str] = ""
    cloudflare_base_url: Optional[str] = default_cf_base_url


class Profiles:

    def __init__(self) -> None:
        self.db = {}
        self.selected_key = default_selected_key

    def get(self, key: str) -> Optional[Cfg]:
        return self.db[key]

    def get_selected(self):
        return self.get(self.selected_key)

    def get_selected_key(self):
        return self.selected_key

    def set(self, key: str, c: Cfg):
        self.db[key] = c

    def set_selected_key(self, key: str):
        self.selected_key = key

    def load_from_file(self, path: str, selected_index: int = 0):
        """
        default select first section
        """
        parser = configparser.ConfigParser()
        parser.read(path)
        for section in parser.sections():
            c = Cfg(**parser[section])
            self.set(section, c)
        self.set_selected_key(parser.sections()[selected_index])
        return self

    def load_from_env(self, selected_key: str = default_selected_key):
        id = os.getenv("AGENT9_ID") or str(uuid.uuid4())
        access_token = os.getenv("AGENT9_ACCESS_TOKEN") or str(time.time())
        cf_base_url = os.getenv("CLOUDFLARE_BASE_URL") or default_cf_base_url
        cf_email = os.getenv("CLOUDFLARE_EMAIL")
        cf_access_token = os.getenv("CLOUDFLARE_ACCESS_TOKEN")
        cf_zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
        bind = os.getenv("BIND", "127.0.0.1")
        port = int(os.getenv("PORT", 2090))
        c = Cfg(bind=bind,
                port=port,
                agent9_id=id,
                agent9_access_token=access_token,
                cloudflare_base_url=cf_base_url,
                cloudflare_email=cf_email,
                cloudflare_zone_id=cf_zone_id,
                cloudflare_access_token=cf_access_token)
        self.set(selected_key, c)
        self.set_selected_key(selected_key)
        return self


profiles = Profiles()
