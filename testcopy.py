
import streamlit as st
import pandas as pd
import openai
import os
import csv
# Set the API key for OpenAI (securely)
os.environ['OPENAI_API_KEY'] = "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"


def query_openai_with_csv_data(dataframe, user_query):
    # Initialize OpenAI client
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Create a summarized version of the data
    summary = dataframe.describe().to_markdown()  # Statistical summary

    # Construct prompt with reduced data and concise description
    prompt_suffix = "\nProvide the answer with a confidence ratio in a table format."
    # Construct prompt using a series of messages
    messages = [
        "### System Instructions\n"
        "You are an AI trained to analyze data and respond to user queries based strictly on the provided data. You should not use any external knowledge.\n\n"
        "### Response Guidelines\n"
        "Provide the answer with a confidence ratio in a table format. Interpret the data accurately and consider all relevant factors and avoid displaying duplicate reults.\n"
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
        simulated_confidence = "95%"  # Placeholder for demonstration
        full_response = f"{response_text}"
        return user_query, full_response
    except Exception as error:
        print("Error querying OpenAI:", error)
        return user_query, "Error in processing your query."



def append_query_result_to_csv(question, response):
    # CSV file to store query results
    file_path = 'query_results.csv'
    # Append to the CSV file, creating it if it doesn't exist
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            csv_writer.writerow(['Question', 'Response'])
        csv_writer.writerow([question, response])

st.set_page_config(layout='wide')
st.title("Cybersecurity Query Interface")

uploaded_csv = st.file_uploader("Upload your CSV for analysis", type=['csv'])

if uploaded_csv:
    column1, column2 = st.columns([1,1])

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
                query, answer = query_openai_with_csv_data(data, query_text)
                append_query_result_to_csv(query, answer)
                st.success(answer)
