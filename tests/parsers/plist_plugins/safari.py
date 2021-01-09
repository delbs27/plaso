#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the Safari history plist plugin."""

import unittest

from plaso.parsers.plist_plugins import safari

from tests.parsers.plist_plugins import test_lib


class SafariPluginTest(test_lib.PlistPluginTestCase):
  """Tests for the Safari history plist plugin."""

  def testProcess(self):
    """Tests the Process function."""
    plist_name = 'History.plist'

    plugin = safari.SafariHistoryPlugin()
    storage_writer = self._ParsePlistFileWithPlugin(
        plugin, [plist_name], plist_name)

    self.assertEqual(storage_writer.number_of_warnings, 0)
    self.assertEqual(storage_writer.number_of_events, 18)

    # The order in which PlistParser generates events is nondeterministic
    # hence we sort the events.
    events = list(storage_writer.GetSortedEvents())

    expected_event_values = {
        'timestamp': '2013-07-08 17:31:00.000000'}

    self.CheckEventValues(storage_writer, events[7], expected_event_values)

    expected_url = 'http://netverslun.sci-mx.is/aminosyrur'

    expected_event_values = {
        'url': expected_url}

    self.CheckEventValues(storage_writer, events[9], expected_event_values)

    expected_message = (
        'Visited: {0:s} (Am\xedn\xf3s\xfdrur ) '
        'Visit Count: 1').format(expected_url)

    event_data = self._GetEventDataOfEvent(storage_writer, events[9])
    self._TestGetMessageStrings(
        event_data, expected_message, expected_message)


if __name__ == '__main__':
  unittest.main()
