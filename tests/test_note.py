import pytest
import genanki


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
