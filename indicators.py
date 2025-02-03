import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import concurrent.futures
from search import read_indicators_file, search_func, format_maturity_levels, create_spider_chart, fetch_indicators_from_web, fetch_indicator, check_for_data

# Streamlit UI

## Title
st.title("Smart City Indicators")
with st.expander("Click to expand and view the details of this application"):
    st.markdown(""" 
    This **Smart City Indicators** app is designed to help urban planners, policymakers, and researchers evaluate the maturity of various smart city indicators for one or more cities. By leveraging Perplexity AI and GPT-4o, the app gathers relevant data and computes a maturity score for each indicator using a predefined smart city maturity model. The app also provides a clear explanation of the results with references to data sources and visual representations, making it a powerful tool for assessing and comparing the technological and infrastructural advancement of cities.

    The app includes the following features:
    - **Indicator Selection**: Users can select specific indicators to evaluate, allowing for customized analysis based on their goals.
    - **Maturity Scoring**: Each indicator is scored based on its development stage, providing a clear picture of where a city stands in its smart city journey.
    - **Visualization**: Results are visually represented using radar graphs to offer a comparative overview.
    """)

# Initialize session state for city inputs
if "city_inputs" not in st.session_state:
    st.session_state.city_inputs = [1]  # Start with one input field

if "add_city_clicks" not in st.session_state:
    st.session_state.add_city_clicks = 1

if "indicator_bool" not in st.session_state:
    st.session_state.indicator_bool = False

if "indicator_option" not in st.session_state:
    st.session_state["indicator_option"] = "Top 5 Indicators"

if "radar_data" not in st.session_state:
    st.session_state["radar_data"] = {}

if "combined_outputs" not in st.session_state:
    st.session_state["combined_outputs"] = ""

if "final_indicator_list" not in st.session_state:
    st.session_state.final_indicator_list = []

if "total_indicators" not in st.session_state:
    st.session_state.total_indicators = ""

if "top_filtered_df" not in st.session_state:
    st.session_state.top_filtered_df = None

if "top_indicators_df" not in st.session_state:
    st.session_state.top_indicators_df = None


# Function to add a new city input field
def add_city_input():
    st.session_state.add_city_clicks += 1
    if len(st.session_state.city_inputs) < 5:
        st.session_state.city_inputs.append(len(st.session_state.city_inputs) + 1)

# Function to remove a city input field
def remove_city_input():
    st.session_state.add_city_clicks = st.session_state.city_inputs[-1] - 1
    if len(st.session_state.city_inputs) > 1:
        st.session_state.city_inputs.pop()

def remove_duplicates(input_list):
    unique_items = []
    for item in input_list:
        if item and item not in unique_items:
            unique_items.append(item)
    return unique_items


# Dynamic city input fields
st.subheader("Enter City Names")
with st.expander("Click to expand and view the details of this section"):
    st.markdown(""" 
    **Purpose**:  
    This section allows users to input the names of cities they wish to analyze.  
                
    **How to Use**:  
    - Enter the name of a city in the input field. 
    - Click **Add City** if you want to add multiple cities.
    - Maximum 5 cities can be added for comparison.
    - If you wish to remove a city, click the **Remove City** button next to its name.
    """)
for i in range(len(st.session_state.city_inputs)):
    st.text_input(f"City {i+1}:", key=f"city_{i+1}")


# Add and Remove buttons for dynamic fields
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Add City", on_click=add_city_input):
        if st.session_state.add_city_clicks > 5:
            st.warning("Only 5 cities allowed.")

with col2:
    if st.button("Remove City", on_click=remove_city_input):
        pass


# Get the list of cities
city_list = [st.session_state[f"city_{i+1}"] for i in range(len(st.session_state.city_inputs))]
# city_list = list(set(city for city in city_list if city))  # Remove empty fields
st.session_state.city_list = remove_duplicates(city_list)

# Horizontal line
st.markdown("---")

# Output the Indictor Data
st.subheader("Generate the list of Indicators")
with st.expander("Click to expand and view the details of this section"):
    st.markdown(""" 
    **Purpose**:  
    This section allows users to choose a category and generate indicators for that category using gpt-4o model. This sections generates upto 20 indicators for the category and lists those indicators that have data for the first city.
                
    **How to Use**:  
    - Choose a category from the dropdown.
    - Select **Type custom category** to give a custom category not present in the dropdown.
    - Click on **Get Indicators** button to generate the list of indicators.
    """)

