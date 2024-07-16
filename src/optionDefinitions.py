from modules import shared

def getOptionDefinitions():
  return {
    'enabled': shared.OptionInfo(True, 'Enable prompt cleaning'),
    'comma_on_linebreak': shared.OptionInfo(True, 'Replace line breaks with commas'),
    'include_uncleaned': shared.OptionInfo(True, 'Include uncleaned prompt in output metadata'),
    'enable_logging': shared.OptionInfo(False, 'Enable logging to console'),
  }
