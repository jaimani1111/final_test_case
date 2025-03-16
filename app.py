# app.py
import streamlit as st
from docx import Document
from test_case_generator import generate_test_cases
from file_formatters import format_test_cases_for_txt, format_test_cases_for_docx, format_test_cases_for_excel
from io import BytesIO
import pandas as pd

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>XC AI Test Case Generator</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Configuration")
    insurance_type = st.selectbox("Insurance Type", ["Auto", "Health", "Home", "Life"])
    region = st.selectbox("Region", ["North America", "Europe", "Asia Pacific", "ANZ"])
    line_of_business = st.selectbox("Line of Business", ["Retail", "Commercial", "Enterprise"])
    
    st.subheader("Acceptance Criteria")
    
    # Initialize session state for file uploader and manual input
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'manual_input_used' not in st.session_state:
        st.session_state.manual_input_used = False
    
    # File uploader
    criteria_file = st.file_uploader("Upload File (txt/csv/docx)", type=["txt", "csv", "docx"], 
                                    disabled=st.session_state.manual_input_used)
    
    # If a file is uploaded, disable manual input
    if criteria_file:
        st.session_state.file_uploaded = True
        st.session_state.manual_input_used = True
    else:
        st.session_state.file_uploaded = False
    
    # Manual input text area
    manual_input = st.text_area("Or enter requirements manually", height=150, 
                               disabled=st.session_state.file_uploaded)
    
    # If manual input is used, disable file uploader
    if manual_input:
        st.session_state.manual_input_used = True
    else:
        st.session_state.manual_input_used = False
    
    # Extract text from file or use manual input
    def extract_text(file):
        if not file: return ""
        try:
            if file.type == "text/plain":
                return file.getvalue().decode()
            elif file.type == "text/csv":
                return pd.read_csv(file).to_string()
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return "\n".join([p.text for p in Document(file).paragraphs])
        except Exception as e:
            st.error(f"File error: {e}")
            return ""
    
    requirements = extract_text(criteria_file) or manual_input

    # Add input for number of test cases
    num_test_cases = st.number_input("Number of Test Cases", min_value=1, max_value=20, value=5)

# Main interface
if st.button("✨ Generate Test Cases"):
    if not requirements:
        st.warning("Please input requirements first!")
    else:
        try:
            with st.spinner("Generating test cases..."):
                generated = generate_test_cases(insurance_type, region, line_of_business, requirements, num_test_cases)
                st.session_state.test_cases = generated
                st.success(f"Generated {len(generated)} test cases!")
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")

st.divider()

# Display results with debugging
if 'test_cases' in st.session_state:
    st.subheader("Generated Test Cases")
    
    # Debug view
    with st.expander("Debug Raw Response"):
        st.code(st.session_state.raw_response)
    
    # Main table display
    if st.session_state.test_cases:
        df = pd.DataFrame(st.session_state.test_cases)
        
        # Remove LOB and Region columns
        df_display = df.drop(columns=["LOB", "Region"])
        
        # Format steps with line breaks
        df_display['Execution Steps'] = df_display['Execution Steps'].str.replace(r'(Step\d+:)', r'\n\1', regex=True)
        
        # Fix: Use raw string for the HTML replacement
        html_table = df_display.to_html(index=False, escape=False)
        html_table = html_table.replace(r'\n', '<br>')
        
        st.markdown(f"""
        <div style='overflow-x: auto; margin: 20px 0;'>
            {html_table}
        </div>
        """, unsafe_allow_html=True)
        
        # Excel export (without LOB and Region)
        excel_buffer = BytesIO()
        excel_content = format_test_cases_for_excel(st.session_state.test_cases)
        st.download_button(
            "📥 Download Excel",
            excel_content,
            "test_cases.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # TXT export (without LOB and Region)
        txt_content = format_test_cases_for_txt(st.session_state.test_cases)
        st.download_button(
            "📥 Download as TXT",
            txt_content,
            "test_cases.txt",
            "text/plain"
        )
        
        # Word (DOCX) export (without LOB and Region)
        doc = format_test_cases_for_docx(st.session_state.test_cases)
        doc_buffer = BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        st.download_button(
            "📥 Download as Word (DOCX)",
            doc_buffer.getvalue(),
            "test_cases.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.warning("No valid test cases could be parsed from the response")

elif 'test_cases' not in st.session_state:
    st.info("Click 'Generate Test Cases' to begin")