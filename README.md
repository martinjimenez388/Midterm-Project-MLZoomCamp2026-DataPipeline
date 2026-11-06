This project repository is for the midterm project of Machine Learning ZoomCamp 2026. The objective is to select a dataset, identify a problem, and apply a machine learning approach to solve it. Additionally, technical aspects of a Python project are put into practice, such as documentation, reproducibility, environment management, and web deployment. For this stage of the course, the objective is not to select a complex problem but rather to present a machine learning solution to a simple problem in a well-structured manner.

For this project, 

## Asset-price feature definitions

Let $O_t$, $H_t$, $L_t$, $C_t$, and $V_t$ denote the open, high, low, close, and volume of an asset on trading session $t$. Let $C_{t-1}$ denote the close on the previous trading session.

The expressions below use decimal fractions. Multiply each result by $100$ if the feature is intended to be expressed in percent.

### Returns

```math
\text{daily return pct}_t
=
100\left(\frac{C_t-C_{t-1}}{C_{t-1}}\right)
```

```math
\text{log return}_t
=
\ln\left(\frac{C_t}{C_{t-1}}\right)
```

```math
\text{intraday return pct}_t
=
100\left(\frac{C_t-O_t}{O_t}\right)
```

```math
\text{overnight gap pct}_t
=
100\left(\frac{O_t-C_{t-1}}{C_{t-1}}\right)
```

### Price range

```math
\text{daily range pct}_t
=
100\left(\frac{H_t-L_t}{C_{t-1}}\right)
```

### Moving averages

```math
\text{sma}_{20,t}
=
\frac{1}{20}\sum_{i=0}^{19}C_{t-i}
```

```math
\text{sma}_{50,t}
=
\frac{1}{50}\sum_{i=0}^{49}C_{t-i}
```

```math
\text{volume sma}_{20,t}
=
\frac{1}{20}\sum_{i=0}^{19}V_{t-i}
```

### Rolling volatility

Let

```math
r_t=\ln\left(\frac{C_t}{C_{t-1}}\right)
```

be the daily log return. The 20-session rolling sample standard deviation is

```math
\text{volatility}_{20,t}
=
100\sqrt{
\frac{1}{19}
\sum_{i=0}^{19}
\left(r_{t-i}-\bar r_t\right)^2
}
```

where

```math
\bar r_t
=
\frac{1}{20}\sum_{i=0}^{19}r_{t-i}.
```

### Drawdown

```math
\text{drawdown pct}_t
=
100\left(
\frac{C_t-\max_{i\le t}C_i}
{\max_{i\le t}C_i}
\right)
```

### Notes

- The daily return is close-to-close and includes the overnight gap.
- The intraday return is open-to-close.
- The overnight gap is previous-close-to-current-open.
- The daily range is normalized here by the previous close.
- The drawdown is non-positive whenever the current close is below its historical maximum.
- The moving averages and rolling volatility are undefined for the first $19$ or $49$ sessions unless an expanding window is used.
