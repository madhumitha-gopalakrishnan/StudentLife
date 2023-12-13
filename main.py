# Importing all the required libraries
import streamlit as st
import plotly_express as px
import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

# Reading Data files: dinning
path = r'data/dinning'
pattern = os.path.join(path, "*.txt")
all_files = glob.glob(pattern)
li = []

for filename in all_files:
    df = pd.read_csv(filename, header=None, names=['date_and_time', 'location', 'meal_type'])
    # Extract the filename without the extension
    df['uid'] = os.path.basename(filename).split('.')[0]
    li.append(df)

# Combine all DataFrames into one
dinning = pd.concat(li, axis=0, ignore_index=True)

# Reading Data files: education, class
classList = pd.read_csv("data/education/class.csv", header=None, engine='python', usecols=lambda xy: xy in range(5))

# Rename the first column to 'uid'
classList.rename(columns={0: 'uid', 1: 'Class 1', 2: 'Class 2', 3: 'Class 3', 4: 'Class 4'}, inplace=True)

# Reshaping the DataFrame from wide format to long format
classList = pd.melt(classList, id_vars=['uid'], value_vars=['Class 1', 'Class 2', 'Class 3', 'Class 4'],
                    var_name='class_number', value_name='class').drop('class_number', axis=1)

# Reading Data files: education, class info
classInfo = pd.read_json("data/education/class_info.json", orient='index')
classInfo.reset_index(inplace=True)
classInfo.rename(columns={'index': 'class'}, inplace=True)

# Explode the 'periods' column into separate rows
classInfo = classInfo.explode('periods')

# Extract 'day', 'start', and 'end' from the 'periods' dictionary
classInfo[['Day', 'Start Time', 'End Time']] = classInfo['periods'].apply(pd.Series)
classInfo.drop('periods', axis=1, inplace=True)

# Merge the transformed CSV data with the JSON data on the 'class' column
classFile = pd.merge(classList, classInfo, on='class', how='left')

# Reading Data files: education, deadlines
deadlines = pd.read_csv("data/education/deadlines.csv")
deadlines = deadlines.melt(id_vars=["uid"], var_name='Date', value_name='No. of Deadlines')

# Reading Data files: education, grades
grades = pd.read_csv("data/education/grades.csv")

# Reading Data files: education, piazza
piazza = pd.read_csv("data/education/piazza.csv")

# Reading Data files: Survey, Loneliness Scale
lonelinessSurvey = pd.read_csv("data/survey/LonelinessScale.csv")

# Reading Data files: Survey, Perceived Stress Scale
perceivedStressSurvey = pd.read_csv("data/survey/PerceivedStressScale.csv")

# Reading Data files: EMA, EMA definition
emaDefinition = pd.read_json("data/EMA/EMA_definition.json")
emaDefinition = emaDefinition.explode('questions')

# Reading Data files: EMA, response, Activity
path = r'data/EMA/response/Activity'
pattern = os.path.join(path, "*.json")
all_files = glob.glob(pattern)
li = []

for filename in all_files:
    df = pd.read_json(filename)
    # Extract the base name of the file without the path and extension to add as a new column
    df['uid'] = os.path.basename(filename).split('.')[0]
    li.append(df)

ActivityEMA = pd.concat(li, axis=0, ignore_index=True)
ActivityEMA['uid'] = ActivityEMA['uid'].str.replace('Activity_', '')

# Reading Data files: EMA, response, Behavior
path = r'data/EMA/response/Behavior'
pattern = os.path.join(path, "*.json")
all_files = glob.glob(pattern)
li = []

for filename in all_files:
    df = pd.read_json(filename)
    # Extract the base name of the file without the path and extension to add as a new column
    df['uid'] = os.path.basename(filename).split('.')[0]
    li.append(df)

BehaviorEMA = pd.concat(li, axis=0, ignore_index=True)
BehaviorEMA['uid'] = BehaviorEMA['uid'].str.replace('Behavior_', '')

# Reading Data files: EMA, response, Class
path = r'data/EMA/response/Class'
pattern = os.path.join(path, "*.json")
all_files = glob.glob(pattern)
li = []

