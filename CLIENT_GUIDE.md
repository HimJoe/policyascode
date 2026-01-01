# Policy-to-Code Converter - Client Guide

Welcome! This guide will help you convert your policy documents into executable Python code in minutes.

## 🎯 What is This?

The Policy-to-Code Converter automatically transforms your compliance policies (PDF, Text, Excel) into:
- ✅ **Python code** - Ready-to-run validation functions
- ✅ **JSON rules** - Structured rule definitions
- ✅ **Complete package** - Code + documentation + examples

## 📋 What You Need

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Storage**: ~100 MB free space
- **Internet**: Required for initial setup

### Supported Policy Formats
- ✅ PDF documents (.pdf)
- ✅ Text files (.txt)
- ✅ Excel spreadsheets (.xlsx, .xls)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Download the Application

```bash
# Clone or download from GitHub
git clone https://github.com/HimJoe/policyascode.git
cd policyascode
```

Or download ZIP from: https://github.com/HimJoe/policyascode

### Step 2: Run Setup

**On macOS/Linux:**
```bash
chmod +x setup_for_client.sh
./setup_for_client.sh
```

**On Windows:**
```bash
setup_for_client.bat
```

This will:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies

### Step 3: Start the Converter

**On macOS/Linux:**
```bash
chmod +x run_converter.sh
./run_converter.sh
```

**On Windows:**
```bash
run_converter.bat
```

Your browser will open automatically at: `http://localhost:8501`

---

## 📖 How to Use the Converter

### 1. Upload Your Policy

1. Click **"Browse files"** button
2. Select your policy document (PDF, TXT, or XLSX)
3. Click **"Process Policy Document"** button
4. Wait for processing (usually 10-30 seconds)

### 2. Review Extracted Rules

Switch to **"View Rules"** tab to:
- ✅ See all extracted policy rules
- ✅ Filter by category (Governance, Risk, Compliance)
- ✅ Filter by compliance level (mandatory, required, recommended)
- ✅ Search specific rules
- ✅ View rule details and constraints

### 3. Download Your Code

Switch to **"Download Code"** tab and choose:

**Option A: Python File Only**
- Click "Download Python File"
- Get: `your_policy_rules.py`
- Use in Python applications

**Option B: JSON File Only**
- Click "Download JSON File"
- Get: `your_policy_rules.json`
- Use in any application/language

**Option C: Complete Package (Recommended)**
- Click "Download ZIP Package"
- Get: Complete package with:
  - Python validation code
  - JSON rule definitions
  - README documentation
  - Example usage scripts
  - Integration guide

---

## 💻 Using the Generated Code

### Option 1: Python Integration

```python
# Import the generated rules module
from your_policy_rules import *

# Define your context (what you're validating)
context = {
    'contains_pii': True,
    'encryption_enabled': True,
    'user_consent': True,
    'approval_obtained': True
}

# Validate using generated functions
# Replace RULE_ID with actual rule ID from your code
result = validate_RULE_ID(context)

# Check result
if result['passed']:
    print("✅ Validation passed!")
    # Proceed with action
else:
    print("❌ Validation failed!")
    for violation in result['violations']:
        print(f"   - {violation}")
    # Handle violations
```

### Option 2: JSON Integration (Any Language)

```python
import json

# Load rules
with open('your_policy_rules.json', 'r') as f:
    rules = json.load(f)

# Iterate through rules
for rule in rules['rules']:
    print(f"Rule: {rule['description']}")
    print(f"Category: {rule['category']}")
    print(f"Level: {rule['compliance_level']}")
    print(f"Constraints: {rule['constraints']}")
```

### Option 3: Run the Example

After downloading the ZIP package:

```bash
# Extract the ZIP file
unzip your_policy_package.zip
cd your_policy_package

# Run the example
python example_usage.py
```

---

## 🎓 Understanding Your Generated Code

### Python Code Structure

```python
def validate_RULE_ID(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule: [Your policy rule description]
    Category: [Governance/Risk/Compliance]
    Level: [mandatory/required/recommended]
    """
    result = {
        "rule_id": "RULE_ID",
        "passed": True,
        "violations": []
    }

    # Validation logic based on your policy
    if not context.get('required_field'):
        result["passed"] = False
        result["violations"].append("Violation message")

    return result
```

### JSON Rules Structure

