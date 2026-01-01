"""
Comprehensive Demo: GRC Multi-Agent Governance System
Demonstrates policy loading, rule generation, and governance enforcement
"""

import asyncio
import json
from grc_agent_system import GRCMultiAgentSystem
from datetime import datetime


def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def print_section(text):
    """Print a section header"""
    print(f"\n{'─'*80}")
    print(f"  {text}")
    print(f"{'─'*80}\n")


async def demo_policy_loading():
    """Demonstrate loading and parsing a policy document"""
    
    print_banner("DEMO 1: POLICY DOCUMENT LOADING & PARSING")
    
    system = GRCMultiAgentSystem()
    
    # Load the sample banking policy
    print("📁 Loading sample banking GRC policy...")
    
    with open('sample_banking_policy.txt', 'r') as f:
        policy_content = f.read()
    
    print(f"   File size: {len(policy_content)} characters")
    print(f"   Lines: {len(policy_content.split(chr(10)))}")
    
    # Upload and process
    result = await system.upload_policy(
        content=policy_content,
        filename='sample_banking_policy.txt',
        file_type='text'
    )
    
    # Display summary
    print_section("📊 Extraction Summary")
    
    print(f"Total Rules Extracted: {result['summary']['total_rules']}")
    print(f"\nBreakdown by Category:")
    for category, count in result['summary']['by_category'].items():
        print(f"  • {category}: {count} rules")
    
    print(f"\nBreakdown by Compliance Level:")
    for level, count in result['summary']['by_compliance_level'].items():
        print(f"  • {level.upper()}: {count} rules")
    
    # Show sample rules
    print_section("📋 Sample Extracted Rules")
    
    for i, rule in enumerate(result['rules'][:5], 1):
        print(f"\n{i}. Rule ID: {rule.rule_id}")
        print(f"   Category: {rule.category} / {rule.subcategory}")
        print(f"   Level: {rule.compliance_level.value}")
        print(f"   Description: {rule.description[:100]}...")
        if rule.constraints:
            print(f"   Constraints: {len(rule.constraints)} constraint(s)")
    
    if len(result['rules']) > 5:
        print(f"\n   ... and {len(result['rules']) - 5} more rules")
    
    return system


async def demo_rule_generation(system):
    """Demonstrate rule code generation"""
    
    print_banner("DEMO 2: AUTOMATED RULE CODE GENERATION")
    
    # Export to JSON
    print_section("📄 JSON Export")
    
    json_export = system.export_rules_json()
    print(f"Total rules in export: {json_export['total_count']}")
    
    # Show sample JSON
    sample_rule = json_export['rules'][0] if json_export['rules'] else None
    if sample_rule:
        print("\nSample Rule (JSON format):")
        print(json.dumps(sample_rule, indent=2)[:500] + "...")
    
    # Export to Python
    print_section("🐍 Python Code Export")
    
    python_code = system.export_rules_python()
    print(f"Generated Python code: {len(python_code)} characters")
    print(f"Functions: {python_code.count('def validate_')}")
    
    print("\nSample Generated Function:")
    # Extract first function
    start = python_code.find('def validate_')
    end = python_code.find('\ndef validate_', start + 1)
    if end == -1:
        end = python_code.find('\n\n# Rule Registry', start)
    sample_function = python_code[start:end] if start != -1 else "N/A"
    print(sample_function[:600] + "..." if len(sample_function) > 600 else sample_function)


