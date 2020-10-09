#!/usr/bin/env python3
import prolog_parser
import re


# Correct


def test_integrate_correct_trivial(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'No errors occurred.\n'


def test_integrate_correct_spaces(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f.       \n\n\n\n  f :- g.      \n '
                                        '         f \n    :-   g, \n\n\nh   ; t  . '
                                        '   \n\n\n')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'No errors occurred.\n'


def test_integrate_correct_empty(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'No errors occurred.\n'


def test_integrate_correct_brackets(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- (g; (f , (g ; e , r ; (a , b)))).\n')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'No errors occurred.\n'


def test_integrate_correct_shtopor(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'No errors occurred.\n'


def test_integrate_correct_big(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g.\nf :- (a, b).\nf :- (a; b), h.\nf :- (a, b); h.\nf :- h, (a; b).\nf '
                                        ':- h; (a, b).\nf :- a , b , c ; d , e , f ; g , h , ((a) , (a , a ; a , '
                                        '((a ; (b)) ; a))) ; u ; a , a , a ; a ; a, a, (a) , (a ; h) , g.\n')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'No errors occurred.\n'


# Incorrect


def test_integrate_incorrect_eof1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file\n'


def test_integrate_incorrect_eof2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file\n'


def test_integrate_incorrect_eof3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :-')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Syntax error: unexpected end of file\n'


def test_integrate_incorrect_id(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g f.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)


def test_integrate_incorrect_no_right_operand(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- a , .')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)


def test_integrate_incorrect_no_left_operand(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- , b.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)


def test_integrate_incorrect_no_head(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text(':- f.')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)


def test_integrate_incorrect_no_body(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- .')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)


def test_integrate_incorrect_bad_brackets(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- (g ; (f).')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)


def test_integrate_incorrect_multiple_lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'input.mod').write_text('f :- g.\nf :- f ; f . f ; (f).\n f.     \nf :- a , b ; .')
    monkeypatch.chdir(tmp_path)
    prolog_parser.main(['input.mod'])
    out, err = capsys.readouterr()
    assert err == ''
    assert re.fullmatch(r'Syntax error: line \d+, colon \d+\n', out)