# Get the list of indicators and their categories
combined_df = read_indicators_file()

# Initialize a placeholder for dynamic input box
input_placeholder = st.empty()

# Checkbox to dynamically fetch indicators from the web
custom_category_select = st.checkbox("Type custom category")

# col_indicators_1, col_indicators_2= st.columns([4, 2])

# with col_indicators_1:
    # Unified input for "Category" (either text input or dropdown)
if custom_category_select:
    selected_category = input_placeholder.text_input("Category (type the custom category):")
else:
    selected_category = input_placeholder.selectbox("Category (select the category from dropdown):", combined_df["Category"].unique(), index=None)


# with col_indicators_2:
#     # Create a radio button toggle
#     option = st.radio(
#         "Choose to display Top 5 or Bottom 5 or custom indicators:",
#         ("Top 5 Indicators", "Bottom 5 Indicators", "Select Indicators")
#     )
#     st.session_state["indicator_option"] = option

# with col_indicators_2:
    # Add space to align the button to the bottom
    # st.markdown("<div style='height: 1.9em;'></div>", unsafe_allow_html=True) 
indicator_button_clicked = st.button("Get Indicators")



# Fetch indicators based on the selected/typed category
if selected_category and indicator_button_clicked:
    st.session_state.indicator_bool = True
    with st.spinner("Generating the Indicator List"):
        indicator_list, maturity_levels_list = fetch_indicators_from_web(category=selected_category)
        filtered_df = pd.DataFrame({
            'Indicator': indicator_list,
            'Category': [selected_category] * len(indicator_list),
            'Maturity Assessment (1-5)': maturity_levels_list
        })

        top_filtered_df = check_for_data(filtered_df, st.session_state.city_list[0])
        st.session_state.top_filtered_df = top_filtered_df
        st.session_state.total_indicators = "\n\n".join([indicator for indicator in st.session_state.top_filtered_df["Indicator"]])

if st.session_state.total_indicators:
    st.subheader("Indicators:")
    st.markdown(st.session_state.total_indicators)


# Horizontal line
st.markdown("---")
# Output the Indictor Data
st.subheader("Data on the Indicators")
with st.expander("Click to expand and view the details of this section"):
    st.markdown(""" 
    **Purpose**:  
    Presents the gathered data and maturity scores for each indicator, along with detailed explanations.  
                
    **How to Use**:  
    - Choose the **Top 5 Indicators** for indicators with highest maturity scores.
    - Choose the **Bottom 5 Indicators** for indicators with lowest maturity scores.
    - Choose the **Select Indicators** to select multiple indicators of your choice. Use **Select All** from the dropdown to select all the indicators.
    - Click on **Generate Data** to generate the data for the selected indicators.
    - Use the provided sources to validate the data or gather more context.
    """)

if st.session_state.top_filtered_df is not None and isinstance(st.session_state.top_filtered_df, pd.DataFrame):
    # Create a radio button toggle
    option = st.radio(
        "Choose to display Top 5 or Bottom 5 or custom indicators:",
        ("Top 5 Indicators", "Bottom 5 Indicators", "Select Indicators")
    )
    st.session_state["indicator_option"] = option

    if st.session_state["indicator_option"] == "Top 5 Indicators":
        top_indicators_df = st.session_state.top_filtered_df.sort_values(by='Maturity Score', ascending=False).head(5)
        # st.session_state.final_indicator_list = list(top_indicators_df["Indicator"])
    elif st.session_state["indicator_option"] == "Bottom 5 Indicators":
        top_indicators_df = st.session_state.top_filtered_df.sort_values(by='Maturity Score', ascending=True).head(5)
        # st.session_state.final_indicator_list = list(top_indicators_df["Indicator"])
    else: 
        # Add "Select All" option at the beginning of the list
        select_all_option = "Select All"
        options_with_select_all = [select_all_option] + list(st.session_state.top_filtered_df["Indicator"])
        selected_indicators = st.multiselect("Select one or more indicators:", 
                                              options_with_select_all)
        
        if select_all_option in selected_indicators:
            top_indicators_df = st.session_state.top_filtered_df
        elif selected_indicators:
            # st.session_state.final_indicator_list = selected_indicators
            top_indicators_df = st.session_state.top_filtered_df[st.session_state.top_filtered_df["Indicator"].isin(selected_indicators)]
        else:
            # st.session_state.final_indicator_list = list(st.session_state.top_filtered_df["Indicator"])[:5]
            top_indicators_df = st.session_state.top_filtered_df.head(5)
            st.warning(f"Please select one or more indicators.")
        

    # st.session_state.city0_outputs = list(top_indicators_df["Perplexity Output"])
    # st.session_state.city0_maturity_scores = list(top_indicators_df["Maturity Score"])
    st.session_state.top_indicators_df = top_indicators_df


