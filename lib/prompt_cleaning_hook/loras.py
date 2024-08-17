from typing import List, Tuple, Optional, TypedDict
import re

class Lora(TypedDict):
  name: str
  weight: Optional[str]


def removeLoras(prompt: str) -> Tuple[str, List[Lora]]:
  lorasPattern = r"<lora:(.+?)((?::\d+(?:\.\d+)?)?)>"
  loras: List[Lora] = []

  def extract_lora(match: re.Match) -> str:
    name = match.group(1)
    weight = match.group(2)
    if weight and weight[0] == ':':
      weight = weight[1:]
    loras.append({'name': name, 'weight': weight if weight else None})
    return ''

  loralessPrompt = re.sub(lorasPattern, extract_lora, prompt)
  return loralessPrompt, loras


def formatLora(lora: Lora) -> str:
  result = '<lora:'
  result += lora['name'].strip()
  weight = lora['weight']
  if weight and float(weight) != 1.0:
    result += ':' + weight.strip()
  result += '>'
  return result

def formatLoras(loras: List[Lora]) -> str:
  result = ''
  for i, lora in enumerate(loras):
    if i > 0:
      result += ' '
    result += formatLora(lora)
  return result
