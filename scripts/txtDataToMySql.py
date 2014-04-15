import MySQLdb
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
    con = MySQLdb.connect(host="localhost", user="root",
                          passwd="", db="icu")

    with con:
        cur = con.cursor()

        for (t, p, v) in data:
            if (p == 'RecordID' and t == '00:00'):
                patid = v
            elif (p == 'Age' and t == '00:00'):
                age = v
            elif (p == 'Gender' and t == '00:00'):
                gender = v
            elif (p == 'Height' and t == '00:00'):
                height = v
            elif (p == 'ICUType' and t == '00:00'):
                icuType = v
            elif (p == 'Weight' and t == '00:00'):
                weight = v
            else:
                # time is initially recored as HH:MM
                # MySQL wants HH:MM:SS
                t = t + ":00"
                # Assuming we already have assigned RecordID to patid
                cmdstr = ('INSERT INTO vstats (id, time, var, value) VALUES ('
                          + str(patid) + ', "' + t + '", "'
                          + p + '", ' + str(v) + ');')
                cur.execute(cmdstr)

        cmdstr = ('INSERT INTO pinfo VALUES('
                  + str(patid) + ', ' + str(age) + ', ' + str(gender) + ', '
                  + str(height) + ', ' + str(icuType) + ', '
                  + str(weight) + ');')
        cur.execute(cmdstr)

except MySQLdb.Error, e:
    try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)
    finally:
        sys.exit(1)
finally:
    con.close()
