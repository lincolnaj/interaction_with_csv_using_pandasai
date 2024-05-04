import streamlit as st
import pandas as pd
import openai
import os
import csv

# Set the API key for OpenAI (securely)
os.environ['OPENAI_API_KEY'] = ''

# Initialize variables for statistics
response_lengths = []
query_success_count = 0
total_queries = 0
total_response_time = 0
error_count = 0


def query_openai_with_csv_data(dataframe, user_query, prompt):
    # Initialize OpenAI client
    openai.api_key = os.environ['OPENAI_API_KEY']
    messages = [{"role": "user", "content": prompt}]

    # Assemble the data context by summarizing the DataFrame columns
    data_context = ""
    for col in dataframe.columns:
        col_values = map(str, dataframe[col].unique())
        data_context += f"{col}: {', '.join(col_values)}\n"

    # Query OpenAI with the constructed prompt
    try:
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            # prompt=f"{data_context}\n\n{user_query}",
            max_tokens=150,
            messages=messages,
            temperature=0
        )
        response_text = completion.choices[0].message["content"]
        return user_query, response_text
    except Exception as error:
        print("Error querying OpenAI:", error)
        return user_query, "Error in processing your query."


# def get_completion(prompt, model="gpt-3.5-turbo-instruct"):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0,
#     )
#     return response.choices[0].message["content"]
#
# text = ""
# prompt = f"""summarise the text delimited by triple backticks into 10 words```{text}```"""
#
# response = get_completion(prompt)
# print(response)


# results being appended into csv
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
    column1, column2 = st.columns([1, 1])

    with column1:
        st.info("File uploaded successfully.")
        data = pd.read_csv(uploaded_csv)
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
