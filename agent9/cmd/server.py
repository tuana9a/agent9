import os
import sys
import json
import time
import traceback
import argparse
import threading
import uvicorn

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi import Query
from pydantic import BaseModel
from typing import Any, List
from agent9.configs.cfg import profiles
from agent9.utils.docker import DockerUtils
from agent9.utils.cloudflare import api as cloudflareapi
from agent9.payloads.cloudflare import UpdateDnsRequest, CreateDnsRequest

parser = argparse.ArgumentParser(prog="agent9")

parser.add_argument("-c",
                    "--config",
                    help="agent9 config path",
                    required=True,
                    type=str)

parser.add_argument("-p",
                    "--profile",
                    help="Profile Selection",
                    type=str,
                    required=False,
                    default=None)

docker_utils = DockerUtils()
app = FastAPI()


@app.get("/docker/containers")
def get_containers(all=False):
    containers = []
    raw_containers: List[Any] = docker_utils.list_containers(all=all)
    for r in raw_containers:
        c = docker_utils.inspect_container(r.name)
        containers.append(c)
    return {"length": len(containers), "containers": containers}


@app.get("/cloudflare/zones")
def get_all_cloudflare_zones(table=False,
                             name_only=False,
                             cols: str = Query("")):
    zone_records = cloudflareapi.list_zone()
    if table:
        if cols:
            cols = cols.split(",")
            arr = map(lambda x: " ".join([getattr(x, key) for key in cols]),
                      zone_records)
            return PlainTextResponse("\n".join(arr))
        if name_only:
            arr = map(lambda x: " ".join([x.id, x.name]), zone_records)
            return PlainTextResponse("\n".join(arr))
        arr = map(lambda x: str(x), zone_records)
        return PlainTextResponse("\n".join(arr))
    return {"length": len(zone_records), "zone_records": zone_records}


@app.get("/cloudflare/dns")
def get_all_cloudflare_dns_records(table=False,
                                   name_only=False,
                                   cols: str = Query("")):
    dns_records = cloudflareapi.list_dns()
    if table:
        if cols:
            cols = cols.split(",")
            arr = map(lambda x: " ".join([getattr(x, key) for key in cols]),
                      dns_records)
            return PlainTextResponse("\n".join(arr))
        if name_only:
            arr = map(lambda x: " ".join([x.id, x.name]), dns_records)
            return PlainTextResponse("\n".join(arr))
        arr = map(lambda x: str(x), dns_records)
        return PlainTextResponse("\n".join(arr))
    return {"length": len(dns_records), "dns_records": dns_records}


@app.post("/cloudflare/dns")
def create_cloudflare_dns_record(body: CreateDnsRequest):
    response = cloudflareapi.create_dns(body)
    return response


@app.put("/cloudflare/dns/{id}")
def update_cloudflare_dns_record(id: str, body: UpdateDnsRequest):
    response = cloudflareapi.update_dns(id, body)
    return response


@app.delete("/cloudflare/dns/{id}")
def delete_cloudflare_dns_record(id: str):
    response = cloudflareapi.delete_dns(id)
    return response


def main():
    args = parser.parse_args()
    profiles.load_from_file(args.config)
    if args.profile: profiles.set_selected_key(args.profile)

    c = profiles.get_selected()
    if not c: raise Exception("no profile selected")

    try:
        uvicorn.run(app, host=c.bind, port=c.port)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
