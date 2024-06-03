import os
from hokuyolx import HokuyoLX
import hokuyolx
import datetime
import psycopg2
import math
import threading
import datetime
import pandas as pd

from function.config import get_db_config, get_lidar_config,store_config
from function.database import insert_lidar_angles,insert_background_scan,store_scans_to_db
from function.iterator import IteratorFile


db_config = get_db_config()
lidar_ip_address,lidar_port = get_lidar_config()
skips,number_of_processed_scans,async_db_store = store_config()

# Connect to database
con = psycopg2.connect(**db_config)
cur = con.cursor()

# Define the laser and its configuratio
laser = HokuyoLX(addr=(lidar_ip_address, lidar_port),buf=1024,timeout=300,time_tolerance=3000,info=False)

# Read and save lidar angles
radian_angles = laser.get_angles()
degree_angles = radian_angles * 180 / math.pi
print("angles", degree_angles)

insert_lidar_angles(cur,con,degree_angles,radian_angles)

is_bg_selected=False
# Store fist scan on background scan
while is_bg_selected==False:
    try:
        for bg_scan, timestamp, _ in laser.iter_dist(0,skips=skips):            
            insert_background_scan(cur,con,degree_angles,bg_scan)
            is_bg_selected=True
            continue
    except hokuyolx.exceptions.HokuyoChecksumMismatch as e:
        continue
    except hokuyolx.exceptions.HokuyoStatusException as e:
        continue
    except hokuyolx.exceptions.HokuyoException as e:
        continue
# Continious store of lidar scan streams
values = []
while True:
    try:
        for scan, timestamp, _ in laser.iter_dist(0,skips=skips):
            scan_str = str(scan.round(3).astype(str).tolist()).replace("'", "")
            values.append((pd.to_datetime(timestamp, utc=True, unit='ms'),scan_str))
            if len(values)>=number_of_processed_scans:
                try:
                    if async_db_store:
                        new_thread = threading.Thread(target=store_scans_to_db,args=(values,db_config))
                        new_thread.start()
                    else:
                        f = IteratorFile(("{}\t{}".format(x[0], x[1]) for x in values))
                        cur.copy_from(f, "Scans", columns=('timestamp', 'scan'))
                        con.commit()
                    values = []
                except:
                    print("Error in database connection")
                    continue
    except hokuyolx.exceptions.HokuyoChecksumMismatch as e:
        continue
    except hokuyolx.exceptions.HokuyoStatusException as e:
        continue
    except hokuyolx.exceptions.HokuyoException as e:
        continue