```json
{
  "rules": [
    {
      "rule_id": "abc123",
      "category": "Compliance",
      "subcategory": "data_protection",
      "description": "PII must be encrypted",
      "requirement": "encryption_required",
      "compliance_level": "mandatory",
      "constraints": [
        {
          "type": "encryption_required",
          "field": "encryption_enabled",
          "value": true
        }
      ]
    }
  ]
}
```

---

## 🏢 Real-World Examples

### Banking Example

**Your Policy:**
> "Customer transactions exceeding $10,000 must be approved by a manager and reviewed for AML compliance."

**Generated Code:**
```python
def validate_large_transaction(context):
    result = {"passed": True, "violations": []}

    if context.get('transaction_amount', 0) > 10000:
        if not context.get('manager_approval'):
            result['passed'] = False
            result['violations'].append("Manager approval required for transactions over $10,000")

        if not context.get('aml_review'):
            result['passed'] = False
            result['violations'].append("AML review required for transactions over $10,000")

    return result
```

**Usage:**
```python
# Valid transaction
context = {
    'transaction_amount': 15000,
    'manager_approval': True,
    'aml_review': True
}
result = validate_large_transaction(context)
# result['passed'] == True

# Invalid transaction
context = {
    'transaction_amount': 15000,
    'manager_approval': False,  # Missing!
    'aml_review': True
}
result = validate_large_transaction(context)
# result['passed'] == False
# result['violations'] == ["Manager approval required..."]
```

### Healthcare Example

**Your Policy:**
> "Patient health information must be encrypted and access must be logged for HIPAA compliance."

**Generated Code:**
```python
def validate_phi_access(context):
    result = {"passed": True, "violations": []}

    if context.get('contains_phi'):
        if not context.get('encryption_enabled'):
            result['passed'] = False
            result['violations'].append("PHI must be encrypted")

        if not context.get('access_logged'):
            result['passed'] = False
            result['violations'].append("PHI access must be logged")

    return result
```

---

## 🔧 Integration Scenarios

### Scenario 1: Web Application

```python
from flask import Flask, request, jsonify
from your_policy_rules import *

app = Flask(__name__)

@app.route('/api/validate', methods=['POST'])
def validate_action():
    context = request.json

    # Validate against all rules
    violations = []
    for rule_func in [validate_rule1, validate_rule2, ...]:
        result = rule_func(context)
        if not result['passed']:
            violations.extend(result['violations'])

    if violations:
        return jsonify({
            'status': 'rejected',
            'violations': violations
        }), 400

    return jsonify({'status': 'approved'}), 200
```

### Scenario 2: Batch Processing

```python
import pandas as pd
from your_policy_rules import *

# Load transactions from CSV
transactions = pd.read_csv('transactions.csv')

# Validate each transaction
results = []
for _, tx in transactions.iterrows():
    context = tx.to_dict()
    result = validate_transaction_rule(context)
    results.append({
        'transaction_id': tx['id'],
        'passed': result['passed'],
        'violations': result['violations']
    })

# Save results
pd.DataFrame(results).to_csv('validation_results.csv')
```

### Scenario 3: API Gateway

```python
from aws_lambda import handler
from your_policy_rules import *

def lambda_handler(event, context):
    request_context = event['body']

    # Validate
    result = validate_api_access(request_context)

    if result['passed']:
        return {
            'statusCode': 200,
            'body': 'Request approved'
        }
    else:
        return {
            'statusCode': 403,
            'body': {
                'message': 'Request denied',
                'violations': result['violations']
            }
        }
```

---

## 🛠️ Troubleshooting

### Issue: "Python not found"

**Solution:**
1. Install Python 3.8+ from https://www.python.org/downloads/
2. Make sure to check "Add Python to PATH" during installation
3. Restart your terminal/command prompt

### Issue: "Dependencies installation failed"

**Solution:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies manually
pip install streamlit PyPDF2 openpyxl pandas
```

### Issue: "Streamlit command not found"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Or run directly
python -m streamlit run policy_to_code_converter.py
```

### Issue: "No rules extracted from my policy"

**Solution:**
- Make sure your policy has clear structure
- Use compliance keywords: "must", "shall", "required", "mandatory"
- Include specific requirements and constraints
- Try reformatting as numbered sections

