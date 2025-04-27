import streamlit as st
from docx import Document
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

    # Track active teams and pitch availability
    active_teams = set()

    for round_matches in fixtures:
        # Track matches scheduled for each pitch in a time slot
        pitch = 1
        for match in round_matches:
            # Move to the next day if time exceeds the last match start time
            if current_day == 1 and current_time > last_match_start_day1:
                current_day = 2
                current_time = start_time_day2
                active_teams.clear()
            if current_day == 2 and current_time > last_match_start_day2:
                break

            # Ensure no overlap and limit matches to available pitches
            if pitch <= num_pitches and match[0] not in active_teams and match[1] not in active_teams:
                schedule.append({
                    "Date": f"Day {current_day}",
                    "Time": current_time.strftime("%H:%M"),
                    "Pitch": pitch,
                    "Team A": match[0],
                    "Team B": match[1],
                })
                active_teams.add(match[0])
                active_teams.add(match[1])
                pitch += 1

            # If all pitches are occupied or teams overlap, move to the next time slot
            if pitch > num_pitches:
                current_time += timedelta(minutes=match_duration)
                pitch = 1
                active_teams.clear()

        # Increment time after processing all matches in the current round
        current_time += timedelta(minutes=match_duration)
        active_teams.clear()

    return schedule



def create_word_output(schedule, team_colors, output_file="football_fixture.docx"):
    doc = Document()
    
    doc.add_heading("Football Match Fixture", level=1)
    doc.add_paragraph("ALL MATCHES ARE 11 MINUTES EACH WAY", style='Intense Quote')
    doc.add_heading("Team Colors", level=2)
    
    for team, color in team_colors.items():
        doc.add_paragraph(f"{team} – {color}")
    
    doc.add_heading("Match Schedule", level=2)
    
    for entry in schedule:
        doc.add_paragraph(f"{entry['Date']} | {entry['Time']} | Pitch {entry['Pitch']} | {entry['Team A']} vs {entry['Team B']}")
    
    doc.save(output_file)
    print(f"Word document saved as {output_file}")


# # Main execution
# fixtures = generate_fixture(teams, num_pitches,seed)
# schedule = schedule_matches(fixtures, start_time_day1, start_time_day2, last_match_start_day1, last_match_start_day2, num_pitches, match_duration)


# df = pd.DataFrame(schedule)
# df=df.reset_index()
# df.rename(columns={'index':'Match #'},inplace=True)
# df['Match #']+=1
# df.set_index('Match #',inplace=True)

# df.to_excel("football_fixture.xlsx", index=False)


# create_word_output(schedule, team_colors)
# print("Fixture has been created and saved to 'football_fixture.xlsx' and 'football_fixture.docx'")

#--------- APP
    
# Streamlit App
st.title("Football Fixture Generator")
st.sidebar.header("Settings")

# Step 1: Select the Number of Teams
num_teams = st.sidebar.number_input("Number of Teams", min_value=2, max_value=20, value=10)

# Step 2: Input Team Names
teams = []
for i in range(num_teams):
    team_name = st.sidebar.text_input(f"Enter Team {i+1} Name", value=f"Team {i+1}")
    teams.append(team_name)

# Step 3: Select Start and End Times for Each Day
start_time_day1 = st.sidebar.text_input("Start Time (Day 1)", value="13:00")
last_match_start_day1 = st.sidebar.text_input("End Time (Day 1)", value="17:00")
start_time_day2 = st.sidebar.text_input("Start Time (Day 2)", value="09:00")
last_match_start_day2 = st.sidebar.text_input("End Time (Day 2)", value="17:00")

# Other Parameters
num_pitches = st.sidebar.number_input("Number of Pitches", min_value=1, value=3)
match_duration = st.sidebar.number_input("Match Duration (minutes)", min_value=1, value=30)
seed = st.sidebar.number_input("Random Seed", value=42)

if st.button("Generate Fixture"):
    random.seed(seed)
    fixtures = generate_fixture(teams, num_pitches,seed)
    schedule = schedule_matches(
        fixtures, start_time_day1, start_time_day2, 
        last_match_start_day1, last_match_start_day2, 
        num_pitches, match_duration
    )
    
    # Display the schedule
    df = pd.DataFrame(schedule)
    df=df.reset_index()
    df.rename(columns={'index':'Match #'},inplace=True)
    df['Match #']+=1
    df.set_index('Match #',inplace=True)

    st.dataframe(df)
    
    # Options for Downloads
    st.download_button(
        label="Download Excel",
        data=df.to_csv(index=False),
        file_name="football_fixture.csv",
        mime="text/csv"
    )
    
    create_word_output(schedule, {team: "Color TBD" for team in teams}, output_file="football_fixture.docx")
    with open("football_fixture.docx", "rb") as doc:
        st.download_button(
            label="Download Word Document",
            data=doc,
            file_name="football_fixture.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )