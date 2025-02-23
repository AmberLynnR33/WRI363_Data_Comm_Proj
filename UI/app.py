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

card_relation["No-relation"] = card_relation.pop(np.nan)

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
    "Academics": "#FFB7B7",
    "CSSC": "#E9853D",
    "Event": "#6596FF",
    "Family-negative": "#92B30D",
    "Family-positive": "#FF7373",
    "Friendship-care": "#B0BAFF",
    "Friendship-negative": "#68D362",
    "Friendship-positive": "#E79961",
    "Hobbies": "#E176E9",
    "LAUNCH": "#B395DD",
    "Life-advice": "#23C4E4",
    "Love": "#08BD7B",
    "Mental-health": "#FF0000",
    "Research": "#AEAEAE",
    "Spirituality": "#FFD900",
    "Work": "#DAC75D",
    "Workload": "#BD9898",
    "No-relation": "#FFFFFF"
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
    ("Date vs Card Pulled", "Misleading Piece", "Counter Data Piece"),
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
        base_data_comm_chart = alt.Chart(filtered_data).mark_circle(size=60).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Card_Num:Q", title="Card Number of Card Pulled"),
            color=alt.Color("Direction I Pulled Card:N", scale=alt.Scale(domain=["Reversed", "Upright"], range=["#FFA7A7", "#A7BFFF"]), legend=alt.Legend(title="Card Direction")),
            tooltip=["Date", "Card_Num", "Direction I Pulled Card"]
        ).properties(
            width=800, height=500  # Adjust size as needed
        )
        circle_outlines = alt.Chart(filtered_data).mark_circle(size=90, opacity=1, stroke="white", strokeWidth=1, fillOpacity=0).encode(
            x=alt.X("Date:T"),
            y=alt.Y("Card_Num:Q")
        )

        # Combine layers
        chart = (circle_outlines + base_data_comm_chart).properties(width=800, height=500).interactive()
        st.altair_chart(chart, use_container_width=True)

        # Figure Caption
        st.caption("""Viewing the relationship between the date and the card pulled does not indicate any 
        anomalies in cards pulled or a preference for upright or reversed card direction. 
        Each dot represents one card drawn, with some days including multiple dots for each card pulled from 
        the deck. Data from A. Richardson (personal communication, February 8, 2025).""")
elif visual_selection == "Misleading Piece":

    st.header("Misleading Data: Frequency of How I Related to Card Theme")

    # create chart
    chart = alt.Chart(misleading_dataframe).mark_circle(opacity=0.9).encode(
        x=alt.X("How I related to the Card Pull", axis=None),
        y=alt.Y("jitter:Q", title="", axis=None),
        size=alt.Size("Frequency:Q", scale=alt.Scale(range=[5000, 6000]), legend=None),
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

    # render chart
    st.altair_chart(chart, use_container_width=True)

    # Figure Caption
    st.caption("""Frequency of card draws that I connected to a specific theme in my life. 
    Each circle represents one overarching theme that I connected the card pull to in my 
    journal, where the size of the circle corresponds to how frequently I made this connection. 
    The “No Relation” circle represents all cards that I did not relate to any theme. 
    Data from A. Richardson (personal communication, February 8, 2025).""")
elif visual_selection == "Counter Data Piece":

    st.header("Counter Data: Representing Date vs Card Pulled in an Audio Format")

    # audio
    st.audio("audio/counterdatapiece.wav")

    # Figure Caption
    st.caption("""A representation of card draws by day created in MIDI audio format. 
    Each note or chord played simultaneously corresponds to the card(s) drawn on a day. 
    Each MIDI note number corresponds to the card pulled plus 34, to ensure the middle card 
    in the deck corresponds to middle C on a piano. The MIDI file was converted to 
    .wav file format for compatibility on various operating systems. 
    Only days with data are represented. 
    Data from A. Richardson (personal communication, February 8, 2025).""")
