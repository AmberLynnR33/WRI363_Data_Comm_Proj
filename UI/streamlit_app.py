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

card_data = pd.read_csv(loc_card_data)
card_data = card_data[["Card_Num", "Card_Theme"]]

# """DEVELOP MISLEADING DATA"""

card_relation = {}

for i in range(np.shape(pull_data)[0]):
    add1 = pull_data["Area_Connection_1"][i]
    add2 = pull_data["Area_Connection_2"][i]
    card_relation[add1] = card_relation.get(add1, 0) + 1
    card_relation[add2] = card_relation.get(add2, 0) + 1

card_relation.pop(np.nan)

card_relation["No-relation"] = (pull_data[pull_data['Connection'] != 1]).shape[0]

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

button_press = False

if st.sidebar.button("About this project", use_container_width=True):
    button_press = True
    st.markdown("""
    ## About This Project

    I started reading oracle cards last July as a self-reflection and divination tool. 
    I logged the cards I draw with my reflection of the theme on the card in a journal. 
    While I personally believe they connect to the supernatural to some degree, 
    I am also highly interested how statistically likely or unlikely my card pulls are, 
    and why I can often connect the card I pull to my current life. 
    Thus, I want to examine both my card pulls, 
    to see how statistically likely my card pulls have been, 
    and in what areas of my life do I connect the card meanings to.

    This communication piece provides insight into the statistics of card pulls,
    as beliefs of Tarot and Oracle cards vary from person to person.

    *Do the statistics show anomalies, or is it all just coincidence?*
    """)
    st.divider()
if st.sidebar.button("The Dataset", use_container_width=True):
    button_press = True
    st.markdown("""
    ## The Oracle Cards

    The specific deck I use for this project is [Woodland Wardens](%s) 
    created and illustrated by Jessica Roux. 
    This deck includes 52 cards, 
    where each card connects a plant and animal to the card theme. 
    Flip-throughs of the deck are available on YouTube.


    While in the future I would love to include more specific breakdowns 
    of my data by card, below is a chart of the upright definition of each card. 
    Reversal card definitions follow typical definitions of reversal cards: 
    they represent an opposite meaning, or means to apply the theme more internally.
    """ %'https://www.woodlandwardens.com/')
    with st.expander("See the card themes"):
        st.table(card_data)

    st.markdown("""
    ## The Journal Data

    I flipped through my journal from the first time I used the Woodland Wardens deck,
     up until the point I began this project. 
     This included 150 total card pulls across July 24th, 2024 to January 19th, 2025. 
     I collected the following data, which you can view [here](%s):

    - Date,
    - Card_Num: the card number of the card I pulled,
    - Reversed: If the card was pulled reversed (1) or upright (0),
    - In_Spread: If the card was a part of a spread (1) or not (0),
    - Connection: In my journal entry that followed, did I connect something in my life to the card (1), or did I not feel the card connected to my current life (0). If no journal entry followed, I put down (2),
    - Area_Connection_1* and Area_Connection_2*: if I connected the card to something in my life, what was the general part of my life I connected it to?

    *This data was collected through thematic analysis of my journal entries. 
    I have experience in this form of analysis on survey data and transcripts.
    """ %'https://github.com/AmberLynnR33/WRI363_Data_Comm_Proj/blob/main/datasets/WRI363_Pulls_Data.csv')

    st.divider()
if st.sidebar.button("Limitations to this Project", use_container_width=True):
    button_press = True
    st.markdown("""
    ## Limitations to this Project

    The project utilizes autoethnography, 
    using my data to examine how I connect the cards to my life and see how regular or irregular the card pulls are. 
    This requires a level of trust between me and viewers like you. 
    I do not share the raw data, as it comes from my personal diary. 
    Yet, even if I did, I acknowledge that some may argue a forgery in my writing 
    as it's written on paper and thus the only time stamps are the dates at the top of each page. 

    I emphasize this data should not be used to make general claims about Tarot or Oracle cards and their legitimacy. 
    This is especially true since the data only comes from one person (me), and includes only 150 data points. 
    Regardless on your beliefs on this topic, 
    I think it's important to respect that these cards can be insightful to some people, 
    even if my data shows the cards drawn are fairly random. I myself fall into that category; 
    this data will not deter me from using my cards as a way to check in with myself and self-reflect.

    ### I took the following steps for transparency:

    - Any data collected past the point I began this project (January 19th, 2025) is not included. I made this choice to reduce skepticism that later data in forged to tell a certain story.
    - I have experience in qualitative coding (on both survey responses and transcripts), and thus I felt comfortable to utilize this skill on my journal entries to assign themes. 
    - Data pulled from my journal (date, card, what general theme in my life I connected the card to in my journal entry) is available on [the datasets folder of the GitHub page for this project](%s). It is available as a .csv, which is formatted directly on the site, or can be downloaded and opened using a spreadsheet program. 
    """ %'https://github.com/AmberLynnR33/WRI363_Data_Comm_Proj/tree/main/datasets')
    st.divider()
