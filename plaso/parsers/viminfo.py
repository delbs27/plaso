# -*- coding: utf-8 -*-
"""Parser for viminfo files."""

import pyparsing

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.lib import errors
from plaso.parsers import manager
from plaso.parsers import text_parser


class VimInfoEventData(events.EventData):
  """VimInfo event data.

  Attributes:
    filename (str): the name of the file that was opened/edited.
    history_type (str): the Vim history type.
    history_value (str): the Vim history value.
    item_number (int): the item number of the history type.
    recorded_time (dfdatetime.DateTimeValues): date and time the log entry
        was recorded.
  """

  DATA_TYPE = 'viminfo:history'

  def __init__(self):
    """Initializes event data."""
    super(VimInfoEventData, self).__init__(data_type=self.DATA_TYPE)
    self.filename = None
    self.history_type = None
    self.history_value = None
    self.item_number = None
    self.recorded_time = None


class VimInfoParser(text_parser.PyparsingMultiLineTextParser):
  """Parses events from Viminfo files."""

  NAME = 'viminfo'
  DATA_FORMAT = 'Viminfo file'

  _ENCODING = 'utf-8'

  _FILENAME = '.viminfo'

  BUFFER_SIZE = 16384

  _INTEGER = pyparsing.Word(pyparsing.nums).setParseAction(
      text_parser.PyParseIntCast)

  _HEADER_1 = (
      pyparsing.Literal('# This viminfo file was generated by Vim ') +
      pyparsing.Word(pyparsing.nums + '.') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _HEADER_2 = (
      pyparsing.Literal('# You may edit it if you\'re careful!') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _VERSION_HEADER = (
      pyparsing.Literal('# Viminfo version') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _VERSION_VALUE = (
      pyparsing.Literal('|') +
      pyparsing.Word(pyparsing.nums + ',').setResultsName('version') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _ENCODING_HEADER = (
      pyparsing.Literal('# Value of \'encoding\' when this file was written') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _ENCODING_VALUE = (
      pyparsing.Literal('*') +
      pyparsing.Literal('encoding=') +
      pyparsing.Word(pyparsing.alphanums + '-').setResultsName('encoding') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _PREAMBLE = (
      _HEADER_1 + _HEADER_2 + _VERSION_HEADER + _VERSION_VALUE +
      _ENCODING_HEADER + _ENCODING_VALUE)

  _HLSEARCH = (
      pyparsing.Literal('# hlsearch on (H) or off (h):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.Word('~/hH').setResultsName('hlsearch') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  # TODO: https://github.com/vim/vim/blob/master/src/viminfo.c#L1525
  _SEARCH_PATTERN = (
      pyparsing.Literal('# Last Search Pattern:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.restOfLine.setResultsName('search_pattern') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  # TODO: https://github.com/vim/vim/blob/master/src/viminfo.c#L1525
  _SUBSTITUTE_SEARCH_PATTERN = (
      pyparsing.Literal('# Last Substitute Search Pattern:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.restOfLine.setResultsName('substitute_search_pattern') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _SUBSTITUTE_STRING = (
      pyparsing.Literal('# Last Substitute String:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.restOfLine.setResultsName('last_substitute_string') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _BAR_ITEM = (
      pyparsing.Literal('|') +
      pyparsing.Word(pyparsing.nums, exact=1) + pyparsing.Suppress(',') +
      pyparsing.Word(pyparsing.nums, exact=1) + pyparsing.Suppress(',') +
      pyparsing.Word(pyparsing.nums, exact=10) + pyparsing.Suppress(',') +
      pyparsing.Optional(_INTEGER) +
      pyparsing.Suppress(',') +
      pyparsing.restOfLine + pyparsing.Suppress(pyparsing.LineEnd()))

  _REGISTER_CONTINUATION = (
      pyparsing.Literal('|<"') +
      pyparsing.restOfLine +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _REGISTER_ITEM = (
      pyparsing.Literal('|') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      pyparsing.Word(pyparsing.nums, exact=10) + pyparsing.Suppress(',') +
      pyparsing.Group(
          pyparsing.restOfLine +
          pyparsing.Suppress(pyparsing.LineEnd()) +
          pyparsing.ZeroOrMore(_REGISTER_CONTINUATION)))

  _FILEMARK_ITEM = pyparsing.Group(
      pyparsing.Literal('|') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      _INTEGER + pyparsing.Suppress(',') +
      pyparsing.Word(pyparsing.nums, exact=10) + pyparsing.Suppress(',') +
      pyparsing.restOfLine + pyparsing.Suppress(pyparsing.LineEnd()))

  _COMMAND_LINE_ITEM = pyparsing.Group(
      pyparsing.Literal(':') +
      pyparsing.restOfLine +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _BAR_ITEM).setResultsName('command_line_items*')

  _COMMAND_LINE_HISTORY = (
      pyparsing.Literal('# Command Line History (newest to oldest):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_COMMAND_LINE_ITEM) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _SEARCH_STRING_ITEM = pyparsing.Group(
      pyparsing.Literal('?') +
      pyparsing.restOfLine +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _BAR_ITEM).setResultsName('search_string_items*')

  _SEARCH_STRING_HISTORY = (
      pyparsing.Literal('# Search String History (newest to oldest):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_SEARCH_STRING_ITEM) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _EXPRESSION_ITEM = pyparsing.Group(
      pyparsing.Literal('=') +
      pyparsing.Word(pyparsing.alphas + '/:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _BAR_ITEM).setResultsName('expression_history_items*')

  _EXPRESSION_HISTORY = (
      pyparsing.Literal('# Expression History (newest to oldest):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_EXPRESSION_ITEM))

  _INPUT_LINE_ITEM = pyparsing.Group(
      pyparsing.Literal('@') +
      pyparsing.Word(pyparsing.alphas + '/:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _BAR_ITEM).setResultsName('input_line_history_items*')

  _INPUT_LINE_HISTORY = (
      pyparsing.Literal('# Input Line History (newest to oldest):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_INPUT_LINE_ITEM))

  _DEBUG_LINE_ITEM = pyparsing.Group(
      pyparsing.Literal('@') +
      pyparsing.Word(pyparsing.alphas + '/:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _BAR_ITEM).setResultsName('debug_line_history_items*')

  _DEBUG_LINE_HISTORY = (
      pyparsing.Literal('# Debug Line History (newest to oldest):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_DEBUG_LINE_ITEM))

  _REGISTERS_CONTENT = (
      pyparsing.Suppress(pyparsing.White('\t')) +
      pyparsing.restOfLine() +
      pyparsing.Suppress(pyparsing.LineEnd()))

  # http://vimdoc.sourceforge.net/htmldoc/change.html#registers
  _REGISTERS_ITEM = pyparsing.Group(
      pyparsing.Literal('"') +
      pyparsing.Or([_INTEGER, pyparsing.Word(pyparsing.printables)]) +
      pyparsing.Suppress(pyparsing.White('\t')) +
      pyparsing.Or(['BLOCK', 'CHAR', 'LINE']) +
      pyparsing.Suppress(pyparsing.White('\t')) +
      _INTEGER + pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.Group(pyparsing.ZeroOrMore(_REGISTERS_CONTENT)) +
      _REGISTER_ITEM).setResultsName('registers_items*')

  _REGISTERS_HISTORY = (
      pyparsing.Literal('# Registers:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_REGISTERS_ITEM))

  _FILEMARKS_ITEM = pyparsing.Group(
      pyparsing.Literal('\'') +
      _INTEGER +
      _INTEGER +
      _INTEGER +
      pyparsing.restOfLine +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _FILEMARK_ITEM).setResultsName('filemarks_items*')

  _FILEMARKS_HISTORY = (
      pyparsing.Literal('# File marks:') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_FILEMARKS_ITEM) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _JUMPLIST_ITEM = pyparsing.Group(
      pyparsing.Word('-\'') +
      _INTEGER +
      _INTEGER +
      pyparsing.restOfLine +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      _FILEMARK_ITEM).setResultsName('jumplist_items*')

  _JUMPLIST_HISTORY = (
      pyparsing.Literal('# Jumplist (newest first):') +
      pyparsing.Suppress(pyparsing.LineEnd()) +
      pyparsing.ZeroOrMore(_JUMPLIST_ITEM) +
      pyparsing.Suppress(pyparsing.LineEnd()))

  _HISTORY_MARKS_HISTORY = (
      pyparsing.Literal('# History of marks within files (newest to oldest):') +
      pyparsing.Suppress(pyparsing.LineEnd()))

  LINE_STRUCTURES = [
      ('preamble', _PREAMBLE),
      ('command_line_history', _COMMAND_LINE_HISTORY),
      ('hlsearch', _HLSEARCH),
      ('search_pattern', _SEARCH_PATTERN),
      ('substitute_search', _SUBSTITUTE_SEARCH_PATTERN),
      ('substitute_string', _SUBSTITUTE_STRING),
      ('search_string_history', _SEARCH_STRING_HISTORY),
      ('expression_history', _EXPRESSION_HISTORY),
      ('input_line_history', _INPUT_LINE_HISTORY),
      ('debug_line_history', _DEBUG_LINE_HISTORY),
      ('registers_history', _REGISTERS_HISTORY),
      ('filemarks_history', _FILEMARKS_HISTORY),
      ('jumplist_history', _JUMPLIST_HISTORY),
      ('history_marks_history', _HISTORY_MARKS_HISTORY)]

  _SUPPORTED_KEYS = frozenset([key for key, _ in LINE_STRUCTURES])

  def _ParseCommandLineHistory(self, parser_mediator, structure):
    """Parses command line history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match a command line history
    """
    for index, item in enumerate(structure.get('command_line_items', [])):
      event_data = VimInfoEventData()
      event_data.history_value = item[1]
      event_data.history_type = 'Command Line History'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[5])

      parser_mediator.ProduceEventData(event_data)

  def _ParseSearchStringHistory(self, parser_mediator, structure):
    """Parses search string history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match a search string history
    """
    for index, item in enumerate(structure.get('search_string_items', [])):
      event_data = VimInfoEventData()
      event_data.history_value = item[1]
      event_data.history_type = 'Search String History'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[5])

      parser_mediator.ProduceEventData(event_data)

  def _ParseExpressionHistory(self, parser_mediator, structure):
    """Parses expression history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match an expression history
    """
    for index, item in enumerate(structure.get('expression_history_items', [])):
      event_data = VimInfoEventData()
      event_data.history_value = item[1]
      event_data.history_type = 'Expression History'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[5])

      parser_mediator.ProduceEventData(event_data)

  def _ParseInputLineHistory(self, parser_mediator, structure):
    """Parses input line history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match an input line history
    """
    for index, item in enumerate(structure.get('input_line_history_items', [])):
      event_data = VimInfoEventData()
      event_data.history_value = item[1]
      event_data.history_type = 'Input Line History'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[5])

      parser_mediator.ProduceEventData(event_data)

  def _ParseDebugLineHistory(self, parser_mediator, structure):
    """Parses debug line history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match a debug line history
    """
    for index, item in enumerate(structure.get('debug_line_history_items', [])):
      event_data = VimInfoEventData()
      event_data.history_value = item[1]
      event_data.history_type = 'Debug Line History'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[5])

      parser_mediator.ProduceEventData(event_data)

  def _ParseRegistersHistory(self, parser_mediator, structure):
    """Parses register history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match a Register history
    """
    for item in structure.get('registers_items', []):
      event_data = VimInfoEventData()
      event_data.history_value = '\n'.join(item[4])
      event_data.history_type = 'Register'
      event_data.item_number = item[1]
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[12])

      parser_mediator.ProduceEventData(event_data)

  def _ParseFilemarksHistory(self, parser_mediator, structure):
    """Parses filemarks history items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match a Filemarks history
    """
    for index, item in enumerate(structure.get('filemarks_items', [])):
      event_data = VimInfoEventData()
      event_data.filename = item[4].strip()
      event_data.history_type = 'File mark'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[5][5])

      parser_mediator.ProduceEventData(event_data)

  def _ParseJumplistHistory(self, parser_mediator, structure):
    """Parses jumplist items and creates VimInfoEventData objects.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      structure (pyparsing.ParseResults): structure of tokens derived from
          lines of text that match a JumpList history
    """
    for index, item in enumerate(structure.get('jumplist_items', [])):
      event_data = VimInfoEventData()
      event_data.filename = item[3].strip()
      event_data.history_type = 'Jumplist'
      event_data.item_number = index
      event_data.recorded_time = dfdatetime_posix_time.PosixTime(
           timestamp=item[4][5])

      parser_mediator.ProduceEventData(event_data)

  def ParseRecord(self, parser_mediator, key, structure):
    """Parse the record and create a viminfo event object

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      key (str): name of the parsed structure.
      structure (pyparsing.ParseResults): structure of tokens derived from
          a line of a text file.

    Raises:
      ParseError: when the structure type is unknown.
    """
    if key not in self._SUPPORTED_KEYS:
      raise errors.ParseError(
        'Unable to parse record, unknown structure: {0:s}'.format(key))

    if key == 'command_line_history':
      self._ParseCommandLineHistory(parser_mediator, structure)
    elif key == 'search_string_history':
      self._ParseSearchStringHistory(parser_mediator, structure)
    elif key == 'expression_history':
      self._ParseExpressionHistory(parser_mediator, structure)
    elif key == 'input_line_history':
      self._ParseInputLineHistory(parser_mediator, structure)
    elif key == 'debug_line_history':
      self._ParseDebugLineHistory(parser_mediator, structure)
    elif key == 'registers_history':
      self._ParseRegistersHistory(parser_mediator, structure)
    elif key == 'filemarks_history':
      self._ParseFilemarksHistory(parser_mediator, structure)
    elif key == 'jumplist_history':
      self._ParseJumplistHistory(parser_mediator, structure)
    # TODO(sydp): add support for history marks history lines
    # elif key == 'history_marks_history':
    #   self._ParseHistoryMarksHistory(self, parser_mediator, structure)

  # pylint: disable=unused-argument
  def VerifyStructure(self, parser_mediator, lines):
    """Verifies whether content corresponds to a viminfo file.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfVFS.
      lines (str): one or more lines from the text file.

    Returns:
      bool: True if this is the correct parser, False otherwise.
    """
    try:
      self._PREAMBLE.parseString(lines)
    except pyparsing.ParseException:
      return False

    return True


manager.ParsersManager.RegisterParser(VimInfoParser)