if st.button("Generate Data"): 
    if st.session_state.city_list and selected_category and st.session_state.indicator_bool:
        with st.spinner(f"Generating Indicator data for city/cities: {', '.join(st.session_state.city_list)}, please wait..."):
            st.session_state.combined_outputs = ""
            st.session_state.radar_data = {}

            st.session_state.combined_outputs += f"# {st.session_state.city_list[0]}: \n\n"
            
            for index, row in st.session_state.top_indicators_df.iterrows():
                st.session_state.combined_outputs += f"""## {row["Indicator"]}: \n\n ### Maturity Score: {row["Maturity Score"]} \n\n ### Output Text: \n\n {row["Perplexity Output"]}\n\n\n\n"""

            # for j, indicator in enumerate(st.session_state.final_indicator_list):
            #     st.session_state.combined_outputs += f"## {indicator}: \n\n ### Maturity Score: {st.session_state.city0_maturity_scores[j]} \n\n ### Output Text: \n\n {st.session_state.city0_outputs[j]}\n\n\n\n"

            st.session_state.radar_data[st.session_state.city_list[0]] = list(st.session_state.top_indicators_df["Maturity Score"])

            if len(st.session_state.city_list) > 1:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Parallelize over cities
                    futures = [executor.submit(search_func, city=city, indicators=list(st.session_state.top_indicators_df["Indicator"])) for city in st.session_state.city_list[1:]]
                    results = [f.result() for f in futures]

                # Process results for each city
                
                for i, city in enumerate(st.session_state.city_list[1:]):
                    perplexity_results, citations, indicator_values, maturity_scores = results[i]
                    st.session_state.combined_outputs += f"\n\n---\n\n # {city}: \n\n"
                    for j, indicator in enumerate(list(st.session_state.top_indicators_df["Indicator"])):
                        st.session_state.combined_outputs += f"## {indicator}: \n\n ### Maturity Score: {maturity_scores[j]} \n\n ### Output Text: \n\n {perplexity_results[j]}\n\n\n\n"

                    st.session_state.radar_data[city] = maturity_scores

        
            # combined_results += "\n\n---\n\n"

            # Render the Markdown content
        #     st.markdown(combined_results)
        # st.success("Successfully generated the Data for the Indicators for each City!")
    else:
        st.warning("Please enter at least one city, select a category and generate the indicators.")

# Show the list of final indicators
if st.session_state.combined_outputs:
    st.markdown(st.session_state.combined_outputs)
    st.success("Successfully generated the Data for the Indicators for each City!")


# Horizontal line
st.markdown("---")

# Generate the Radar Graph
st.subheader("Generate Radar Graph")
with st.expander("Click to expand and view the details of this section"):
    st.markdown(""" 
    **Purpose**:  
    Creates a radar graph to visualize and compare the maturity of different indicators for one or more cities.  
                
    **How to Use**:  
    - Click on "Generate Radar Graph" to display the graph.
    - Analyze the graph to compare the performance of different indicators or cities.
    """)
if st.button("Radar Graph"): 
    if st.session_state.radar_data:
        # Create a spider chart for the indicators
        create_spider_chart(
            indicators=list(st.session_state.top_indicators_df["Indicator"]),
            values_dict=st.session_state.radar_data,
            title=f"Comparative Radar Chart for {selected_category} for cities: {', '.join(st.session_state.city_list)}",
        )
    else:
        st.warning("First Get the Radar Data")