if st.sidebar.button("Definitions", use_container_width=True):
    button_press = True
    st.markdown("""
    ### Definitions:

    - Divination: gaining insight into the unknown or future. This can be done in many ways, one of which is through Tarot or oracle cards.
    - Magick: an alternative spelling to “magic” that is sometimes used to differentiate the magic tricks magicians use to magic of the spiritual kind.
    - Oracle cards: a deck of cards that works like the more common Tarot cards; one can pull cards for the purpose of divination, to gain insight on a theme in their life, or to self-reflect. Tarot differs from oracle because it has a set 78 cards, each with a specific meaning. On the other hand, each oracle card deck differs in the number of cards, meanings, and deck themes; the creator of the cards decides these differences. 
    - Upright card: a card that is drawn upright.
    - Reversed card: a card that is drawn upside-down.
    - Guidebook: a booklet that comes with Tarot or oracle decks that describes each card's meaning
    """)
    st.divider()
visual_selection = st.sidebar.selectbox(
    'Which visual would you like to explore?', 
    ("Date vs Card Pulled", "Misleading Piece", "Counter Data Piece"),
    index=None,
    placeholder="Select a visual to display...",
)


# """ DISPLAYING VISUALS"""

if visual_selection == None or button_press == True:
    st.write("Want to see the visualizations? Select a visual to display on the sidebar!")
    button_press = False
elif visual_selection == "Date vs Card Pulled":
    st.sidebar.markdown("### Filter Options:")
    card_num_selection = st.sidebar.number_input("Card Number (enter -1 to view all cards)", -1, 51, -1)
    st.sidebar.write("Date Range:")
    start_date_range = st.sidebar.date_input("Select a Starting Date", value=datetime.date(2024, 7,17), min_value=datetime.date(2024, 7, 17), max_value=datetime.date(2025, 1, 19))
    end_date_range = st.sidebar.date_input("Select an Ending Date", value=datetime.date(2025, 1, 19), min_value=datetime.date(2024, 7, 17), max_value=datetime.date(2025, 1, 19))
    if start_date_range > end_date_range:
        st.error("Start date cannot be after end date.")
    else:
        # Filter DataFrame based on selected range
        filtered_data = pull_data.loc[
            (pull_data["Date"] >= pd.to_datetime(start_date_range)) & 
            (pull_data["Date"] <= pd.to_datetime(end_date_range))
        ]
        filtered_data["Reversed"] = filtered_data["Reversed"].replace({1: "Reversed", 0: "Upright"})
        filtered_data = filtered_data.rename(columns={"Reversed": "Direction I Pulled Card"})
        if card_num_selection != -1:
            filtered_data = filtered_data[filtered_data["Card_Num"] == card_num_selection]
        base_data_comm_chart = alt.Chart(filtered_data).mark_circle(size=100).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Card_Num:Q", title="Card Number of Card Pulled"),
            color=alt.Color("Direction I Pulled Card:N", scale=alt.Scale(domain=["Reversed", "Upright"], range=["#8a9cce", "#e2d68e"]), legend=alt.Legend(title="Card Direction")),
            tooltip=["Date", "Card_Num", "Direction I Pulled Card"]
        ).properties(
            width=800, height=500  # Adjust size as needed
        ).interactive()
        st.altair_chart(base_data_comm_chart, use_container_width=True)

        # Figure Caption
        st.markdown("""Viewing the relationship between the date and the card pulled does not indicate any 
        anomalies in cards pulled or a preference for upright or reversed card direction. 
        Each dot represents one card drawn, with some days including multiple dots for each card pulled from 
        the deck. Data from A. Richardson (personal communication, February 8, 2025).
        """)
        st.markdown("### To filter through this data, use the selections on the sidebar.")
        st.divider()
        st.markdown("""
        This data displays the randomness of card pulls. Examining the card number of the card direction,
        there's no pattern or anomalies in this data.

        
        I choose to display this data using a scatter plot, to provide you with data as close to the raw data as possible.
        While fancier charts or visuals could display this data, 
        I felt keeping the data in this simpler format the best way to allow you to interpret the data,
        especially since Oracle cards are subject to a lot of skepticism. 
        """)
