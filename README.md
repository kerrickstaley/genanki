# genanki: A Library for Generating Anki Decks

`genanki` allows you to programatically generate decks in Python 3 for Anki, a popular spaced-repetition flashcard
program. Please see below for concepts and usage.

*This library and its author(s) are not affiliated/associated with the main Anki project in any way.*

[![Build Status](https://travis-ci.org/kerrickstaley/genanki.svg?branch=master)](https://travis-ci.org/kerrickstaley/genanki)

## Notes
The basic unit in Anki is the `Note`, which contains a fact to memorize. `Note`s correspond to one or more `Card`s.

Here's how you create a `Note`:

```python
my_note = genanki.Note(
  model=my_model,
  fields=['Capital of Argentina', 'Buenos Aires'])
```

You pass in a `Model`, discussed below, and a set of `fields`.

## Models
A `Model` defines the fields and cards for a type of `Note`. For example:

```python
my_model = genanki.Model(
  1607392319,
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
```

This note-type has two fields and one card. The card displays the `Question` field on the front and the `Question` and
`Answer` fields on the back, separated by a `<hr>`. You can also pass a `css` argument to `Model()` to supply custom
CSS.

You need to pass a `model_id` so that Anki can keep track of your model. It's important that you use a unique `model_id`
for each `Model` you define. Use `random.randrange(1 << 30, 1 << 31)` to generate a suitable model_id, and hardcode it
into your `Model` definition.

## Generating a Deck/Package
To import your notes into Anki, you need to add them to a `Deck`:

```python
my_deck = genanki.Deck(
  2059400110,
  'Country Capitals')

my_deck.add_note(my_note)
```

Once again, you need a unique `deck_id` that you should generate once and then hardcode into your `.py` file.

Then, create a `Package` for your `Deck` and write it to a file:

```python
genanki.Package(my_deck).write_to_file('output.apkg')
```

You can then load `output.apkg` into Anki using File -> Import...

## Media Files
To add sounds or images, set the `media_files` attribute on your `Package`:

```python
my_package = genanki.Package(my_deck)
my_package.media_files = ['sound.mp3', 'image.jpg']
```

The media files should be in the current working directory. They can be referenced in notes like this:

```html
[sound:sound.mp3]
<img src="image.jpg">
```

## Note GUIDs
`Note`s have a `guid` property that uniquely identifies the note. If you import a new note that has the same GUID as an
existing note, the new note will overwrite the old one (as long as their models have the same fields).

This is an important feature if you want to be able to tweak the design/content of your notes, regenerate your deck, and
import the updated version into Anki. Your notes need to have stable GUIDs in order for the new note to replace the
existing one.

By default, the GUID is a hash of all the field values. This may not be desirable if, for example, you add a new field
with additional info that doesn't change the identity of the note. You can create a custom GUID implementation to hash
only the fields that identify the note:

```python
class MyNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0], self.fields[1])
```

## sort_field
Anki has a value for each `Note` called the `sort_field`. Anki uses this value to sort the cards in the Browse
interface. Anki also is happier if you avoid having two notes with the same `sort_field`, although this isn't strictly
necessary. By default, the `sort_field` is the first field, but you can change it by passing `sort_field=` to `Note()`
or implementing `sort_field` as a property in a subclass (similar to `guid`).

## YAML for Templates (and Fields)
You can create your template definitions in the YAML format and pass them as a `str` to `Model()`. You can also do this
for fields.

## Using genanki inside an Anki addon
`genanki` supports adding generated notes to the local collection when running inside an Anki 2.1 addon (Anki 2.0
may work but has not been tested). See the [`.write_to_collection_from_addon() method`](
https://github.com/kerrickstaley/genanki/blob/0c2cf8fea9c5e382e2fae9cd6d5eb440e267c637/genanki/__init__.py#L275).
