import streamlit as st
import pandas as pd
import openai
import os
import csv
import keyword

# Set the API key for OpenAI (securely)
os.environ['OPENAI_API_KEY'] = 

def query_openai_with_csv_data(dataframe, user_query):
    # Initialize OpenAI client
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Define the provided prompt
    prompt = """
    Read the dataset containing TTP (Tactics, Techniques, and Procedures) information from dataset.csv. Each row should contain the following fields: 
    - Date
    - Source
    - Link
    - Actor
    - Tactic ID
    - Tactic Name
    - Technique ID
    - Technique
    - Sub-technique ID
    - Sub-Technique Name
    - Target

    Your tasks:
    1. Answer the query in a clear and concise manner. Avoid big block of text.
    2. Limit the response to 200 words or 4 sentences or present the result in tabular format if possible.
    3. Ensure the response is relevant to the provided query.
    4. The result of the query must not go outside of the data provided in the Dataset.csv. Avoid model hallucination.
    5. The result of the query must not change for the same question.
    6. Use examples to illustrate the query result.

    Examples:
    - Query: What is the most common Tactic?
    Response: The most common tactic is Initial Access, which appeared 17 times. Show in table format.
    
    - Query: What is the most common Technique?
    Response: The most common technique is Valid Accounts, which appeared 15 times.Show in table format.
    
    - Query: What is the rarest Tactic?
    Response: The rarest tactic is Collection and Lateral Movement, which appeared 3 times. Show in table format.
    """

    # Query OpenAI with the constructed prompt
    try:
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt + f"\n\n{user_query}",
            max_tokens=150
        )
        response_text = completion.choices[0].text.strip()
        return user_query, response_text
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

def query_data_and_provide_result(dataframe, user_query):
    # Check if user query contains Python keywords or invalid identifiers
    if any(keyword.iskeyword(word) for word in user_query.split()):
        return None

    # Query the DataFrame based on sanitized user input
    try:
        # Limit the query scope to the dataset columns
        result_df = dataframe.query(user_query)
        if not result_df.empty:
            # Validate the query result to ensure it's within the dataset
            if result_df.columns.tolist() == dataframe.columns.tolist():
                return result_df
            else:
                return None
        else:
            return None
    except Exception as e:
        print("Error querying data:", e)
        return None


st.set_page_config(layout='wide')
st.title("Cybersecurity Query Interface")

uploaded_csv = st.file_uploader("Upload your CSV for analysis", type=['csv'])

if uploaded_csv:
    column1, column2 = st.columns([1,1])

    with column1:
        st.info("File uploaded successfully.")
        data = pd.read_csv(uploaded_csv, encoding='latin1')
        st.dataframe(data, height=300)

    with column2:
        st.info("Enter your query below:")
        query_text = st.text_area("Query")
        if query_text:
            if st.button("Submit Query"):
                st.info("Processing your query...")
                result_df = query_data_and_provide_result(data, query_text)
                if result_df is not None:
                    st.success("Query Result:")
                    st.table(result_df)
                else:
                    query, answer = query_openai_with_csv_data(data, query_text)
                    append_query_result_to_csv(query, answer)
                    st.success(answer[:200])  # Limiting the response to 200 words