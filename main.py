import requests
import json
import streamlit as st
import time

from Utils.functions import num_processor, date_parser

NOT_AVAILABLE = "N.A."

def scrape_url(url):
    print(f"Scraping {url}...")
    r = requests.get(url)
    print(r.status_code)
    return r


def get_element_name_by_id(elem_id = 351, players = None):
    print("Elem_id  :  ",elem_id)
    for element in players:
        if element['id'] == elem_id:
            return element['web_name']

def get_static_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = scrape_url(url)
    data = json.loads(r.content)
    return data

def get_standings_data():
    url = "https://fantasy.premierleague.com/api/leagues-classic/314/standings/"
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

def render_top_5():
    standings = get_standings_data()
    top_5 = standings['standings']['results'][:5]
    print(top_5)

    st.header(":blue[Top 5 teams]")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("***:blue[Team name]***")
    with col2:
        st.markdown("***:blue[Player name]***")
    with col3:
        st.markdown("***:blue[Points]***")
    with col4:
        st.markdown("***:blue[Team Link]***")

    for team_dict in top_5:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(team_dict['entry_name'])
        with col2:
            st.write(team_dict['player_name'])
        with col3:
            st.text(team_dict['total'])
        with col4:
            st.link_button("View Team", f"https://fantasy.premierleague.com/entry/{team_dict['entry']}/event/{next_round_index}")

def render_chip_usage():
    cap_3x_dict = {}
    bboost_dict = {}
    wildcard_dict = {}
    freehit_dict = {}
    for i in range(next_round_index):
        cap_3x_dict.update({i+1 : events[i]['chip_plays'][-1]['num_played']})
        bboost_dict.update({i+1 : events[i]['chip_plays'][0]['num_played']})
        if i!=0:
            wildcard_dict.update({i+1 : events[i]['chip_plays'][2]['num_played']})
            freehit_dict.update({i+1 : events[i]['chip_plays'][1]['num_played']})

    
    tc_val = sum(cap_3x_dict.values())
    tc_perc = round(tc_val*100/total_players,2)

    fh_val = sum(freehit_dict.values())
    fh_perc = round(fh_val*100/total_players,2)

    bb_val = sum(bboost_dict.values())
    bb_perc = round(bb_val*100/total_players,2)

    wc_val = sum(wildcard_dict.values())
    wc_perc = round(wc_val*100/total_players,2)


    st.header(":blue[Chip Usage]")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("***:blue[Triple Captain]***")
    with col2:
        st.markdown(f"{num_processor(tc_val)} ({tc_perc}%)")
    with col3:
        tc_bar = st.progress(0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("***:blue[Freehit]***")
    with col2:
        st.markdown(f"{num_processor(fh_val)} ({fh_perc}%)")
    with col3:
        fh_bar = st.progress(0)
   
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("***:blue[Wildcard]***")
    with col2:
        st.markdown(f"{num_processor(wc_val)} ({wc_perc}%)")
    with col3:
        wc_bar = st.progress(0)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("***:blue[Bench Boost]***")
    with col2:
        st.markdown(f"{num_processor(bb_val)} ({bb_perc}%)")
    with col3:
        bb_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.01)
        tc= int(min(percent_complete, tc_perc))
        tc_bar.progress(tc)
        fh= int(min(percent_complete, fh_perc))
        fh_bar.progress(fh)
        wc= int(min(percent_complete, wc_perc))
        wc_bar.progress(wc)
        bb= int(min(percent_complete, bb_perc))
        bb_bar.progress(bb)

if __name__ == "__main__":
    st.title(":blue[Fantasy Premier League 2024/25 Overview]")

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

    st.divider()
    st.subheader(f":blue[Total players :] {num_processor(data['total_players'])}")
    st.subheader(f":blue[Upcoming deadline :] {date_parser(events[next_round_index]['deadline_time'])}")
    render_top_5()
    st.divider()
    render_chip_usage()

    

