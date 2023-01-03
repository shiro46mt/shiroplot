# shiroplot
Shiroplot is a Python visualization library inspired by seaborn.

## Installation
Use pip
```
pip install git+https://github.com/shiro46mt/shiroplot
```

## Usage

### Slope chart
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.slopechart(data=df, x='Year', y='Life_Expectancy', group='Country', x_items=[2018, 2019, 2020], fmt='{:.1f}')
```
![slopechart-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/slopechart-01.png)

## Reference
https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