for filename in all_files:
    df = pd.read_json(filename)
    # Extract the base name of the file without the path and extension to add as a new column
    df['uid'] = os.path.basename(filename).split('.')[0]
    li.append(df)

ClassEMA = pd.concat(li, axis=0, ignore_index=True)
ClassEMA['uid'] = ClassEMA['uid'].str.replace('Class_', '')

# Reading Data files: EMA, response, Sleep
path = r'data/EMA/response/Sleep'
pattern = os.path.join(path, "*.json")
all_files = glob.glob(pattern)
li = []

for filename in all_files:
    df = pd.read_json(filename)
    # Extract the base name of the file without the path and extension to add as a new column
    df['uid'] = os.path.basename(filename).split('.')[0]
    li.append(df)

SleepEMA = pd.concat(li, axis=0, ignore_index=True)
SleepEMA['uid'] = SleepEMA['uid'].str.replace('Sleep_', '')

# Reading Data files: EMA, response, Mood 2
path = r'data/EMA/response/Mood 2'
pattern = os.path.join(path, "*.json")
all_files = glob.glob(pattern)
li = []

for filename in all_files:
    df = pd.read_json(filename)
    # Extract the base name of the file without the path and extension to add as a new column
    df['uid'] = os.path.basename(filename).split('.')[0]
    li.append(df)

Mood2EMA = pd.concat(li, axis=0, ignore_index=True)
Mood2EMA['uid'] = Mood2EMA['uid'].str.replace('Mood 2_', '')

# Piazza Page
st.title("Piazza Activity")

# Top 20 Contributors
st.header("Top 20 Contributors")

np.random.seed(0)  # For reproducibility
piazza1 = pd.DataFrame({
    'uid': [f'user{i}' for i in range(1, 101)],
    'contributions': np.random.poisson(20, 100)
})

# Sort by contributions and take the top 20
top_contributors = piazza1.nlargest(20, 'contributions')
top_contributors['area'] = (top_contributors['contributions'] / top_contributors['contributions'].max())

# Initialize the figure
fig, ax = plt.subplots(figsize=(10, 10))

# Set the axes limits to be closer to the total area covered by the circles
ax.set_xlim(2, 10)
ax.set_ylim(2, 10)

# Initialize an empty list to store circle positions
positions = []

# Plot each circle with the user's name and number of contributions on it
for (_, row) in top_contributors.iterrows():
    radius = np.sqrt(row['area'] / np.pi)  # Calculate radius from area

    # Generate random positions until a non-overlapping position is found
    while True:
        x = np.random.uniform(2 + radius, 10 - radius)
        y = np.random.uniform(2 + radius, 10 - radius)
        overlapping = False

        # Check if the new circle overlaps with any existing circle
        for (x_existing, y_existing, radius_existing) in positions:
            distance = np.sqrt((x - x_existing) ** 2 + (y - y_existing) ** 2)
            if distance < radius + radius_existing:
                overlapping = True
                break

        # If no overlap, add the position and break the loop
        if not overlapping:
            positions.append((x, y, radius))
            break

    circle = plt.Circle((x, y), radius, color=np.random.rand(3, ), alpha=0.5)
    ax.add_patch(circle)

    # Show user's name
    plt.text(x, y, row['uid'], ha='center', va='center', fontsize=8, color='black')

    # Show number of contributions below the user's name
    plt.text(x, y - radius / 2, f"{row['contributions']}", ha='center', va='center', fontsize=8,
             color='black')

# Remove axes for visual appeal
ax.axis('off')

# Set the aspect of the plot to be equal
ax.set_aspect('equal', adjustable='datalim')
plt.style.use('dark_background')

st.pyplot(plt)

# No of days users were active on Piazza
st.header('Number of Days Users Were Active')
fig1 = px.bar(piazza, x='uid', y='days online')
fig1.update_layout(xaxis_title='Users', yaxis_title='Active Days')
fig1.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig1)

