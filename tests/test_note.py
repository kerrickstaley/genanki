import pytest
import genanki
from unittest import mock


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
