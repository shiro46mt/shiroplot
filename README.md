# shiroplot
Shiroplot is a Python visualization library inspired by seaborn.

# Installation
Use pip
```
pip install git+https://github.com/shiro46mt/shiroplot
```

# Usage - Highlight chart
Draw seaborn charts, highlighting the specific items.

The following seaborn functions are supported.
- `sns.scatterplot`
- `sns.lineplot`
- `sns.histplot`

## 📊 Scatter plot with highlight
```python
import seaborn as sns
df = sns.load_dataset('tips')

import shiroplot as splt
splt.scatterplot(data=df, x='total_bill', y='tip', hue='day', highlights=['Sat', 'Sun'])
```
![highlight-scatterplot-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/highlight-scatterplot-01.png)

## 📊 Line plot with highlight
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.lineplot(data=df, x='Year', y='Life_Expectancy', hue='Country', highlights=['Japan', 'USA'])
```
![highlight-lineplot-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/highlight-lineplot-01.png)

## 📊 Histgram with highlight
```python
import seaborn as sns
df = sns.load_dataset('penguins')

import shiroplot as splt
splt.histplot(data=df, x='flipper_length_mm', hue='species', highlights='Adelie')
```
![highlight-histplot-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/highlight-histplot-01.png)

# Usage - Additional charts
Draw charts which is not implemented in seaborn.
- Slope chart
- Dumbbell chart

## 📊 Slope chart
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.slopechart(data=df, x='Year', y='Life_Expectancy', group='Country', x_items=[2018, 2020],
    increase_color='tab:red', decrease_color='tab:blue', even_color='dimgray', size=8, fmt='{:.1f}', margin=0.2)
```
![slopechart-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/slopechart-01.png)

## 📊 Dumbbell chart
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.dumbbellchart(data=df, group='Year', x='Life_Expectancy', y='Country', group_items=[2019, 2020],
    beforecolor='dimgray', aftercolor='tab:red', edgecolor='gray', size=8)
```
![dumbbellchart-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/dumbbellchart-01.png)

# License
This software is released under the MIT License, see LICENSE.

# Reference
https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
