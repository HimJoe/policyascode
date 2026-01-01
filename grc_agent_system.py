"""
GRC Policy-to-Code Multi-Agent System
Deterministic governance layer over probabilistic AI agents for regulated industries
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
from datetime import datetime
import hashlib


class ComplianceLevel(Enum):
    """Compliance requirement levels"""
    MANDATORY = "mandatory"
    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class AgentRole(Enum):
    """Different agent roles in the system"""
    POLICY_PARSER = "policy_parser"
    RULE_GENERATOR = "rule_generator"
    COMPLIANCE_VALIDATOR = "compliance_validator"
    GOVERNANCE_ENFORCER = "governance_enforcer"
    AUDIT_LOGGER = "audit_logger"
    EXECUTOR = "executor"


@dataclass
class PolicyRule:
    """Structured policy rule extracted from documents"""
    rule_id: str
    category: str  # Governance, Risk, Compliance
    subcategory: str
    description: str
    requirement: str
    compliance_level: ComplianceLevel
    constraints: List[Dict[str, Any]] = field(default_factory=list)
    validation_logic: Optional[str] = None
    source_document: str = ""
    section_reference: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "category": self.category,
            "subcategory": self.subcategory,
            "description": self.description,
            "requirement": self.requirement,
            "compliance_level": self.compliance_level.value,
            "constraints": self.constraints,
            "validation_logic": self.validation_logic,
            "source_document": self.source_document,
            "section_reference": self.section_reference
        }


@dataclass
class ExecutionContext:
    """Context for agent execution with governance controls"""
    request_id: str
    timestamp: datetime
    user_id: str
    action: str
    parameters: Dict[str, Any]
    applicable_rules: List[PolicyRule] = field(default_factory=list)
    compliance_checks: Dict[str, bool] = field(default_factory=dict)
    risk_score: float = 0.0
    approved: bool = False
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)


class PolicyParser:
    """Agent responsible for parsing policy documents into structured rules"""
    
    def __init__(self):
        self.role = AgentRole.POLICY_PARSER
        
    async def parse_text(self, content: str, source: str) -> List[PolicyRule]:
        """Parse text content into policy rules"""
        rules = []
        
        # Enhanced parsing logic for GRC documents
        # Looking for common patterns in regulatory documents
        
        patterns = {
            'mandatory': r'(?i)(must|shall|required to|mandatory)',
            'prohibited': r'(?i)(must not|shall not|prohibited|forbidden)',
            'recommended': r'(?i)(should|recommended|advised to)',
            'data_retention': r'(?i)(retain|retention period|keep.*for|maintain.*(?:for|during))\s+(\d+)\s+(days?|months?|years?)',
            'approval_required': r'(?i)(approval required|must be approved|requires authorization)',
            'encryption': r'(?i)(encrypt|encryption|encrypted)',
            'pii_handling': r'(?i)(personally identifiable|PII|personal data|customer information)',
        }
        
        lines = content.split('\n')
        current_section = "General"
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if re.match(r'^[A-Z\s]{5,}$', line) or re.match(r'^\d+\.', line):
                current_section = line
                continue
            
            # Extract rules based on patterns
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, line):
                    rule_id = hashlib.md5(f"{source}:{i}:{line}".encode()).hexdigest()[:12]
                    
                    # Determine compliance level
                    if re.search(patterns['mandatory'], line):
                        level = ComplianceLevel.MANDATORY
                    elif re.search(patterns['prohibited'], line):
                        level = ComplianceLevel.MANDATORY
                    elif re.search(patterns['recommended'], line):
                        level = ComplianceLevel.RECOMMENDED
                    else:
                        level = ComplianceLevel.REQUIRED
                    
                    # Extract constraints
                    constraints = []
                    
                    # Data retention constraint
                    retention_match = re.search(patterns['data_retention'], line)
                    if retention_match:
                        constraints.append({
                            "type": "data_retention",
                            "duration": f"{retention_match.group(2)} {retention_match.group(3)}"
                        })
                    
                    # Encryption constraint
                    if re.search(patterns['encryption'], line):
                        constraints.append({
                            "type": "encryption_required",
                            "algorithm": "AES-256"  # Default
                        })
                    
                    # PII handling
                    if re.search(patterns['pii_handling'], line):
                        constraints.append({
                            "type": "pii_handling",
                            "requires_consent": True,
                            "requires_encryption": True
                        })
                    
                    rule = PolicyRule(
                        rule_id=rule_id,
                        category=self._categorize_rule(line),
                        subcategory=pattern_name,
                        description=line,
                        requirement=line,
                        compliance_level=level,
                        constraints=constraints,
                        source_document=source,
                        section_reference=current_section
                    )
                    rules.append(rule)
                    break  # Only match first pattern per line
        
        return rules
    
    def _categorize_rule(self, text: str) -> str:
        """Categorize rule into Governance, Risk, or Compliance"""
        governance_keywords = ['approval', 'authorization', 'oversight', 'board', 'committee']
        risk_keywords = ['risk', 'threat', 'vulnerability', 'security', 'breach']
        
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in governance_keywords):
            return "Governance"
        elif any(kw in text_lower for kw in risk_keywords):
            return "Risk"
        else:
            return "Compliance"


class RuleGenerator:
    """Agent that generates executable Python code from policy rules"""
    
    def __init__(self):
        self.role = AgentRole.RULE_GENERATOR
    
    def generate_rule_code(self, rule: PolicyRule) -> str:
        """Generate Python validation function for a rule"""
        
        function_name = f"validate_{rule.rule_id}"
        
        code_template = f'''
def {function_name}(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rule: {rule.description}
    Category: {rule.category} - {rule.subcategory}
    Level: {rule.compliance_level.value}
    Source: {rule.source_document}
    """
    result = {{
        "rule_id": "{rule.rule_id}",
        "passed": True,
        "violations": [],
        "warnings": []
    }}
    
