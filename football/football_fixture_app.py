import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta

# Original code here: parameters, functions, etc.



# Parameters
teams = [
    "Wargrave Wolves", "Oakfield Eagles", "Wollaston Blue", "Parkfield Youth", 
    "Ware Lions", "Ware FC", "West Wight Youth", "Brading Youth", 
    "Brockworth Albion", "Gurnard Rockets"
]
team_colors = {
    "Wargrave Wolves": "Red & Black",
    "Oakfield Eagles": "Royal Blue",
    "Wollaston Blue": "Blue & White",
    "Parkfield Youth": "Red & White",
    "Ware Lions": "Black & White",
    "Ware FC": "Royal Blue & White",
    "West Wight Youth": "Yellow & Black",
    "Brading Youth": "Red & White",
    "Brockworth Albion": "Black & White",
    "Gurnard Rockets": "Green"
}
num_pitches = 3
start_time_day1 = "13:00"
start_time_day2 = "09:00"
last_match_start_day1 = "17:00"
last_match_start_day2 = "17:00"
match_duration = 30  # minutes
seed = 42




def generate_fixture(teams, num_pitches,seed):
    random.seed(seed)
    random.shuffle(teams)  
    fixtures = []
    num_teams = len(teams)
    if num_teams % 2 != 0:
        teams.append("Bye")
        num_teams += 1

    for round_num in range(num_teams - 1):
        round_matches = []
        for i in range(num_teams // 2):
            home = teams[i]
            away = teams[num_teams - 1 - i]
            if home != "Bye" and away != "Bye":
                round_matches.append((home, away))
        fixtures.append(round_matches)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1] 
    return fixtures


def schedule_matches(fixtures, start_time_day1, start_time_day2, last_match_start_day1, last_match_start_day2, num_pitches, match_duration):
    schedule = []
    start_time_day1 = datetime.strptime(start_time_day1, "%H:%M")
    start_time_day2 = datetime.strptime(start_time_day2, "%H:%M")
    last_match_start_day1 = datetime.strptime(last_match_start_day1, "%H:%M")
    last_match_start_day2 = datetime.strptime(last_match_start_day2, "%H:%M")
    current_time = start_time_day1
    current_day = 1
    pitch = 1

    for round_matches in fixtures:
        for match in round_matches:
            if current_day == 1 and current_time > last_match_start_day1:
                current_day = 2
                current_time = start_time_day2
                pitch = 1
            if current_day == 2 and current_time > last_match_start_day2:
                break
            schedule.append({
                "Date": f"Day {current_day}",
                "Time": current_time.strftime("%H:%M"),
                "Pitch": pitch,
                "Team A": match[0],
                "Team B": match[1],
            })
            pitch += 1
            if pitch > num_pitches:
                pitch = 1
                current_time += timedelta(minutes=match_duration)
    return schedule

    
    
st.title("Football Fixture Generator")
st.sidebar.header("Settings")

num_pitches = st.sidebar.number_input("Number of Pitches", min_value=1, value=3)
match_duration = st.sidebar.number_input("Match Duration (minutes)", min_value=1, value=30)
seed = st.sidebar.number_input("Seed", min_value=1, value=42)

if st.button("Generate Fixture"):
    fixtures = generate_fixture(teams, num_pitches,seed)
    schedule = schedule_matches(
        fixtures, start_time_day1, start_time_day2, 
        last_match_start_day1, last_match_start_day2, 
        num_pitches, match_duration
    )
    
    df = pd.DataFrame(schedule)
    st.dataframe(df)
    st.download_button(
        label="Download Excel", 
        data=df.to_csv(index=False), 
        file_name="football_fixture.csv", 
        mime="text/csv"
    )
