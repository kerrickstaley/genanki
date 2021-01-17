import re
import warnings
from cached_property import cached_property

from .card import Card
from .util import guid_for
import genanki


class _TagList(list):
  @staticmethod
  def _validate_tag(tag):
    if ' ' in tag:
      raise ValueError('Tag "{}" contains a space; this is not allowed!'.format(tag))

  def __init__(self, tags=()):
    super().__init__()
    self.extend(tags)

  def __repr__(self):
    return '{}({})'.format(self.__class__.__name__, super().__repr__())

  def __setitem__(self, key, val):
    if isinstance(key, slice):
      # val may be an iterator, convert to a list so we can iterate multiple times
      val = list(val)
      for tag in val:
        self._validate_tag(tag)
    else:
      self._validate_tag(val)

    super().__setitem__(key, val)

  def append(self, tag):
    self._validate_tag(tag)
    super().append(tag)

  def extend(self, tags):
    # tags may be an iterator, convert to list so we can iterate multiple times
    tags = list(tags)
    for tag in tags:
      self._validate_tag(tag)
    super().extend(tags)

  def insert(self, i, tag):
    self._validate_tag(tag)
    super().insert(i, tag)


class Note:
  _INVALID_HTML_TAG_RE = re.compile(r'<(?!/?[a-z0-9]+(?: .*|/?)>)(?:.|\n)*?>')
  _GUID_METHOD_OLD = 'old'
  _GUID_METHOD_0_11 = '0.11'
  _VALID_GUID_METHODS = [None, _GUID_METHOD_OLD, _GUID_METHOD_0_11]

  def __init__(self, model=None, fields=None, sort_field=None, tags=None, guid=None, guid_method=None):
    self.model = model
    self.fields = fields
    self.sort_field = sort_field
    self.tags = tags or []
    try:
      self.guid = guid
    except AttributeError:
      # guid was defined as a property
      pass
    self.guid_method = guid_method

  @property
  def sort_field(self):
    return self._sort_field or self.fields[0]

  @sort_field.setter
  def sort_field(self, val):
    self._sort_field = val

  @property
  def tags(self):
    return self._tags

  @tags.setter
  def tags(self, val):
    self._tags = _TagList()
    self._tags.extend(val)

  # We use cached_property instead of initializing in the constructor so that the user can set the model after calling
  # __init__ and it'll still work.
  @cached_property
  def cards(self):
    if self.model.model_type == self.model.FRONT_BACK:
      return self._front_back_cards()
    elif self.model.model_type == self.model.CLOZE:
      return self._cloze_cards()
    raise ValueError('Expected model_type CLOZE or FRONT_BACK')

  def _cloze_cards(self):
    """Returns a Card with unique ord for each unique cloze reference."""
    card_ords = set()
    # find cloze replacements in first template's qfmt, e.g "{{cloze::Text}}"
    cloze_replacements = set(
      re.findall(r"{{[^}]*?cloze:(?:[^}]?:)*(.+?)}}", self.model.templates[0]['qfmt']) +
      re.findall("<%cloze:(.+?)%>", self.model.templates[0]['qfmt']))
    for field_name in cloze_replacements:
      field_index = next((i for i, f in enumerate(self.model.fields) if f['name'] == field_name), -1)
      field_value = self.fields[field_index] if field_index >= 0 else ""
      # update card_ords with each cloze reference N, e.g. "{{cN::...}}"
      card_ords.update(int(m)-1 for m in re.findall(r"{{c(\d+)::.+?}}", field_value, re.DOTALL) if int(m) > 0)
    if card_ords == {}:
      card_ords = {0}
    return([Card(ord) for ord in card_ords])

  def _front_back_cards(self):
    """Create Front/Back cards"""
    rv = []
    for card_ord, any_or_all, required_field_ords in self.model._req:
      op = {'any': any, 'all': all}[any_or_all]
      if op(self.fields[ord_] for ord_ in required_field_ords):
        rv.append(Card(card_ord))
    return rv

  @property
  def guid(self):
    if self._guid is None:
      if self.guid_method is None:
        warnings.warn(
          ('guid_method is not set. Add this code near the top of your Python file:\n'
           + '  genanki.guid_method = {new}\n'
           + 'If this deck is already in use (e.g. published to AnkiWeb), use the old guid_method instead:\n'
           + '  genanki.guid_method = {old}\n'
           + "The default will change in a later version of genanki, so if you don't explicitly set guid_method, the "
           + "GUIDs of your notes will change when you upgrade genanki.\n"
           + "You can also set this on an individual Note if you don't want to change it globally:\n"
           + '  my_note.guid_method = {new}  # or {old}\n'
           + 'See [TODO DOC LINK] for details on why this is necessary.').format(
             old=repr(self._GUID_METHOD_OLD), new=repr(self._GUID_METHOD_0_11)))
        return guid_for(*self.fields)
      elif self.guid_method is self._GUID_METHOD_OLD:
        return guid_for(*self.fields)
      else:  # _GUID_METHOD_0_11
        if self.model is None:
          raise ValueError('.model field is None on Note {}. Need .model to calculate GUID.'.format(self.__repr__(skip_attrs=['guid'])))
        if self.model.model_id is None:
          raise ValueError('.model_id field of Model is None on Note {}. Need .model_id to calculate GUID.'.format(self.__repr__(skip_attrs=['guid'])))

        return guid_for(*self.fields, model_id=self.model.model_id)

    return self._guid

  @guid.setter
  def guid(self, val):
    self._guid = val

  def _check_number_model_fields_matches_num_fields(self):
    if len(self.model.fields) != len(self.fields):
      raise ValueError(
          'Number of fields in Model does not match number of fields in Note: '
          '{} has {} fields, but {} has {} fields.'.format(
              self.model, len(self.model.fields), self, len(self.fields)))

  @property
  def guid_method(self):
    if self._guid_method is not None:
      ret = self._guid_method
    else:
      ret = genanki.guid_method

    if ret not in self._VALID_GUID_METHODS:
      raise ValueError('guid_method {} is not valid; valid values are {}'.format(
          repr(ret), repr(self._VALID_GUID_METHODS)))

    return ret

  @guid_method.setter
  def guid_method(self, val):
    if val not in self._VALID_GUID_METHODS:
      raise ValueError('guid_method {} is not valid; valid values are {}'.format(
          repr(val), repr(self._VALID_GUID_METHODS)))
    self._guid_method = val

  @classmethod
  def _find_invalid_html_tags_in_field(cls, field):
    return cls._INVALID_HTML_TAG_RE.findall(field)

  def _check_invalid_html_tags_in_fields(self):
    for idx, field in enumerate(self.fields):
      invalid_tags = self._find_invalid_html_tags_in_field(field)
      if invalid_tags:
        # You can disable the below warning by calling warnings.filterwarnings:
        #
        # warnings.filterwarnings('ignore', module='genanki', message='^Field contained the following invalid HTML tags')
        #
        # If you think you're getting a false positive for this warning, please file an issue at
        # https://github.com/kerrickstaley/genanki/issues
        warnings.warn("Field contained the following invalid HTML tags. Make sure you are calling html.escape() if"
                      " your field data isn't already HTML-encoded: {}".format(' '.join(invalid_tags)))

  def write_to_db(self, cursor, timestamp: float, deck_id, id_gen):
    self._check_number_model_fields_matches_num_fields()
    self._check_invalid_html_tags_in_fields()
    cursor.execute('INSERT INTO notes VALUES(?,?,?,?,?,?,?,?,?,?,?);', (
        next(id_gen),                 # id
        self.guid,                    # guid
        self.model.model_id,          # mid
        int(timestamp),               # mod
        -1,                           # usn
        self._format_tags(),          # TODO tags
        self._format_fields(),        # flds
        self.sort_field,              # sfld
        0,                            # csum, can be ignored
        0,                            # flags
        '',                           # data
    ))

    note_id = cursor.lastrowid
    for card in self.cards:
      card.write_to_db(cursor, timestamp, deck_id, note_id, id_gen)

  def _format_fields(self):
    return '\x1f'.join(self.fields)

  def _format_tags(self):
    return ' ' + ' '.join(self.tags) + ' '

  def __repr__(self, skip_attrs=()):
    attrs = ['model', 'fields', 'sort_field', 'tags', 'guid']
    pieces = ['{}={}'.format(attr, '?' if attr in skip_attrs else repr(getattr(self, attr))) for attr in attrs]
    return '{}({})'.format(self.__class__.__name__, ', '.join(pieces))
