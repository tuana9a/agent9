import requests

from agent9.configs.cfg import profiles
from agent9.models.cloudflare import DnsRecord, ZoneRecord
from agent9.payloads.cloudflare import CreateDnsRequest, UpdateDnsRequest


def delete_dns(id: str):
    c = profiles.get_selected()
    if not c: raise Exception("no profile selected")
    response = requests.delete(
        f"{c.cloudflare_base_url}/zones/{c.cloudflare_zone_id}/dns_records/{id}",
        headers={
            "X-Auth-Email": str(c.cloudflare_email),
            "Authorization": f"Bearer {c.cloudflare_access_token}",
            "Content-Type": "application/json"
        }).json()
    return response


def create_dns(body: CreateDnsRequest):
    c = profiles.get_selected()
    if not c: raise Exception("no profile selected")
    response = requests.post(
        f"{c.cloudflare_base_url}/zones/{c.cloudflare_zone_id}/dns_records",
        headers={
            "X-Auth-Email": str(c.cloudflare_email),
            "Authorization": f"Bearer {c.cloudflare_access_token}",
            "Content-Type": "application/json"
        },
        json={
            "type": body.type,
            "name": body.name,
            "content": body.content,
            "proxied": body.proxied
        }).json()
    return response


def update_dns(id: str, body: UpdateDnsRequest):
    c = profiles.get_selected()
    if not c: raise Exception("no profile selected")
    response = requests.put(
        f"{c.cloudflare_base_url}/zones/{c.cloudflare_zone_id}/dns_records/{id}",
        headers={
            "X-Auth-Email": str(c.cloudflare_email),
            "Authorization": f"Bearer {c.cloudflare_access_token}",
            "Content-Type": "application/json"
        },
        json={
            "type": body.type,
            "name": body.name,
            "content": body.content,
            "proxied": body.proxied
        }).json()
    return response


def list_dns():
    c = profiles.get_selected()
    if not c: raise Exception("no profile selected")
    response = requests.get(
        f"{c.cloudflare_base_url}/zones/{c.cloudflare_zone_id}/dns_records",
        headers={
            "X-Auth-Email": str(c.cloudflare_email),
            "Authorization": f"Bearer {c.cloudflare_access_token}",
            "Content-Type": "application/json"
        }).json()
    dns_records = []
    for x in response["result"]:
        dns_records.append(DnsRecord(**x))
    return dns_records


def list_zone():
    c = profiles.get_selected()
    if not c: raise Exception("no profile selected")
    response = requests.get(f"{c.cloudflare_base_url}/zones",
                            headers={
                                "X-Auth-Email": str(c.cloudflare_email),
                                "Authorization":
                                f"Bearer {c.cloudflare_access_token}",
                                "Content-Type": "application/json"
                            }).json()
    zone_records = []
    for x in response["result"]:
        zone = ZoneRecord(**x)
        zone_records.append(zone)
    return zone_records
