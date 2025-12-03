# ddg_app.py (FINAL VERSION)

import streamlit as st
import urllib.parse 

# --- 1. TITLE AND PHENOMENON SELECTION (NGSS PEs) ---
st.title("Dynamic Data Generator (DDG)")
st.markdown("Configure parameters below to generate a synthetic data set.")

# Select the phenomenon based on the Performance Expectation (PE) ID
# Corrected: Added the list of options
pe_id = st.selectbox(
    "1. Select Target NGSS Phenomenon (PE ID):",
    options=(
        "Select a Phenomenon", 
        "LS2-1", 
        "PS3-1_KE"
    ), 
    index=2, # This defaults the selection to "PS3-1_KE"
    help="LS2-1: Population Dynamics | PS3-1_KE: Kinetic Energy"
)

# --- 2. SCIENTIFIC CONTROLS (DCI Parameters) ---
#... (Conditional logic for sliders remains identical to your working code)...
st.header("2. Scientific Controls (DCI Parameters)")
st.markdown("Adjust the core scientific variables for the selected phenomenon.")

if pe_id == "LS2-1":
    L_param = st.slider("Carrying Capacity (L):", min_value=1000, max_value=20000, value=8000, step=100, help="The theoretical maximum population the ecosystem can support.")
    k_param = st.slider("Growth Rate (k):", min_value=0.1, max_value=1.0, value=0.7, step=0.1, help="The rate at which the population approaches carrying capacity.")
    t_range = st.slider("Simulation Length (Time Steps):", min_value=10, max_value=100, value=60, help="The number of data points/time periods to generate.")
    mass_const = 0.0
    
elif pe_id == "PS3-1_KE":
    mass_const = st.slider("Object Mass (m) in kg:", min_value=1.0, max_value=50.0, value=10.0, step=1.0, help="The mass of the object whose kinetic energy is measured.")
    t_range = st.slider("Velocity Range (v) Max:", min_value=10, max_value=100, value=60, help="The range of velocities (0 up to this value) to measure. Acts as time steps.")
    L_param = 0
    k_param = 0

else:
    st.info("Select a phenomenon to view specific controls.")
    L_param = 0
    k_param = 0
    t_range = 0
    mass_const = 0

# --- 3. PEDAGOGICAL CONTROL (SEP Parameter) ---
st.header("3. Pedagogical Noise Control (SEP Parameter)")

sigma_noise = st.slider(
    "Measurement Noise (Sigma) $\sigma$:", 
    min_value=0, 
    max_value=1000, 
    value=200, 
    step=50,
    help="Controls data variability. Higher values require statistical analysis (SEP 4)." 
)

# --- 4. DATA SUBMISSION LOGIC ---

# CRITICAL: These are the actual codes extracted from your pre-filled form URL
# These variables map the input to the correct column in your Google Sheet queue.
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdHG4YeDy8TVSV8OqnyAMt19MIus4OkHgvnN4E6P8j7n0syWw/formResponse" 
PE_ID_ENTRY = 'entry.1507860347' 
L_PARAM_ENTRY = 'entry.556163887' 
SIGMA_ENTRY = 'entry.368579672' 

if st.button("Generate Synthetic Data"):
    if pe_id == "Select a Phenomenon":
        st.error("Please select a phenomenon before generating data.")
    else:
        # 1. Define the parameters using the extracted entry IDs
        url_params = {
            PE_ID_ENTRY: pe_id,       # Takes PE_ID from selectbox
            L_PARAM_ENTRY: L_param,     # Takes L_param/Mass from slider
            SIGMA_ENTRY: sigma_noise, # Takes Noise_Sigma from slider
            'submit': 'submit' # Critical: ensures the form is submitted
        }
        
        # 2. Build the final submission link
        submission_url = GOOGLE_FORM_URL + "?" + urllib.parse.urlencode(url_params)
        
        # 3. Display success and use a redirect link to finalize the submission
        st.success(f"Request Sent for PE ID: {pe_id}!")
        st.markdown(f"**Data parameters have been recorded in the Control Sheet queue.**")
        st.info("The DDG Engine will execute the computation based on the latest entry shortly.")
        
        # This link forces the browser to submit the GET request to the Google Form,
        # thereby adding the new request row to your DDG_Control_Sheet.
        st.markdown(f'<a href="{submission_url}" target="_self">Click Here to Finalize Submission and Check Queue</a>', unsafe_allow_html=True)
