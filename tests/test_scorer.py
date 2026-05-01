import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── score_identity ─────────────────────────────────────────

def test_score_identity_returns_dict():
    from scorer import score_identity
    result = score_identity({'mfa_coverage_pct': 100.0, 'sso_enabled': True, 'privileged_accounts_reviewed': True})
    assert isinstance(result, dict)
    assert 'score' in result and 'issues' in result


def test_score_identity_perfect():
    from scorer import score_identity
    result = score_identity({'mfa_coverage_pct': 100.0, 'sso_enabled': True, 'privileged_accounts_reviewed': True})
    assert result['score'] == 100


def test_score_identity_low_mfa_reduces_score():
    from scorer import score_identity
    result = score_identity({'mfa_coverage_pct': 30.0, 'sso_enabled': True, 'privileged_accounts_reviewed': True})
    assert result['score'] < 70
    assert len(result['issues']) > 0


def test_score_identity_no_sso_reduces_score():
    from scorer import score_identity
    result = score_identity({'mfa_coverage_pct': 100.0, 'sso_enabled': False, 'privileged_accounts_reviewed': True})
    assert result['score'] < 100


def test_score_identity_unreviewed_privileged_reduces_score():
    from scorer import score_identity
    result = score_identity({'mfa_coverage_pct': 100.0, 'sso_enabled': True, 'privileged_accounts_reviewed': False})
    assert result['score'] < 100


# ── score_device ───────────────────────────────────────────

def test_score_device_returns_dict():
    from scorer import score_device
    result = score_device({'mdm_coverage_pct': 100.0, 'edr_enabled': True, 'os_patch_compliance_pct': 100.0})
    assert isinstance(result, dict)


def test_score_device_perfect():
    from scorer import score_device
    result = score_device({'mdm_coverage_pct': 100.0, 'edr_enabled': True, 'os_patch_compliance_pct': 100.0})
    assert result['score'] == 100


def test_score_device_low_mdm_reduces_score():
    from scorer import score_device
    result = score_device({'mdm_coverage_pct': 20.0, 'edr_enabled': True, 'os_patch_compliance_pct': 100.0})
    assert result['score'] < 70


def test_score_device_no_edr_reduces_score():
    from scorer import score_device
    result = score_device({'mdm_coverage_pct': 100.0, 'edr_enabled': False, 'os_patch_compliance_pct': 100.0})
    assert result['score'] < 100


# ── score_application ──────────────────────────────────────

def test_score_application_returns_dict():
    from scorer import score_application
    result = score_application({'saml_oauth_pct': 100.0, 'shadow_it_count': 0, 'api_auth_enforced': True})
    assert isinstance(result, dict)


def test_score_application_perfect():
    from scorer import score_application
    result = score_application({'saml_oauth_pct': 100.0, 'shadow_it_count': 0, 'api_auth_enforced': True})
    assert result['score'] == 100


def test_score_application_shadow_it_reduces_score():
    from scorer import score_application
    result = score_application({'saml_oauth_pct': 100.0, 'shadow_it_count': 5, 'api_auth_enforced': True})
    assert result['score'] < 100


# ── score_network ──────────────────────────────────────────

def test_score_network_returns_dict():
    from scorer import score_network
    result = score_network({'vpn_dependent': False, 'microsegmentation': True, 'traffic_inspection': True})
    assert isinstance(result, dict)


def test_score_network_perfect():
    from scorer import score_network
    result = score_network({'vpn_dependent': False, 'microsegmentation': True, 'traffic_inspection': True})
    assert result['score'] == 100


def test_score_network_vpn_dependent_reduces_score():
    from scorer import score_network
    result = score_network({'vpn_dependent': True, 'microsegmentation': False, 'traffic_inspection': False})
    assert result['score'] <= 40


# ── calculate_maturity_score ───────────────────────────────

def test_calculate_maturity_score_returns_dict():
    from scorer import calculate_maturity_score
    axes = {k: {'score': 80, 'issues': []} for k in ['identity', 'device', 'application', 'network']}
    result = calculate_maturity_score(axes)
    assert 'total' in result and 'grade' in result


def test_calculate_maturity_score_all_perfect_is_s():
    from scorer import calculate_maturity_score
    axes = {k: {'score': 100, 'issues': []} for k in ['identity', 'device', 'application', 'network']}
    result = calculate_maturity_score(axes)
    assert result['total'] == 100 and result['grade'] == 'S'


def test_calculate_maturity_score_grade_c():
    from scorer import calculate_maturity_score
    axes = {k: {'score': 65, 'issues': []} for k in ['identity', 'device', 'application', 'network']}
    result = calculate_maturity_score(axes)
    assert result['grade'] == 'C'


def test_calculate_maturity_score_grade_d():
    from scorer import calculate_maturity_score
    axes = {k: {'score': 55, 'issues': []} for k in ['identity', 'device', 'application', 'network']}
    result = calculate_maturity_score(axes)
    assert result['grade'] == 'D'
