
formulaone_Teams = [
  'Mercedes','Ferrari','McLaren',
  'Red Bull Racing','Haas','Aston Martin',
  'Racing Bulls','Audi','Alpine','Williams','Cadillac'
  ]
from formulaone.models import Type
Teams = [Type(name=type) for type in formulaone_Teams]