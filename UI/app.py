import streamlit as st
import numpy as np
import pandas as pd
import datetime

st.set_page_config(layout="wide")

st.title("Oracle Cards: Divination, Magick, or Statistically Likely Outcomes?")

loc_pull_data = "data/WRI363_Pulls_Data.csv"
loc_card_data = "data/WRI363_Oracle_Data.csv"

pull_data = pd.read_csv(loc_pull_data)
pull_data["Date"] = pd.to_datetime(pull_data["Date"])


# SIDEBAR 


# explanation box
with st.sidebar.expander("About this project"):
    st.write("TODO")
with st.sidebar.expander("The dataset"):
    st.write("TODO")
with st.sidebar.expander("What are oracle cards?"):
    st.write("TODO")

visual_selection = st.sidebar.selectbox(
    'Which visual would you like to explore?', 
    ("Date vs Card Pulled", "Misleading Piece"),
    index=None,
    placeholder="Select a visual to display...",
)


# DISPLAYING VISUALS

if visual_selection == None:
    st.write("Select a visual to display on the sidebar!")
elif visual_selection == "Date vs Card Pulled":
    st.sidebar.write("Date Range:")
    start_date_range = st.sidebar.date_input("Select a Starting Date", value=datetime.date(2024, 7,17), min_value=datetime.date(2024, 7, 17), max_value=datetime.date(2025, 1, 19))
    end_date_range = st.sidebar.date_input("Select an Ending Date", value=datetime.date(2025, 1, 19), min_value=datetime.date(2024, 7, 17), max_value=datetime.date(2025, 1, 19))
    if start_date_range > end_date_range:
        st.error("Start date cannot be after end date.")
    else:
        # Filter DataFrame based on selected range
        filtered_data = pull_data[(pull_data["Date"] >= pd.to_datetime(start_date_range)) & (pull_data["Date"] <= pd.to_datetime(end_date_range))]
        filtered_data["Reversed"] = filtered_data["Reversed"].replace({1: "Reversed", 0: "Upright"})
        filtered_data = filtered_data.rename(columns={"Reversed": "Direction I Pulled Card"})
        st.scatter_chart(data=filtered_data, x="Date", y="Card_Num", x_label="Date", y_label="Card Number of Card Pulled", color="Direction I Pulled Card", use_container_width=True)
        st.write("TODO: Figure caption")
elif visual_selection == "Misleading Piece":
    # I am going to do a bar chart, where x is card num, y is times pulled upright and times pulled reversed. However, the times pulled upright will go into negatives and times pulled in reverse will go positive
    st.scatter_chart(data=pull_data, x="Connection", x_label="Did I connect to the card?", y="Reversed", y_label="Card Direction")
    st.write("TODO: Figure caption")