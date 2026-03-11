
formulaone_Teams = [
  'Water', 'Fire', 'Grass', 'Flying', 'Rock',
  'Ground', 'Steel', 'Electric', 'Fairy', 'Ghost',
  'Dark', 'Dragon', 'Ice', 'Bug', 'Fighting', 'Poison',
  'Psychic', 'Normal'
]

from formulaone.models import Type
Teams = [Type(name=type) for type in formulaone_Teams]