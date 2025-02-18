import streamlit as st
import numpy as np
import pandas as pd
import datetime
import altair as alt

st.set_page_config(layout="wide")

st.title("Oracle Cards: Divination, Magick, or Statistically Likely Outcomes?")

loc_pull_data = "datasets/WRI363_Pulls_Data.csv"
loc_card_data = "datasets/WRI363_Oracle_Data.csv"

pull_data = pd.read_csv(loc_pull_data)
pull_data["Date"] = pd.to_datetime(pull_data["Date"])

# """DEVELOP MISLEADING DATA"""

card_relation = {}

for i in range(np.shape(pull_data)[0]):
    add1 = pull_data["Area_Connection_1"][i]
    add2 = pull_data["Area_Connection_2"][i]
    card_relation[add1] = card_relation.get(add1, 0) + 1
    card_relation[add2] = card_relation.get(add2, 0) + 1

card_relation.pop(np.nan)

# creating dataframe
meaning_code = []
times_related = []

for k in card_relation.keys():
    meaning_code.append(k)
    times_related.append(card_relation[k])
misleading_data = {"How I related to the Card Pull": meaning_code, "Frequency": times_related}
misleading_dataframe = pd.DataFrame(data=misleading_data)
# to make misleading: map colours to not be related to the theme
theme_colours = {
    "Academics": "#1f77b4",
    "CSSC": "#EBD249",
    "Event": "#2ca02c",
    "Family-negative": "#4FDA04",
    "Family-positive": "#E78A8A",
    "Friendship-care": "#8c564b",
    "Friendship-negative": "#6FB14C",
    "Friendship-positive": "#FFCCCCS",
    "Hobbies": "#bcbd22",
    "LAUNCH": "#37B8A7",
    "Life-advice": "#ffbb78",
    "Love": "#98df8a",
    "Mental-health": "#ff9896",
    "Research": "#c5b0d5",
    "Spirituality": "#c49c94",
    "Work": "#f7b6d2",
    "Workload": "#dbdb8d"
}

# """ SIDEBAR """


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


# """ DISPLAYING VISUALS"""

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

    st.header("Misleading Data: Frequency of How I Related to Card Theme")

    # Create Bubble Chart
    chart = alt.Chart(misleading_dataframe).mark_circle(opacity=0.9).encode(
        x=alt.X("How I related to the Card Pull", axis=None),
        y=alt.Y("jitter:Q", title="", axis=None),
        size=alt.Size("Frequency:Q", scale=alt.Scale(range=[5000, 6000]), legend=None),  # Circle size based on count
        color=alt.Color("How I related to the Card Pull",  
        scale=alt.Scale(domain=list(theme_colours.keys()), range=list(theme_colours.values())),  
        legend=alt.Legend(orient="right") ),
        tooltip=["How I related to the Card Pull", "Frequency"]
    ).transform_calculate(
        jitter="random() * 0.5"  # Random Y jitter between 0 and 0.5
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    st.write("TODO: Figure caption")