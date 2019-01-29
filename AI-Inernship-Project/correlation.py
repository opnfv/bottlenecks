import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
dataset = pandas.read_csv(
    'posca_factor_ping-final.csv', usecols=[2, 3, 4, 5, 6], engine='python', skipfooter=3)
plt.rcParams['figure.figsize'] = [16, 6]
fig, ax = plt.subplots(nrows=1, ncols=3)
ax = ax.flatten()
cols = ['duration_time', 'success_time', 'no_of_stacks']
colors = ['#415952', '#f35134', '#243AB5', '#243AB5']
j = 0
for i in ax:
    if j == 0:
        i.set_ylabel('result')
    i.scatter(dataset[cols[j]], dataset['result'], alpha=0.5, color=colors[j])
    i.set_xlabel(cols[j])
    i.set_title('Pearson: %s' %
                dataset.corr().loc[cols[j]]['result'].round(2) +
                ' Spearman: %s' %
                dataset.corr(method='spearman').loc[cols[j]]['result'].round(2))
    j += 1
mpg_data = pd.read_csv('posca_factor_ping-final.csv')
mpg_data.head()
mpg_data.drop(['stop_date', 'start_date'], axis=1).corr(method='pearson')
sns.heatmap(mpg_data.corr(), annot=True, fmt=".3f")
plt.show()
mpg_data = pd.read_csv('posca_factor_ping-final.csv')
mpg_data.head()
mpg_data.drop(['stop_date', 'start_date'], axis=1).corr(method='spearman')
sns.heatmap(mpg_data.corr(), annot=True, fmt=".3f")
plt.show()
sns.jointplot(
    data=mpg_data,
    x='duration_time',
    y='success_rate',
    kind='reg',
    color='g')
plt.show()
sns.jointplot(
    data=mpg_data,
    x='no_of_stacks',
    y='success_rate',
    kind='reg',
    color='g')
plt.show()
