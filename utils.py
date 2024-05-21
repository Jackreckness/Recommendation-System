import pandas as pd
import numpy as np
from surprise import Reader
from surprise import Dataset
from surprise import SVD
from datetime import datetime, timedelta

# Function to read the ratings data
def readRatings():
    path = "data/filtered_ratings.csv"
    data = pd.read_csv(path)
    return data

# Function to read the books data
def readBooks():
    path = "data/filtered_books.csv"
    data = pd.read_csv(path)
    return data

# Function to re-fit a SVD model and return the top n recommendations for a user
def get_top_n_recommendations(user_id, n=5, timespan='long term'):
    df = readRatings()

    # Define the time filtering logic
    now = datetime.now()
    if timespan == 'recent 2 weeks':
        start_date = now - timedelta(weeks=2)
    elif timespan == '3 months':
        start_date = now - timedelta(weeks=12)
    elif timespan == '6 months':
        start_date = now - timedelta(weeks=24)
    elif timespan == 'this year':
        start_date = datetime(now.year, 1, 1)
    else:  # 'long term'
        start_date = datetime.min  # earliest possible date

    # Filter the ratings data based on the selected timespan
    df['RatingDate'] = pd.to_datetime(df['RatingDate'])
    df = df[df['RatingDate'] >= start_date]

    reader = Reader(rating_scale = (0, 10))
    data = Dataset.load_from_df(df[['UserId', 'BookId', 'Rating']], reader)
    trainset = data.build_full_trainset()
    
    # the best parameters using grid search: {'n_epochs': 10, 'lr_all': 0.01, 'reg_all': 0.4}
    # more detals in the notebook: recommendation.ipynb
    model_svd = SVD()
    model_svd.fit(trainset)
    user_books = df[df['UserId'] == user_id]['BookId'].unique()
    all_books = df['BookId'].unique()
    books_to_predict = list(set(all_books) - set(user_books))
    user_book_pairs = [(user_id, book_id, 0) for book_id in books_to_predict]
    predictions_cf = model_svd.test(user_book_pairs)
    top_n_recommendations = sorted(predictions_cf, key = lambda x: x.est, reverse = True)[:n]
    
    for pred in top_n_recommendations:
        predicted_rating = pred.est
        print(predicted_rating)

    top_n_book_ids = [int(pred.iid) for pred in top_n_recommendations]

    return top_n_book_ids

def addFeedback(userId, bookId):
    # Load the existing ratings data
    df = pd.read_csv('data/filtered_ratings.csv')
    
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    new_row = {'UserId': userId, 'BookId': bookId, 'Rating': 1, 'RatingDate': today_date}
     # Convert new_row to DataFrame and concatenate it with the existing DataFrame
    new_row_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_row_df], ignore_index=True)
    df.to_csv('data/filtered_ratings.csv', index=False)
