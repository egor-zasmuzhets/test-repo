def say_message(m, echo=False):
  print(m)
  print("message said")
  if not echo:
    return m
  return None
