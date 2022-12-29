# shiroplot
Shiroplot is a Python visualization library inspired with seaborn.

## Installation
Use pip
```
pip install git+https://github.com/shiro46mt/shiroplot
```

## Usage

### Slope chart
```
import seaborn as sns
df = sns.load_dataset('healthexp')

sp.slopechart(data=df, x='Year', y='Life_Expectancy', group='Country', x_items=[2018, 2019, 2020], fmt='{:.1f}')
```
![slopechart-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/slopechart-01.png)

## Reference
https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
