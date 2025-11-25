import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(page_title="User Activity Dashboard", layout="wide")

# --- Helper Function: Generate Mock Data ---
# In a real app, this data would come from a database or log file.
@st.cache_data
def load_mock_data(rows=200):
    users = ['admin', 'j.doe', 'a.smith', 'guest_user', 'm.jones']
    actions = ['Login', 'View Page', 'Submit Form', 'Download Report', 'Logout', 'Error']
    status = ['Success', 'Success', 'Success', 'Success', 'Failed'] # Weighted to allow some failures
    
    data = []
    base_time = datetime.now()
    
    for _ in range(rows):
        # Randomize time within last 7 days
        random_minutes = np.random.randint(0, 10000)
        timestamp = base_time - timedelta(minutes=random_minutes)
        
        row = {
            "Timestamp": timestamp,
            "User": np.random.choice(users),
            "Action": np.random.choice(actions),
            "Status": np.random.choice(status),
            "Session_Duration_Sec": np.random.randint(10, 600)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    df = df.sort_values(by="Timestamp", ascending=False)
    return df

# --- Load Data ---
st.title("📊 Application Activity & Audit Dashboard")
st.markdown("Monitor user interactions, track errors, and analyze session performance.")

df = load_mock_data()

# --- Sidebar: Filters ---
st.sidebar.header("Filter Logs")

# User Filter
selected_user = st.sidebar.multiselect(
    "Select User(s)",
    options=df["User"].unique(),
    default=df["User"].unique()
)

# Action Filter
selected_action = st.sidebar.multiselect(
    "Select Action Type",
    options=df["Action"].unique(),
    default=df["Action"].unique()
)

# Apply Filters
df_filtered = df[
    (df["User"].isin(selected_user)) & 
    (df["Action"].isin(selected_action))
]

# --- Top Level Metrics ---
col1, col2, col3, col4 = st.columns(4)

total_actions = len(df_filtered)
failed_actions = len(df_filtered[df_filtered['Status'] == 'Failed'])
unique_users = df_filtered['User'].nunique()
avg_duration = df_filtered['Session_Duration_Sec'].mean()

col1.metric("Total Events", total_actions)
col2.metric("Failed Actions", failed_actions, delta_color="inverse" if failed_actions > 0 else "normal")
col3.metric("Active Users", unique_users)
col4.metric("Avg Duration", f"{avg_duration:.1f}s")

st.markdown("---")

# --- Charts Section ---
col_left, col_right = st.columns(2)

# Chart 1: Activity over Time (Histogram)
with col_left:
    st.subheader("Activity Timeline")
    fig_time = px.histogram(
        df_filtered, 
        x="Timestamp", 
        color="Status", 
        nbins=20,
        title="Events over Time (Success vs Failed)",
        color_discrete_map={"Success": "#00CC96", "Failed": "#EF553B"}
    )
    st.plotly_chart(fig_time, use_container_width=True)

# Chart 2: Action Breakdown (Pie)
with col_right:
    st.subheader("Action Distribution")
    fig_pie = px.pie(
        df_filtered, 
        names="Action", 
        title="Distribution of User Actions",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Chart 3: User Activity Heatmap (or Bar)
st.subheader("User Activity Volume")
user_activity = df_filtered['User'].value_counts().reset_index()
user_activity.columns = ['User', 'Count']

fig_bar = px.bar(
    user_activity, 
    x='User', 
    y='Count', 
    color='Count',
    title="Total Actions per User",
    text_auto=True
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Detailed Data View ---
with st.expander("📂 View Raw Log Data"):
    st.dataframe(
        df_filtered.style.applymap(
            lambda x: 'background-color: #ffcdd2' if x == 'Failed' else '', 
            subset=['Status']
        )
    )
    
    # Download Button
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name='activity_logs_export.csv',
        mime='text/csv',
    )
