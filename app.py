import streamlit as st
import os
from prompts import policy_levers, max_num_queries
from utils import generate_document_contents, generate_stakeholders
import subprocess

# Set page configuration
st.set_page_config(
    page_title="Smart City Tool Kit",
    layout="wide"
)

# Title
st.title("Smart City Tool Kit - Indicators, Policy Levers and Diagnostic Report Generator")

# Navigation logic
if "page" not in st.session_state:
    st.session_state.page = "home"
if "stakeholders_list" not in st.session_state:
    st.session_state.stakeholders_list = []
if "generated_stakeholders" not in st.session_state:
    st.session_state.generated_stakeholders = ""
if "toc" not in st.session_state:
    st.session_state.toc = ""
if "modify_toc" not in st.session_state:
    st.session_state.modify_toc = True

# Main navigation buttons
st.subheader("Choose a Functionality:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Indicators", key="indicators"):
        st.session_state.page = "indicators"
        st.rerun()

with col2:
    if st.button("⚙️ Policy Levers", key="policy_levers"):
        st.session_state.page = "policy_levers"
        st.rerun()

with col3:
    if st.button("📋 Diagnostic Report Generator", key="diagnostic"):
        st.session_state.page = "diagnostic"
        st.rerun()



if st.session_state.page == "indicators":
    # Run the provided Streamlit indicator app
    st.switch_page("pages/indicators.py")

elif st.session_state.page == "policy_levers":
    st.subheader("⚙️ Policy Levers")
    st.write("The following are key policy levers for smart city development:")
    
    for lever in policy_levers:
        st.write(f"- {lever}")

elif st.session_state.page == "diagnostic":
    st.subheader("📋 Smart City Diagnostic Report Generation")

    # Inputs for Country, City
    country = st.text_input("🏳️ Enter Country:")
    city = st.text_input("🏙️ Enter City:")

    # Stakeholder selection
    st.subheader("Stakeholder Selection")
    stakeholder_option = st.radio("Would you like to provide stakeholders or generate them using AI?", 
                                  ("Provide stakeholders", "Generate using AI"))

    if stakeholder_option == "Provide stakeholders":
        stakeholders = st.text_area("Enter stakeholders (comma-separated)")
        if st.button("Get Stakeholders"):
            if stakeholders.strip():
                st.session_state.stakeholders_list = stakeholders.split(",")
                st.rerun()
    
    # Display manually entered stakeholders
    if st.session_state.stakeholders_list:
        st.subheader("✅ Provided Stakeholders")
        for stakeholder in st.session_state.stakeholders_list:
            st.write(f"- {stakeholder}")

    elif stakeholder_option == "Generate using AI":
        if st.button("Get Stakeholders"):
            with st.spinner("Generating the Stakeholders"):
                st.session_state.generated_stakeholders = generate_stakeholders(city=city, country=country)
            st.rerun()

    # Display AI-generated stakeholders
    if st.session_state.generated_stakeholders:
        st.subheader("✅ AI-Generated Stakeholders")
        st.markdown(st.session_state.generated_stakeholders)

    # Report Structure and Framework
    st.subheader("Report Structure and Framework")
    report_structure = st.text_area("Describe the structure and framework of the report:")

    

    # Generate Table of Contents
    if st.button("📑 Generate Table of Contents"):
        with st.spinner("Generating the Table of Contents for the Smart City Diagnostic Report"):
            st.session_state.toc = generate_document_contents(city=city, 
                                                              country=country, 
                                                              policy_levers=policy_levers, 
                                                              stakeholders=(", ".join(st.session_state.stakeholders_list) 
                                                                           if stakeholder_option == "Provide stakeholders" 
                                                                           else st.session_state.generated_stakeholders), 
                                                              report_structure=report_structure,
                                                              max_num_queries=max_num_queries)
            
        st.session_state.modify_toc = True
        st.rerun()
    
    # Display Table of Contents
    if st.session_state.toc:
        st.subheader("📌 Generated Table of Contents")
        st.markdown(st.session_state.toc)

        # User input for modifying contents
        modify = st.radio("Do you want to modify the contents?", 
                          ["No, proceed to report generation", "Yes, provide additional inputs"])

        if modify == "Yes, provide additional inputs":
            extra_inputs = st.text_area("Enter additional details or modifications:")
            
            # Button to regenerate Table of Contents
            if st.button("🔄 Update Table of Contents"):
                if extra_inputs:
                    with st.spinner("Generating the Table of Contents for the Smart City Diagnostic Report"):
                        st.session_state.toc = generate_document_contents(city=city, 
                                                                          country=country, 
                                                                          policy_levers=policy_levers, 
                                                                          stakeholders=(", ".join(st.session_state.stakeholders_list) 
                                                                           if stakeholder_option == "Provide stakeholders" 
                                                                           else st.session_state.generated_stakeholders), 
                                                                          report_structure=extra_inputs,
                                                                          max_num_queries=max_num_queries)
                    st.session_state.modify_toc = True
                    st.rerun()  # Refresh the UI to show the updated ToC


        elif modify == "No, proceed to report generation":
            st.session_state.modify_toc = False  # Stop cycling but retain the latest ToC

            # Final report generation button
            if st.button("🚀 Run Report Generation"):
                st.success("The report is being generated based on the provided inputs!")
