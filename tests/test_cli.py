from forge.cli import build_parser


def test_build_parser_exists():
    parser = build_parser()
    assert parser is not None
    assert any(action.dest == "command" for action in parser._actions)