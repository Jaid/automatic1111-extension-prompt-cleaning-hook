from typing import Any
from modules import shared
from src.prompt_cleaning_hook.cleanerModules import cleanerModules
from src.prompt_cleaning_hook.extension import extensionId, extensionTitle

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

def getOptionId(suffix: (str | None) = None) -> str:
  prefix = extensionId
  if suffix is not None:
    return f'{prefix}_{suffix}'
  return prefix

def getOption(optionId: str, defaultValue: Any) -> (Any):
  if not hasattr(shared.opts, optionId):
    return defaultValue
  fullOptionId = getOptionId(optionId)
  value = getattr(shared.opts, fullOptionId, defaultValue)
  return value

def onUiSettings():
  section = (extensionId, extensionTitle)
  optionDefinitions = getOptionDefinitions()
  for optionId, optionInfo in optionDefinitions.items():
    optionInfo.section = section
    fullOptionId = getOptionId(optionId)
    shared.opts.add_option(fullOptionId, optionInfo)
