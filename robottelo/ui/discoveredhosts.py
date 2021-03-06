# -*- encoding: utf-8 -*-
"""Implements Discovered Hosts from UI."""
from robottelo.ui.base import Base, UIError
from robottelo.ui.locators import locators
from robottelo.ui.navigator import Navigator


class DiscoveredHosts(Base):
    """Manipulates Discovered Hosts from UI"""

    def navigate_to_entity(self):
        """Navigate to Discovered Hosts entity page"""
        Navigator(self.browser).go_to_discovered_hosts()

    def _search_locator(self):
        """Specify locator for Discovered Hosts entity search procedure"""
        return locators["discoveredhosts.hostname"]

    def delete(self, hostname, really=True):
        """Delete existing discovered hosts from UI"""
        Navigator(self.browser).go_to_discovered_hosts()
        self.delete_entity(
            hostname,
            really,
            locators['discoveredhosts.delete'],
            drop_locator=locators['discoveredhosts.dropdown'],
        )

    def delete_from_facts(self, hostname, really=True):
        """Delete existing discovered host from facts page"""
        host = self.search(hostname)
        if not host:
            raise UIError(
                'Could not find the selected discovered host "{0}"'
                .format(hostname)
            )
        host.click()
        strategy, value = locators['discoveredhosts.delete_from_facts']
        self.click((strategy, value % hostname), wait_for_ajax=False)
        self.handle_alert(really)

    def multi_delete(self, really=True):
        """Bulk delete discovered hosts"""
        select_all_element = locators['discoveredhosts.select_all']
        select_action_element = locators['discoveredhosts.select_action']
        multi_delete_element = locators['discoveredhosts.multi_delete']
        bulk_submit_button = locators['discoveredhosts.bulk_submit_button']
        if not self.find_element(select_all_element):
            raise UIError(
                'Could not find the check-box to select all discovered hosts'
            )
        self.click(select_all_element)
        if not self.find_element(select_action_element):
            raise UIError(
                'Could not find the select_action dropdown for bulk operations'
            )
        self.click(select_action_element)
        if not self.find_element(multi_delete_element):
            raise UIError(
                'Could not find the delete option from select_action dropdown'
            )
        self.click(multi_delete_element)
        if not self.find_element(bulk_submit_button):
            raise UIError(
                'Could not find the bulk submit button'
            )
        self.click(bulk_submit_button)

    def refresh_facts(self, hostname):
        """Refresh the facts of discovered host"""
        host = self.search(hostname)
        if not host:
            raise UIError(
                'Could not find the selected discovered host "{0}"'
                .format(hostname)
            )
        strategy, value = locators['discoveredhosts.dropdown']
        self.click((strategy, value % hostname))
        strategy, value = locators['discoveredhosts.refresh_facts']
        self.click((strategy, value % hostname))

    def fetch_fact_value(self, hostname, element):
        """Fetch the value of selected fact from discovered hosts page"""
        host = self.search(hostname)
        if not host:
            raise UIError(
                'Could not find the selected discovered host "{0}"'
                .format(hostname)
            )
        if not self.find_element(element):
            raise UIError(
                'Could not find element to fetch interfaces from facts page'
            )
        web_element = self.find_element(element)
        element_value = web_element.text
        return element_value
