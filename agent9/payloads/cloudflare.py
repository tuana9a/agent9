from dataclasses import dataclass


@dataclass
class CreateDnsRequest:
    name: str
    content: str
    type: str = "A"
    proxied: bool = False


@dataclass
class UpdateDnsRequest:
    name: str
    content: str
    type: str = "A"
    proxied: bool = False