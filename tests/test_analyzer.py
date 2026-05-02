import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch

SAMPLE_SCORE_DATA = {
    'total': 48,
    'grade': 'E',
    'org_type': 'municipal',
    'axes': {
        'identity': {'score': 60, 'issues': ['MFAカバレッジ不足: 55%', '特権アカウント棚卸し未実施']},
        'device': {'score': 65, 'issues': ['MDMカバレッジ不足: 70%']},
        'application': {'score': 20, 'issues': ['SAML/OAuth統合率: 60%', 'シャドーIT: 8件', 'API認証未実装']},
        'network': {'score': 35, 'issues': ['VPN依存', 'マイクロセグメンテーション未実装']},
    },
}


def make_mock_response(text: str):
    mock_content = MagicMock()
    mock_content.text = text
    mock_response = MagicMock()
    mock_response.content = [mock_content]
    return mock_response


@patch('analyzer.anthropic.Anthropic')
def test_analyze_maturity_returns_list(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response(
        "1. 全職員へのMFA強制適用を3ヶ月以内に完了してください\n"
        "2. シャドーIT8件の棚卸しと承認/廃止判断を実施してください\n"
        "3. ZTNA製品の評価を開始し、VPN依存からの脱却計画を策定してください"
    )
    from analyzer import analyze_maturity
    result = analyze_maturity(SAMPLE_SCORE_DATA)
    assert isinstance(result, list)
    assert len(result) >= 1


@patch('analyzer.anthropic.Anthropic')
def test_analyze_maturity_returns_strings(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response("1. 提案A\n2. 提案B")
    from analyzer import analyze_maturity
    result = analyze_maturity(SAMPLE_SCORE_DATA)
    for item in result:
        assert isinstance(item, str) and len(item) > 0


@patch('analyzer.anthropic.Anthropic')
def test_analyze_maturity_calls_claude(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response("1. 提案")
    from analyzer import analyze_maturity
    analyze_maturity(SAMPLE_SCORE_DATA)
    mock_client.messages.create.assert_called_once()
    kwargs = mock_client.messages.create.call_args[1]
    assert kwargs['model'] == 'claude-sonnet-4-6'


@patch('analyzer.anthropic.Anthropic')
def test_analyze_maturity_prompt_includes_org_type(mock_cls):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_client.messages.create.return_value = make_mock_response("1. 提案")
    from analyzer import analyze_maturity
    analyze_maturity(SAMPLE_SCORE_DATA)
    kwargs = mock_client.messages.create.call_args[1]
    prompt = kwargs['messages'][0]['content']
    assert 'municipal' in prompt or '自治体' in prompt or '48' in prompt
