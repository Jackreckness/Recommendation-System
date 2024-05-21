import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from datetime import datetime, timedelta

# Constants for file paths
RATINGS_FILE_PATH = "data/filtered_ratings.csv"
BOOKS_FILE_PATH = "data/filtered_books.csv"

def readRatings():
    """
    Read the ratings data from a CSV file.
    
    Returns:
        DataFrame: A pandas DataFrame containing the ratings data.
    """
    data = pd.read_csv(RATINGS_FILE_PATH)
    return data

def readBooks():
    """
    Read the books data from a CSV file.
    
    Returns:
        DataFrame: A pandas DataFrame containing the books data.
    """
    data = pd.read_csv(BOOKS_FILE_PATH)
    return data

def get_top_n_recommendations(user_id, n=5, timespan='long term'):
    """
    Fit a SVD model and return the top n recommendations for a user based on the selected timespan.
    
    Args:
        user_id (int): The ID of the user for whom recommendations are to be generated.
        n (int): The number of top recommendations to return. Default is 5.
        timespan (str): The timespan to filter the ratings data. Options are 'recent 2 weeks', '3 months', '6 months', 'this year', 'long term'.
    
    Returns:
        list: A list of book IDs recommended for the user.
    """
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

    # Load data into Surprise dataset format
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(df[['UserId', 'BookId', 'Rating']], reader)
    trainset = data.build_full_trainset()
    
    # Fit the SVD model
    model_svd = SVD()
    model_svd.fit(trainset)
    
    # Get the list of books not rated by the user
    user_books = df[df['UserId'] == user_id]['BookId'].unique()
    all_books = df['BookId'].unique()
    books_to_predict = list(set(all_books) - set(user_books))
    
    # Predict ratings for the books not rated by the user
    user_book_pairs = [(user_id, book_id, 0) for book_id in books_to_predict]
    predictions_cf = model_svd.test(user_book_pairs)
    top_n_recommendations = sorted(predictions_cf, key=lambda x: x.est, reverse=True)[:n]
    
    # Print predicted ratings for debugging
    for pred in top_n_recommendations:
        predicted_rating = pred.est
        print(predicted_rating)

    top_n_book_ids = [int(pred.iid) for pred in top_n_recommendations]

    return top_n_book_ids

def addFeedback(userId, bookId):
    """
    Add feedback for a book by marking it as not interested.
    
    Args:
        userId (int): The ID of the user providing feedback.
        bookId (int): The ID of the book to be marked as not interested.
    
    Updates:
        The ratings CSV file by adding a new row with the user's feedback.
    """
    # Load the existing ratings data
    df = pd.read_csv(RATINGS_FILE_PATH)
    
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    new_row = {'UserId': userId, 'BookId': bookId, 'Rating': 1, 'RatingDate': today_date}
    
    # Convert new_row to DataFrame and concatenate it with the existing DataFrame
    new_row_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_row_df], ignore_index=True)
    df.to_csv(RATINGS_FILE_PATH, index=False)