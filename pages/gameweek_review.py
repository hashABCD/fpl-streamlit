import requests
import json
import streamlit as st

from Utils.functions import num_processor, date_parser

NOT_AVAILABLE = "N.A."

def scrape_url(url):
    print(f"Scraping {url}...")
    r = requests.get(url)
    print(r.status_code)
    return r

def render_gw_info(gw_id = 3):
    print("GW ID : ",gw_id)
    gw_id = int(gw_id)
    event = events[gw_id-1]
    st.header(f"GAMEWEEK {gw_id} SUMMARY")

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
        
    most_sel = get_element_name_by_id(event['most_selected'])
    most_cap = get_element_name_by_id(event['most_captained'])
    most_vc = get_element_name_by_id(event['most_vice_captained'])
    top_scr = get_element_name_by_id(event['top_element'])
    top_scr_pts = event['top_element_info']['points']

    if gw_id != 1:
        most_tr = get_element_name_by_id(event['most_transferred_in'])
    else:
        most_tr = most_sel
        

    st.subheader("Key Players")
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
    st.subheader("Chips Usage")
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
    st.header(f"Deadline due on : {date_parser(deadline)}")

def render_invalid_gw():
    st.header("Invalid Gameweek Number Entered!!!")

def get_element_name_by_id(elem_id = 351):
    for element in elements:
        if element['id'] == elem_id:
            return element['web_name']


def get_static_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = scrape_url(url)
    data = json.loads(r.content)
    return data

def get_stored_data():
    with open('data.json') as data_file:
        data = json.load(data_file)
        return data

def save_static_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = scrape_url(url)
    data = json.loads(r.content)
    with open("data.json", 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    st.title("FPL Gameweek Analysis")

    # data = get_static_data()
    data = get_stored_data()

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