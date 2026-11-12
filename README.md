## Project goals

This project repository is for the midterm project of Machine Learning ZoomCamp 2026. The objective is to select a dataset, identify a problem, and apply a machine learning approach to solve it. Additionally, technical aspects of a Python project are put into practice, such as documentation, reproducibility, environment management, and web deployment. For this stage of the course, the objective is not to select a complex problem but rather to present a machine learning solution to a simple problem in a well-structured manner.

## Prediction of the NVIDIA assets

For this project, I chose the Kaggle dataset [NVIDIA_DATA](https://www.kaggle.com/datasets/muhammadishahrukh/nvidia-historical-stock-data), containing the price of the NVIDIA assets from 1999 to September 2026. The proposed problem is to use these data to train a model that predicts the closing price of the assets for the next 7 days from today's data. Since the closing price is a very volatile variable, we work with the relative variation from one trading session to the next week, which is a more stable quantity. For people from areas not related to finances, a brief description of what the different variables included in the dataset are is provided in [Section `Asset-price feature definitions`](## Asset-price feature definitions).

## Prerequisites
- Python >= 3.13.
- uv library: `pip install uv`

## Installation

In a terminal, go to the project's path and run
```
uv sync
```

To use the jupyter notebook inside the project, run
```
uv run --with jupyter jupyter lab
```
to open this into your web browser, or choose the environment's kernel from the kernel's list if you open the notebook in VS Code.

To load the model as a web service, move to the folder `src\nvidia_stock` inside the project's directory, and run
```
uv run uvicorn stock_api:app --host 0.0.0.0 --port 9696
```
Then, in the same directory, run the script that deploys and evaluates the model with the command
```
uv run deploy_stock_predictor.py
```
You will be asked whether you are deploying the model from the web service hosted on the cloud or if you initiated in into your local machine.

Build the docker image by running in the project's head directory
```
docker build -t predict-assets-price .
```
and run it in the same directory with the command
```
docker run -it --rm -p 9696:9696 predict-assets-price
```
Remember that even though the Docker image is run from the head directory, the script that evaluates the model is located in `src\nvidia_stock`.

The web service is served in the Railway cloud provider. To access this, run the deploy_stock_predictor.py script and select the `y` option when the program asks you if you are using the web service hosted on the cloud. The script already contains the service url
```
midterm-project-mlzoomcamp2026-datapipeline-production.up.railway.app/predict
```

If you are interested in using this web provider, it only requires you to enter the project's repository containing the Dockerfile (preferably in the main directory, otherwise specify the subdirectory), and then go to your service → Settings → Networking → Generate Domain.

**Important note**: Railway only provides a finite amount of free credits for new users, and a free trial period of 30 days. So the web service will be available for deployment from Railway only during the peer-review period of this course's project. Afterwards, the web service will only be accessible via locally running the API.

## Asset-price feature definitions

Let $O_t$, $H_t$, $L_t$, $C_t$, and $V_t$ denote the open, high, low, close, and volume of an asset on trading session $t$. Let $C_{t-1}$ denote the close on the previous trading session.

The target variable `future weekly return` is not directly available in the provided dataset, so we compute it manually and add it to the dataframe as an additional column. It is computed as
```math
\text{weekly return pct}_t
=
\left(\frac{C_{t+7}-C_{t}}{C_{t}}\right)
```
The expressions below that are related to variations in price are expressed in percentage.

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