'''
        
        # Generate validation logic based on constraints
        for constraint in rule.constraints:
            if constraint['type'] == 'encryption_required':
                code_template += '''
    # Check encryption requirement
    if not context.get('encryption_enabled', False):
        result["passed"] = False
        result["violations"].append("Encryption is required but not enabled")
'''
            
            elif constraint['type'] == 'pii_handling':
                code_template += '''
    # Check PII handling requirements
    if context.get('contains_pii', False):
        if not context.get('user_consent', False):
            result["passed"] = False
            result["violations"].append("PII processing requires user consent")
        if not context.get('encryption_enabled', False):
            result["passed"] = False
            result["violations"].append("PII must be encrypted")
'''
            
            elif constraint['type'] == 'data_retention':
                code_template += f'''
    # Check data retention policy
    retention_days = context.get('retention_days', 0)
    max_retention = "{constraint['duration']}"
    # Additional retention validation logic here
'''
        
        # Add compliance level check
        if rule.compliance_level == ComplianceLevel.MANDATORY:
            code_template += '''
    # Mandatory rule - must pass
    if not result["passed"]:
        result["severity"] = "CRITICAL"
'''
        
        code_template += '''
    return result
'''
        
        return code_template
    
    def generate_rule_module(self, rules: List[PolicyRule]) -> str:
        """Generate complete Python module with all rules"""
        
        module_code = '''"""
Auto-generated GRC Compliance Rules
Generated from policy documents
DO NOT EDIT MANUALLY
"""

from typing import Dict, Any, List
from datetime import datetime

'''
        
        # Generate all rule functions
        for rule in rules:
            module_code += self.generate_rule_code(rule)
            module_code += "\n"
        
        # Generate rule registry
        module_code += '''

# Rule Registry
COMPLIANCE_RULES = {
'''
        
        for rule in rules:
            module_code += f'    "{rule.rule_id}": validate_{rule.rule_id},\n'
        
        module_code += '''}

