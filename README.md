# shiroplot
Shiroplot is a Python visualization library inspired by seaborn.

## Installation
Use pip
```
pip install git+https://github.com/shiro46mt/shiroplot
```

## Usage

### Highlight chart
Draw seaborn chart, highlighting the specific items.

#### 📊 Scatter plot with highlight
```python
import seaborn as sns
df = sns.load_dataset('tips')

import shiroplot as splt
splt.highlightplot(func=sns.scatterplot, data=df, x='total_bill', y='tip', hue='day', highlights=['Sat', 'Sun'], ax=ax)
```
![highlight-scatterplot-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/highlight-scatterplot-01.png)

#### 📊 Line plot with highlight
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.highlightplot(func=sns.lineplot, data=df, x='Year', y='Life_Expectancy', hue='Country', highlights=['Japan', 'USA'], ax=ax)
```
![highlight-lineplot-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/highlight-lineplot-01.png)

#### 📊 Histgram with highlight
```python
import seaborn as sns
df = sns.load_dataset('penguins')

import shiroplot as splt
splt.highlightplot(func=sns.histplot, data=df, x='flipper_length_mm', hue='species', highlights='Adelie', binwidth=3, ax=ax)
```
![highlight-histplot-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/highlight-histplot-01.png)

---

### Slope chart
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.slopechart(data=df, x='Year', y='Life_Expectancy', group='Country', x_items=[2018, 2019, 2020], fmt='{:.1f}')
```
![slopechart-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/slopechart-01.png)

### Dumbbell chart
```python
import seaborn as sns
df = sns.load_dataset('healthexp')

import shiroplot as splt
splt.dumbbellchart(data=df, group='Year', x='Life_Expectancy', y='Country', group_items=[2019, 2020], ax=ax)
```
![dumbbellchart-01](https://raw.githubusercontent.com/shiro46mt/shiroplot/images/dumbbellchart-01.png)

# License
This software is released under the MIT License, see LICENSE.

## Reference
https://www.machinelearningplus.com/plots/top-50-matplotlib-visualizations-the-master-plots-python/
