First configure the hokuyo lidar and find the IP address and port address

Create a postgres database:

    psql -U postgres -d postgres -f schema.sql


Run the driver to store scan in realtime with maximum frequency>=40Hz

    docker build -f Dockerfile -t hokuyo-driver-test:latest .


    docker run -d -it \
    --net=host \
    -e DB_HOST=3.26.77.78 \
    -e DB_NAME=postgres \
    -e DB_USER=postgres \
    -e DB_PASSWORD=pass \
    -e LIDAR_IP_ADDRESS=192.168.0.10 \
    -e LIDAR_PORT=10940 \
    -e SCAN_FREQUENCY=40 \
    -e ASYNC_DB_STORE=True \
    -e NUMBER_OF_PROCESSED_SCANS=200 \
    --restart always \
    hokuyo-driver-test:latest

Here, 
    
    NUMBER_OF_PROCESSED_SCANS = How many scans are stored at once in database
    DB_ = Database configuration
    LIDAR_IP_ADDRESS = ip address of connected lidar
    LIDAR_PORT = port of the lidar
    SCAN_FREQUENCY = Control Lidar frequency, default = 40 Hz, but can change to lower frequency
    ASYNC_DB_STORE = True, If want to store scans parallelly

      