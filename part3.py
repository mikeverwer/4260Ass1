# part3.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

def split_train_test_pd(df, test_size=0.2):
    train_dfs = []
    test_dfs = []
    for name, group in df.groupby('name'):
        n = len(group)
        train_split = int(n * (1 - test_size))
        train = group.iloc[:train_split]
        test = group.iloc[train_split:]
        train_dfs.append(train)
        test_dfs.append(test)
    return pd.concat(train_dfs), pd.concat(test_dfs)

def shift_align(X, y):
    y = y.shift(-1)[:-1]
    X = X[:-1]
    return X, y

# Importing Data and Defining Features
df = pd.read_csv('all_stocks_5yr.csv', parse_dates=['date'])
df = df.sort_values(['name', 'date'])

features = ['open', 'high', 'low', 'volume', 'SMA_20', 'RSI_14']
target = 'close'

# Adding Technical Indicators
# SMA: 20-day moving average of close
df['SMA_20'] = df.groupby('name')['close'].transform(lambda x: x.rolling(20).mean())

# RSI: 14-day relative strength index
delta = df.groupby('name')['close'].transform(lambda x: x.diff())
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
df['RSI_14'] = 100 - (100 / (1 + rs))

# Splitting Data
train, test = split_train_test_pd(df)
train.dropna(inplace=True)
test.dropna(inplace=True)

X_train_pd, y_train_pd = shift_align(train[features], train[target])
X_test_pd, y_test_pd = shift_align(test[features], test[target])

# Training model
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train_pd, y_train_pd)

# Preparing dataframe for dashboard
features_df = df[features]
predictions = rf.predict(features_df)
df['predicted_close'] = predictions

# Building dashboard
st.title("Stock Price Prediction")
# Dropdown: pick company
company = st.selectbox("Select company", sorted(df["name"].unique()))
# Slider: past N days
N = st.slider("Number of past days", min_value=10, max_value=365, value=30)
# Filter data
df_c = df[df["name"] == company].sort_values("date").tail(N)

st.line_chart(
    df_c.set_index("date")[["close", "predicted_close"]],
    height=400
)