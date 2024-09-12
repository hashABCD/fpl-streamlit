import requests
import json
import pandas as pd
import streamlit as st
import time

RAND_ID = 95037
AB_ID = 9508937

def get_entry_personal_data(entry_id):
    """ Retrieve the summary/history data for a specific entry/team
    Args:
        entry_id (int) : ID of the team whose data is to be retrieved
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    full_url = base_url + str(entry_id) + "/"
    response = ''
    while response == '':
        try:
            response = requests.get(full_url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.text)
    return data

def get_entry_data(entry_id):
    """ Retrieve the summary/history data for a specific entry/team
    Args:
        entry_id (int) : ID of the team whose data is to be retrieved
    """
    base_url = "https://fantasy.premierleague.com/api/entry/"
    full_url = base_url + str(entry_id) + "/history/"
    response = ''
    while response == '':
        try:
            response = requests.get(full_url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.text)
    return data

def get_cumulative_player_data(player_id):
    personal_data=get_entry_personal_data(player_id)
    f_name=personal_data['player_first_name']
    l_name=personal_data['player_last_name']
    name=f_name+" "+l_name
    current_data=get_entry_data(player_id)['current']
    return name, current_data

def generate_df(current_data, name, metric):
    current_gw = current_data[-1]['event']
    gws_played = len(current_data)

    not_played = current_gw-gws_played

    gw_list = []
    tot_pts =[]

    #for late joiners 
    for i in range(1,not_played+1):
        gw_list.append(int(i))
        tot_pts.append(None)
        
    for gw_data in current_data:
        gw_list.append(int(gw_data['event'])) 
        tot_pts.append(gw_data[metric])
        
    df=pd.DataFrame({"GW":(gw_list), name:tot_pts})

    return df

def get_metric_df(player_ids, metric_list):
    df_list = []
    names = []
    for id in player_ids:
        name, current_data = get_cumulative_player_data(id)
        names.append(name)
        metric_df_dict = {}
        for metric in metric_list:
            metric_df_dict.update({metric : generate_df(current_data, name, metric)})
        df_list.append(metric_df_dict)

    metric_df_list =[]
    for metric in metric_list:
        df = df_list[0][metric]
        for x in df_list[1:]:
            df=df.join(x[metric].set_index('GW'), on='GW')
        metric_df_list.append(df)

    return metric_df_list, names



st.header("FANTASY PREMIER LEAGUE COMPARE")
st.markdown("Enter your Entry Id and competitor's ID to compare.")
    
entry_list=[]
entry_list.append(st.text_input("Enter your Entry ID :", AB_ID))
entry_list.append(st.text_input("Enter competitor Entry ID :",RAND_ID))
st.markdown("You can find entry id on points page URL")
st.image("entry_id_help.png")

metric_list = ['total_points', 'percentile_rank']
metric_df_list, names = get_metric_df(entry_list, metric_list)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Total Points")
    st.line_chart(metric_df_list[0], x="GW",y=names, x_label="Gameweeks")
with col2:
    st.subheader("Percentile Rank")
    st.line_chart(metric_df_list[1], x="GW",y=names, x_label="Gameweeks")