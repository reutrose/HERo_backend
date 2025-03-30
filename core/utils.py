def try_parse_int(value:str, default=None):
     try:
          return int(value)
     except:
          return default