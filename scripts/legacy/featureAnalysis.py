import sys
import sqlite3 as sqlite
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.tools.merge import concat


def create_df():
    query = {
        'mortality': """
SELECT id, vstats.time, vstats.var, vstats.value
FROM outcome JOIN vstats USING (id)
WHERE outcome.death = 1""",
        'survival': """
SELECT id, vstats.time, vstats.var, vstats.value
FROM outcome JOIN vstats USING (id)
WHERE outcome.death = 0""",
    }

    con = None
    col_names = ('id', 'time', 'var', 'value')
    data = {}
    df = {}

    try:
        con = sqlite.connect('data/data.db')

        with con:
            cur = con.cursor()

            cur.execute(query['mortality'])
            data['mortality'] = cur.fetchall()
            cur.execute(query['survival'])
            data['survival'] = cur.fetchall()

    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        con.close()

        df['mortality'] = pd.DataFrame.from_records(data['mortality'])
        df['mortality'].columns = col_names
        df['mortality'] = pd.pivot_table(df['mortality'],
                                         values='value',
                                         rows=['id', 'time'],
                                         cols='var')
        df['mortality']['death'] = np.ones(len(df['mortality']))

        df['survival'] = pd.DataFrame.from_records(data['survival'])
        df['survival'].columns = col_names
        df['survival'] = pd.pivot_table(df['survival'],
                                        values='value',
                                        rows=['id', 'time'],
                                        cols='var')
        df['survival']['death'] = np.ones(len(df['survival']))

        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        df['survival'].to_pickle('data/survival.pkl')
        df['mortality'].to_pickle('data/mortality.pkl')

        return df


def main():
    try:
        print "Attempting to read pickle-d DataFrames."
        df = {}
        df['survival'] = pd.DataFrame()
        df['mortality'] = pd.DataFrame()

        df['survival'] = pd.read_pickle('data/survival.pkl')
        df['mortality'] = pd.read_pickle('data/mortality.pkl')
        print "DataFrames imported!"
    except:
        print "Reading failed! Creating DataFrames."
        df = create_df()
    finally:

        # print "Creating mortality scatter plot matrix."
        # plt.figure()
        # pd.tools.plotting.scatter_matrix(df['mortality'])
        # F = plt.gcf()
        # F.set_size_inches((50, 50))
        # F.savefig('graphs/scatter_mortality.png',
        #           bbox_inches='tight',
        #           dpi=150)
        #
        # print "Creating survival scatter plot matrix."
        # plt.figure()
        # pd.tools.plotting.scatter_matrix(df['survival'])
        # F = plt.gcf()
        # F.set_size_inches((50, 50))
        # F.savefig('graphs/scatter_survival.png',
        #           bbox_inches='tight',
        #           dpi=150)

        print "Creating Andrew plot."
        plt.figure()
        pd.tools.plotting.andrews_curves(concat([df['mortality'][0::10],
                                                 df['survival'][0::10]]),
                                         'death')
        F = plt.gcf()
        F.set_size_inches((10, 10))
        F.savefig('graphs/andrews_curves.png',
                  bbox_inches='tight',
                  dpi=150)


if __name__ == '__main__':
    main()
