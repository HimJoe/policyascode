# Quick Start Guide: GRC Multi-Agent Governance System

## For GRC Specialists in Regulated Banking

### 🎯 What This System Does

Automatically converts your GRC policy documents into **executable code** that enforces compliance rules on AI agent systems in real-time.

**Input:** Policy PDFs, Word docs, Excel spreadsheets  
**Output:** Python code + JSON rules + Real-time enforcement

---

## ⚡ 5-Minute Quick Start

### Step 1: Install (30 seconds)

```bash
# Install required packages
pip install streamlit PyPDF2 openpyxl

# Or use the requirements file
pip install -r requirements.txt
```

### Step 2: Run Demo (2 minutes)

```bash
# Run the comprehensive demo
python demo.py
```

This will:
- Load a sample banking policy
- Extract compliance rules automatically
- Generate Python code for enforcement
- Test governance scenarios
- Create an audit trail

### Step 3: Try Web Interface (2 minutes)

```bash
# Launch the web application
streamlit run streamlit_app.py
```

Navigate to `http://localhost:8501` and:
1. Upload your policy document (PDF, Excel, or Text)
2. View extracted rules
3. Test governance enforcement
4. Export rules as Python or JSON

---

## 📤 Uploading Your First Policy

### Via Command Line

```python
from grc_agent_system import GRCMultiAgentSystem
import asyncio

async def main():
    system = GRCMultiAgentSystem()
    
    # Read your policy file
    with open('your_policy.pdf', 'r') as f:
        content = f.read()
    
    # Upload and process
    result = await system.upload_policy(
        content=content,
        filename='your_policy.pdf',
        file_type='pdf'
    )
    
    # View results
    print(f"Extracted {result['summary']['total_rules']} rules")

asyncio.run(main())
```

### Via Web Interface

1. Click "📤 Policy Upload"
2. Drag and drop your file
3. Click "Process Policy Document"
4. Review extracted rules

---

## 🔍 What The System Extracts

From your policy documents, the system automatically identifies:

### 1. **Mandatory Requirements**
- Keywords: "must", "shall", "required to"
- Example: *"Customer PII must be encrypted"*
- Action: Creates CRITICAL enforcement rule

### 2. **Prohibited Actions**
- Keywords: "must not", "shall not", "prohibited"
- Example: *"Data must not be shared without consent"*
- Action: Creates blocking rule

### 3. **Recommended Practices**
- Keywords: "should", "recommended"
- Example: *"Transactions should be reviewed daily"*
- Action: Creates warning rule

### 4. **Specific Constraints**

| Type | Example | System Action |
|------|---------|---------------|
| **Data Retention** | "Retain for 7 years" | Validates retention periods |
| **Encryption** | "AES-256 required" | Checks encryption enabled |
| **PII Handling** | "Requires consent" | Validates consent obtained |
| **Approval Required** | "Manager approval" | Checks authorization |
| **Monetary Thresholds** | "Exceeds $10,000" | Compares amounts |

---

## 🎮 Common Use Cases

### Use Case 1: Customer Data Processing

**Your Policy:**
```
Section 2.1: Customer PII must be encrypted using AES-256 
and requires explicit consent before processing.
```

**Generated Rule:**
```python
def validate_customer_pii(context):
    if context['contains_pii']:
        if not context['encryption_enabled']:
            return BLOCKED("PII must be encrypted")
        if not context['user_consent']:
            return BLOCKED("Consent required")
    return APPROVED
```

**Usage:**
```python
# This gets BLOCKED
await system.execute_with_governance(
    action='process customer data',
    parameters={
        'contains_pii': True,
        'encryption_enabled': False  # ❌ Violation
    }
)

# This gets APPROVED
await system.execute_with_governance(
    action='process customer data',
    parameters={
        'contains_pii': True,
        'encryption_enabled': True,  # ✅
        'user_consent': True          # ✅
    }
)
```

### Use Case 2: High-Value Transactions

**Your Policy:**
```
Section 3.2: Transactions exceeding $10,000 require 
manager approval and AML review.
```

**Generated Rule:**
```python
def validate_high_value_transaction(context):
    if context['amount'] > 10000:
        if not context['manager_approval']:
            return BLOCKED("Manager approval required")
        if not context['aml_review']:
            return BLOCKED("AML review required")
    return APPROVED
```

### Use Case 3: Data Retention

**Your Policy:**
```
Section 4.1: Transaction records must be retained 
for 7 years per federal requirements.
```

**Generated Rule:**
```python
def validate_retention(context):
    if context['record_type'] == 'transaction':
        if context['retention_days'] < 2555:  # 7 years
            return BLOCKED("Must retain for 7 years")
    return APPROVED
```

---

## 📊 Understanding System Output

### JSON Export Format

```json
{
  "rules": [
    {
      "rule_id": "unique_id_123",
      "category": "Compliance",
      "subcategory": "encryption",
      "description": "Customer PII must be encrypted",
      "compliance_level": "mandatory",
      "constraints": [
        {
          "type": "encryption_required",
          "algorithm": "AES-256"
        }
      ]
    }
  ]
}
```

### Python Code Export

```python
# Auto-generated compliance rules
# DO NOT EDIT MANUALLY

def validate_unique_id_123(context):
    """
    Rule: Customer PII must be encrypted
    Level: MANDATORY
    """
    result = {"passed": True, "violations": []}
    
    if context.get('contains_pii'):
        if not context.get('encryption_enabled'):
            result['passed'] = False
            result['violations'].append(
                "PII must be encrypted"
            )
    
    return result
```

