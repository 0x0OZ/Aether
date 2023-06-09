#!/usr/bin/python3
# Simplicity and Readability is our concern.

import subprocess
import json
import time
import mongo

Peers = []
Logs = []


DB = "mongodb://localhost:27017/"
DB_NAME = "monate"
DB_NODES_COLLECTION = "nodes"
DB_PUBLIC_NODES_COLLECTION = "public_nodes"
DB_LOGS_COLLECTION = "logs"

DEFAULT_PEERS = ["127.0.0.1"]
RPC_ADMIN_PEERS = "admin_peers"
RPC_NET_VERSION = "net_version"

CONNECTION_TIMEOUT = 1  # seconds
UPDATE_CONNECTED_PEERS = 6 * 60
RUN_CODE_TIMES = 1  # code runs value * RUN_CODE_TIMES_MULTIPLY
RUN_CODE_TIMES_MULTIPLY = 10


def get_cmd(node_url, port, call):
    return [
        "curl",
        "-s",
        "--connect-timeout",
        str(CONNECTION_TIMEOUT),
        "-H",
        "Content-Type: application/json",
        "-X",
        "POST",
        "--data",
        '{"jsonrpc":"2.0","method":"' + call + '","params":[],"id":67}',
        node_url + ":" + port,
    ]


def node_call(url, port, call):
    global Logs
    cmd = get_cmd(url, port, call)
    results = json.loads(subprocess.check_output(cmd).decode())
    Logs.append(results)
    return results  # {"jsonrpc":"<int>","id":<int>, "results": [ {} ] }


def get_peers(node, port="8545"):
    peers = node_call(node, port, RPC_ADMIN_PEERS)["result"]
    return (
        peers,
        [peer["network"]["remoteAddress"].split(":")[0] for peer in peers],
    )  # [ip]


def check_rpc(peers=[], port="8545"):
    public_nodes = []
    for peer in peers:
        cmd = get_cmd(peer, port, RPC_NET_VERSION)
        try:
            int(subprocess.check_output(cmd)["result"])
            public_nodes.append(peer)
        except:
            pass

    return public_nodes  # [ip]


def has_rpc(peer, port="8545"):
    cmd = get_cmd(peer, port, RPC_NET_VERSION)
    try:
        int(json.loads(subprocess.check_output(cmd))["result"])
        return True
    except:
        return False


def store_peers(peers=[]):  # write to db
    pass


def read_peers():  # read db
    pass


def get_public_peers(nodes):
    peers = []
    for node in nodes:
        if has_rpc(node):
            peers.append(node)
    return peers


def add_peers(peers):  # return new peers || IGNORE
    new_peers = []
    for peer in peers:
        if peer not in Peers:
            new_peers.append(peer)
    return new_peers


def main():
    global Peers
    global Logs
    monate = mongo.Monate(
        DB, DB_NAME, DB_NODES_COLLECTION, DB_PUBLIC_NODES_COLLECTION, DB_LOGS_COLLECTION
    )
    connected_peers = DEFAULT_PEERS
    time_start = time.time()
    for x in range(RUN_CODE_TIMES):
        print("===============================================")
        print("Connected Peers:", connected_peers)
        for i in range(RUN_CODE_TIMES_MULTIPLY):
            print(f"[{(i+1)+(x*10)}] - Scanning..", end=".\r")
            new_peers = []
            for peer in connected_peers:
                (_, tmp) = get_peers(peer)
                new_peers += tmp

            new_peers = list(dict.fromkeys(new_peers))
            connected_peers = list(
                dict.fromkeys(connected_peers + check_rpc(new_peers))
            )
            Peers += new_peers
            time.sleep(0.5)
            if time.time() >= time_start + (UPDATE_CONNECTED_PEERS):
                connected_peers = check_rpc(connected_peers)
        print()
        print("New Peers:", Peers)
        monate.insert_peers(list(map(lambda x: {"node": x}, Peers)))
        monate.insert_logs(Logs)
        monate.insert_public_peers(list(map(lambda x: {"": x}, connected_peers)))
        Peers = []
        Logs = []


if __name__ == "__main__":
    main()
