from django import template


register = template.Library()


@register.filter()
def censor(value):
   prohibited_words = ['бренд', 'нашли', 'обнаружил', 'манипулятор', 'интеллект', 'робот', 'подвешиват', 'шильдик', 'популярны', 'спецификации']
   if isinstance(value, str):
      for word in prohibited_words:
         value = value.replace(word[1:], '*' * len(word[1:]))
   else:
      raise ValueError('Incorrect data type is entered, please enter a string')
   return value

