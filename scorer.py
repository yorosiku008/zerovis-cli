from typing import Dict, List

WEIGHTS = {
    'identity':    0.35,
    'device':      0.25,
    'application': 0.25,
    'network':     0.15,
}

GRADES = [(90, 'S'), (80, 'A'), (70, 'B'), (60, 'C'), (50, 'D'), (0, 'E')]


def score_identity(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    mfa = data.get('mfa_coverage_pct', 100.0)
    if mfa < 50:
        score -= 40
        issues.append(f'MFAカバレッジが低い: {mfa:.0f}%（全ユーザーへの適用が必要）')
    elif mfa < 80:
        score -= 20
        issues.append(f'MFAカバレッジ不足: {mfa:.0f}%（80%以上を推奨）')

    if not data.get('sso_enabled', True):
        score -= 20
        issues.append('SSOが未導入（IDプロバイダーとの統合を推奨）')

    if not data.get('privileged_accounts_reviewed', True):
        score -= 20
        issues.append('特権アカウントの棚卸し・レビューが未実施')

    return {'score': max(0, score), 'issues': issues}


def score_device(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    mdm = data.get('mdm_coverage_pct', 100.0)
    if mdm < 50:
        score -= 35
        issues.append(f'MDM管理対象デバイスが少ない: {mdm:.0f}%')
    elif mdm < 80:
        score -= 15
        issues.append(f'MDMカバレッジ不足: {mdm:.0f}%（80%以上を推奨）')

    if not data.get('edr_enabled', True):
        score -= 25
        issues.append('EDR/XDRが未導入（エンドポイント検知・対応が必要）')

    patch_pct = data.get('os_patch_compliance_pct', 100.0)
    if patch_pct < 80:
        score -= 20
        issues.append(f'OSパッチ適用率が低い: {patch_pct:.0f}%')

    return {'score': max(0, score), 'issues': issues}


def score_application(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    saml_pct = data.get('saml_oauth_pct', 100.0)
    if saml_pct < 70:
        score -= 30
        issues.append(f'SAML/OAuth統合率が低い: {saml_pct:.0f}%（認証の標準化が必要）')
    elif saml_pct < 90:
        score -= 10
        issues.append(f'SAML/OAuth統合率: {saml_pct:.0f}%（90%以上を推奨）')

    shadow_it = data.get('shadow_it_count', 0)
    if shadow_it > 0:
        score -= min(shadow_it * 5, 30)
        issues.append(f'未承認SaaSアプリ（シャドーIT）: {shadow_it}件')

    if not data.get('api_auth_enforced', True):
        score -= 20
        issues.append('APIレベルの認証・認可が未実装')

    return {'score': max(0, score), 'issues': issues}


def score_network(data: Dict) -> Dict:
    score = 100
    issues: List[str] = []

    if data.get('vpn_dependent', False):
        score -= 30
        issues.append('VPN依存の境界型セキュリティ（ZTNA移行を検討）')

    if not data.get('microsegmentation', True):
        score -= 35
        issues.append('マイクロセグメンテーションが未実装（東西トラフィックの制御が不可）')

    if not data.get('traffic_inspection', True):
        score -= 20
        issues.append('内部通信の検査・ログ取得が未整備')

    return {'score': max(0, score), 'issues': issues}


def calculate_maturity_score(axes: Dict) -> Dict:
    total = sum(
        axes[axis]['score'] * weight
        for axis, weight in WEIGHTS.items()
        if axis in axes
    )
    total = round(total)

    grade = 'E'
    for threshold, g in GRADES:
        if total >= threshold:
            grade = g
            break

    return {'total': total, 'grade': grade}


def build_score(assessment: Dict) -> Dict:
    axes = {
        'identity':    score_identity(assessment.get('identity', {})),
        'device':      score_device(assessment.get('device', {})),
        'application': score_application(assessment.get('application', {})),
        'network':     score_network(assessment.get('network', {})),
    }
    summary = calculate_maturity_score(axes)
    return {**summary, 'axes': axes}
