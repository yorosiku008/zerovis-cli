import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch


def test_parse_args_defaults():
    from main import parse_args
    args = parse_args([])
    assert args.demo is False
    assert args.org_type == 'general'
    assert args.output_md is False


def test_parse_args_demo_flag():
    from main import parse_args
    args = parse_args(['--demo'])
    assert args.demo is True


def test_parse_args_org_type():
    from main import parse_args
    args = parse_args(['--org-type', 'municipal'])
    assert args.org_type == 'municipal'


def test_parse_args_output_md():
    from main import parse_args
    args = parse_args(['--output-md'])
    assert args.output_md is True


def test_run_demo_uses_demo_data():
    from main import run
    with patch('main.get_demo_score') as mock_demo, \
         patch('main.print_report') as mock_print:
        mock_demo.return_value = {'total': 65, 'grade': 'C', 'axes': {}, 'org_type': 'general'}
        run(demo=True)
        mock_demo.assert_called_once()
        mock_print.assert_called_once()


def test_run_saves_md_when_flag_set():
    from main import run
    with patch('main.get_demo_score') as mock_demo, \
         patch('main.print_report'), \
         patch('main.build_md_report') as mock_build, \
         patch('main.save_md_report') as mock_save:
        mock_demo.return_value = {'total': 65, 'grade': 'C', 'axes': {}, 'org_type': 'general'}
        mock_build.return_value = '# report'
        run(demo=True, output_md=True)
        mock_save.assert_called_once()