async def demo_governance_enforcement(system):
    """Demonstrate governance enforcement with various scenarios"""
    
    print_banner("DEMO 3: GOVERNANCE ENFORCEMENT SCENARIOS")
    
    # Scenario 1: Compliant PII Processing
    print_section("Scenario 1: Compliant Customer Data Processing")
    
    print("Request Details:")
    print("  User: customer_service_rep_001")
    print("  Action: Process customer account update")
    print("  Parameters:")
    print("    • Contains PII: Yes")
    print("    • Encryption Enabled: Yes ✓")
    print("    • User Consent: Yes ✓")
    print("    • Support Ticket: Active ✓")
    
    result1 = await system.execute_with_governance(
        user_id='customer_service_rep_001',
        action='process customer data',
        parameters={
            'contains_pii': True,
            'encryption_enabled': True,
            'user_consent': True,
            'support_ticket_active': True
        }
    )
    
    print(f"\n{'✅ DECISION: APPROVED' if result1['status'] == 'approved' else '❌ DECISION: BLOCKED'}")
    print(f"Risk Score: {result1['enforcement']['risk_score']}")
    print(f"Rules Evaluated: {len(result1['enforcement']['validation']['rules_evaluated'])}")
    
    # Scenario 2: Non-compliant (Missing Encryption)
    print_section("Scenario 2: Non-Compliant Data Processing (Missing Encryption)")
    
    print("Request Details:")
    print("  User: analyst_002")
    print("  Action: Export customer report")
    print("  Parameters:")
    print("    • Contains PII: Yes")
    print("    • Encryption Enabled: No ✗")
    print("    • User Consent: Yes")
    
    result2 = await system.execute_with_governance(
        user_id='analyst_002',
        action='process customer data',
        parameters={
            'contains_pii': True,
            'encryption_enabled': False,  # Violation
            'user_consent': True
        }
    )
    
    print(f"\n{'✅ DECISION: APPROVED' if result2['status'] == 'approved' else '❌ DECISION: BLOCKED'}")
    print(f"Risk Score: {result2['enforcement']['risk_score']}")
    
    if result2['enforcement']['validation']['violations']:
        print("\n⚠️  Compliance Violations:")
        for violation in result2['enforcement']['validation']['violations']:
            print(f"    • {violation}")
    
    # Scenario 3: High-Value Transaction
    print_section("Scenario 3: High-Value Transaction Processing")
    
    print("Request Details:")
    print("  User: teller_003")
    print("  Action: Process wire transfer")
    print("  Parameters:")
    print("    • Transaction Amount: $15,000")
    print("    • AML Review: Pending ✗")
    print("    • Manager Approval: No ✗")
    
    result3 = await system.execute_with_governance(
        user_id='teller_003',
        action='process transaction',
        parameters={
            'transaction_amount': 15000,
            'aml_review_completed': False,  # Violation
            'manager_approval': False  # Violation
        }
    )
    
    print(f"\n{'✅ DECISION: APPROVED' if result3['status'] == 'approved' else '❌ DECISION: BLOCKED'}")
    print(f"Risk Score: {result3['enforcement']['risk_score']}")
    
    if result3['enforcement']['validation']['violations']:
        print("\n⚠️  Compliance Violations:")
        for violation in result3['enforcement']['validation']['violations']:
            print(f"    • {violation}")
    
    # Scenario 4: Compliant High-Value Transaction
    print_section("Scenario 4: Compliant High-Value Transaction")
    
    print("Request Details:")
    print("  User: senior_teller_004")
    print("  Action: Process wire transfer")
    print("  Parameters:")
    print("    • Transaction Amount: $15,000")
    print("    • AML Review: Completed ✓")
    print("    • Manager Approval: Yes ✓")
    print("    • OFAC Screening: Passed ✓")
    
    result4 = await system.execute_with_governance(
        user_id='senior_teller_004',
        action='process transaction',
        parameters={
            'transaction_amount': 15000,
            'aml_review_completed': True,
            'manager_approval': True,
            'ofac_screening_passed': True
        }
    )
    
    print(f"\n{'✅ DECISION: APPROVED' if result4['status'] == 'approved' else '❌ DECISION: BLOCKED'}")
    print(f"Risk Score: {result4['enforcement']['risk_score']}")
    
    return [result1, result2, result3, result4]


async def demo_audit_trail(system, results):
    """Demonstrate audit trail capabilities"""
    
    print_banner("DEMO 4: AUDIT TRAIL & COMPLIANCE REPORTING")
    
    audit_trail = system.get_audit_trail()
    
    print_section("📜 Audit Trail Summary")
    
    print(f"Total Audit Entries: {len(audit_trail)}")
    
    # Statistics
    approved = sum(1 for entry in audit_trail if entry['approved'])
    blocked = len(audit_trail) - approved
    
    print(f"\nApproval Statistics:")
    print(f"  • Approved: {approved} ({approved/len(audit_trail)*100:.1f}%)")
    print(f"  • Blocked: {blocked} ({blocked/len(audit_trail)*100:.1f}%)")
    
    avg_risk = sum(entry['risk_score'] for entry in audit_trail) / len(audit_trail)
    print(f"\nAverage Risk Score: {avg_risk:.2f}")
    
    # Detailed audit entries
    print_section("📋 Detailed Audit Entries")
    
    for i, entry in enumerate(audit_trail, 1):
        status_icon = "✅" if entry['approved'] else "❌"
        print(f"\n{status_icon} Entry {i}:")
        print(f"   Request ID: {entry['request_id']}")
        print(f"   Timestamp: {entry['timestamp']}")
        print(f"   User: {entry['user_id']}")
        print(f"   Action: {entry['action']}")
        print(f"   Status: {'APPROVED' if entry['approved'] else 'BLOCKED'}")
        print(f"   Risk Score: {entry['risk_score']}")
        print(f"   Rules Evaluated: {entry['rules_evaluated']}")
        
        if entry['violations']:
            print(f"   Violations:")
            for violation in entry['violations']:
                print(f"     • {violation}")
    
    # Export audit trail
    print_section("💾 Audit Trail Export")
    
    audit_export = {
        'export_timestamp': datetime.now().isoformat(),
        'total_entries': len(audit_trail),
        'summary': {
            'approved': approved,
            'blocked': blocked,
            'average_risk_score': avg_risk
        },
        'entries': audit_trail
    }
    
    export_filename = f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(export_filename, 'w') as f:
        json.dump(audit_export, f, indent=2)
    
    print(f"Audit trail exported to: {export_filename}")
    print(f"File size: {len(json.dumps(audit_export))} bytes")


