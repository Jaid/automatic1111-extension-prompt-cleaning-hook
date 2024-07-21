from typing import Any
from modules import shared
from src.prompt_cleaning_hook.cleanerModules import cleanerModules
from src.prompt_cleaning_hook.extension import extensionId, extensionTitle
import gradio

defaults = {'enabled': True, 'comma_on_linebreak': False, 'save_metadata': True, 'log_changes': False}

uiInfos = {
  'enabled': {
    'label': 'Enable prompt cleaning',
    'component': gradio.Checkbox
  },
  'comma_on_linebreak': {
    'label': 'Replace line breaks with commas',
    'component': gradio.Checkbox
  },
  'save_metadata': {
    'label': 'Include uncleaned prompt in output metadata',
    'component': gradio.Checkbox
  },
  'log_changes': {
    'label': 'Print a log line to console for every changed prompt',
    'component': gradio.Checkbox
  }
}

for cleanerModule in cleanerModules:
  moduleId = cleanerModule['id']
  if 'isConfigurable' in cleanerModule and not cleanerModule['isConfigurable']:
    continue
  defaults[f'cleaner_module_{moduleId}'] = True if 'enabledByDefault' in cleanerModule and cleanerModule['enabledByDefault'] else False
  uiInfo = {
    'label': cleanerModule['title'] if 'title' in cleanerModule else moduleId,
    'component': gradio.Checkbox
  }
  uiInfos[f'cleaner_module_{moduleId}'] = uiInfo

def getOptionId(suffix: (str | None) = None) -> str:
  prefix = extensionId
  if suffix is not None:
    return f'{prefix}_{suffix}'
  return prefix

def getOption(optionId: str, defaultValue: Any = None) -> Any:
  if optionId in defaults:
    defaultValue = defaults[optionId]
  fullOptionId = getOptionId(optionId)
  if not hasattr(shared.opts, fullOptionId):
    return defaultValue
  value = getattr(shared.opts, fullOptionId)
  return value

def onUiSettings():
  section = (extensionId, extensionTitle)
  for optionId, defaultValue in defaults.items():
    uiInfo: dict[str, Any] = {
      'default': defaultValue
    }
    if optionId in uiInfos:
      uiInfo.update(uiInfos[optionId])
    optionInfo = shared.OptionInfo(**uiInfo)
    optionInfo.section = section
    fullOptionId = getOptionId(optionId)
    shared.opts.add_option(fullOptionId, optionInfo)
