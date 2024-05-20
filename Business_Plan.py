'''
# =========================================================================
# Where should you open the next catering unit to maximize profits?
# =========================================================================

Central Place Theory explains conditions necessary to create Malls. These are:
Threshold \t– the minimum population and income required to sustain a market
Range \t\t– the maximum distance consumers are prepared to travel to acquire goods

'''

print(__doc__)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import scale


#
data = pd.read_csv('business_plan.csv', index_col=0)

data['TA'] = data['Take_Away'] - data['Take_Away_Delivery']
data['D'] = data['Delivery'] - data['Take_Away_Delivery']
data['R'] = data['Restaurants'] - (data['Take_Away_Delivery'] + data['TA'] + data['D'])
data['TAD'] = data['Take_Away_Delivery']
data['PD'] = data['Population'] / (data['Area'] * 10000)

subset = ['Area', 'Population', 'PD', 'TAD', 'TA', 'D', 'R', 'Restaurants']

df = data.loc[:'Mombasa Road', subset]

df['Product'] = df['Restaurants'] * df['PD']
df['Probability'] = df['Product'] / df['Product'].sum()
df['Entropy'] = -1 * (df['Probability'] * np.log(df['Probability']))


print('-'*70,'\n')
print(df.sort_values('Entropy', ascending=False))
print('-'*70,'\n')