# test_case_generator.py
from groq import Groq
from config import GROQ_API_KEY
from database import initialize_vector_db
from response_parser import clean_ai_response
import streamlit as st

groq_client = Groq(api_key=GROQ_API_KEY)
vector_db = initialize_vector_db()

def generate_test_cases(insurance_type, region, line_of_business, user_requirements, num_test_cases):
    """Generate test cases with variable execution steps"""
    query = f"{insurance_type} {region} {line_of_business} {user_requirements}"
    
    # Print the query used for similarity search
    print(f"Query for similarity search: {query}")
    
    # Perform similarity search
    similar_cases = vector_db.similarity_search(query, k=4)
    
    # Print the similar cases retrieved
    print("Similar cases retrieved from vector database:")
    for i, case in enumerate(similar_cases, 1):
        print(f"Case {i}:\n{case.page_content}\n{'-' * 50}")
    
    # Construct context from similar cases
    context = "\n".join([case.page_content for case in similar_cases])
    
    # Print the context used for generating new test cases
    print("Context constructed from similar cases:")
    print(context)
    
    # Construct the prompt
    prompt = f"""As an Insurance QA Expert, create {num_test_cases} test cases. Generated test cases should be based on the specific line of business and region. Please make sure the generated test cases are very high in quality and detail with this structure:

**Test Case X: [Scenario]**

Sl No.: [number]
Requirement ID: [REQ-XXX]
Test Case ID: [TC-XXX]
Module: [Specific Module]
LOB: {line_of_business}
Region: {region}
Test Case Description: [Clear description]
Execution Steps:
Step1: [Action]
Step2: [Action]
... (Add as many steps as needed for the test case)
Expected Result: [Measurable outcome]

Avoid these examples but take inspiration from them only: {context}"""
    
    # Print the prompt sent to the Groq API
    print("Prompt sent to Groq API:")
    print(prompt)
    
    # Send the prompt to Groq API
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
    )
    
    raw_content = response.choices[0].message.content
    st.session_state.raw_response = raw_content  # Store for debugging
    return clean_ai_response(raw_content)