def validate_all_rules(context: Dict[str, Any]) -> Dict[str, Any]:
    """Validate context against all compliance rules"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "overall_passed": True,
        "rules_checked": len(COMPLIANCE_RULES),
        "violations": [],
        "warnings": [],
        "details": {}
    }
    
    for rule_id, validator in COMPLIANCE_RULES.items():
        rule_result = validator(context)
        results["details"][rule_id] = rule_result
        
        if not rule_result["passed"]:
            results["overall_passed"] = False
            results["violations"].extend(rule_result.get("violations", []))
        
        results["warnings"].extend(rule_result.get("warnings", []))
    
    return results
'''
        
        return module_code


class ComplianceValidator:
    """Agent that validates actions against generated rules"""
    
    def __init__(self, rules_module: Optional[Any] = None):
        self.role = AgentRole.COMPLIANCE_VALIDATOR
        self.rules_module = rules_module
    
    async def validate(self, context: ExecutionContext) -> Dict[str, Any]:
        """Validate execution context against all applicable rules"""
        
        validation_result = {
            "context_id": context.request_id,
            "timestamp": datetime.now().isoformat(),
            "passed": True,
            "violations": [],
            "warnings": [],
            "risk_score": 0.0,
            "rules_evaluated": []
        }
        
        # Evaluate each applicable rule
        for rule in context.applicable_rules:
            rule_check = self._evaluate_rule(rule, context)
            validation_result["rules_evaluated"].append(rule_check)
            
            if not rule_check["passed"]:
                validation_result["passed"] = False
                validation_result["violations"].extend(rule_check.get("violations", []))
                
                # Increase risk score for violations
                if rule.compliance_level == ComplianceLevel.MANDATORY:
                    validation_result["risk_score"] += 10.0
                elif rule.compliance_level == ComplianceLevel.REQUIRED:
                    validation_result["risk_score"] += 5.0
        
        return validation_result
    
    def _evaluate_rule(self, rule: PolicyRule, context: ExecutionContext) -> Dict[str, Any]:
        """Evaluate a single rule against context"""
        
        result = {
            "rule_id": rule.rule_id,
            "category": rule.category,
            "passed": True,
            "violations": []
        }
        
        # Check constraints
        for constraint in rule.constraints:
            if constraint['type'] == 'encryption_required':
                if not context.parameters.get('encryption_enabled', False):
                    result["passed"] = False
                    result["violations"].append(
                        f"Violation: {rule.description} - Encryption not enabled"
                    )
            
            # Add more constraint checks here
        
        return result


class GovernanceEnforcer:
    """Master agent that enforces governance policies over all other agents"""
    
    def __init__(self):
        self.role = AgentRole.GOVERNANCE_ENFORCER
        self.policy_parser = PolicyParser()
        self.rule_generator = RuleGenerator()
        self.validator = ComplianceValidator()
        self.audit_log: List[Dict[str, Any]] = []
        self.active_rules: List[PolicyRule] = []
    
    async def load_policies(self, content: str, source: str, file_type: str) -> Dict[str, Any]:
        """Load and parse policy documents"""
        
        print(f"📋 Loading policy from: {source} (type: {file_type})")
        
        # Parse policies
        rules = await self.policy_parser.parse_text(content, source)
        self.active_rules.extend(rules)
        
        print(f"✅ Extracted {len(rules)} policy rules")
        
        # Generate rule code
        rule_code = self.rule_generator.generate_rule_module(rules)
        
        # Create JSON representation
        rules_json = {
            "metadata": {
                "source": source,
                "generated_at": datetime.now().isoformat(),
                "total_rules": len(rules)
            },
            "rules": [rule.to_dict() for rule in rules]
        }
        
        return {
            "rules": rules,
            "rules_json": rules_json,
            "python_code": rule_code,
            "summary": {
                "total_rules": len(rules),
                "by_category": self._count_by_category(rules),
                "by_compliance_level": self._count_by_compliance_level(rules)
            }
        }
    
    async def enforce_governance(self, context: ExecutionContext) -> Dict[str, Any]:
        """Enforce governance rules on an execution context"""
        
        # Find applicable rules
        context.applicable_rules = self._find_applicable_rules(context)
        
        # Validate against rules
        validation = await self.validator.validate(context)
        
        # Make governance decision
        context.approved = validation["passed"]
        context.risk_score = validation["risk_score"]
        
        # Log to audit trail
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "request_id": context.request_id,
            "action": context.action,
            "user_id": context.user_id,
            "approved": context.approved,
            "risk_score": context.risk_score,
            "violations": validation["violations"],
            "rules_evaluated": len(context.applicable_rules)
        }
        
        self.audit_log.append(audit_entry)
        context.audit_trail.append(audit_entry)
        
        return {
            "approved": context.approved,
            "risk_score": context.risk_score,
            "validation": validation,
            "audit_entry": audit_entry
        }
    
    def _find_applicable_rules(self, context: ExecutionContext) -> List[PolicyRule]:
        """Find rules applicable to the execution context"""
        applicable = []
        
        for rule in self.active_rules:
            # Match based on action type, category, etc.
            if self._rule_applies(rule, context):
                applicable.append(rule)
        
        return applicable
    
    def _rule_applies(self, rule: PolicyRule, context: ExecutionContext) -> bool:
        """Check if a rule applies to the given context"""
        # Basic matching - can be enhanced with more sophisticated logic
        action_lower = context.action.lower()
        
        # Check if rule keywords appear in action
        rule_text = (rule.description + " " + rule.requirement).lower()
        
        # Simple keyword matching
        if any(word in rule_text for word in action_lower.split()):
            return True
        
        return False
    
    def _count_by_category(self, rules: List[PolicyRule]) -> Dict[str, int]:
        """Count rules by category"""
        counts = {}
        for rule in rules:
            counts[rule.category] = counts.get(rule.category, 0) + 1
        return counts
    
    def _count_by_compliance_level(self, rules: List[PolicyRule]) -> Dict[str, int]:
        """Count rules by compliance level"""
        counts = {}
        for rule in rules:
            level = rule.compliance_level.value
            counts[level] = counts.get(level, 0) + 1
        return counts


class GRCMultiAgentSystem:
    """Main orchestrator for the GRC multi-agent system"""
    
    def __init__(self):
        self.governance_enforcer = GovernanceEnforcer()
        self.sessions: Dict[str, Any] = {}
    
    async def upload_policy(self, content: str, filename: str, file_type: str) -> Dict[str, Any]:
        """Upload and process a policy document"""
        
        print(f"\n{'='*70}")
        print(f"🔐 GRC POLICY UPLOAD - {filename}")
        print(f"{'='*70}\n")
        
        result = await self.governance_enforcer.load_policies(content, filename, file_type)
        
        return result
    
    async def execute_with_governance(
        self, 
        user_id: str,
        action: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute an action with full governance controls"""
        
        # Create execution context
        context = ExecutionContext(
            request_id=hashlib.md5(f"{user_id}:{action}:{datetime.now()}".encode()).hexdigest()[:16],
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            parameters=parameters
        )
        
        print(f"\n{'='*70}")
        print(f"⚖️  GOVERNANCE CHECK - {action}")
        print(f"{'='*70}\n")
        
        # Enforce governance
        enforcement_result = await self.governance_enforcer.enforce_governance(context)
        
        if enforcement_result["approved"]:
            print(f"✅ Action APPROVED (Risk Score: {enforcement_result['risk_score']})")
            return {
                "status": "approved",
                "context": context,
                "enforcement": enforcement_result
            }
        else:
            print(f"❌ Action BLOCKED")
            print(f"Violations: {len(enforcement_result['validation']['violations'])}")
            for violation in enforcement_result['validation']['violations']:
                print(f"  - {violation}")
            
            return {
                "status": "blocked",
                "context": context,
                "enforcement": enforcement_result
            }
    
    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Get complete audit trail"""
        return self.governance_enforcer.audit_log
    
    def export_rules_json(self) -> Dict[str, Any]:
        """Export all rules as JSON"""
        return {
            "rules": [rule.to_dict() for rule in self.governance_enforcer.active_rules],
            "total_count": len(self.governance_enforcer.active_rules)
        }
    
    def export_rules_python(self) -> str:
        """Export all rules as Python code"""
        return self.governance_enforcer.rule_generator.generate_rule_module(
            self.governance_enforcer.active_rules
        )


# Example usage
async def main():
    """Demo of the GRC multi-agent system"""
    
    system = GRCMultiAgentSystem()
    
    # Sample banking policy
    sample_policy = """
    BANKING DATA GOVERNANCE POLICY
    
    1. DATA PROTECTION REQUIREMENTS
    
    1.1 Customer data must be encrypted at rest and in transit using AES-256 encryption.
    
    1.2 Personally identifiable information (PII) shall not be processed without explicit customer consent.
    
    1.3 All customer data access must be approved by a data steward.
    
    2. DATA RETENTION POLICY
    
    2.1 Transaction records must be retained for 7 years as per regulatory requirements.
    
    2.2 Customer account information shall be retained for 10 years after account closure.
    
    3. RISK MANAGEMENT
    
    3.1 High-risk transactions exceeding $10,000 must be flagged for review.
    
    3.2 Suspicious activity must be reported within 24 hours.
    
    4. COMPLIANCE REQUIREMENTS
    
    4.1 All data transfers to third parties require legal review and approval.
    
    4.2 Annual compliance audits are mandatory for all data processing systems.
    """
    
    # Upload policy
    result = await system.upload_policy(sample_policy, "banking_policy.txt", "text")
    
    print(f"\n📊 Policy Summary:")
    print(f"  Total Rules: {result['summary']['total_rules']}")
    print(f"  By Category: {result['summary']['by_category']}")
    print(f"  By Level: {result['summary']['by_compliance_level']}")
    
    # Test governance enforcement
    print("\n" + "="*70)
    print("Testing Governance Enforcement")
    print("="*70)
    
    # Test 1: Action without encryption (should be blocked)
    await system.execute_with_governance(
        user_id="user123",
        action="process customer data",
        parameters={
            "contains_pii": True,
            "encryption_enabled": False,
            "user_consent": True
        }
    )
    
    # Test 2: Compliant action (should be approved)
    await system.execute_with_governance(
        user_id="user123",
        action="process customer data",
        parameters={
            "contains_pii": True,
            "encryption_enabled": True,
            "user_consent": True
        }
    )


if __name__ == "__main__":
    asyncio.run(main())
