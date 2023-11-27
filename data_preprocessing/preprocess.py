from datetime import datetime, timedelta

import pandas as pd


def clean_trades(trades):

    """Cleans trade data by dropping columns, converting datetime to index, and dropping rows with 0 trade volume or price

    Sets Index to be Effective Date + Participant Timestamp


    """
    trades = trades.drop(columns=trades.columns[0:2])

    # convert datetime to index using participant timestamp
    trades["Date"] = pd.to_datetime(trades["Date"])
    trades["Participant_Timestamp"] = pd.to_datetime(
        trades["Participant_Timestamp"].astype(str).str.zfill(15), format="%H%M%S%f"
    )
    trades.index = trades["Date"].apply(lambda x: x) + trades["Participant_Timestamp"].apply(
        lambda x: timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    )

    trades = trades.sort_index()
    trades = trades.drop(columns=["Time"])

    trades = trades.dropna(axis=1, how="all")

    trades = trades[trades["Trade_Volume"] > 0]

    trades = trades[trades["Trade_Price"] > 0]

    grouped_trades = trades.groupby("Date").groups

    # drop trade data outside of market hours

    for day in grouped_trades.keys():
        subset = trades[trades["Date"] == day]
        grouped_trades[day] = subset[subset.index < datetime.strptime(f"{day.date()} 16:00:00", "%Y-%m-%d %H:%M:%S")]
        grouped_trades[day] = subset[subset.index > datetime.strptime(f"{day.date()} 09:30:00", "%Y-%m-%d %H:%M:%S")]

    new_trades = pd.concat(list(grouped_trades.values())).sort_index()

    return new_trades


def clean_quotes(quotes, drop_after_hours=True):

    """Cleans Quotes by removing quotes with invalid spreads, quotes with bid or offer price of 0, and quotes outside of market hours

    Sets Index to Effective Date + Participant Timestamp
    """

    quotes = quotes.drop(columns=quotes.columns[0:2])

    # parse date and time
    quotes["Date"] = pd.to_datetime(quotes["Date"])
    quotes["Participant_Timestamp"] = pd.to_datetime(
        quotes["Participant_Timestamp"].astype(str).str.zfill(15), format="%H%M%S%f"
    )

    # convert datetime to index
    quotes.index = quotes["Date"].apply(lambda x: x) + quotes["Participant_Timestamp"].apply(
        lambda x: timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    )

    quotes = quotes.sort_index()

    quotes = quotes.drop(columns=["Time"])

    quotes = quotes.dropna(axis=1, how="all")

    quotes = quotes[quotes["Offer_Price"] > quotes["Bid_Price"]]  # removed quotes with invalid spreads
    quotes = quotes[quotes["Bid_Price"] > 0]  # bid and offer price >0

    # drop after hours for quotes, preserve if want to prepend lob
    if drop_after_hours:
        quotes["Date"] = quotes.index.date

        grouped_quotes = quotes.groupby("Date").groups

        # drop trade data outside of market hours

        for day in grouped_quotes.keys():
            subset = quotes[quotes["Date"] == day]
            grouped_quotes[day] = subset[subset.index < datetime.strptime(f"{day} 16:00:00", "%Y-%m-%d %H:%M:%S")]
            grouped_quotes[day] = subset[subset.index > datetime.strptime(f"{day} 09:30:00", "%Y-%m-%d %H:%M:%S")]
        new_quotes = pd.concat(list(grouped_quotes.values())).sort_index()

        return new_quotes
    else:
        return quotes


# grossman transcnction costs
def chunk_clean(path, quotes=True):
    counter = 1

    # remove .csv if present
    if ".csv" in path:
        path = path.replace(".csv", "")

    # remove temp/ dir if present
    if "temp/" in path:
        path = path.replace("temp/", "")

    for df in pd.read_csv(f"{path}.csv", iterator=True, chunksize=100000, low_memory=False):

        if quotes:
            cleaned_data = clean_quotes(df)
        else:
            cleaned_data = clean_trades(df)

        if counter == 1:
            pd.DataFrame(columns=cleaned_data.columns).to_csv(f"{path}_cleaned.csv", index=False)

        # append to csvs
        cleaned_data.to_csv(f"{path}_cleaned.csv", mode="a", header=False)
        cleaned_path = f"{path}_cleaned.csv"

        counter += 1

    return cleaned_path