# No of question users asked on Piazza
st.header("Who's asking questions")
fig1 = px.bar(piazza, x='uid', y='questions')
fig1.update_layout(xaxis_title='Users', yaxis_title='No of Questions')
fig1.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig1)

# No of answers users provided on Piazza
st.header("Who's answering questions")
fig1 = px.bar(piazza, x='uid', y='answers')
fig1.update_layout(xaxis_title='Users', yaxis_title='No of Answers')
fig1.update_xaxes(categoryorder='total descending')

st.plotly_chart(fig1)

# Grouped Bar Chart for Metric Comparison
st.header("Metric Comparison for Understanding the Nature of Contributions")

user_metrics = piazza[['uid', 'views', 'contributions', 'questions', 'notes', 'answers']]
fig2 = px.bar(user_metrics, x='uid', y=['views', 'contributions', 'questions', 'notes', 'answers'],
              title='Comparison of Metrics Across Users')
fig2.update_layout(xaxis_title='Users', yaxis_title='Metrics')
st.plotly_chart(fig2)

# Correlation between grades and contributions
# Combining piazza and grade csvs
gradePiazza = pd.merge(piazza, grades, on='uid', how='inner')
st.header("How does activity on Piazza affect student performance?")

# Dropdown to select the variable for correlation
selected_variable = st.selectbox("Select a Variable", ['views', 'contributions', 'days online', 'questions', 'answers'])

# Scatter plot to visualize the correlation
fig = px.scatter(gradePiazza, x=selected_variable, y=' gpa all',
                 title=f"Correlation between cumulative GPA and {selected_variable}")
st.plotly_chart(fig)

# Student Well-being Page
st.title("Student Well-being")

# Correlation of Well-being to Student Performance
st.header("Select a variable to see how it affects students performance")

# Dropdown to select the variable for correlation
selected_variable = st.selectbox("Select a Variable", ['Loneliness at the start of term',
                                                       'Loneliness at the end of term', 'Average Hours of Sleep',
                                                       'Average Workload Hours',
                                                       'Perceived Stress at the start of term',
                                                       'Perceived Stress at the end of term'])

# Calculating Loneliness
# Scoring system
scoring = {
    "Never": 1,
    "Rarely": 2,
    "Sometimes": 3,
    "Often": 4
}

# Apply the scoring system to the relevant columns
for col in lonelinessSurvey.columns:
    if col not in ['uid', 'type']:
        lonelinessSurvey[col] = lonelinessSurvey[col].map(scoring)

# Calculate the loneliness score for each user using sum
lonelinessSurvey['loneliness_score'] = lonelinessSurvey.drop(columns=['uid', 'type']).sum(axis=1)/20
lonelinessSurvey = lonelinessSurvey[['uid', 'type', 'loneliness_score']]
lonelinessSurveyPre = (lonelinessSurvey[lonelinessSurvey['type'] == 'pre'].
                       rename(columns={'loneliness_score': 'Loneliness at the start of term'}))
lonelinessSurveyPost = (lonelinessSurvey[lonelinessSurvey['type'] == 'post']
                        .rename(columns={'loneliness_score': 'Loneliness at the end of term'}))
lonelinessSurvey = lonelinessSurveyPre.merge(lonelinessSurveyPost, how="inner",
                                             on='uid').drop(columns=['type_x', 'type_y'])

# Calculating Sleep
averageSleepEMA = (SleepEMA.groupby('uid')['hour'].mean().reset_index()
                   .rename(columns={'hour': 'Average Hours of Sleep'}))

# Calculating Workload
WorkloadEMA = ClassEMA.groupby('uid')['hours'].mean().reset_index().rename(columns={'hours': 'Average Workload Hours'})

# Calculating Perceived Stress
# Scoring system
scoring = {
    "Never": 1,
    "Almost never": 2,
    "Sometime": 3,
    "Fairly often": 4,
    "Very often": 5
}

# Apply the scoring system to the relevant columns
for col in perceivedStressSurvey.columns:
    if col not in ['uid', 'type']:
        perceivedStressSurvey[col] = perceivedStressSurvey[col].map(scoring)

