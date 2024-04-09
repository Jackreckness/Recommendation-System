import streamlit as st
import utils
import numpy as np
import pandas as pd

books = utils.readBooks()
ratings = utils.readRatings()
books.set_index("Book.Id", drop=False, inplace=True)
myuserId = 262151
feedback_userId = 262151


def PrintBook(Title, ISBN, BookId, Author, Year, Publisher, Image):
    sc1, sc2 = st.columns(2)
    with sc1:
        st.image(Image, width=200)
    with sc2:
        markdown = f"""
        <h3>{Title}</h3>
        <p>ISBN: {ISBN}</p>
        <p>BookID: {BookId}</p>
        <p>Author: {Author}</p>
        <p>Year: {Year}</p>
        <p>Publisher: {Publisher}</p>
        """
        st.markdown(markdown, unsafe_allow_html=True)
        if st.button("Not interested", key="recommend_btn_" + str(BookId)):
            utils.addFeedback(feedback_userId, BookId, 1)
            st.info("Book '" + Title + "'  is added to my dislike list")
        st.write("---")


def Recommendation():
    st.header("Optimized recommendation system")

    if st.button("Generate recommendation"):
        bookIds = utils.get_top_n_recommendations(myuserId, feedback_userId, 5)
        print(bookIds)
        st.session_state["top5"] = bookIds

    if "top5" in st.session_state:
        for book_id in st.session_state["top5"]:
            # Get a row by Book.Id
            row = books.loc[book_id]
            PrintBook(
                row["Book.Title"],
                row["ISBN"],
                book_id,
                row["Book.Author"],
                row["Year.Of.Publication"],
                row["Publisher"],
                row["Image.URL.L"],
            )


def Books():
    st.header("List all the Books")
    for index, row in books.iterrows():
        PrintBook(
            row["Book.Title"],
            row["ISBN"],
            row["Book.Id"],
            row["Book.Author"],
            row["Year.Of.Publication"],
            row["Publisher"],
            row["Image.URL.L"],
        )
        st.write("---")


def MyFeedbacks():
    st.title("My Feedbacks")
    df = utils.readFeedback()
    edited_df = st.data_editor(df, num_rows="dynamic")
    if st.button("Update"):
        edited_df.to_csv("feedback.csv", index=False)

def MyRatings():
    st.title("My Ratings")
    df = utils.readRatings()
    edited_df = st.data_editor(df)
    if st.button("Update"):
        edited_df.to_csv("filtered_ratings.csv", index=False)

def main():
    with st.sidebar:
        st.header("Select the page")
    page = st.sidebar.radio(
        "", ["Recommendation", "My Ratings", "My Feedbacks", "All Books"]
    )
    if page == "Recommendation":
        Recommendation()
    elif page == "My Ratings":
        MyRatings()
    elif page == "My Feedbacks":
        MyFeedbacks()
    elif page == "All Books":
        Books()
    else:
        Test()


if __name__ == "__main__":
    main()
