import os
import google.generativeai as genai
import csv
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

def identify_money_column(headers):
    user_prompt = ", ".join(headers)
    response = model.generate_content(f"""
    Your task is to extract data that is money from the user's input and return it as a
    raw csv format. Go through all the column names and identify those that are related to money.
    Only answer with one word: name of the column
    
    User input: {user_prompt}
    """)
    
    # Extract the column name from the response
    column_name = response.text.strip()
    return column_name
