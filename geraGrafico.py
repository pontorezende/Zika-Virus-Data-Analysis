import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker

# getting data and define my dataframe
url = 'https://raw.githubusercontent.com/BuzzFeedNews/zika-data/master/data/parsed/brazil/brazil-microcephaly-2016-01-30-table-1.csv'
df = pd.read_csv(url, index_col='state')

# the columns look like this
# no,state,cases_under_investigation,cases_confirmed,cases_discarded,cases_reported_total
# but as I just need integers from columns 'cases_under_investigation' to 'cases_reported_total'
# now I gonna convert all non integers to int and NaN to 0
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')

# graph style
plt.style.use('seaborn-pastel')

# Plotting reported cases
def casosRegistradosEstado():
    df.sort_values(by=['cases_reported_total'], ascending=False).plot(use_index=True, y='cases_reported_total', kind='bar', align='center')
    plt.gca().yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
    plt.title('Casos registrados em 2016')
    plt.xticks(rotation=75)
    plt.ylabel('n de casos registrados')
    return plt.show()

# Plotting difference between confirmed cases and discarted cases
def compConfDisc():
    indice = np.arange(27)
    plt.plot(indice, df['cases_confirmed'], '--', marker='o',  label='confirmados')
    plt.plot(indice, df['cases_discarded'], '.-.', marker='x', label='descartados', color='xkcd:salmon')
    plt.grid()
    plt.gca().yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
    plt.legend(loc='best')
    plt.xticks(indice, df.index)
    plt.xticks(rotation=90)
    plt.tight_layout()
    return plt.show()

# % of confirmed cases per states
def casosConfirmados():
    # creating a new dataframe without values equals 0
    df_slice = df.copy()
    df_slice.drop(df_slice[df_slice.cases_confirmed == 0].index, inplace=True)

    plt.pie(df_slice['cases_confirmed'], labels=df_slice.index, autopct='%1.1f %%',
            pctdistance=.8, wedgeprops={'linewidth': 3, 'edgecolor': 'white'})

    #create white circle/hole in pie graph
    c = plt.Circle((0,0), 0.5, color='white')
    plt.gca().add_artist(c)
    plt.axis('equal')
    plt.tight_layout()
    return plt.show()