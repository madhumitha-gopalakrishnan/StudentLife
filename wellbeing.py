# Importing all the required libraries
import streamlit as st
import plotly_express as px
import pandas as pd
import glob
import os


def show():
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

    # Reading Data files: EMA, response, Stress
    path = r'data/EMA/response/Stress'
    pattern = os.path.join(path, "*.json")
    all_files = glob.glob(pattern)
    li = []

    for filename in all_files:
        df = pd.read_json(filename)
        # Extract the base name of the file without the path and extension to add as a new column
        df['uid'] = os.path.basename(filename).split('.')[0]
        li.append(df)

    StressEMA = pd.concat(li, axis=0, ignore_index=True)
    StressEMA['uid'] = StressEMA['uid'].str.replace('Stress_', '')

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

    st.header('Anxiety Level Trend of Students')
    # Unique list of students
    BehaviorEMA['resp_time'] = pd.to_datetime(BehaviorEMA['resp_time'], unit='s')

    # Sort the DataFrame by 'resp_time'
    BehaviorEMA = BehaviorEMA.sort_values(by='resp_time')

    # Find the start date (first entry in the sorted DataFrame)
    start_date = BehaviorEMA['resp_time'].iloc[0]

    # Calculate the number of weeks since the start date for each entry
    BehaviorEMA['week'] = (BehaviorEMA['resp_time'] - start_date).dt.days // 7 + 1

    students = BehaviorEMA['uid'].unique()

    # Dropdown to select a student
    selected_student = st.selectbox('Select a Student', students)

    # Filter the data for the selected student
    student_data = BehaviorEMA[BehaviorEMA['uid'] == selected_student]

    # Plotting
    st.line_chart(student_data, x='resp_time', y='anxious')

    st.header('Stress Level Trend of Students')
    # Unique list of students
    student = StressEMA['uid'].unique()

    # Dropdown to select a student
    selected_student = st.selectbox('Select Student', student)

    # Filter the data for the selected student
    student_data = StressEMA[StressEMA['uid'] == selected_student]

    # Plotting
    st.line_chart(student_data, x='resp_time', y='level')

    st.header('Sleep Trend of Students')
    # Unique list of students
    student = SleepEMA['uid'].unique()

    # Dropdown to select a student
    selected_student = st.selectbox('Select the Student', student)

    # Filter the data for the selected student
    student_data = SleepEMA[SleepEMA['uid'] == selected_student]

    # Plotting
    st.line_chart(student_data, x='resp_time', y='hour')