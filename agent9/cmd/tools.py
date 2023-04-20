import time
import uuid
import argparse

parser = argparse.ArgumentParser(prog="agent9-tools")

parser.add_argument("which",
                    help="Which module",
                    choices=["gen-config"],
                    type=str)

config_template = """[default]
id={id}
access_token={access_token}
"""


def main():
    args = parser.parse_args()
    if args.which == "gen-config":
        print(config_template.format(id=uuid.uuid4().hex,
                                     access_token=str(time.time())),
              end="")
