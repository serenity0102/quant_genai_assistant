# Data Analyst Assistant

Inspired by [Bridgewater associates' Investment Analysis](https://aws.amazon.com/tw/awstv/watch/5b319684c66/). This Streamlit-based application generates and executes Python code for various data analysis tasks using AWS Bedrock's Claude-3 LLM. 


## Description

This Data Analyst Assistant is an interactive web application that helps users generate and execute Python code for various data analysis tasks. It uses AWS Bedrock's Claude-3 model to generate code based on natural language queries and provides real-time code execution capabilities.

## Features

- Natural language to Python code generation
- Pre-defined templates for common financial analyses:
  - CPI (Consumer Price Index) analysis
  - HSI (Hang Seng Index) market data visualization
  - Sharpe ratio calculations
- Interactive code editing
- Real-time code execution

## Prerequisites

- Python 3.x
- AWS account with Bedrock access
- Required Python packages:
  ```
  streamlit
  boto3
  pandas
  numpy
  ```

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure AWS credentials with Bedrock access

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Enter your query in the text area
3. Click "Go" to generate and execute code
4. Edit generated code if needed
5. Click "Re-run Code" to execute edited code

## Example Queries

- "What's the Sharpe ratio of HSI in 2024?"
- "Plot a chart of CPI of China and US"
- "Plot HSI daily chart of 2024"
- "Create a bar chart of random data"
- "Generate a multiplication table"
- "Calculate fibonacci sequence"

## Project Structure

- `app.py`: Main application file
- `cpi.py`: Pre-defined code for CPI analysis
- `md.py`: Pre-defined code for market data analysis
- `hsi.2024.csv`: HSI market data file

## Class Structure

### BedrockAgent
- Handles communication with AWS Bedrock
- Manages code generation and execution
- Provides file reading capabilities
- Implements safety measures for code execution
