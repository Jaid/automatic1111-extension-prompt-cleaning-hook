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
    if 'isConfigurable' in cleanerModule and not cleanerModule['isConfigurable']:
      continue
    moduleId = cleanerModule['id']
    optionInfo = shared.OptionInfo()
    if 'enabledByDefault' in cleanerModule:
      optionInfo.default = cleanerModule['enabledByDefault']
    if 'title' in cleanerModule:
      optionInfo.label = cleanerModule['title']
    else:
      optionInfo.label = cleanerModule['id']
    if 'description' in cleanerModule:
      description = cleanerModule['description']
      optionInfo.info(description)
      optionInfo.infotext = description
    optionDefinitions[f'cleaner_module_{moduleId}'] = optionInfo
  return optionDefinitions
