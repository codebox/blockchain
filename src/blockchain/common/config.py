config = {
    'difficulty' : 20,
    'block_size' : 5,
    'block_reward' : 10,
    'block_reward_from' : '0',
    'key_store_dir' : '.',
    'key_format' : 'pem',
    'key_size' : 1024,
    'blockchain_store' : 'blockchain.json',
    'genesis_block_id' : 'genesis',
    'status_broadcast_interval_seconds' : 5,
    'transaction_broadcast_interval_seconds' : 5,
    'status_broadcast_port' : 2606,
    'block_server_port' : 2607,
    'transaction_port' : 2608
}


def update_config_from_args(args):
    other_args = []
    for arg in args:
        k, v = arg.split('=') if '=' in arg else (None,None)
        if k in config:
            if isinstance(config[k], int):
                config[k] = int(v)
            else:
                config[k] = v
        else:
            other_args.append(arg)

    return other_args