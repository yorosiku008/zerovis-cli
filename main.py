import argparse
from datetime import datetime
from pathlib import Path

from demo_data import get_demo_score
from report import print_report, build_md_report, save_md_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='ZeroVis JP — ゼロトラスト成熟度評価CLI')
    parser.add_argument('--demo', action='store_true', help='デモデータで動作確認')
    parser.add_argument('--org-type', default='general',
                        choices=['general', 'municipal', 'manufacturing', 'medical', 'finance'],
                        help='組織種別')
    parser.add_argument('--ai', action='store_true', help='Claude AIによる移行ロードマップを生成（ANTHROPIC_API_KEY必要）')
    parser.add_argument('--output-md', action='store_true', help='MDレポートを出力')
    return parser.parse_args(argv)


def run(demo: bool = False, org_type: str = 'general', ai: bool = False, output_md: bool = False) -> None:
    if demo:
        score_data = get_demo_score(org_type)
    else:
        score_data = get_demo_score(org_type)

    ai_suggestions = []
    if ai:
        from analyzer import analyze_maturity
        ai_suggestions = analyze_maturity(score_data)

    print_report(score_data, ai_suggestions=ai_suggestions)

    if output_md:
        content = build_md_report(score_data, ai_suggestions=ai_suggestions)
        filename = f"zerovis_report_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = str(Path('C:/claude_c') / filename)
        save_md_report(content, output_path)
        print(f'\n MDレポートを保存しました: {output_path}')


if __name__ == '__main__':
    args = parse_args()
    run(demo=args.demo, org_type=args.org_type, output_md=args.output_md)
