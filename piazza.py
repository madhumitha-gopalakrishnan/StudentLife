# Importing all the required libraries
import streamlit as st
import plotly_express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def show():
    # Reading Data files: education, grades
    grades = pd.read_csv("data/education/grades.csv")

    # Reading Data files: education, piazza
    piazza = pd.read_csv("data/education/piazza.csv")

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
    selected_variable = st.selectbox("Select a Variable", ['views', 'contributions',
                                                           'days online', 'questions', 'answers'])

    # Scatter plot to visualize the correlation
    fig = px.scatter(gradePiazza, x=selected_variable, y=' gpa all',
                     title=f"Correlation between cumulative GPA and {selected_variable}")
    st.plotly_chart(fig)
