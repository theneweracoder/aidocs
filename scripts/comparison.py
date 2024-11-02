import os
import requests
import json
from document_loader import load_documents
# from embedding_generation import generate_embeddings

# Azure OpenAI API endpoint and key
endpoint = "https://gsm-ml-oai.openai.azure.com/openai/deployments/gpt-4o-2024-05-13/chat/completions?api-version=2023-03-15-preview"
api_key = "3ab6dae367bf4332a651399908f99d01"

# Headers for the Azure API request
headers = {
    "Content-Type": "application/json",
    "api-key": api_key,
}

# Function to call Azure OpenAI API with detailed prompt
def call_openai_api(doc1_section, doc2_section, section_name):
    prompt = f"""
    You are an expert document analyst specializing in comparing legal and professional documents. 
    Your task is to compare two sections from different documents and identify all differences, 
    including additions, deletions, modifications, formatting changes, and structural changes. 
    Follow the steps outlined below to ensure accuracy.

    Sections to Compare:
    Document 1 ({section_name}): {doc1_section}
    Document 2 ({section_name}): {doc2_section}

    Steps to Complete the Task:
    
    1. Identify Differences:
    - Additions: Identify any text present in Document 2 but not in Document 1. Highlight these additions clearly.
    - Deletions: Identify any text present in Document 1 but missing in Document 2. Highlight these deletions clearly.
    - Modifications: Identify any text that has been altered, specifying the changes from Document 1 to Document 2. Highlight these modifications clearly.
    - Formatting Changes: Note significant changes in formatting such as bold, italics, headings, or bullet points. Highlight these changes clearly.
    - Structural Changes: Identify changes in the structure, such as reordering of sections or paragraphs. Highlight these structural changes clearly.

    2. Provide a Detailed Comparison in JSON format:
    - List all identified differences with specific details.
    - For each type of difference (additions, deletions, modifications, formatting changes, structural changes), provide a separate section.
    - Ensure each difference includes its type, exact location (e.g., "Page 1, Paragraph 1"), and text comparison.
    
    Example JSON Format for Reporting Differences:
    {{
        "section_name": "{section_name}",
        "differences": {{
            "additions": [
                {{
                    "location": "Page 1, Line 1",
                    "document_2": "© 2022, General Motors Company - All rights reserved."
                }},
                {{
                    "location": "Page 1, Posted Date",
                    "document_2": "Posted Date: December 22, 2022"
                }}
            ],
            "deletions": [
                {{
                    "location": "Page 1, Line 1",
                    "document_1": "© 2020, General Motors Company - All rights reserved."
                }},
                {{
                    "location": "Page 1, Posted Date",
                    "document_1": "Posted Date: November 05, 2020"
                }}
            ],
            "modifications": [
                {{
                    "location": "Page 1, Paragraph 2",
                    "original_text": "Customer Specific Requirements",
                    "modified_text": "Customer Specific R equirements"
                }}
            ],
            "formatting_changes": [
                {{
                    "location": "Page 1, Paragraph 3",
                    "change": "Text changed from normal to bold"
                }}
            ],
            "structural_changes": [
                {{
                    "location": "Page 3",
                    "change": "Paragraph 3 moved under Paragraph 4"
                }}
            ]
        }}
    }}

    If no differences are found in a category, use an empty array for that category.
    """
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.5,
        "top_p": 1,
        "n": 1,
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Function to compare two documents and highlight differences
def compare_documents(doc1_path, doc2_path):
    # Load and split documents into comparable sections
    doc1_sections, doc2_sections = load_documents(doc1_path, doc2_path)

    differences = {}

    # Iterate over sections and compare
    for section in doc1_sections.keys():
        if section in doc2_sections:
            response = call_openai_api(doc1_sections[section], doc2_sections[section], section)
            
        # # Parse the JSON response from GPT if it's in JSON format
        # try:
        #     response_json = json.loads(response)  # Convert JSON string to a dictionary
        # except json.JSONDecodeError:
        #     print(f"Failed to parse JSON for section {section}")
        #     response_json = {"error": "Invalid JSON format returned from GPT"}

        # Add the response to differences if any exist
            differences[section] = {
                "pdf1": doc1_sections[section],
                "pdf2": doc2_sections[section],
                "difference": response  # Store the parsed JSON directly
            }

    # Return structured differences
    return differences

# Paths to the two PDF documents
doc1_path = os.getcwd()+"/scripts/2020.pdf"
doc2_path = os.getcwd()+"/scripts/2023.pdf"

# Run comparison
document_differences = compare_documents(doc1_path, doc2_path)

with open('document_differences.json', 'w', encoding="utf-8") as file:
    file.write(json.dumps(document_differences, indent=4, ensure_ascii=False))