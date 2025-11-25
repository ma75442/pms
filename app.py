import streamlit as st
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Input Forensics Logger", layout="centered")

# --- Session State Initialization ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

if 'last_input' not in st.session_state:
    st.session_state.last_input = ""

# --- Callback Function ---
def log_input_change():
    """
    This function triggers every time the user interacts with the text area.
    It captures the current content and logs it.
    """
    current_text = st.session_state.user_input
    
    # Only log if there's an actual change to avoid duplicates
    if current_text != st.session_state.last_input:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Calculate the length change (to simulate keystroke volume)
        diff = len(current_text) - len(st.session_state.last_input)
        action_type = "Addition" if diff > 0 else "Deletion"
        
        log_entry = {
            "Timestamp": timestamp,
            "Action Type": action_type,
            "Char_Diff": diff,
            "Captured_Content": current_text
        }
        
        st.session_state.logs.append(log_entry)
        st.session_state.last_input = current_text

# --- UI Layout ---
st.title("🛡️ Input Forensics Logger")
st.markdown("""
    **Academic Demo:** This tool demonstrates how to track the *evolution* of user input. 
    It logs the state of the text field every time you press `Ctrl+Enter` or click outside the box.
""")

st.warning("⚠️ This runs locally in the browser. No data is sent externally.")

# The Target Input Field
# Note: standard Streamlit text_area updates on focus loss or Ctrl+Enter.
st.text_area(
    "Target Input Field (Type here and press Ctrl+Enter to log):", 
    key="user_input", 
    height=150,
    on_change=log_input_change
)

st.divider()

# --- Visualization of the "Logs" ---
st.subheader("📝 Captured Input History")

if st.session_state.logs:
    # Convert logs to DataFrame for display
    df = pd.DataFrame(st.session_state.logs)
    
    # Reverse order to show newest first
    df_display = df.iloc[::-1]
    
    # metrics
    total_edits = len(df)
    net_chars = len(st.session_state.last_input)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Edit Events", total_edits)
    col2.metric("Current String Length", net_chars)

    # Show the table
    st.dataframe(
        df_display, 
        column_config={
            "Timestamp": "Time",
            "Captured_Content": st.column_config.TextColumn("Captured State", width="large")
        },
        use_container_width=True
    )
    
    # Option to clear logs
    if st.button("Clear Log History"):
        st.session_state.logs = []
        st.session_state.last_input = ""
        st.rerun()
else:
    st.info("Start typing in the box above to generate logs.")