async def demo_advanced_scenarios(system):
    """Demonstrate advanced governance scenarios"""
    
    print_banner("DEMO 5: ADVANCED GOVERNANCE SCENARIOS")
    
    # Scenario 1: Data Retention Compliance
    print_section("Advanced Scenario 1: Data Retention Validation")
    
    print("Attempting to archive transaction records with 2-year retention...")
    result = await system.execute_with_governance(
        user_id='archive_system',
        action='archive transaction records',
        parameters={
            'record_type': 'transaction',
            'retention_days': 730,  # 2 years - should fail (requires 7)
            'encryption_enabled': True
        }
    )
    
    print(f"Decision: {'APPROVED' if result['status'] == 'approved' else 'BLOCKED'}")
    
    # Scenario 2: Multi-Factor Authentication
    print_section("Advanced Scenario 2: Remote Access Control")
    
    print("Remote production access without MFA...")
    result = await system.execute_with_governance(
        user_id='developer_005',
        action='access production database',
        parameters={
            'access_type': 'remote',
            'mfa_enabled': False,  # Should fail
            'approved_by_security_team': True
        }
    )
    
    print(f"Decision: {'APPROVED' if result['status'] == 'approved' else 'BLOCKED'}")
    if result['enforcement']['validation']['violations']:
        for violation in result['enforcement']['validation']['violations']:
            print(f"  Violation: {violation}")
    
    # Scenario 3: Vendor Data Sharing
    print_section("Advanced Scenario 3: Third-Party Data Sharing")
    
    print("Sharing customer data with vendor without legal review...")
    result = await system.execute_with_governance(
        user_id='business_analyst_006',
        action='share data with third party',
        parameters={
            'contains_pii': True,
            'encryption_enabled': True,
            'legal_review_completed': False,  # Should fail
            'data_processing_agreement': False  # Should fail
        }
    )
    
    print(f"Decision: {'APPROVED' if result['status'] == 'approved' else 'BLOCKED'}")
    if result['enforcement']['validation']['violations']:
        for violation in result['enforcement']['validation']['violations']:
            print(f"  Violation: {violation}")


async def main():
    """Run complete demonstration"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║         GRC MULTI-AGENT GOVERNANCE SYSTEM - COMPREHENSIVE DEMO            ║")
    print("║                                                                            ║")
    print("║         Deterministic Control Over Probabilistic AI Agents                ║")
    print("║         For Regulated Industries (Banking, Finance, Healthcare)           ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    try:
        # Demo 1: Policy Loading
        system = await demo_policy_loading()
        
        # Demo 2: Rule Generation
        await demo_rule_generation(system)
        
        # Demo 3: Governance Enforcement
        results = await demo_governance_enforcement(system)
        
        # Demo 4: Audit Trail
        await demo_audit_trail(system, results)
        
        # Demo 5: Advanced Scenarios
        await demo_advanced_scenarios(system)
        
        # Final Summary
        print_banner("DEMO COMPLETE - SYSTEM SUMMARY")
        
        print("✅ Successfully Demonstrated:")
        print("   1. Policy document parsing and rule extraction")
        print("   2. Automatic Python code generation from policies")
        print("   3. JSON export for system integration")
        print("   4. Real-time governance enforcement")
        print("   5. Risk scoring and violation detection")
        print("   6. Comprehensive audit trail")
        print("   7. Multi-scenario compliance validation")
        
        print("\n📊 System Statistics:")
        print(f"   • Total Policies Loaded: {len(system.sessions) + 1}")
        print(f"   • Active Rules: {len(system.governance_enforcer.active_rules)}")
        print(f"   • Governance Checks Performed: {len(system.get_audit_trail())}")
        print(f"   • Violations Detected: {sum(len(e['violations']) for e in system.get_audit_trail())}")
        
        print("\n🎯 Key Benefits:")
        print("   • Deterministic governance over AI agents")
        print("   • Automated compliance enforcement")
        print("   • Policy-as-Code approach")
        print("   • Complete audit trail for regulators")
        print("   • Real-time risk scoring")
        print("   • Multi-format policy support")
        
        print("\n📁 Generated Files:")
        print("   • compliance_rules_*.py - Executable Python rules")
        print("   • grc_rules_*.json - JSON rule definitions")
        print("   • audit_trail_*.json - Complete audit trail")
        
        print("\n🚀 Next Steps:")
        print("   1. Review generated rules in exported files")
        print("   2. Integrate with your agent system")
        print("   3. Upload additional policy documents")
        print("   4. Customize rule generators for your needs")
        print("   5. Deploy governance layer in production")
        
        print("\n" + "="*80)
        print("For web interface, run: streamlit run streamlit_app.py")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
