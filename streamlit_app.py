"""
Streamlit Web Interface for GRC Multi-Agent System
Allows users to upload policies and test governance enforcement
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grc_agent_system import GRCMultiAgentSystem, ExecutionContext
from document_processor import DocumentProcessorFactory
import tempfile


# Page config
st.set_page_config(
    page_title="GRC Governance System",
    page_icon="🔐",
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
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .approved {
        color: #28a745;
        font-weight: bold;
    }
    .blocked {
        color: #dc3545;
        font-weight: bold;
    }
    .rule-card {
        background-color: #fff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'grc_system' not in st.session_state:
    st.session_state.grc_system = GRCMultiAgentSystem()
if 'loaded_policies' not in st.session_state:
    st.session_state.loaded_policies = []
if 'audit_trail' not in st.session_state:
    st.session_state.audit_trail = []
if 'generated_rules' not in st.session_state:
    st.session_state.generated_rules = None


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🔐 GRC Multi-Agent Governance System</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=GRC+System", use_container_width=True)
        st.markdown("### Navigation")
        page = st.radio(
            "Select Page:",
            ["📤 Policy Upload", "⚙️ Rule Generation", "⚖️ Governance Testing", "📊 Analytics & Audit"]
        )
        
        st.markdown("---")
        st.markdown("### System Status")
        st.metric("Loaded Policies", len(st.session_state.loaded_policies))
        st.metric("Active Rules", 
                 len(st.session_state.grc_system.governance_enforcer.active_rules))
        st.metric("Audit Entries", len(st.session_state.audit_trail))
    
    # Main content
    if page == "📤 Policy Upload":
        policy_upload_page()
    elif page == "⚙️ Rule Generation":
        rule_generation_page()
    elif page == "⚖️ Governance Testing":
        governance_testing_page()
    elif page == "📊 Analytics & Audit":
        analytics_page()


def policy_upload_page():
    """Policy upload and processing page"""
    
    st.markdown('<div class="sub-header">📤 Policy Document Upload</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Upload your GRC policy documents in any of the following formats:
    - **Text files** (.txt)
    - **PDF documents** (.pdf)
    - **Excel spreadsheets** (.xlsx, .xls)
    
    The system will automatically parse policies and extract compliance rules.
    """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a policy document",
        type=['txt', 'pdf', 'xlsx', 'xls'],
        help="Upload a GRC policy document to parse and convert into rules"
    )
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.info(f"**File Type:** {uploaded_file.type}")
        with col2:
            st.info(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
        
        # Process button
        if st.button("🔄 Process Policy Document", type="primary"):
            with st.spinner("Processing policy document..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Determine file type
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    
                    # Process document
                    content = DocumentProcessorFactory.process_file(tmp_path, file_ext)
                    
                    # Upload to GRC system
                    result = asyncio.run(
                        st.session_state.grc_system.upload_policy(
                            content, 
                            uploaded_file.name, 
                            file_ext
                        )
                    )
                    
                    # Store results
                    st.session_state.loaded_policies.append({
                        'filename': uploaded_file.name,
                        'timestamp': datetime.now().isoformat(),
                        'rules_count': result['summary']['total_rules'],
                        'result': result
                    })
                    
                    st.session_state.generated_rules = result
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    # Display results
                    st.success("✅ Policy processed successfully!")
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Rules", result['summary']['total_rules'])
                    with col2:
                        governance_count = result['summary']['by_category'].get('Governance', 0)
                        st.metric("Governance", governance_count)
                    with col3:
                        risk_count = result['summary']['by_category'].get('Risk', 0)
                        st.metric("Risk", risk_count)
                    with col4:
                        compliance_count = result['summary']['by_category'].get('Compliance', 0)
                        st.metric("Compliance", compliance_count)
                    
                    # Show sample rules
                    st.markdown("### 📋 Extracted Rules (Sample)")
                    
                    for i, rule in enumerate(result['rules'][:5], 1):
                        with st.expander(f"Rule {i}: {rule.description[:60]}..."):
                            st.json(rule.to_dict())
                    
                    if len(result['rules']) > 5:
                        st.info(f"... and {len(result['rules']) - 5} more rules")
                    
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
    
    # Show loaded policies
    if st.session_state.loaded_policies:
        st.markdown("---")
        st.markdown("### 📚 Loaded Policy Documents")
        
        for policy in st.session_state.loaded_policies:
            with st.expander(f"📄 {policy['filename']} - {policy['rules_count']} rules"):
                st.write(f"**Loaded:** {policy['timestamp']}")
                st.write(f"**Rules Extracted:** {policy['rules_count']}")


def rule_generation_page():
    """Generated rules viewing and export page"""
    
    st.markdown('<div class="sub-header">⚙️ Generated Compliance Rules</div>', unsafe_allow_html=True)
    
    if not st.session_state.grc_system.governance_enforcer.active_rules:
        st.warning("No rules loaded yet. Please upload a policy document first.")
        return
    
    # Export options
    st.markdown("### 📥 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as JSON", use_container_width=True):
            json_export = st.session_state.grc_system.export_rules_json()
            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(json_export, indent=2),
                file_name=f"grc_rules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🐍 Export as Python", use_container_width=True):
            python_code = st.session_state.grc_system.export_rules_python()
            st.download_button(
                label="⬇️ Download Python",
                data=python_code,
                file_name=f"compliance_rules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                mime="text/x-python"
            )
    
    # Display rules
    st.markdown("### 📋 Active Compliance Rules")
    
    # Filters
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.multiselect(
            "Filter by Category",
            options=['Governance', 'Risk', 'Compliance'],
            default=['Governance', 'Risk', 'Compliance']
        )
    
    with col2:
        level_filter = st.multiselect(
            "Filter by Compliance Level",
            options=['mandatory', 'required', 'recommended', 'optional'],
            default=['mandatory', 'required', 'recommended', 'optional']
        )
    
    # Get filtered rules
    filtered_rules = [
        rule for rule in st.session_state.grc_system.governance_enforcer.active_rules
        if rule.category in category_filter and rule.compliance_level.value in level_filter
    ]
    
    st.info(f"Showing {len(filtered_rules)} of {len(st.session_state.grc_system.governance_enforcer.active_rules)} rules")
    
    # Display rules
    for i, rule in enumerate(filtered_rules, 1):
        with st.expander(f"Rule {i}: {rule.description[:80]}..."):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Rule ID:** `{rule.rule_id}`")
                st.markdown(f"**Category:** {rule.category}")
                st.markdown(f"**Subcategory:** {rule.subcategory}")
            
            with col2:
                st.markdown(f"**Compliance Level:** `{rule.compliance_level.value}`")
                st.markdown(f"**Source:** {rule.source_document}")
            
            st.markdown("**Description:**")
            st.write(rule.description)
            
            if rule.constraints:
                st.markdown("**Constraints:**")
                for constraint in rule.constraints:
                    st.json(constraint)


def governance_testing_page():
    """Test governance enforcement page"""
    
    st.markdown('<div class="sub-header">⚖️ Governance Enforcement Testing</div>', unsafe_allow_html=True)
    
    if not st.session_state.grc_system.governance_enforcer.active_rules:
        st.warning("No rules loaded yet. Please upload a policy document first.")
        return
    
    st.markdown("""
    Test how the governance system evaluates actions against loaded compliance rules.
    The system will check your action parameters against all applicable rules.
    """)
    
    # Test configuration
    col1, col2 = st.columns(2)
    
    with col1:
        user_id = st.text_input("User ID", value="test_user_001")
        action = st.text_input("Action Description", value="process customer data")
    
    with col2:
        risk_level = st.select_slider(
            "Expected Risk Level",
            options=["Low", "Medium", "High", "Critical"],
            value="Medium"
        )
    
    # Action parameters
    st.markdown("### Action Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        contains_pii = st.checkbox("Contains PII", value=True)
        encryption_enabled = st.checkbox("Encryption Enabled", value=False)
    
    with col2:
        user_consent = st.checkbox("User Consent Obtained", value=True)
        approval_obtained = st.checkbox("Approval Obtained", value=False)
    
    with col3:
        data_retention_days = st.number_input("Data Retention (days)", min_value=0, value=30)
    
    # Test button
    if st.button("🧪 Test Governance", type="primary", use_container_width=True):
        with st.spinner("Evaluating against compliance rules..."):
            
            # Build parameters
            parameters = {
                'contains_pii': contains_pii,
                'encryption_enabled': encryption_enabled,
                'user_consent': user_consent,
                'approval_obtained': approval_obtained,
                'retention_days': data_retention_days
            }
            
            # Execute governance check
            result = asyncio.run(
                st.session_state.grc_system.execute_with_governance(
                    user_id=user_id,
                    action=action,
                    parameters=parameters
                )
            )
            
            # Store in audit trail
            st.session_state.audit_trail.append(result)
            
            # Display results
            st.markdown("---")
            st.markdown("### 📊 Governance Decision")
            
            if result['status'] == 'approved':
                st.success("✅ **ACTION APPROVED**")
                st.markdown(f'<div class="approved">Status: APPROVED</div>', unsafe_allow_html=True)
            else:
                st.error("❌ **ACTION BLOCKED**")
                st.markdown(f'<div class="blocked">Status: BLOCKED</div>', unsafe_allow_html=True)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Risk Score", f"{result['enforcement']['risk_score']:.1f}")
            with col2:
                violations = len(result['enforcement']['validation']['violations'])
                st.metric("Violations", violations)
            with col3:
                rules_checked = result['enforcement']['validation']['rules_evaluated']
                st.metric("Rules Evaluated", len(rules_checked))
            
            # Violations
            if result['enforcement']['validation']['violations']:
                st.markdown("### ⚠️ Compliance Violations")
                for violation in result['enforcement']['validation']['violations']:
                    st.error(f"• {violation}")
            
            # Rules evaluated
            st.markdown("### 📋 Rules Evaluated")
            for rule_result in result['enforcement']['validation']['rules_evaluated']:
                status_icon = "✅" if rule_result['passed'] else "❌"
                with st.expander(f"{status_icon} {rule_result['category']} - Rule {rule_result['rule_id']}"):
                    st.json(rule_result)


def analytics_page():
    """Analytics and audit trail page"""
    
    st.markdown('<div class="sub-header">📊 Analytics & Audit Trail</div>', unsafe_allow_html=True)
    
    if not st.session_state.audit_trail:
        st.info("No audit entries yet. Test some governance actions first.")
        return
    
    # Summary metrics
    st.markdown("### 📈 Summary Metrics")
    
    total_checks = len(st.session_state.audit_trail)
    approved = sum(1 for entry in st.session_state.audit_trail if entry['status'] == 'approved')
    blocked = total_checks - approved
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Checks", total_checks)
    with col2:
        st.metric("Approved", approved, delta=f"{approved/total_checks*100:.1f}%")
    with col3:
        st.metric("Blocked", blocked, delta=f"-{blocked/total_checks*100:.1f}%")
    with col4:
        avg_risk = sum(e['enforcement']['risk_score'] for e in st.session_state.audit_trail) / total_checks
        st.metric("Avg Risk Score", f"{avg_risk:.1f}")
    
    # Audit trail
    st.markdown("### 📜 Audit Trail")
    
    for i, entry in enumerate(reversed(st.session_state.audit_trail), 1):
        status_color = "green" if entry['status'] == 'approved' else "red"
        
        with st.expander(
            f"{'✅' if entry['status'] == 'approved' else '❌'} "
            f"Entry {i}: {entry['context'].action} - "
            f"{entry['context'].timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Request ID:** `{entry['context'].request_id}`")
                st.markdown(f"**User ID:** {entry['context'].user_id}")
                st.markdown(f"**Action:** {entry['context'].action}")
                st.markdown(f"**Status:** :{status_color}[{entry['status'].upper()}]")
            
            with col2:
                st.markdown(f"**Risk Score:** {entry['enforcement']['risk_score']:.1f}")
                st.markdown(f"**Rules Evaluated:** {len(entry['enforcement']['validation']['rules_evaluated'])}")
                violations = len(entry['enforcement']['validation']['violations'])
                st.markdown(f"**Violations:** {violations}")
            
            st.markdown("**Parameters:**")
            st.json(entry['context'].parameters)
            
            if entry['enforcement']['validation']['violations']:
                st.markdown("**Violations:**")
                for violation in entry['enforcement']['validation']['violations']:
                    st.error(violation)
    
    # Export audit trail
    if st.button("📥 Export Audit Trail"):
        audit_export = [
            {
                'timestamp': entry['context'].timestamp.isoformat(),
                'request_id': entry['context'].request_id,
                'user_id': entry['context'].user_id,
                'action': entry['context'].action,
                'status': entry['status'],
                'risk_score': entry['enforcement']['risk_score'],
                'violations': entry['enforcement']['validation']['violations']
            }
            for entry in st.session_state.audit_trail
        ]
        
        st.download_button(
            label="⬇️ Download Audit Trail (JSON)",
            data=json.dumps(audit_export, indent=2),
            file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


if __name__ == "__main__":
    main()
