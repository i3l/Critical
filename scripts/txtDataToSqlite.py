import sqlite3 as sqlite
import numpy as np
import sys

fname = sys.argv[1]
con = None

data = np.genfromtxt(fname=fname, skip_header=1, delimiter=',',
                     dtype=None)

# Patient descriptors go into the pinfo table. Patient descriptors denoted
# by timestamp of 00:00 and parameter names:
#       RecordID
#       Age
#       Gender
#       Height
#       ICUType
#       Weight
try:
    con = sqlite.connect('data/data.db')

    with con:
        cur = con.cursor()

        for (t, p, v) in data:
            if (p == 'RecordID'):
                patid = v
            elif (p == 'Age'):
                age = v
            elif (p == 'Gender'):
                gender = v
            elif (p == 'Height'):
                height = v
            elif (p == 'ICUType'):
                icuType = v
            elif (p == 'Weight'):
                weight = v
            else:
                # Assuming we already have assigned RecordID to patid
                cmdstr = ('INSERT INTO vstats VALUES('
                          + str(patid) + ', "' + t + '", "'
                          + p + '", ' + str(v) + ');')
                cur.execute(cmdstr)

        cmdstr = ('INSERT INTO pinfo VALUES('
                  + str(patid) + ', ' + str(age) + ', ' + str(gender) + ', '
                  + str(height) + ', ' + str(icuType) + ', '
                  + str(weight) + ');')
        cur.execute(cmdstr)

except sqlite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    con.close()
