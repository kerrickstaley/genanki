import pytest
import genanki
from unittest import mock
import textwrap
import warnings


def test_ok():
  my_model = genanki.Model(
    1376484377,
    'Simple Model',
    fields=[
      {'name': 'Question'},
      {'name': 'Answer'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])

  my_note = genanki.Note(
    model=my_model,
    fields=['Capital of Argentina', 'Buenos Aires'])

  with pytest.warns(None) as warn_recorder:
    my_note.write_to_db(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

  # Should be no warnings issued.
  assert not warn_recorder


class TestTags:
  def test_init(self):
    n = genanki.Note(tags=['foo', 'bar', 'baz'])
    with pytest.raises(ValueError):
      n = genanki.Note(tags=['foo', 'b ar', 'baz'])

  def test_assign(self):
    n = genanki.Note()
    n.tags = ['foo', 'bar', 'baz']
    with pytest.raises(ValueError):
      n.tags = ['foo', 'bar', ' baz']

  def test_assign_element(self):
    n = genanki.Note(tags=['foo', 'bar', 'baz'])
    n.tags[0] = 'dankey_kang'
    with pytest.raises(ValueError):
      n.tags[0] = 'dankey kang'

  def test_assign_slice(self):
    n = genanki.Note(tags=['foo', 'bar', 'baz'])
    n.tags[1:3] = ['bowser', 'daisy']
    with pytest.raises(ValueError):
      n.tags[1:3] = ['bowser', 'princess peach']

  def test_append(self):
    n = genanki.Note(tags=['foo', 'bar', 'baz'])
    n.tags.append('sheik_hashtag_melee')
    with pytest.raises(ValueError):
      n.tags.append('king dedede')

  def test_extend(self):
    n = genanki.Note(tags=['foo', 'bar', 'baz'])
    n.tags.extend(['palu', 'wolf'])
    with pytest.raises(ValueError):
      n.tags.extend(['dat fox doe'])

  def test_insert(self):
    n = genanki.Note(tags=['foo', 'bar', 'baz'])
    n.tags.insert(0, 'lucina')
    with pytest.raises(ValueError):
      n.tags.insert(0, 'nerf joker pls')


def test_num_fields_equals_model_ok():
  m = genanki.Model(
    1894808898,
    'Test Model',
    fields=[
      {'name': 'Question'},
      {'name': 'Answer'},
      {'name': 'Extra'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])

  n = genanki.Note(
    model=m,
    fields=['What is the capital of Taiwan?', 'Taipei',
            'Taipei was originally inhabitied by the Ketagalan people prior to the arrival of Han settlers in 1709.'])

  n.write_to_db(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())
  # test passes if code gets to here without raising


def test_num_fields_less_than_model_raises():
  m = genanki.Model(
    1894808898,
    'Test Model',
    fields=[
      {'name': 'Question'},
      {'name': 'Answer'},
      {'name': 'Extra'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])

  n = genanki.Note(model=m, fields=['What is the capital of Taiwan?', 'Taipei'])

  with pytest.raises(ValueError):
    n.write_to_db(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())


def test_num_fields_more_than_model_raises():
  m = genanki.Model(
    1894808898,
    'Test Model',
    fields=[
      {'name': 'Question'},
      {'name': 'Answer'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])

  n = genanki.Note(
    model=m,
    fields=['What is the capital of Taiwan?', 'Taipei',
            'Taipei was originally inhabitied by the Ketagalan people prior to the arrival of Han settlers in 1709.'])

  with pytest.raises(ValueError):
    n.write_to_db(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())


class TestFindInvalidHtmlTagsInField:
  def test_ok(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<h1>') == []

  def test_ok_with_space(self):
    assert genanki.Note._find_invalid_html_tags_in_field(' <h1> ') == []

  def test_ok_multiple(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<h1>test</h1>') == []

  def test_ok_br(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<br>') == []

  def test_ok_br2(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<br/>') == []

  def test_ok_br3(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<br />') == []

  def test_ok_attrs(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<h1 style="color: red">STOP</h1>') == []

  def test_ng_empty(self):
    assert genanki.Note._find_invalid_html_tags_in_field(' hello <> goodbye') == ['<>']

  def test_ng_empty_space(self):
    assert genanki.Note._find_invalid_html_tags_in_field(' hello < > goodbye') == ['< >']

  def test_ng_invalid_characters(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<@h1>') == ['<@h1>']

  def test_ng_invalid_characters_end(self):
    assert genanki.Note._find_invalid_html_tags_in_field('<h1@>') == ['<h1@>']

  def test_ng_issue_28(self):
    latex_code = r'''
        [latex]
        \schemestart
        \chemfig{*6(--(<OH)-(<:Br)---)}
        \arrow{->[?]}
        \chemfig{*6(--(<[:30]{O}?)(<:H)-?[,{>},](<:H)---)}
        \schemestop
        [/latex]
        '''
    latex_code = textwrap.dedent(latex_code[1:])

    expected_invalid_tags = [
      '<OH)-(<:Br)---)}\n\\arrow{->',
      '<[:30]{O}?)(<:H)-?[,{>',
    ]

    assert genanki.Note._find_invalid_html_tags_in_field(latex_code) == expected_invalid_tags


def test_warns_on_invalid_html_tags():
  my_model = genanki.Model(
    1376484377,
    'Simple Model',
    fields=[
      {'name': 'Question'},
      {'name': 'Answer'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])

  my_note = genanki.Note(
    model=my_model,
    fields=['Capital of <$> Argentina', 'Buenos Aires'])

  with pytest.warns(UserWarning, match='^Field contained the following invalid HTML tags.*$'):
    my_note.write_to_db(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())


def test_suppress_warnings(recwarn):
  my_model = genanki.Model(
    1376484377,
    'Simple Model',
    fields=[
      {'name': 'Question'},
      {'name': 'Answer'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
      },
    ])

  my_note = genanki.Note(
    model=my_model,
    fields=['Capital of <$> Argentina', 'Buenos Aires'])

  with pytest.warns(None) as warn_recorder:
    warnings.filterwarnings('ignore', message='^Field contained the following invalid HTML tags', module='genanki')
    my_note.write_to_db(mock.MagicMock(), mock.MagicMock(), mock.MagicMock())

  assert not warn_recorder
