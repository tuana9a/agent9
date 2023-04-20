from typing import List
from dataclasses import dataclass
from pydantic import BaseModel


class DnsRecord(BaseModel):
    id: str
    name: str
    type: str
    content: str
    ttl: int = 0
    proxied: bool = False

    def __str__(self):
        return "%s %-4s %-20s %-15s %s %s" % (
            self.id, self.type, self.name, self.content,
            f"proxied={str(self.proxied)}", f"ttl={str(self.ttl)}")


class ZoneRecord():
    id: str
    name: str
    status: str
    name_servers: List[str]

    def __init__(self, id: str, name: str, status: str,
                 name_servers: List[str], **kwargs):
        self.id = id
        self.name = name
        self.status = status
        self.name_servers = name_servers
        pass

    def __str__(self) -> str:
        return "%s %-20s %s %s" % (self.id, self.name,
                                   f"name_servers={str(self.name_servers)}",
                                   self.status)