elif visual_selection == "Misleading Piece":

    st.header("Misleading Data: Frequency of How I Related to Card Theme")
    st.sidebar.markdown("""### The Misleading Scale:""")
    
    chosen_scalar = st.sidebar.slider("Slide me to change how to mislead!", 0, 3, 3)
    scaler_vals = [[333,9990],[10,9999],[333,9990],[5000,6000]]

    st.sidebar.markdown("""
    **0:** reverse the scale (larger values become smaller, smaller values become larger)

    **1:** stretch the scale (smaller values are even smaller than they should appear)

    **2:** true scaling of frequency to bubble size

    **3:** squish the scale (all values look around the same size)
    """)

    # create chart
    chart = alt.Chart(misleading_dataframe).mark_circle(opacity=0.9).encode(
        x=alt.X("How I related to the Card Pull", axis=None),
        y=alt.Y("jitter:Q", title="", axis=None),
        size=alt.Size("Frequency:Q", scale=alt.Scale(range=scaler_vals[chosen_scalar]), legend=None),
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
    st.markdown("""Frequency of card draws that I connected to a specific theme in my life. 
    Each circle represents one overarching theme that I connected the card pull to in my 
    journal, where the size of the circle corresponds to how frequently I made this connection. 
    The “No Relation” circle represents all cards that I did not relate to any theme. 
    Data from A. Richardson (personal communication, February 8, 2025).""")

    st.markdown("### To modify how misleading this piece is, use the slider on the sidebar.")
    st.divider()
    st.markdown("""
    This piece aims to show you how easy it is to mislead.

    The main way is through the misleading scale. 
    Unless you set the misleading scale to 2, you can further mislead using the scaling. 
    Whether this is through reversing, stretching, or squishing the scale, 
    you can see how easily it is make different conclusions about the data.

    Colour further misleads you on the theme. 
    For example, the bright red circle represents “Mental Health” and the bright green circle represents “Love.” 

    I place the circles using a “jitter” effect, which randomizes location. 
    This means some circles may overlap and imply a relationship between them, 
    when I independently counted the number of times I references each theme. 
    Any changes you make to the page (refreshing, resizing, modifying the misleading scale...) 
    will alter the placement of the circles.

    The circle placement and jitter effect can both cause frustration. 
    With 18 total themes, it's hard to keep track of which bubble is which. 
    This further amplifies the misleading aspect: if you didn't know this was misleading data, 
    you may be more inclined to make an assumption on the data as opposed to critically analyzing it.
    """)

elif visual_selection == "Counter Data Piece":

    st.header("Counter Data: Representing Date vs Card Pulled in an Audio Format")

    # audio
    st.audio("counterdatapiece.wav")

    # Figure Caption
    st.markdown('''A representation of card draws by day created in MIDI audio format. 
    Each note or chord played simultaneously corresponds to the card(s) drawn on a day. 
    Each MIDI note number corresponds to the card pulled plus 34, to ensure the middle card 
    in the deck corresponds to middle C on a piano. The MIDI file was converted to 
    .wav file format for compatibility on various operating systems. 
    Only days with data are represented. 
    Data from A. Richardson (personal communication, February 8, 2025).''')

    st.divider()
    st.markdown("""
        An audio representation of my card draws “counters” data by representing numerical data in an uncommon format. 
        The data collection and cleaning process created data that we commonly format in visual ways. 
        With each data point being associated with a date and a card number, 
        this suggests a visual format of the data through a chart, graph, or visual connecting the cards to data. 
        Instead, I represented the data with music, a strictly auditory format. 
        If you have a visual impairments that makes interpreting the "Date vs. Card Pull" visual difficult, 
        this provides you an alternative avenue to understand my data.

        With MIDI notes, I represented card numbers as notes to turn into a music file, 
        sorting the ordering of notes and chords by date. 
        As the card numbers range from 0 to 51, this created very low notes. 
        I adjusted the notes to make the middle card (26) represent middle C, 
        which meant adding 34 to every card number to have a new range of 34 to 85.

        The music is unpleasant and jarring at times, because it represents data and not creative ability. 
        In fact, it helps show the true randomness of the data: something with a distinctive pattern would create a more pleasant sound.
    """)