---

## 🔐 Integrating With Your Systems

### Pattern 1: API Wrapper

Wrap your existing AI agents:

```python
class ComplianceWrappedAgent:
    def __init__(self, agent, grc_system):
        self.agent = agent
        self.grc = grc_system
    
    async def execute(self, action, **params):
        # Pre-check compliance
        decision = await self.grc.execute_with_governance(
            user_id=self.agent.user_id,
            action=action,
            parameters=params
        )
        
        if decision['status'] != 'approved':
            raise ComplianceViolation(
                decision['enforcement']['violations']
            )
        
        # Execute if approved
        return await self.agent.run(action, **params)
```

### Pattern 2: Middleware

Add to existing request pipeline:

```python
@app.before_request
async def check_compliance():
    decision = await grc.execute_with_governance(
        user_id=request.user_id,
        action=request.endpoint,
        parameters=request.get_json()
    )
    
    if decision['status'] == 'blocked':
        return jsonify({
            'error': 'Compliance violation',
            'violations': decision['violations']
        }), 403
```

### Pattern 3: Pre-Deployment Check

Validate before production:

```python
# In your CI/CD pipeline
def test_compliance():
    system = GRCMultiAgentSystem()
    
    # Load all policies
    system.load_policies('prod_policies/')
    
    # Test critical scenarios
    scenarios = load_test_scenarios()
    
    for scenario in scenarios:
        result = await system.execute_with_governance(
            action=scenario['action'],
            parameters=scenario['params']
        )
        
        assert result['status'] == scenario['expected']
```

---

## 📈 Monitoring & Audit

### View Audit Trail

```python
# Get all governance decisions
audit_trail = system.get_audit_trail()

# Statistics
approved = sum(1 for e in audit_trail if e['approved'])
blocked = len(audit_trail) - approved

print(f"Approval Rate: {approved/len(audit_trail)*100}%")
print(f"Average Risk Score: {sum(e['risk_score'] for e in audit_trail)/len(audit_trail)}")
```

### Export for Regulators

```python
# Generate compliance report
audit_export = {
    'period': '2024-Q4',
    'total_checks': len(audit_trail),
    'violations_count': sum(len(e['violations']) for e in audit_trail),
    'details': audit_trail
}

with open('compliance_report_Q4.json', 'w') as f:
    json.dump(audit_export, f, indent=2)
```

---

## 🎓 Best Practices

### 1. **Organize Policies by Domain**

```
policies/
  ├── data_protection/
  │   ├── pii_handling.txt
  │   └── encryption_standards.pdf
  ├── transactions/
  │   ├── aml_rules.xlsx
  │   └── high_value_approval.txt
  └── access_control/
      └── authentication.pdf
```

### 2. **Use Clear Policy Language**

✅ **Good:**
```
Customer PII must be encrypted using AES-256 before storage.
```

❌ **Avoid:**
```
It would be beneficial if customer information could potentially 
be secured through some form of encryption mechanism.
```

### 3. **Test Rules Before Production**

```python
# Create test scenarios
test_cases = [
    {
        'name': 'PII without encryption',
        'params': {'pii': True, 'encrypted': False},
        'should_block': True
    },
    {
        'name': 'PII with encryption',
        'params': {'pii': True, 'encrypted': True},
        'should_block': False
    }
]

# Validate
for test in test_cases:
    result = await system.execute_with_governance(
        action='test',
        parameters=test['params']
    )
    assert (result['status'] == 'blocked') == test['should_block']
```

### 4. **Version Control Your Rules**

```bash
# Tag rule versions
git tag -a v1.0-rules -m "Q4 2024 compliance rules"

# Track policy changes
git log --follow policies/pii_handling.txt
```

---

## ❓ Troubleshooting

### Issue: Rules not being extracted

**Solution:** Ensure your policy uses clear requirement keywords:
- Use: "must", "shall", "required"
- Not: "could", "might", "perhaps"

### Issue: Too many false positives

**Solution:** Adjust compliance levels:
- MANDATORY: Critical violations only
- REQUIRED: Important but not critical
- RECOMMENDED: Best practices

### Issue: Performance with large policies

**Solution:** 
1. Split policies into smaller documents
2. Use category filters
3. Index rules for faster lookup

---

## 📞 Support & Resources

### Documentation
- Full README: `README.md`
- Architecture: `architecture_diagram.mermaid`
- API Reference: See docstrings in code

### Example Files
- `sample_banking_policy.txt` - Complete banking policy example
- `demo.py` - Comprehensive demonstration
- `streamlit_app.py` - Web interface

### Getting Help

1. Review the demo output
2. Check audit trail for decision details
3. Examine generated rules
4. Test with simplified policies first

---

## 🚀 Production Deployment Checklist

- [ ] Load all production policies
- [ ] Test all critical scenarios
- [ ] Set up audit log storage (database)
- [ ] Configure backup and retention
- [ ] Add authentication/authorization
- [ ] Set up monitoring and alerts
- [ ] Document rule versions
- [ ] Train team on system
- [ ] Establish review process
- [ ] Create runbooks for incidents

---

**Ready to get started?**

```bash
# Try it now!
python demo.py
```

For questions or issues, review the comprehensive README.md file.
