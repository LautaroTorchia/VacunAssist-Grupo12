import base64
from django import template
from django.contrib.staticfiles.finders import find as find_static_file

register = template.Library()

@register.simple_tag
def encode_static(path, encoding='base64', file_type='image'):
  print(path)
  try:
    file_path = find_static_file(path)
    ext = file_path.split('.')[-1]
    file_str = _get_file_data(file_path).decode('utf-8')
    return f"data:{file_type}/{ext};{encoding}, {file_str}"
  except IOError:
    return ''

def _get_file_data(file_path):
  with open(file_path, 'rb') as f:
    data = base64.b64encode(f.read())
    f.close()
    return data