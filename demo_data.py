from typing import Dict


def get_demo_score(org_type: str = 'general') -> Dict:
    from scorer import build_score

    assessment = {
        'identity': {
            'mfa_coverage_pct': 55.0,
            'sso_enabled': True,
            'privileged_accounts_reviewed': False,
        },
        'device': {
            'mdm_coverage_pct': 70.0,
            'edr_enabled': True,
            'os_patch_compliance_pct': 75.0,
        },
        'application': {
            'saml_oauth_pct': 60.0,
            'shadow_it_count': 8,
            'api_auth_enforced': False,
        },
        'network': {
            'vpn_dependent': True,
            'microsegmentation': False,
            'traffic_inspection': True,
        },
    }

    result = build_score(assessment)
    result['org_type'] = org_type
    return result
