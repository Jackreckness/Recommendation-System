# Calibratable Recommendation System
## A DATA417 course project  
This project implements a calibratable recommendation system based on the report "A Calibratable Recommendation System Using User Interaction Timespan." The main goal is to provide personalized book recommendations by allowing users to adjust the timespan of the input data used for generating predictions.

## Introduction

Recommender systems are widely used in various online applications, such as e-commerce, social media, and news sites. This project addresses the ethical issue of personalization in recommendation systems by enabling users to control the timespan of the data used for recommendations. This approach enhances the system's ability to capture fluctuations in user interests, providing more accurate recommendations.

## Features

- **Adjustable Timespan**: Users can select different timespans (e.g., recent 2 weeks, 3 months, 6 months, this year, or long term) to adjust the recommendations.
- **User Feedback**: Users can provide feedback on recommended items to refine future recommendations.
- **Streamlit Interface**: A user-friendly interface built with Streamlit to interact with the recommendation system.

## Installation

### Prerequisites

- Python 3.6 or higher

### Steps

1. Install the required packages:
```bash
pip install -r requirements.txt
```
2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

### Recommendation Page
- Generate new recommendations based on the selected timespan.
- Adjust the timespan for the data to see different recommendation results.
- Provide feedback on each recommended book.

### My Ratings Page
- View and edit your ratings data.

### All Books Page
- Browse all available books.


