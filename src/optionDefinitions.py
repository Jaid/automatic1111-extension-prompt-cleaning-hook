from modules import shared
from src.cleanerModules import cleanerModules

def getOptionDefinitions():
  optionDefinitions = {
    'enabled': shared.OptionInfo(True, 'Enable prompt cleaning'),
    'comma_on_linebreak': shared.OptionInfo(False, 'Replace line breaks with commas'),
    'save_metadata': shared.OptionInfo(True, 'Include uncleaned prompt in output metadata'),
    'log_changes': shared.OptionInfo(False, 'Print a log line to console for every changed prompt'),
  }
  for cleanerModule in cleanerModules:
    moduleId = cleanerModule['id']
    optionInfo = shared.OptionInfo(cleanerModule['enabledByDefault'])
    optionInfo.label = cleanerModule['title']
    optionInfo.comment_after = cleanerModule['description']
    optionDefinitions[f'cleaner_module_{moduleId}'] = optionInfo
