# ddg_app.py (FINAL VERSION WITH ALL CRITICAL MAPPING FIXES)

import streamlit as st
import urllib.parse 

# --- 1. TITLE AND PHENOMENON SELECTION (NGSS PEs) ---

st.title("Dynamic Data Generator (DDG)") 
st.markdown("Configure parameters below to generate a synthetic data set.")

# Select the phenomenon based on the Performance Expectation (PE) ID
pe_id = st.selectbox(
    "1. Select Target NGSS Phenomenon (PE ID):",
    options=(
        "Select a Phenomenon", 
        "LS2-1 (Population Dynamics)",        # MS/HS Life Science
        "HS-PS3-1 (Energy Conservation)",     # HS Physical Science
        "HS-PS1-5 (Reaction Kinetics)",       # HS Physical Science (Enzymes/Chemistry)
        "MS-ESS1-3 (Solar System Scaling)",   # MS Earth Science
        "HS-ESS2-2 (Climate Feedback Loop)",  # HS Earth Science
        "PS3-1_KE (Kinetic Energy)"           # MS/HS Physical Science
    ), 
    index=0, 
    help="PEs require quantitative analysis, models, or simulations."
)

# --- 2. SCIENTIFIC CONTROLS (DCI Parameters) ---
st.header("2. Scientific Controls (DCI Parameters)")
st.markdown("Adjust the core scientific variables for the selected phenomenon.")

# Initialize variables to ensure they are defined before submission (CRITICAL FOR MAPPING)
L_param = 0.0
k_param = 0.0
t_range = 0
mass_const = 0.0
sigma_noise = 0.0 

# --- LOGIC TO GATHER PARAMETERS ---

if pe_id == "LS2-1 (Population Dynamics)":
    # Parameters for Logistic Growth (Population Dynamics)
    L_param = st.slider("Carrying Capacity (L):", min_value=1000, max_value=20000, value=8000, step=100, help="The theoretical maximum population the ecosystem can support.")
    k_param = st.slider("Growth Rate (k):", min_value=0.1, max_value=1.0, value=0.7, step=0.1, help="The rate at which the population approaches carrying capacity.")
    t_range = st.slider("Simulation Length (Time Steps):", min_value=10, max_value=100, value=60, help="The number of data points/time periods to generate.")
    mass_const = 0.0
    
elif pe_id == "PS3-1_KE (Kinetic Energy)":
    # Parameters for Kinetic Energy (Energy vs. Motion)
    mass_const = st.slider("Object Mass (m) in kg:", min_value=1.0, max_value=50.0, value=10.0, step=1.0, help="The mass of the object whose kinetic energy is measured.")
    t_range = st.slider("Velocity Range (v) Max:", min_value=10, max_value=100, value=60, help="The range of velocities (0 up to this value) to measure. Acts as time steps.")
    L_param = 0.0
    k_param = 0.0

elif pe_id == "HS-PS3-1 (Energy Conservation)":
    # Parameters for Energy Conservation (HS Computational Model) [1, 2, 3, 4, 5, 6, 7]
    E_in = st.number_input("Energy Input (E_in, Joules):", min_value=100.0, max_value=5000.0, value=1000.0, step=50.0, help="Total energy put into the closed system.")
    Efficiency = st.slider("System Efficiency (η):", min_value=0.5, max_value=0.99, value=0.85, step=0.01, help="Fraction of energy converted to useful output (E_out = E_in * η).")
    Num_Trials = st.slider("Number of Data Points:", min_value=10, max_value=100, value=30)
    L_param = E_in
    k_param = Efficiency
    t_range = Num_Trials
    mass_const = 0.0

elif pe_id == "HS-PS1-5 (Reaction Kinetics)":
    # Parameters for Chemical Kinetics (Reaction Rate vs. Temperature/Concentration)
    Optimum_Temp = st.slider("Optimum Temperature (°C):", min_value=10, max_value=70, value=40, step=5, help="Temperature where reaction rate peaks (e.g., Enzyme B in your example).")
    Temp_Effect = st.slider("Thermal Stability Factor:", min_value=1.0, max_value=10.0, value=3.0, step=0.5, help="Controls how quickly activity drops off at non-optimal temperatures (simulates denaturation).")
    Conc_Range = st.slider("Max Substrate Concentration:", min_value=10, max_value=200, value=100, step=10, help="Range of the independent variable.")
    L_param = float(Optimum_Temp)
    k_param = Temp_Effect
    t_range = Conc_Range
    mass_const = 0.0

