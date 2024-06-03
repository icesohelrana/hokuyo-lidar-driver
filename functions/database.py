from iterator import IteratorFile
def insert_lidar_angles(cur,con,degree_angles,radian_angles):
    values = []
    for i,(degree_angle,radian_angle) in enumerate(zip(degree_angles,radian_angles)):
        values.append((i,degree_angle,radian_angle))
    args = ','.join(cur.mogrify("(%s,%s,%s)", i).decode('utf-8')
                for i in values)
    cur.execute("""INSERT INTO "Angles" (index,degree,radian) VALUES """+args+"""ON CONFLICT DO NOTHING""")
    con.commit()

def insert_background_scan(cur,con,degree_angles,scans):
    values = []
    for i,(degree_angle,scan) in enumerate(zip(degree_angles,scans)):
        values.append((i,degree_angle,float(scan)))
    args = ','.join(cur.mogrify("(%s,%s,%s)", i).decode('utf-8')
                for i in values)
    cur.execute("""INSERT INTO "Background" (index,angles,scan) VALUES """+args+"""ON CONFLICT DO NOTHING""")
    con.commit()

def store_scans_to_db(values,db_config):
    '''Asynchronous process to store scan in database'''
    
    try:
        con = psycopg2.connect(**db_config)
        cur = con.cursor()
        f = IteratorFile(("{}\t{}".format(x[0], x[1]) for x in values))
        cur.copy_from(f, "Scans", columns=('timestamp', 'scan'))
        con.commit()
        con.close()
        return
    except:
        print("Error in inserting into database")
        exit()
