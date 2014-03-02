import sqlite3 as sqlite
import numpy as np
import sys

fname = sys.argv[1]
con = None

data = np.genfromtxt(fname=fname, skip_header=1, delimiter=',',
                     dtype=None)
patid = data[0][2]
age = data[1][2]
gender = data[2][2]
height = data[3][2]
icuType = data[4][2]
weight = data[5][2]

try:
    con = sqlite.connect('../data/data.db')

    with con:
        cur = con.cursor()

        cmdstr = "INSERT INTO pinfo VALUES(%d, %d, %d, %d, %d, %d);" \
                % (patid, age, gender, height, icuType, weight)
        # print cmdstr
        cur.execute(cmdstr)

        for (t, p, v) in data[6:]:
            cmdstr = "INSERT INTO vstats VALUES(%d, '%s', '%s', %f);" % \
                    (patid, t, p, v)
            # print cmdstr
            cur.execute(cmdstr)

except sqlite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    con.close()
