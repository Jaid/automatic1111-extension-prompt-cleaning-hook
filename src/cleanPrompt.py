import logging

from modules import scripts, shared
from modules.processing import StableDiffusionProcessing

from src.cleanerModules import cleanerModules
from src.optionDefinitions import getOptionDefinitions

extensionTitle = 'Prompt Cleaner Hook'
extensionId = 'prompt_cleaner_hook'
logger = logging.getLogger(extensionTitle)
logger.setLevel(logging.DEBUG)
logger.info(f'Loading {extensionTitle}')

def getOptionId(suffix: (str | None) = None) -> str:
  prefix = extensionId
  if suffix is not None:
    return f'{prefix}_{suffix}'
  return prefix

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
  modulesString = '/'.join(result['changingModules'])
  logMessage = f'Cleaned {promptName} from “{originalPromptSingleLine}” to “{cleanedSingleLine}” using modules {modulesString}'
  logger.debug(logMessage)

class PromptCleaner(scripts.Script):
  def title(self):
    logger.debug('title')
    return extensionTitle

  def show(self, isImg2img):
    logger.debug('show')
    return scripts.AlwaysVisible

  def process(self, processing: StableDiffusionProcessing):
    logger.debug('process')
    if not hasattr(shared.opts, getOptionId('enabled') or not shared.opts[getOptionId('enabled')]): # type: ignore
      return

    commaOnLinebreak = getattr(shared.opts, getOptionId('comma_on_linebreak'), True)
    includeUncleaned = getattr(shared.opts, getOptionId('include_uncleaned'), True)
    enableLogging = getattr(shared.opts, getOptionId('enable_logging'), False)

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

    logger.info(f'Cleaned {changedCount}/{len(processing.all_prompts) + len(processing.all_negative_prompts)} prompts')
    if includeUncleaned:
      processing.extra_generation_params.setdefault(f'{extensionId}_original_prompt', originalPrompt)
      processing.extra_generation_params.setdefault(f'{extensionId}_original_negative_prompt', originalNegativePrompt)

  def onUiSettings(self):
    logger.debug('onUiSettings')
    section = (extensionId, extensionTitle)
    optionDefinitions = getOptionDefinitions()
    for optionId, optionInfo in optionDefinitions.items():
      optionInfo.section = section
      fullOptionId = getOptionId(optionId)
      shared.opts.add_option(fullOptionId, optionInfo)
