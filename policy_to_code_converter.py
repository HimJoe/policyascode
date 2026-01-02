"""
Policy-to-Code Converter
Standalone application for converting policy documents to executable Python code

This app allows clients to:
1. Upload policy documents (PDF, Text, Excel)
2. View extracted rules
3. Download generated Python code
4. Export rules as JSON

Version: 1.0.1 - Fixed file type handling for PDF/Excel/Text
"""

import streamlit as st
import asyncio
from datetime import datetime
import json
import zipfile
import io
from pathlib import Path

# Import core components
from grc_agent_system import GRCMultiAgentSystem
from document_processor import DocumentProcessorFactory

# Page configuration
st.set_page_config(
    page_title="Policy-to-Code Converter",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stDownloadButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = GRCMultiAgentSystem()
if 'rules_generated' not in st.session_state:
    st.session_state.rules_generated = False
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None
if 'rules_json' not in st.session_state:
    st.session_state.rules_json = None
if 'policy_name' not in st.session_state:
    st.session_state.policy_name = None

# Header
st.markdown('<div class="main-header">📜 Policy-to-Code Converter</div>', unsafe_allow_html=True)
st.caption("Version 1.0.1 - Updated file handling")
st.markdown("""
<div class="info-box">
<strong>Welcome!</strong> Upload your policy documents and get executable Python code instantly.
<br>Supported formats: PDF, Text (.txt), Excel (.xlsx, .xls)
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar - Instructions
with st.sidebar:
    st.header("📖 How to Use")
    st.markdown("""
    ### Step-by-Step Guide

    1. **Upload Policy**
       - Click "Browse files"
       - Select your policy document
       - Supported: PDF, TXT, XLSX

    2. **Review Rules**
       - See extracted policy rules
       - Check rule categories
       - Verify compliance levels

    3. **Download Code**
       - Get Python validation code
       - Download JSON rules
       - Get complete package (ZIP)

    4. **Integration**
       - Use generated code in your app
       - Import and run validations
       - Check documentation
    """)

    st.markdown("---")

    st.header("💡 Tips")
    st.info("""
    - Clear, structured policies work best
    - Include compliance keywords (must, shall, required)
    - Specify data types and thresholds
    - Use numbered sections
    """)

    st.markdown("---")

    st.header("📊 Statistics")
    if st.session_state.rules_generated:
        system = st.session_state.system
        total_rules = len(system.governance_enforcer.policy_parser.parsed_rules)
        st.metric("Total Rules Extracted", total_rules)

        # Count by category
        categories = {}
        for rule in system.governance_enforcer.policy_parser.parsed_rules:
            cat = rule.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1

        for cat, count in categories.items():
            st.metric(f"{cat} Rules", count)

# Main content area
tab1, tab2, tab3 = st.tabs(["📤 Upload Policy", "🔍 View Rules", "💾 Download Code"])

with tab1:
    st.header("Upload Your Policy Document")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose a policy document",
            type=['txt', 'pdf', 'xlsx', 'xls'],
            help="Upload your policy document in PDF, Text, or Excel format"
        )

    with col2:
        st.markdown("### File Info")
        if uploaded_file is not None:
            st.success(f"**Name:** {uploaded_file.name}")
            st.info(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
            st.info(f"**Type:** {uploaded_file.type}")

    if uploaded_file is not None:
        st.markdown("---")

        if st.button("🚀 Process Policy Document", type="primary", use_container_width=True):
            with st.spinner("Processing your policy document... This may take a moment."):
                try:
                    # Read file content
                    file_bytes = uploaded_file.read()

                    # Determine file type and prepare content
                    file_extension = Path(uploaded_file.name).suffix.lower()
                    if file_extension == '.pdf':
                        file_type = 'pdf'
                        content = file_bytes  # Keep as bytes for PDF
                    elif file_extension in ['.xlsx', '.xls']:
                        file_type = 'excel'
                        content = file_bytes  # Keep as bytes for Excel
                    else:
                        file_type = 'text'
                        # Decode text files to string
                        try:
                            content = file_bytes.decode('utf-8')
                        except UnicodeDecodeError:
                            # Try with different encoding
                            content = file_bytes.decode('latin-1')

                    # Process the policy
                    async def process_policy():
                        return await st.session_state.system.upload_policy(
                            content=content,
                            filename=uploaded_file.name,
                            file_type=file_type
                        )

                    result = asyncio.run(process_policy())

                    # Store policy name
                    st.session_state.policy_name = uploaded_file.name.replace('.', '_').replace(' ', '_')

                    # Generate code using the correct methods
                    python_code = st.session_state.system.export_rules_python()
                    json_rules_dict = st.session_state.system.export_rules_json()
                    json_rules = json.dumps(json_rules_dict, indent=2)

                    st.session_state.generated_code = python_code
                    st.session_state.rules_json = json_rules
                    st.session_state.rules_generated = True

                    # Success message
                    st.markdown(f"""
                    <div class="success-box">
                    <h3>✅ Success!</h3>
                    <p><strong>Processed:</strong> {uploaded_file.name}</p>
                    <p><strong>Rules Extracted:</strong> {result['summary']['total_rules']}</p>
                    <p><strong>Governance Rules:</strong> {result['summary']['by_category'].get('Governance', 0)}</p>
                    <p><strong>Risk Rules:</strong> {result['summary']['by_category'].get('Risk', 0)}</p>
                    <p><strong>Compliance Rules:</strong> {result['summary']['by_category'].get('Compliance', 0)}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.balloons()

                    st.info("👉 Go to the 'View Rules' tab to see extracted rules or 'Download Code' to get your Python code!")

                except Exception as e:
                    st.error(f"Error processing policy: {str(e)}")
                    st.exception(e)

with tab2:
    st.header("Extracted Policy Rules")

    if not st.session_state.rules_generated:
        st.info("📤 Please upload and process a policy document first (see 'Upload Policy' tab)")
    else:
        system = st.session_state.system
        rules = system.governance_enforcer.policy_parser.parsed_rules

        if not rules:
            st.warning("No rules were extracted from the document.")
        else:
            # Filter options
            col1, col2, col3 = st.columns(3)

            with col1:
                categories = list(set(r.get('category', 'Unknown') for r in rules))
                selected_category = st.selectbox("Filter by Category", ["All"] + categories)

            with col2:
                levels = list(set(r.get('compliance_level', 'Unknown') for r in rules))
                selected_level = st.selectbox("Filter by Compliance Level", ["All"] + levels)

            with col3:
                search = st.text_input("Search rules", placeholder="Enter keywords...")

            # Filter rules
            filtered_rules = rules
            if selected_category != "All":
                filtered_rules = [r for r in filtered_rules if r.get('category') == selected_category]
            if selected_level != "All":
                filtered_rules = [r for r in filtered_rules if r.get('compliance_level') == selected_level]
            if search:
                filtered_rules = [r for r in filtered_rules if search.lower() in r.get('description', '').lower()]

            st.info(f"Showing {len(filtered_rules)} of {len(rules)} rules")

            # Display rules
            for idx, rule in enumerate(filtered_rules, 1):
                with st.expander(f"Rule {idx}: {rule.get('description', 'No description')[:100]}..."):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**Rule ID:** `{rule.get('rule_id', 'N/A')}`")
                        st.markdown(f"**Category:** {rule.get('category', 'N/A')}")
                        st.markdown(f"**Subcategory:** {rule.get('subcategory', 'N/A')}")

                    with col2:
                        st.markdown(f"**Compliance Level:** `{rule.get('compliance_level', 'N/A')}`")
                        st.markdown(f"**Requirement:** {rule.get('requirement', 'N/A')}")

                    st.markdown("**Description:**")
                    st.info(rule.get('description', 'No description available'))

                    if rule.get('constraints'):
                        st.markdown("**Constraints:**")
                        st.json(rule['constraints'])

with tab3:
    st.header("Download Generated Code")

    if not st.session_state.rules_generated:
        st.info("📤 Please upload and process a policy document first (see 'Upload Policy' tab)")
    else:
        st.success("✅ Your code is ready for download!")

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        policy_name = st.session_state.policy_name or "policy"

        # Show code preview
        st.markdown("### 📄 Python Code Preview")
        st.code(st.session_state.generated_code[:2000] + "\n\n# ... (code continues) ...", language="python")

        st.markdown("---")

        # Download options
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🐍 Python Code")
            st.download_button(
                label="⬇️ Download Python File",
                data=st.session_state.generated_code,
                file_name=f"{policy_name}_rules_{timestamp}.py",
                mime="text/x-python",
                use_container_width=True
            )
            st.caption("Complete Python validation module")

        with col2:
            st.markdown("### 📋 JSON Rules")
            st.download_button(
                label="⬇️ Download JSON File",
                data=st.session_state.rules_json,
                file_name=f"{policy_name}_rules_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )
            st.caption("Structured rule definitions")

        with col3:
            st.markdown("### 📦 Complete Package")

            # Create ZIP file with all assets
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add Python code
                zip_file.writestr(f"{policy_name}_rules.py", st.session_state.generated_code)

                # Add JSON rules
                zip_file.writestr(f"{policy_name}_rules.json", st.session_state.rules_json)

                # Add README
                readme_content = f"""# Policy Rules - {policy_name}

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Files Included

1. **{policy_name}_rules.py** - Python validation module
2. **{policy_name}_rules.json** - Structured rule definitions
3. **README.md** - This file
4. **example_usage.py** - Example usage code

## How to Use

### Python Code

```python
# Import the generated rules
from {policy_name}_rules import *

# Example: Validate a rule
context = {{
    'contains_pii': True,
    'encryption_enabled': True,
    'user_consent': True
}}

# Call validation function (replace RULE_ID with actual rule ID)
# result = validate_RULE_ID(context)
# print(result)
```

### JSON Rules

Load and use the JSON rules in any application:

```python
import json

with open('{policy_name}_rules.json', 'r') as f:
    rules = json.load(f)

for rule in rules['rules']:
    print(f"Rule: {{rule['description']}}")
```

## Integration

Include these files in your application:
- Import the Python module for runtime validation
- Load JSON rules for configuration
- Use with GRC Multi-Agent System for full governance

## Support

For questions or issues, refer to the main documentation at:
https://github.com/HimJoe/policyascode
"""
                zip_file.writestr("README.md", readme_content)

                # Add example usage
                example_usage = f"""#!/usr/bin/env python3
\"\"\"
Example Usage of Generated Policy Rules
\"\"\"

import json
from {policy_name}_rules import *

def main():
    print("=" * 60)
    print("Policy Rules Validation Example")
    print("=" * 60)

    # Load JSON rules
    with open('{policy_name}_rules.json', 'r') as f:
        rules_data = json.load(f)

    print(f"\\nTotal Rules Loaded: {{len(rules_data['rules'])}}")

    # Example validation context
    example_context = {{
        'user_id': 'user_123',
        'action': 'process_data',
        'contains_pii': True,
        'encryption_enabled': True,
        'user_consent': True,
        'approval_obtained': True
    }}

    print("\\nExample Context:")
    print(json.dumps(example_context, indent=2))

    # Iterate through rules and validate
    print("\\nValidation Results:")
    print("-" * 60)

    for rule in rules_data['rules']:
        rule_id = rule['rule_id']
        func_name = f"validate_{{rule_id}}"

        # Check if validation function exists
        if func_name in globals():
            result = globals()[func_name](example_context)
            status = "✅ PASSED" if result['passed'] else "❌ FAILED"
            print(f"{{status}} - {{rule['description'][:60]}}")

            if not result['passed']:
                for violation in result.get('violations', []):
                    print(f"    ⚠️  {{violation}}")
        else:
            print(f"⚠️  Function {{func_name}} not found")

    print("=" * 60)

if __name__ == "__main__":
    main()
"""
                zip_file.writestr("example_usage.py", example_usage)

            zip_buffer.seek(0)

            st.download_button(
                label="⬇️ Download ZIP Package",
                data=zip_buffer,
                file_name=f"{policy_name}_package_{timestamp}.zip",
                mime="application/zip",
                use_container_width=True
            )
            st.caption("All files + documentation + examples")

        st.markdown("---")

        # Integration instructions
        st.markdown("### 🔌 Integration Instructions")

        with st.expander("📘 How to use the generated code in your application"):
            st.markdown(f"""
            #### Option 1: Direct Import (Python)

            1. Download the Python file
            2. Place it in your project directory
            3. Import and use:

            ```python
            from {policy_name}_rules import *

            # Your validation logic
            context = {{'contains_pii': True, 'encryption_enabled': True}}
            # result = validate_RULE_ID(context)
            ```

            #### Option 2: JSON Integration (Any Language)

            1. Download the JSON file
            2. Load in your application:

            ```python
            import json

            with open('{policy_name}_rules.json') as f:
                rules = json.load(f)

            # Use rules for validation logic
            for rule in rules['rules']:
                # Implement your validation
                pass
            ```

            #### Option 3: Complete Package

            1. Download the ZIP package
            2. Extract all files
            3. Run the example:

            ```bash
            python example_usage.py
            ```

            4. Integrate files into your application

            #### Option 4: Use with GRC Multi-Agent System

            ```python
            from grc_agent_system import GRCMultiAgentSystem
            import asyncio

            async def main():
                system = GRCMultiAgentSystem()

                # Upload your policy
                with open('policy.pdf', 'rb') as f:
                    await system.upload_policy(f.read(), 'policy.pdf', 'pdf')

                # Validate actions
                decision = await system.execute_with_governance(
                    user_id='user_001',
                    action='process_data',
                    parameters={{'contains_pii': True, 'encryption_enabled': True}}
                )

                print(f"Decision: {{decision['status']}}")

            asyncio.run(main())
            ```
            """)

        with st.expander("🚀 Deployment Options"):
            st.markdown("""
            ### Deploy Your Generated Code

            #### 1. Standalone Script
            - Run directly: `python {policy_name}_rules.py`
            - Import in other scripts

            #### 2. REST API
            - Wrap in Flask/FastAPI
            - Expose validation endpoints
            - Deploy to cloud

            #### 3. Lambda Function
            - Package as AWS Lambda
            - Deploy serverless
            - API Gateway integration

            #### 4. Microservice
            - Containerize with Docker
            - Deploy to Kubernetes
            - Scale horizontally

            #### 5. Integration Library
            - Package as Python module
            - Publish to PyPI
            - Install via pip
            """)

        with st.expander("📚 Example Use Cases"):
            st.markdown("""
            ### Real-World Applications

            #### Banking Application
            ```python
            # Before processing transaction
            context = {
                'transaction_amount': 15000,
                'manager_approval': True,
                'aml_review': True
            }

            # Validate against policy
            result = validate_transaction_rule(context)
            if result['passed']:
                process_transaction()
            else:
                log_violation(result['violations'])
            ```

            #### Healthcare System
            ```python
            # Before accessing patient data
            context = {
                'contains_phi': True,
                'user_authorized': True,
                'audit_logged': True
            }

            result = validate_access_rule(context)
            if not result['passed']:
                deny_access()
            ```

            #### E-commerce Platform
            ```python
            # Before processing customer data
            context = {
                'contains_pii': True,
                'encryption_enabled': True,
                'user_consent': True,
                'gdpr_compliant': True
            }

            result = validate_privacy_rule(context)
            ```
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Policy-to-Code Converter | Part of <a href="https://github.com/HimJoe/policyascode">GRC Multi-Agent Governance System</a></p>
    <p>Powered by Multi-Agent AI Architecture | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
