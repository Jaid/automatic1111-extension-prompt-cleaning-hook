from modules import script_callbacks

from lib.prompt_cleaning_hook.options import onUiSettings

from modules import scripts
from modules.processing import StableDiffusionProcessing

from src.prompt_cleaning_hook.cleanerModules import cleanerModules
from lib.prompt_cleaning_hook.options import getOption
from src.prompt_cleaning_hook.extension import extensionId, extensionTitle
from lib.prompt_cleaning_hook.logger import logger

def process(text: str, commaOnLinebreak: bool) -> dict[str, str | list[str]]:
  changingModules: list[str] = []
  for module in cleanerModules:
    newText = module['process'](text)
    if newText != text:
      changingModules.append(module['id'])
      text = newText
  return {'text': text, 'changingModules': changingModules}

def logChange(result, original: str, isPositive: bool = True):
  cleaned: str = result['text']
  originalPromptSingleLine = original.replace('\n', '¶')
  cleanedSingleLine = cleaned.replace('\n', '¶')
  promptName = 'prompt' if isPositive else 'negative prompt'
  modulesString = ' → '.join(result['changingModules'])
  logMessage = f'Cleaned {promptName} from “{originalPromptSingleLine}” to “{cleanedSingleLine}” using modules {modulesString}'
  logChanges = getOption('log_changes', False)
  if logChanges:
    logger.info(logMessage)
  else:
    logger.debug(logMessage)

class PromptCleaningHook(scripts.Script):
  def __init__(self):
    logger.debug('PromptCleaningHook initialized')
    super().__init__()

  def title(self):
    return extensionTitle

  def show(self, isImg2img):
    return scripts.AlwaysVisible

  def process(self, processing: StableDiffusionProcessing):
    if getOption('enabled', False) == False:
      return

    commaOnLinebreak = getOption('comma_on_linebreak', True)
    saveMetadata = getOption('save_metadata', True)

    changedCount = 0
    originalPrompt = processing.prompt
    originalNegativePrompt = processing.negative_prompt

    for i in range(len(processing.all_prompts)):
      cleanResult = process(processing.all_prompts[i], commaOnLinebreak)
      if cleanResult['changingModules'].count == 0:
        continue
      logChange(cleanResult, processing.all_prompts[i])
      changedCount += 1
      processing.all_prompts[i] = cleanResult['text']

    for i in range(len(processing.all_negative_prompts)):
      cleanResult = process(processing.all_negative_prompts[i], commaOnLinebreak)
      if cleanResult['changingModules'].count == 0:
        continue
      logChange(cleanResult, processing.all_negative_prompts[i], False)
      changedCount += 1
      processing.all_negative_prompts[i] = cleanResult['text']

    if changedCount == 0:
      return

    logger.debug(f'Cleaned {changedCount}/{len(processing.all_prompts) + len(processing.all_negative_prompts)} prompts')
    if saveMetadata:
      processing.extra_generation_params.setdefault(f'{extensionId}_original_prompt', originalPrompt)
      processing.extra_generation_params.setdefault(f'{extensionId}_original_negative_prompt', originalNegativePrompt)

script_callbacks.on_ui_settings(onUiSettings)