# Calculate the loneliness score for each user using sum
perceivedStressSurvey['perceived-stress_score'] = perceivedStressSurvey.drop(columns=['uid', 'type']).sum(axis=1)/10
perceivedStressSurvey = perceivedStressSurvey[['uid', 'type', 'perceived-stress_score']]
perceivedStressSurveyPre = (perceivedStressSurvey[perceivedStressSurvey['type'] == 'pre']
                            .rename(columns={'perceived-stress_score': 'Perceived Stress at the start of term'}))
perceivedStressSurveyPost = (perceivedStressSurvey[perceivedStressSurvey['type'] == 'post']
                             .rename(columns={'perceived-stress_score': 'Perceived Stress at the end of term'}))
perceivedStressSurvey = perceivedStressSurveyPre.merge(perceivedStressSurveyPost, how="inner",
                                                       on='uid').drop(columns=['type_x', 'type_y'])

# For an outer join
wellbeing = perceivedStressSurvey.merge(WorkloadEMA, on='uid', how='inner')
wellbeing = wellbeing.merge(averageSleepEMA, on='uid', how='inner')
wellbeing = wellbeing.merge(lonelinessSurvey, on='uid', how='inner')

gradeWellbeing = wellbeing.merge(grades, on='uid', how='inner')

# Scatter plot to visualize the correlation
fig = px.scatter(gradeWellbeing, x=selected_variable, y=' gpa all',
                 title=f"Correlation between cumulative GPA and {selected_variable}")
st.plotly_chart(fig)

# Mood Scale
st.header("How's Everyone Feeling")

# Convert 'resp_time' from Unix timestamp to readable date
Mood2EMA['resp_time'] = pd.to_datetime(Mood2EMA['resp_time'], unit='s')
Mood2EMA = Mood2EMA.drop(columns=['location', 'null'])

# Sort the DataFrame by 'resp_time'
Mood2EMA = Mood2EMA.sort_values(by='resp_time')

# Find the start date (first entry in the sorted DataFrame)
start_date = Mood2EMA['resp_time'].iloc[0]

# Calculate the number of weeks since the start date for each entry
Mood2EMA['week'] = (Mood2EMA['resp_time'] - start_date).dt.days // 7 + 1

# Pivot the data to form a matrix of 'uid' (rows) and 'relative_week' (columns)
heatmap_data = Mood2EMA.pivot_table(index='uid', columns='week', values='how', aggfunc='first')

# Custom color mapping for 'how' values
color_scale = [(0, "grey"),   # for NaN values
               (1/3, "green"),  # happy
               (2/3, "blue"),   # stressed
               (1, "yellow")]   # tired

# Create a heatmap
fig = px.imshow(heatmap_data, labels=dict(x="Week", y="Student ID", color="Mood"),
                color_continuous_scale=color_scale)

# Update color axis to display custom mood labels
fig.update_layout(
    coloraxis_colorbar=dict(
        tickvals=[1/6, 1/2, 5/6],
        ticktext=["Happy", "Stressed", "Tired"]
    )
)

st.plotly_chart(fig)

st.dataframe(Mood2EMA)

# Define mood labels
mood_labels = ['Happy', 'Stressed', 'Tired']

# Create a spider plot
fig = px.line_polar(Mood2EMA, r='week', theta=mood_labels, line_close=True,
                    labels={'1': 'Week 1', '2': 'Week 2', '3': 'Week 3', '4': 'Week 4'},
                    color_discrete_sequence=['red', 'blue', 'green'],
                    category_orders={'theta': mood_labels})

# Customize the spider plot layout
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    legend_title_text='Users',
    polar_angularaxis_rotation=90,
    title='Mood Spider Plot',
)

# Display the spider plot using Streamlit
st.plotly_chart(fig)

st.dataframe(Mood2EMA)


# Displaying EMA tables
st.dataframe(emaDefinition)
st.dataframe(ActivityEMA)
st.dataframe(BehaviorEMA)

# Displaying Education tables
st.dataframe(deadlines)
st.dataframe(grades)
st.dataframe(piazza)

# Displaying Other tables
st.dataframe(dinning.head())
