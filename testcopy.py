import streamlit as st
import pandas as pd
import openai
import os
import csv

# Set the API key for OpenAI (securely)
os.environ['OPENAI_API_KEY'] = 

def query_openai_with_csv_data(dataframe, user_query):
    # Initialize OpenAI client
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Create a summarized version of the data
    summary = dataframe.describe().to_markdown()  # Statistical summary

    # Construct prompt with reduced data and concise description
    prompt_suffix = "\nProvide the answer with a confidence ratio in a table format from the csv."

    # Construct prompt using a series of messages
    messages = [
        "### System Instructions\n"
        "You are a csv analyzing expert, an AI trained to analyze data and respond to user queries based strictly on the provided data as csv and don't go beyond that. You should not use any external knowledge.\n\n"
        "### Response Guidelines\n"
        "Look for keywords in the query and then search in the csv.\n"
        "Find column which will match a keyword in the query\n"
        "in the query if common between two columns are mentioned, inner join the 2 columns and then find the output.\n"
        "Answer row by row\n"
        "DO not display duplicate outputs\n"
        "Do not modify anything in the CSV",
        f"Data Summary:\n{summary}",
        f"User Query:\n{user_query}{prompt_suffix}"
    ]
    prompt = "\n\n".join(messages)  # Combine messages into a single string with new lines

    try:
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=250,
            temperature=0.5
        )
        response_text = completion.choices[0].text.strip()
        return response_text
    except Exception as error:
        print("Error querying OpenAI:", error)
        return "Error in processing your query."

def parse_table_response(response):
    lines = response.split('\n')
    headers = [header.strip() for header in lines[0].split('|') if header.strip()]
    data = [[item.strip() for item in line.split('|') if item.strip()] for line in lines[2:] if line]
    return headers, data

def beautify_and_save_to_csv(headers, data):
    # Create a DataFrame for better formatting
    df = pd.DataFrame(data, columns=headers)
    
    # CSV file to store query results
    file_path = 'query_results.csv'
    
    # Write to the CSV file, creating it if it doesn't exist
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

st.set_page_config(layout='wide')
st.title("Cybersecurity Query Interface")

uploaded_csv = st.file_uploader("Upload your CSV for analysis", type=['csv'])

if uploaded_csv:
    column1, column2 = st.columns([1, 1])

    with column1:
        st.info("File uploaded successfully.")
        data = pd.read_csv(uploaded_csv, encoding="latin1")
        st.dataframe(data, height=300)

    with column2:
        st.info("Enter your query below:")
        query_text = st.text_area("Query")
        if query_text:
            if st.button("Submit Query"):
                st.info("Processing your query...")
                answer = query_openai_with_csv_data(data, query_text)
                headers, data = parse_table_response(answer)
                beautify_and_save_to_csv(headers, data)
                st.success(answer)