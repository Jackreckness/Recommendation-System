import streamlit as st
import utils
import numpy as np
import pandas as pd

books = utils.readBooks()
ratings = utils.readRatings()
books.set_index("BookId", drop=False, inplace=True)
myuserId = 0


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
            utils.addFeedback(myuserId, BookId)
            st.info("Book '" + Title + "'  is added to my dislike list")
        st.write("---")


def Recommendation():
    st.header("Optimized recommendation system")

    col1, col2 = st.columns([2, 2])
    with col1:
        if st.button("Generate recommendation"):
            timespan = st.session_state.get("timespan", "recent 2 weeks")
            bookIds = utils.get_top_n_recommendations(myuserId, 5, timespan=timespan)
            print(bookIds)
            st.session_state["top5"] = bookIds
    
    with col2:
        timespan = st.select_slider(
            "Select timespan to filter the data used to make prediction:",
            options=["short term", "3 months", "6 months", "this year", "long term"],
            key="timespan"
        )

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
            row["BookId"],
            row["Book.Author"],
            row["Year.Of.Publication"],
            row["Publisher"],
            row["Image.URL.L"],
        )
        st.write("---")



def MyRatings():
    st.title("My Ratings")
    df = utils.readRatings()
    df_filtered = df[df["UserId"] == myuserId]
    edited_df = st.data_editor(df_filtered)
    if st.button("Update"):
        df_notmy = df[df["UserId"] != myuserId]
        df = pd.concat([edited_df, df_notmy], ignore_index=True)
        df.to_csv("data/filtered_ratings.csv", index=False)


def main():
    with st.sidebar:
        st.header("Select the page")
    page = st.sidebar.radio(
        "", ["Recommendation", "My Ratings", "All Books"]
    )
    if page == "Recommendation":
        Recommendation()
    elif page == "My Ratings":
        MyRatings()
    elif page == "All Books":
        Books()


if __name__ == "__main__":
    main()