elif pe_id == "MS-ESS1-3 (Solar System Scaling)":
    # Parameters for Solar System Scaling (MS Quantitative Analysis)
    Scale_Factor = st.slider("Scale Factor (Ratio base):", min_value=1, max_value=1000, value=100, help="Used as a divisor to scale large numbers for easier graphing (e.g., 100).")
    Data_Points = st.slider("Number of Data Points (Planets/Moons):", min_value=5, max_value=20, value=10)
    L_param = float(Scale_Factor)
    k_param = 0.0
    t_range = Data_Points
    mass_const = 0.0

elif pe_id == "HS-ESS2-2 (Climate Feedback Loop)":
    # Parameters for Climate Feedback Loop (HS Computational Model) [8, 9, 10, 11]
    Initial_GHG_Increase = st.slider("Initial GHG Anomaly (ppm):", min_value=1, max_value=50, value=10, help="Initial shock to the system (e.g., CO2 pulse).")
    Albedo_Feedback_Strength = st.slider("Feedback Multiplier (Ice-Albedo):", min_value=0.01, max_value=0.5, value=0.1, step=0.01, help="Controls the speed at which ice melt accelerates warming.")
    Time_Steps_Years = st.slider("Simulation Time (Years):", min_value=10, max_value=500, value=100)
    L_param = float(Initial_GHG_Increase)
    k_param = Albedo_Feedback_Strength
    t_range = Time_Steps_Years
    mass_const = 0.0

else:
    st.info("Select a phenomenon to view specific controls.")

# --- 3. PEDAGOGICAL CONTROL (SEP Parameter) ---
st.header("3. Pedagogical Noise Control (SEP Parameter)")

sigma_noise = st.slider(
    "Measurement Noise (Sigma) $\sigma$:", 
    min_value=0.0, 
    max_value=1000.0, 
    value=200.0, 
    step=50.0,
    help="Controls data variability. Higher values require statistical analysis (SEP 4)." 
)

# --- 4. DATA SUBMISSION LOGIC (FINAL CORRECTED BLOCK) ---

# CRITICAL: These Entry IDs are now all correct and finalized.
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdHG4YeDy8TVSV8OqnyAMt19MIus4OkHgvnN4E6P8j7n0syWw/formResponse" 
PE_ID_ENTRY = 'entry.1507860347' 
L_PARAM_ENTRY = 'entry.556163887' 
SIGMA_ENTRY = 'entry.368579672' 

# NEWLY DISCOVERED IDs:
K_PARAM_ENTRY = 'entry.875928263'  
T_RANGE_ENTRY = 'entry.681731572'  


if st.button("Generate Synthetic Data"):
    if pe_id == "Select a Phenomenon":
        st.error("Please select a phenomenon before generating data.")
    else:
        # 1. Define the parameters, now including k_param and t_range
        url_params = {
            PE_ID_ENTRY: pe_id,       
            L_PARAM_ENTRY: L_param,     
            SIGMA_ENTRY: sigma_noise, 
            K_PARAM_ENTRY: k_param,     # Sends Growth Rate, Efficiency, or Feedback Multiplier
            T_RANGE_ENTRY: t_range,     # Sends Simulation Length or Data Points
            'submit': 'submit'
        }
        
        # 2. Build the final submission link
        submission_url = GOOGLE_FORM_URL + "?" + urllib.parse.urlencode(url_params)
        
        # 3. Display success and use a redirect link to finalize the submission
        st.success(f"Request Sent for PE ID: {pe_id}!")
        st.markdown(f"**Data parameters have been recorded in the Control Sheet queue.**")
        st.info("The DDG Engine will execute the computation based on the latest entry shortly.")
        
        # This link forces the browser to submit the GET request to the Google Form
        st.markdown(f'<a href="{submission_url}" target="_self">Click Here to Finalize Submission and Check Queue</a>', unsafe_allow_html=True)
