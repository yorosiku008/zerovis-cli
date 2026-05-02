from typing import Dict, List
import anthropic

ORG_TYPE_LABELS = {
    'general': '一般企業',
    'municipal': '地方自治体',
    'manufacturing': '製造業',
    'medical': '医療機関',
    'finance': '金融機関',
}

MATURITY_ANALYSIS_PROMPT = """あなたはゼロトラストセキュリティの専門家です。
以下のZT成熟度評価データを分析し、{org_label}が優先すべきゼロトラスト移行アクションを3件、日本語で簡潔に提示してください。

【評価データ】
組織種別: {org_label}
総合スコア: {total}/100  グレード: {grade}

軸別スコア:
{axes_summary}

主な問題点:
{issues}

【回答形式】
1. [具体的な移行アクション] → [期待効果・対応ガイドライン]
2. [具体的な移行アクション] → [期待効果・対応ガイドライン]
3. [具体的な移行アクション] → [期待効果・対応ガイドライン]

NISC・総務省ガイドラインの要件も踏まえて、実施優先度が高い順に提案してください。"""


def analyze_maturity(score_data: Dict) -> List[str]:
    client = anthropic.Anthropic()

    org_type = score_data.get('org_type', 'general')
    org_label = ORG_TYPE_LABELS.get(org_type, org_type)

    axes = score_data.get('axes', {})
    axes_summary = '\n'.join(
        f"  {k}: {v['score']}点" for k, v in axes.items()
    )

    all_issues = []
    for v in axes.values():
        all_issues.extend(v.get('issues', []))
    issues_text = '\n'.join(f"  - {i}" for i in all_issues) or '  なし'

    prompt = MATURITY_ANALYSIS_PROMPT.format(
        org_label=org_label,
        total=score_data['total'],
        grade=score_data['grade'],
        axes_summary=axes_summary,
        issues=issues_text,
    )

    response = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=500,
        messages=[{'role': 'user', 'content': prompt}],
    )

    lines = response.content[0].text.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]
