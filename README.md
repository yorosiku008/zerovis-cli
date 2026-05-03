# ZeroVis JP

[![Tests](https://github.com/yorosiku008/zerovis-cli/actions/workflows/test.yml/badge.svg)](https://github.com/yorosiku008/zerovis-cli/actions)
[![Beta](https://img.shields.io/badge/β版-募集中-brightgreen)](mailto:yorosiku008@gmail.com)

ゼロトラスト成熟度評価CLI — NIST SP 800-207準拠。ID・デバイス・アプリケーション・ネットワークの4軸で成熟度を100点満点でスコアリング。NISC・総務省ガイドライン対応。

## インストール

```bash
git clone https://github.com/yorosiku008/zerovis-cli.git
cd zerovis-cli
pip install -r requirements.txt
```

## 使い方

```bash
# デモデータで動作確認（外部API不要）
python main.py --demo

# 組織種別を指定（自治体向け）
python main.py --demo --org-type municipal

# Markdownレポートも保存
python main.py --demo --org-type manufacturing --output-md
```

**対応組織種別:** `general` / `municipal`（自治体） / `manufacturing`（製造業） / `medical`（医療） / `finance`（金融）

## スコアリング軸

| 軸 | 重み | 評価内容 |
|---|---|---|
| ID・認証 | 35% | MFAカバレッジ / SSO / 特権アカウント管理 |
| デバイス | 25% | MDM管理率 / EDR導入 / OSパッチ適用率 |
| アプリケーション | 25% | SAML/OAuth統合率 / シャドーIT / API認証 |
| ネットワーク | 15% | VPN依存度 / マイクロセグメンテーション / 通信検査 |

## 成熟度レベル

| グレード | スコア | 成熟度レベル |
|---|---|---|
| S | 90+ | Level 5: 最適化段階 |
| A | 80+ | Level 4: 定量的管理 |
| B | 70+ | Level 3: 定義済み |
| C | 60+ | Level 2: 管理段階 |
| D | 50+ | Level 1: 初期段階 |
| E | 0+ | Level 0: 未着手 |

## 対応規制・ガイドライン

- 総務省ゼロトラスト移行ガイドライン（2023年版）
- NISC サイバーセキュリティ対策基準
- 医療情報システム安全管理ガイドライン第6.0版
- NIST SP 800-207 Zero Trust Architecture

## テスト

```bash
pytest tests/ -v
# 25 passed
```

---

*ZeroVis JP v0.1.0 — β版ユーザー募集中: yorosiku008@gmail.com*
