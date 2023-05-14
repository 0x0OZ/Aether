# Aether 
- this tool designed to demonstrate how much a publically accessible node could be abused. 

## variables
- `Peers` [] => every found peer
- `Logs` [] => every received API response
## methods

- get_cmd(node_url, port, call) => a returns a curl template to API call `call` for `node_url`:`port`
- get_peers() => return 
- detect_vulns() => return 
- check_rpc(peers[]) => check if rpc API is public for  peers[]


## Steps
- `connected_peers` vaiable stores a nodes with accessable JSON-RPC API         **done**
- connect to each node in `connected_peers` JSON-RPC API,                       **done**
- fetch connected peers,                                                        **done**
- check if any of those peers has a public JSON-RPC API,                        **done**
- if one has add it to the `connected_peers` list,                              **done**
- go through the added peers, find vulns using teatime framework.
- store the peers into NoSql database                                           **done**
- store the logs of every `node_call` into NoSql database                       **done**
- store the peers with public accessable JOSON-RPC to some database or storage  **canceled** 
- Repeat.                                                                       **done**


## Design Notes
- methods with return always return arrays
- `Logs` array stores every `node_call` response 

## Storage Design
- MongoDB used.
    - <ip>  
    - <net_version>
    - <personal_listWallets>
    