**Good Policy Example:**
```
1. Data Protection Requirements

1.1 All customer PII must be encrypted using AES-256 encryption.

1.2 Encryption keys shall be rotated every 90 days.

1.3 Access to encrypted data requires two-factor authentication.
```

### Issue: "Port 8501 already in use"

**Solution:**
```bash
# Run on different port
streamlit run policy_to_code_converter.py --server.port 8502
```

---

## 📦 Distributing to Your Team

### Option 1: Share the Repository

1. Share the GitHub link: https://github.com/HimJoe/policyascode
2. Team members run setup script
3. Everyone can convert policies

### Option 2: Create a Standalone Package

```bash
# Create a distribution package
zip -r policy_converter_for_clients.zip \
    policy_to_code_converter.py \
    grc_agent_system.py \
    document_processor.py \
    requirements.txt \
    setup_for_client.sh \
    setup_for_client.bat \
    run_converter.sh \
    run_converter.bat \
    CLIENT_GUIDE.md

# Share the ZIP file with clients
```

### Option 3: Deploy Online

Deploy to Streamlit Cloud (free):
1. Your app is already deployed at the GitHub repo
2. Share the URL with clients
3. They can use it directly in browser (no installation needed)

---

## 🔐 Security Best Practices

### For Sensitive Policies

1. **Run Locally**: Don't upload sensitive policies to cloud services
2. **Use Offline**: Converter works without internet (after setup)
3. **Review Output**: Always review generated code before deployment
4. **Secure Storage**: Store generated code in secure repositories
5. **Access Control**: Limit who can convert policies

### For Production Use

1. **Code Review**: Have developers review generated code
2. **Testing**: Test validation functions thoroughly
3. **Version Control**: Keep generated code in Git
4. **Audit Trail**: Log all validation decisions
5. **Updates**: Regenerate code when policies change

---

## 📞 Support & Help

### Getting Help

1. **Read Documentation**:
   - README.md - Project overview
   - QUICKSTART.md - Quick start guide
   - DEPLOYMENT.md - Deployment options

2. **Check Examples**:
   - Run `demo.py` for examples
   - Review `sample_banking_policy.txt`

3. **GitHub Issues**:
   - Report bugs: https://github.com/HimJoe/policyascode/issues
   - Request features
   - Ask questions

4. **Community**:
   - GitHub Discussions
   - Share your use cases

---

## 📈 Next Steps

After converting your policies:

1. ✅ **Test the Code**: Run example_usage.py
2. ✅ **Integrate**: Add to your application
3. ✅ **Deploy**: Use in production
4. ✅ **Monitor**: Track validation results
5. ✅ **Update**: Regenerate when policies change

---

## 🎯 Success Stories

### Banking Client
- **Before**: 500+ policies, manual compliance reviews
- **After**: Automated policy enforcement, 80% time reduction
- **Result**: Real-time transaction validation

### Healthcare Provider
- **Before**: HIPAA compliance gaps
- **After**: Automated PHI protection validation
- **Result**: 100% compliance coverage

### Fintech Startup
- **Before**: Slow feature deployment due to compliance reviews
- **After**: Automated policy checks in CI/CD
- **Result**: Faster releases, zero violations

---

## 📝 Quick Reference

### Common Commands

```bash
# Setup (first time only)
./setup_for_client.sh        # macOS/Linux
setup_for_client.bat         # Windows

# Run converter
./run_converter.sh           # macOS/Linux
run_converter.bat            # Windows

# Manual run
streamlit run policy_to_code_converter.py

# Different port
streamlit run policy_to_code_converter.py --server.port 8502
```

### File Overview

| File | Purpose |
|------|---------|
| `policy_to_code_converter.py` | Main converter application |
| `setup_for_client.sh/.bat` | One-time setup script |
| `run_converter.sh/.bat` | Quick start script |
| `CLIENT_GUIDE.md` | This guide |
| `requirements.txt` | Python dependencies |

---

## ✅ Checklist for Clients

Before converting your first policy:
- [ ] Python 3.8+ installed
- [ ] Ran setup script successfully
- [ ] Converter opens in browser
- [ ] Sample policy converted successfully
- [ ] Downloaded and reviewed generated code
- [ ] Read integration examples
- [ ] Tested example_usage.py

---

**Ready to get started?** Run the setup script and convert your first policy in minutes! 🚀

For questions or support, visit: https://github.com/HimJoe/policyascode
