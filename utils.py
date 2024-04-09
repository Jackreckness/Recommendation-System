import pandas as pd
import numpy as np
from surprise import Reader
from surprise import Dataset
from surprise import SVD
import random 


def readRatings():
    path = "filtered_ratings.csv"
    data = pd.read_csv(path, usecols=[0, 1, 2])
    return data

def readBooks():
    path = "filtered_books.csv"
    data = pd.read_csv(path)
    return data


def get_top_n_recommendations(user_id, feedback_userid, n=5):
    random.seed(99)                                                                    
    np.random.seed(99)
    df = readRatings()
    df.columns = ['userID', 'bookID', 'bookRating']
    feedbackDf = readFeedback()    
    feedbackDf.columns = ['userID', 'bookID', 'bookRating']
    df = pd.concat([df, feedbackDf], ignore_index=True)
    
    reader = Reader(rating_scale = (0, 10))
    data = Dataset.load_from_df(df[['userID', 'bookID', 'bookRating']], reader)
    trainset = data.build_full_trainset()
    model_svd = SVD()
    model_svd.fit(trainset)
    user_books = df[df['userID'] == user_id]['bookID'].unique()
    all_books = df['bookID'].unique()
    books_to_predict = list(set(all_books) - set(user_books))
    user_book_pairs = [(user_id, book_id, 0) for book_id in books_to_predict]
    predictions_cf = model_svd.test(user_book_pairs)
    top_n_recommendations = sorted(predictions_cf, key = lambda x: x.est, reverse = True)[:n]
    
    for pred in top_n_recommendations:
        predicted_rating = pred.est
        print(predicted_rating)

    top_n_book_ids = [int(pred.iid) for pred in top_n_recommendations]

    return top_n_book_ids

def readFeedback():
    path = "feedback.csv"
    data = pd.read_csv(path)
    return data


def removeFeedbackByBookId(feedback, bookid):
    feedback = feedback[feedback["Book.Id"] != bookid]
    feedback.to_csv("feedback.csv", index=False)
    return feedback


def addFeedback(UserId, BookId, Rating):
    feedback = readFeedback()
    filtered_rows = feedback.loc[feedback["BookId"] == BookId]
    if filtered_rows.empty:
        feedback.loc[len(feedback.index)] = [
            UserId,
            BookId,
            Rating,
        ]
        feedback.to_csv("feedback.csv", index=False)


def splitTrainSetTestSet(odatas):
    testset = odatas.sample(frac=0.2, axis=0)
    trainset = odatas.drop(index=testset.index.values.tolist(), axis=0)
    return trainset, testset


# def getMatrix(dataset):
#     userSet, itemSet = set(), set()

#     for d in dataset.values:
#         userSet.add(int(d[0]))
#         itemSet.add(int(d[1]))

#     userList = list(userSet)
#     itemList = list(itemSet)

#     df = pd.DataFrame(0, index=userList, columns=itemList, dtype=float)
#     for d in dataset.values:
#         df.loc[d[0], d[1]] = d[2]

#     return df, userList, itemList


# def svd(m, k):
#     u, i, v = np.linalg.svd(m)
#     return u[:, 0:k], np.diag(i[0:k]), v[0:k, :]


# def predict(u, i, v, user_index, item_index):
#     return float(u[user_index].dot(i).dot(v.T[item_index].T))


# def getPredictsForUser(userId, userList, itemList, u, i, v):
#     user_index = userList.index(userId)
#     y_hat = []
#     for item in itemList:
#         item_index = itemList.index(item)
#         prediction = predict(u, i, v, user_index, item_index)
#         y_hat.append([item_index, prediction])
#     return y_hat


# def RMSE(a, b):
#     return (np.average((np.array(a) - np.array(b)) ** 2)) ** 0.5
