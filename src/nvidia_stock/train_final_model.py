import kagglehub
from kagglehub import KaggleDatasetAdapter
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import pickle

df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "muhammadishahrukh/nvidia-historical-stock-data",
    "nvda_stock_clean.csv",
)

df["weekly_return_pct"] = df["close"].shift(-7) / df["close"] - 1
df = df.iloc[:-7]

for var in ["sma_20", "sma_50", "volatility_20_pct", "volume_sma_20"]:
    avr = df[var].mean()
    df[var] = df[var].fillna(avr)

df = df.drop(columns=["ticker", "date"])

df_train, df_val = train_test_split(
    df, test_size=0.3, random_state=1
)

train_dict = df_train.drop(['weekly_return_pct'], axis=1).to_dict(orient='records')
val_dict = df_val.drop(['weekly_return_pct'], axis=1).to_dict(orient='records')

pipeline = make_pipeline(
    DictVectorizer(sparse=False),
    RandomForestRegressor(n_estimators=50, max_depth=25, random_state=42)
)

pipeline.fit(train_dict, df_train['weekly_return_pct'])
y_pred = pipeline.predict(val_dict)
print("RMSE for random split: ", root_mean_squared_error(df_val['weekly_return_pct'], y_pred))

with open('RF_NVIDIA_model.bin', 'wb') as f_out:
    pickle.dump(pipeline, f_out)