# response_parser.py
import re

import streamlit as st
def clean_ai_response(response):
    """Improved parser to handle variable numbers of execution steps"""
    test_cases = []
    
    # Split into test case blocks using numbered headers
    case_blocks = re.split(r'\n\*\*Test Case \d+:', response)
    
    for block in case_blocks[1:]:  # Skip first empty split
        current_case = {
            "Sl No.": "",
            "Requirement ID": "",
            "Test Case ID": "",
            "Module": "",
            "LOB": "",
            "Region": "",
            "Test Case Description": "",
            "Execution Steps": "",
            "Expected Result": ""
        }
        
        # Extract fields using regex
        sl_no_match = re.search(r'Sl No\.:\s*(\d+)', block)
        if sl_no_match:
            current_case["Sl No."] = sl_no_match.group(1).strip()
        
        req_id_match = re.search(r'Requirement ID:\s*([^\n]+)', block)
        if req_id_match:
            current_case["Requirement ID"] = req_id_match.group(1).strip()
        
        tc_id_match = re.search(r'Test Case ID:\s*([^\n]+)', block)
        if tc_id_match:
            current_case["Test Case ID"] = tc_id_match.group(1).strip()
        
        module_match = re.search(r'Module:\s*([^\n]+)', block)
        if module_match:
            current_case["Module"] = module_match.group(1).strip()
        
        lob_match = re.search(r'LOB:\s*([^\n]+)', block)
        if lob_match:
            current_case["LOB"] = lob_match.group(1).strip()
        
        region_match = re.search(r'Region:\s*([^\n]+)', block)
        if region_match:
            current_case["Region"] = region_match.group(1).strip()
        
        desc_match = re.search(r'Test Case Description:\s*([^\n]+)', block)
        if desc_match:
            current_case["Test Case Description"] = desc_match.group(1).strip()
        
        # Extract execution steps dynamically
        steps_match = re.search(r'Execution Steps:\s*(.*?)(?=\nExpected Result:)', block, re.DOTALL)
        if steps_match:
            steps = steps_match.group(1).strip()
            # Ensure each step is on a new line with a gap line between steps
            steps = re.sub(r'Step(\d+):', r'\nStep\1:', steps)  # Add newline before each step
            steps = steps.replace('\n', '\n\n')  # Add an extra newline to create a gap
            steps = steps.strip()  # Remove leading/trailing whitespace
            current_case["Execution Steps"] = steps
        
        # Extract expected result
        result_match = re.search(r'Expected Result:\s*(.*)', block, re.DOTALL)
        if result_match:
            current_case["Expected Result"] = result_match.group(1).strip()
        
        # Add only if all required fields are present
        if all(current_case.values()):
            test_cases.append(current_case)
        else:
            # Debugging: Print the block that failed to parse
            st.warning(f"Failed to parse block: {block}")
    
    return test_cases