class Food:
  def __init__(self):
    self.data = dict()

    with open('food.csv', 'r') as f:
      foods = [x.strip() for x in f.readlines()]

    for food in foods:
      elements = food.split(',')
      self.data[elements[1]] = {'id': elements[0], 'count': elements[2]}

  def catalog(self, name):
    if name in self.data:
      return self.data[name]['count']
    else:
      return None
