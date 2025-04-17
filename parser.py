from config import Host, ConfigLine
import json

# def parse_file(config):
#     hosts = []
#     idx = 0
#     for line in config:
#         in_host = False
#         configline = line.strip()
#         if (configline.startswith("Host ")):
#             in_host = True
#             k, v = parse_file(configline)
#             hosts[idx].append(Host())
#             idx += 1
#         elif in_host:
#             print(hosts[idx - 1].name, parse_line(configline))
#         else:
#             print("White space")
#     return hosts
#


def parse_file(config):
    in_host = False
    hosts = []
    idx = 0
    for line in config:
        if (line.strip()):
            values = parse_line(line)
            key = values[0]
            value = values[1]
            if (key == "Host"):
                in_host = True
                hosts.append(Host(name=value))
            elif in_host:
                hosts[len(
                    hosts) - 1].add_config(ConfigLine(hosts[len(hosts) - 1].name, key, value))

    return hosts


def parse_line(line):
    if (line.strip()):
        clean = " ".join(line.split())
        key, sep, value = clean.partition(" ")
        return [key, value]
