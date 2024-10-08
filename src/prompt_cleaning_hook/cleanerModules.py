from lib.prompt_cleaning_hook import sanitizeText

cleanerModules = [
  {
    'id': 'moveLoras',
    'title': 'Move Loras',
    'description': 'Move Loras to the end of the prompt',
    'isConfigurable': False,
    'enabledByDefault': True,
    'process': sanitizeText.moveLoras
  },{
  'id': 'normalizeLineEndings',
  'title:': 'Normalize Line Endings',
  'description': 'Replace all line endings with \\n',
  'isConfigurable': False,
  'enabledByDefault': True,
  'process': sanitizeText.normalizeLineEndings
}, {
  'id': 'compressLines',
  'title:': 'Compress Lines',
  'description': 'Replace multiple line breaks with a single line break',
  'enabledByDefault': True,
  'process': sanitizeText.compressLines,
}, {
  'id': 'trimAroundBreakKeyword',
  'title:': 'Trim Around Break Keyword',
  'description': 'Remove commas near “BREAK” keywords (potentially changes generated outputs)',
  'enabledByDefault': True,
  'process': sanitizeText.trimAroundBreakKeyword
}, {
  'id': 'compressWhitespace',
  'title:': 'Compress Whitespace',
  'description': 'Replace multiple whitespace characters with a single space',
  'enabledByDefault': True,
  'process': sanitizeText.compressWhitespace
}, {
  'id': 'normalizeUnicode',
  'title:': 'Normalize Unicode',
  'description': 'Normalize unicode characters (potentially changes generated outputs)',
  'enabledByDefault': True,
  'process': sanitizeText.normalizeUnicode
}, {
  'id': 'clearUnprintable',
  'title:': 'Clear Unprintable',
  'description': 'Remove unprintable characters (potentially changes generated outputs)',
  'enabledByDefault': True,
  'process': sanitizeText.clearUnprintable
}, {
  'id': 'strip',
  'title:': 'Strip',
  'description': 'Remove leading and trailing whitespace',
  'enabledByDefault': True,
  'process': sanitizeText.strip
}, {
  'id': 'stripLineEndings',
  'title:': 'Strip Line Endings',
  'description': 'Remove trailing whitespace',
  'enabledByDefault': True,
  'process': sanitizeText.stripLineEndings
}, {
  'id': 'stripLineStarts',
  'title:': 'Strip Line Starts',
  'description': 'Remove leading whitespace',
  'enabledByDefault': True,
  'process': sanitizeText.stripLineStarts
}, {
  'id': 'compressCommas',
  'title:': 'Compress Commas',
  'description': 'Replace multiple commas with a single comma (potentially changes generated outputs)',
  'enabledByDefault': True,
  'process': sanitizeText.compressCommas
}, {
  'id': 'trimBeforeCommas',
  'title:': 'Trim Before Commas',
  'description': 'Remove whitespace before commas',
  'enabledByDefault': True,
  'process': sanitizeText.trimBeforeCommas
}, {
  'id': 'trimEdgeCommas',
  'title:': 'Trim Edge Commas',
  'description': 'Remove leading and trailing commas (potentially changes generated outputs)',
  'enabledByDefault': True,
  'process': sanitizeText.trimEdgeCommas
}]

def getCleanerModules():
  return cleanerModules
