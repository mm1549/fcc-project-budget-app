from math import floor

class Category:
  def __init__(self,cat):
    self.category = cat
    self.ledger = []
    self.balance = 0

  def __str__(self):
    lines = []
    stars1 = (30 - len(self.category)) // 2
    stars2 = 30 - len(self.category) - stars1
    
    lines.append(
     '*' * stars1 + self.category + '*' * stars2 
    )
    
    for obj in self.ledger:
      description = obj['description'][:23]
      amount = format(obj['amount'], '.2f')
      white = 30 - len(description) - len(amount)
      lines.append(
        description + ' ' * white + amount
      )

    lines.append(
     'Total: ' + format(self.balance, '.2f') 
    )
      
    return '\n'.join(lines)
    
  def deposit(self,amount, description = ''):
    entry = {
      'amount': amount,
      'description': description
    }
    self.balance += amount
    self.ledger.append(entry)

  def withdraw(self,amount, description = ''):
    if self.check_funds(amount):
      entry = {
        'amount': -amount,
        'description': description  
      }
      self.ledger.append(entry)
      self.balance -= amount
      return True
    else:
      return False
      

  def get_balance(self):
    return self.balance

  def transfer(self,amount,cat):
    if self.check_funds(amount):
      entry = {
        'amount': -amount,
        'description': 'Transfer to ' + cat.category
      }
      self.ledger.append(entry)
      cat.deposit(amount, 'Transfer from ' + self.category)
      self.balance -= amount
      return True
    else:
      return False
      
  def check_funds(self,amount):
    return amount <= self.balance
   
def create_spend_chart(categories):
  chart = ['Percentage spent by category']
  spending = {}
  spentTotal = 0
  
  for cat in categories:
    spentCat = -sum(min(0,x['amount']) for x in cat.ledger)
    spentTotal += spentCat
    spending[cat.category] = spentCat

  for key in spending:
    spending[key] = floor(spending[key] / spentTotal * 10) * 10

  for perc in range(100, -1, -10):
    perc = str(perc)
    line= ' ' * (3 - len(perc)) + perc + '| '
    for key in spending:
      if spending[key] >= int(perc):
        line += 'o  '
      else:
        line += '   '
    chart.append(line)

  chart.append('    -' + '---' * len(spending))

  maxLen = max(len(x) for x in spending.keys())

  for i in range(maxLen):
    line = '     '
    for key in spending:
      if i < len(key):
        line += key[i] + '  '
      else:
        line += '   '
    chart.append(line)
      
      
  return '\n'.join(chart)
    
  
  