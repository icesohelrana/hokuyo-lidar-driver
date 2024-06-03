import os
def get_db_config():
    '''Get database configurations from environment variables.'''

    db_config = {}
    if "DB_HOST" in os.environ and \
       "DB_NAME" in os.environ and \
       "DB_USER" in os.environ and \
       "DB_PASSWORD" in os.environ:

        db_config['host'] = os.environ.get('DB_HOST')
        db_config['database'] = os.environ.get('DB_NAME')
        db_config['user'] = os.environ.get('DB_USER')
        db_config['password'] = os.environ.get('DB_PASSWORD')
    else:
        print("Set DB_HOST, DB_NAME, DB_USER and DB_PASSWORD environment variables.")
        exit()

    return db_config
def get_lidar_config():
    # Get lidar ip address and port from environment variables
    if "LIDAR_IP_ADDRESS" in os.environ:
        lidar_ip_address = os.environ.get('LIDAR_IP_ADDRESS')
    else:
        print('Set LIDAR_IP_ADDRESS environment variable')
        exit()
    if "LIDAR_PORT" in os.environ:
        lidar_port = int(os.environ.get('LIDAR_PORT'))
    else:
        print('Set LIDAR_PORT environment variable')
        exit()
    return lidar_ip_address, lidar_port
def store_config():
    # Default 40 hz
    skips=0 # skip=0 means no scan will be skipped
    if "SCAN_FREQUENCY" in os.environ:
        if int(os.environ.get('SCAN_FREQUENCY'))==40:
            skips=0
        if int(os.environ.get('SCAN_FREQUENCY'))==20:
            skips=1
    number_of_processed_scans=40 # Default 40 scans are stored at once
    if "NUMBER_OF_PROCESSED_SCANS" in os.environ:
        number_of_processed_scans = int(os.environ.get('NUMBER_OF_PROCESSED_SCANS'))
    async_db_store=True # Default True for storing data asyncronously
    if "ASYNC_DB_STORE" in os.environ:
        async_db_store = eval(os.environ.get('ASYNC_DB_STORE'))
    return skips,number_of_processed_scans,async_db_store
