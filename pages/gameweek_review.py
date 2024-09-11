import requests
import json
import streamlit as st

from Utils.functions import num_processor, date_parser
from main import scrape_url, get_stored_data, get_static_data, save_static_data, get_element_name_by_id
from main import NOT_AVAILABLE

def render_gw_info(gw_id = 3):
    print("GW ID : ",gw_id)
    gw_id = int(gw_id)
    event = events[gw_id-1]
    st.subheader(f":blue[GAMEWEEK {gw_id} SUMMARY]")

    high_scr_team_page = f"https://fantasy.premierleague.com/entry/{event['highest_scoring_entry']}/event/{gw_id}"
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Averge score", event['average_entry_score'])
    with col2:
        st.metric("Highest score", event['highest_score'])
        st.link_button("View Team", high_scr_team_page)
    with col3:
        st.metric("Total transfers", num_processor(event['transfers_made']))

    st.divider()
    print(event['most_selected'],type(elements), len(elements))
    most_sel = get_element_name_by_id(elem_id=event['most_selected'], players=elements)
    most_cap = get_element_name_by_id(event['most_captained'], elements)
    most_vc = get_element_name_by_id(event['most_vice_captained'], elements)
    top_scr = get_element_name_by_id(event['top_element'], elements)
    top_scr_pts = event['top_element_info']['points']

    if gw_id != 1:
        most_tr = get_element_name_by_id(event['most_transferred_in'], elements)
    else:
        most_tr = most_sel
        

    st.subheader(":blue[Key Players]")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Most selected", most_sel)

    with col2:
        st.metric("Most Cap", most_cap)
    
    with col3:
        st.metric("Most VC", most_vc)
    
    with col4:
        st.metric("Most transfered in", most_tr)
    with col5:
        st.metric("Top Scorer", top_scr, f"{top_scr_pts} pts")


    st.divider()
    st.subheader(":blue[Chips Usage]")
    chip_plays = event['chip_plays']
        
    cap_3x = [chip['num_played'] for chip in chip_plays if chip['chip_name'] == '3xc'][0]
    bboost = [chip['num_played'] for chip in chip_plays if chip['chip_name'] == 'bboost'][0]
    try:
        wildcard = [chip['num_played'] for chip in chip_plays if chip['chip_name'] == 'wildcard'][0]
    except:
        wildcard = NOT_AVAILABLE
        
    try:
        freehit = [chip['num_played'] for chip in chip_plays if chip['chip_name'] == 'freehit'][0]
    except:
        freehit = NOT_AVAILABLE

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Bench Boost", num_processor(bboost))

    with col2:
        st.metric("Triple Captain", num_processor(cap_3x))
    
    with col3:
        st.metric("Wildcard", num_processor(wildcard))
    
    with col4:
        st.metric("Freehit", num_processor(freehit))

def render_due_gw(gw):
    deadline = events[gw-1]['deadline_time']
    print(deadline)
    st.subheader(f":blue[Deadline due on :] {date_parser(deadline)}")

def render_invalid_gw():
    st.header(":red[Invalid Gameweek Number Entered!!!]")


if __name__ == "__main__":
    st.title(":blue[FPL Gameweek Analysis]")

    data = get_static_data()
    # data = get_stored_data()

    total_players = data['total_players']
    events = data['events']
    elements = data['elements']

    # Get next round index
    next_round_index = 0
    for i, event in enumerate(events):
        if(event['is_next']):
            next_round_index = i

    gw = st.number_input("Enter gameweek number : ",value=1)

    if gw<1 or gw>38:
        render_invalid_gw()
    elif(gw>next_round_index):
        render_due_gw(gw)
    else:
        render_gw_info(gw)

    st.divider()