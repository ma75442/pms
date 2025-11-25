import streamlit as st
import time
import Levenshtein # Requires: pip install python-Levenshtein

# --- Helper Functions ---
def calculate_wpm(text, time_taken):
    """Calculates Words Per Minute."""
    if time_taken == 0:
        return 0
    words = len(text.split())
    minutes = time_taken / 60
    return round(words / minutes, 2)

def calculate_accuracy(original, target):
    """Calculates accuracy percentage using Levenshtein distance."""
    if not original:
        return 0.0
    distance = Levenshtein.distance(original, target)
    max_len = max(len(original), len(target))
    accuracy = (1 - (distance / max_len)) * 100
    return round(accuracy, 2)

# --- App State Management ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'test_active' not in st.session_state:
    st.session_state.test_active = False

# --- App Layout ---
st.set_page_config(page_title="Typing Biometrics Lab")
st.title("⌨️ Typing Behavior & Speed Analyzer")
st.markdown("This tool analyzes user input efficiency (WPM) and precision (Accuracy).")

target_sentence = "The quick brown fox jumps over the lazy dog."

st.info(f"**Target Sentence:** {target_sentence}")

# --- Logic ---
if st.button("Start Test"):
    st.session_state.test_active = True
    st.session_state.start_time = time.time()
    st.rerun()

if st.session_state.test_active:
    st.write("⏱️ **Timer Running... Type the sentence below!**")
    
    # We use a form to capture the final input
    with st.form("typing_form"):
        user_input = st.text_input("Type here:", autocomplete="off")
        submitted = st.form_submit_button("Submit Result")
        
        if submitted:
            end_time = time.time()
            elapsed_time = end_time - st.session_state.start_time
            
            # Reset state
            st.session_state.test_active = False
            st.session_state.start_time = None
            
            # Calculations
            wpm = calculate_wpm(user_input, elapsed_time)
            accuracy = calculate_accuracy(user_input, target_sentence)
            
            st.divider()
            st.subheader("📊 Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Time Taken", f"{round(elapsed_time, 2)}s")
            col2.metric("Typing Speed", f"{wpm} WPM")
            col3.metric("Accuracy", f"{accuracy}%")
            
            if accuracy < 100:
                st.error(f"Mismatch detected. You typed: '{user_input}'")
            else:
                st.success("Perfect Match!")
            
            # Educational Note on Biometrics
            st.caption(f"""
                **Biometric Data Point:** Your typing cadence for this session was approx {round(len(user_input)/elapsed_time, 2)} characters per second. 
                In security contexts, this 'flight time' can be used for behavioral authentication.
            """)

# --- Reset ---
if st.button("Reset Application"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
