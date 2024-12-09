import streamlit as st
import boto3
import json
import sys
from io import StringIO
import contextlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time

class BedrockAgent:
    def __init__(self):
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'
        )
    
    def read_file(self, filename):
        try:

            time.sleep(2) 
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def create_output_or_prompt(self, user_query):
        # Check if query is about CPI
        # this is an example to hard code pre-defined code
        if any(term in user_query.lower() for term in ['cpi', 'consumer price index', 'inflation']):
            return self.read_file('cpi.py')
        
        # Check if query is about sharpe ratio
        # This is an exmaple to specify the data source
        elif any(term in user_query.lower() for term in ['hsi', 'sharpe', 'sharpe ratio', 'return']):
            return f"""You have the market data in file hsi.2024.csv with column Date,Open,High,Low,Close,Adj Close,Volume.
                You can read HSI market data from file hsi.2024.csv.
                Generate Python code for the following requirement using Streamlit for any visualizations and calculations. 
                Important: Use st.pyplot() instead of plt.show() for matplotlib plots. 
                Only provide the code, no explanations, no beginning ```python and ending ```: {user_query}\n\nAssistant:
                """
        
        # For other queries, use LLM handle it
        else:
            return f"""Generate Python code for the following requirement using Streamlit for any visualizations. 
                Important: Use st.pyplot() instead of plt.show() for matplotlib plots. 
                Only provide the code, no explanations, no beginning ```python and ending ```: {user_query}\n\nAssistant:
                """
               

    def get_response(self, prompt, model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=1000):
        # If prompt is direct file content, return it without LLM processing
        if prompt.startswith('Error reading file:') or prompt.startswith('import streamlit'):
            return prompt
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": f"\n\nHuman: {prompt}\n\nAssistant:",
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9,
        })
        
        try:
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=body
            )
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
        except Exception as e:
            return f"Error getting response from Bedrock: {str(e)}"


    def execute_code_safely(self, code):
        # Create string buffer to capture output
        output_buffer = StringIO()

        try:
            # Redirect stdout to our buffer
            with contextlib.redirect_stdout(output_buffer):
                exec(code)
            return output_buffer.getvalue(), None
        except Exception as e:
            return None, str(e)

# Streamlit UI
st.title("Data Analyst Assistant")

# Initialize agent
agent = BedrockAgent()

# Initialize session state for storing generated code
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""

# User input
user_query = st.text_area("What would you like to research?", height=100, placeholder="Such as CPI, HSI market data, or any other financial questions")

if st.button("Go"):
    if user_query:
        with st.spinner("Generating code..."):
            # Get prompt and generate response
            prompt = agent.create_output_or_prompt(user_query)
            st.session_state.generated_code = agent.get_response(prompt)
            
            # Display generated code
            # st.code(st.session_state.generated_code, language='python')
            
            # Execute code
            with st.spinner("Executing code..."):
                output, error = agent.execute_code_safely(st.session_state.generated_code)
                
                if error:
                    st.error(f"Error during execution: {error}")
                else:
                    st.success("Code executed successfully!")
                    if output:
                        st.text("Output:")
                        st.text(output)

# Editable code area
if st.session_state.generated_code:
    st.markdown("### Edit Code")
    edited_code = st.text_area("Edit generated code:", 
                              value=st.session_state.generated_code,
                              height=300,
                              key="code_editor")
    
    # Re-run button for edited code
    if st.button("Re-run Code"):
        with st.spinner("Executing edited code..."):
            output, error = agent.execute_code_safely(edited_code)
            
            if error:
                st.error(f"Error during execution: {error}")
            else:
                st.success("Code executed successfully!")
                if output:
                    st.text("Output:")
                    st.text(output)


# Add sidebar with examples
with st.sidebar:
    st.header("Example Queries")
    st.markdown("""
    - What’s the Sharpe ratio of HSI in 2024?
    - Plot a chart of CPI of China and US 
    - Plot HSI daily chart of 2024
    - Create a bar chart of random data
    - Generate a multiplication table
    - Calculate fibonacci sequence
    """)
