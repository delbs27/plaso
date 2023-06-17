# -*- coding: utf-8 -*-
"""Tests for the iOS identityservices plist plugin."""

import unittest

from plaso.parsers.plist_plugins import ios_identityservices

from tests.parsers.plist_plugins import test_lib


class IOSIdstatusachePlistPluginTest(test_lib.PlistPluginTestCase):
  """Tests for the iOS identityservices plist plugin."""

  def testProcess(self):
    """Tests the Process function."""
    plist_name = 'com.apple.identityservices.idstatuscache.plist'

    plugin = ios_identityservices.IOSIdstatusachePlistPlugin()
    storage_writer = self._ParsePlistFileWithPlugin(
        plugin, [plist_name], plist_name)

    number_of_event_data = storage_writer.GetNumberOfAttributeContainers(
        'event_data')
    self.assertEqual(number_of_event_data, 40)

    number_of_warnings = storage_writer.GetNumberOfAttributeContainers(
        'recovery_warning')
    self.assertEqual(number_of_warnings, 0)

    expected_event_values = {
        'apple_identifier': 'tel:+13233208923',
        'data_type': 'ios:idstatuscache:lookup',
        'lookup_time': '2021-02-20T01:00:30.799723+00:00',
        'process_name': 'com.apple.private.alloy.tincan.audio'}

    event_data = storage_writer.GetAttributeContainerByIndex('event_data', 9)
    self.CheckEventData(event_data, expected_event_values)


if __name__ == '__main__':
  unittest.main()