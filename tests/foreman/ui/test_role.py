# -*- encoding: utf-8 -*-
"""Test class for Roles UI

@Requirement: Role

@CaseAutomation: Automated

@CaseLevel: Acceptance

@CaseComponent: UI

@TestType: Functional

@CaseImportance: High

@Upstream: No
"""

from fauxfactory import gen_string
from nailgun import entities
from robottelo.datafactory import generate_strings_list, invalid_values_list
from robottelo.decorators import stubbed, tier1, tier2
from robottelo.test import UITestCase
from robottelo.ui.factory import make_domain, make_role, make_user, set_context
from robottelo.ui.locators import common_locators, menu_locators
from robottelo.ui.session import Session


class RoleTestCase(UITestCase):
    """Implements Roles tests from UI"""

    @tier1
    def test_positive_create_with_name(self):
        """Create new role using different names

        @id: 8170598b-cf3b-4ff7-9baa-bee73f90d255

        @Assert: Role is created successfully
        """
        with Session(self.browser) as session:
            for name in generate_strings_list(length=10):
                with self.subTest(name):
                    make_role(session, name=name)
                    self.assertIsNotNone(self.role.search(name))

    @tier1
    def test_negative_create_with_invalid_name(self):
        """Create new role using invalid names

        @id: 4159a2ad-0952-4196-9e3b-56c721d24355

        @Assert: Role is not created
        """
        with Session(self.browser) as session:
            for name in invalid_values_list(interface='ui'):
                with self.subTest(name):
                    make_role(session, name=name)
                    self.assertIsNotNone(session.nav.wait_until_element(
                        common_locators['name_haserror']))

    @tier1
    def test_positive_delete(self):
        """Delete an existing role

        @id: c8bd515a-e556-4b98-a993-ec37f541ffc3

        @Assert: Role is deleted successfully
        """
        with Session(self.browser) as session:
            for name in generate_strings_list(length=10):
                with self.subTest(name):
                    make_role(session, name=name)
                    self.role.delete(name)

    @tier1
    def test_positive_update_name(self):
        """Update existing role name

        @id: c3ad9eed-6896-470d-9043-3fda37bbe489

        @Assert: Role is updated
        """
        name = gen_string('utf8')
        with Session(self.browser) as session:
            make_role(session, name=name)
            self.assertIsNotNone(self.role.search(name))
            for new_name in generate_strings_list(length=10):
                with self.subTest(new_name):
                    self.role.update(name, new_name)
                    self.assertIsNotNone(self.role.search(new_name))
                    name = new_name  # for next iteration

    @tier1
    def test_positive_update_permission(self):
        """Update existing role permissions

        @id: d57abcf2-a42f-40db-a61c-61b56bcc55b9

        @Assert: Role is updated
        """
        name = gen_string('alpha')
        with Session(self.browser) as session:
            make_role(session, name=name)
            self.assertIsNotNone(self.role.search(name))
            self.role.add_permission(
                name,
                resource_type='Architecture',
                permission_list=['view_architectures', 'create_architectures'],
            )


class CannedRoleTestCases(UITestCase):
    """Implements Canned Roles tests from UI"""

    @classmethod
    def setUpClass(cls):
        """Create Organization and Location to be used in tests"""
        super(CannedRoleTestCases, cls).setUpClass()
        cls.role_org = entities.Organization().create().name
        cls.role_loc = entities.Location().create().name
        cls.filter_org = entities.Organization().create().name
        cls.filter_loc = entities.Location().create().name

    @tier1
    def test_positive_create_role_with_taxonomies(self):
        """create role with taxonomies

        @id: 5d9da688-f371-4654-93d3-b221211be280

        @steps: Create new role with taxonomies

        @assert: New role is created with taxonomies
        """
        name = gen_string('alpha')
        with Session(self.browser) as session:
            make_role(
                session,
                name=name,
                locations=[self.role_loc],
                organizations=[self.role_org],
            )
            self.assertIsNotNone(self.role.search(name))

    @tier1
    def test_positive_create_filter_without_override(self):
        """Create filter in role w/o overriding it

        @id: a7f76f6e-6c13-4b34-b38c-19501b65786f

        @steps:

        1. Create a role with taxonomies assigned
        2. Create filter in role without overriding it
        3. Create user and assign new role to it
        4. Re-login into application using new user with a role

        @assert:

        1. Filter w/o override is created in role
        2. The taxonomies of role are inherited to filter
        3. Override check is not marked by default in filters table
        4. User can access application sections specified in a filter only
        """
        name = gen_string('alpha')
        username = gen_string('alpha')
        password = gen_string('alpha')
        domain_name = gen_string('alpha')
        with Session(self.browser) as session:
            make_role(
                session,
                name=name,
                locations=[self.role_loc],
                organizations=[self.role_org],
            )
            self.assertIsNotNone(self.role.search(name))
            self.role.add_permission(
                name,
                resource_type='Domain',
                permission_list=['view_domains', 'create_domains'],
                override_check=True,
            )
            self.assertTrue(self.role.wait_until_element(
                common_locators['alert.success']))
            make_user(
                session,
                username=username,
                password1=password,
                password2=password,
                roles=[name],
                locations=[self.role_loc],
                organizations=[self.role_org],
                edit=True
            )
        with Session(self.browser, username, password) as session:
            set_context(session, org=self.role_org)
            set_context(session, loc=self.role_loc)
            make_domain(session, name=domain_name)
            self.assertIsNotNone(self.domain.search(domain_name))
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.content'], timeout=3))
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.configure'], timeout=3))

    @tier1
    def test_positive_create_non_overridable_filter(self):
        """Create non overridden filter in role

        @id: 5ee281cf-28fa-439d-888d-b1f9aacc6d57

        @steps:

        1. Create a filter to which taxonomies cannot be associated.
        e.g Architecture filter

        @assert:

        1. Filter is created without taxonomies
        2. Override checkbox is not available to check.
        """
        name = gen_string('alpha')
        username = gen_string('alpha')
        password = gen_string('alpha')
        with Session(self.browser) as session:
            make_role(
                session,
                name=name,
                locations=[self.role_loc],
                organizations=[self.role_org],
            )
            self.assertIsNotNone(self.role.search(name))
            self.role.add_permission(
                name,
                resource_type='Architecture',
                permission_list=['view_architectures', 'edit_architectures'],
                override_check=False,
            )
            self.assertTrue(self.role.wait_until_element(
                common_locators['alert.success']))
            make_user(
                session,
                username=username,
                password1=password,
                password2=password,
                roles=[name],
                locations=[self.role_loc],
                organizations=[self.role_org],
                edit=True
            )
        with Session(self.browser, username, password) as session:
            set_context(session, org=self.role_org)
            set_context(session, loc=self.role_loc)
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.content'], timeout=3))
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.infrastructure'], timeout=3))
            # check that we can access edit functionality at all
            self.architecture.update(old_name='x86_64', new_name='x86_64')

    @tier1
    def test_positive_create_overridable_filter(self):
        """Create overridden filter in role

        @id: 325e7e3e-60fc-4182-9585-0449d9660e8d

        @steps:

        1. Create a filter to which taxonomies can be associated
        e.g Domain filter
        2. Override a filter with some taxonomies

        @assert:

        1. Filter is created with taxonomies
        2. Override check is marked in filters table
        3. Filter doesnt inherits taxonomies from role
        """
        name = gen_string('alpha')
        username = gen_string('alpha')
        password = gen_string('alpha')
        domain_name = gen_string('alpha')
        with Session(self.browser) as session:
            make_role(
                session,
                name=name,
                locations=[self.role_loc],
                organizations=[self.role_org],
            )
            self.assertIsNotNone(self.role.search(name))
            self.role.add_permission(
                name,
                resource_type='Domain',
                permission_list=['view_domains', 'create_domains'],
                override=True,
                override_check=True,
                organization=[self.filter_org],
                location=[self.filter_loc],
            )
            make_user(
                session,
                username=username,
                password1=password,
                password2=password,
                roles=[name],
                locations=[self.role_loc, self.filter_loc],
                organizations=[self.role_org, self.filter_org],
                edit=True
            )
        with Session(self.browser, username, password) as session:
            set_context(session, org=self.filter_org)
            set_context(session, loc=self.filter_loc)
            make_domain(session, name=domain_name)
            self.assertIsNotNone(self.domain.search(domain_name))
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.content'], timeout=3))
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.configure'], timeout=3))

        with Session(self.browser, username, password) as session:
            set_context(session, org=self.role_org)
            set_context(session, loc=self.role_loc)
            self.assertIsNone(self.domain.search(domain_name))
            self.assertIsNone(session.nav.wait_until_element(
                menu_locators['menu.hosts'], timeout=3))

    @stubbed
    @tier1
    def test_positive_update_role_taxonomies(self):
        """Update role taxonomies which applies to its non-overrided filters

        @id: f705faea-0d1c-4c11-b82d-b6b0e848f75d

        @steps:

        1. Update existing role with different taxonomies

        @assert: The taxonomies are applied only to non-overrided role filters

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_negative_update_role_taxonomies(self):
        """Update role taxonomies which doesnt applies to its overrided filters

        @id: 9ffca18f-8784-48e2-8972-a67979a44508

        @steps:

        1. Update existing role with different taxonomies

        @assert: The overridden role filters are not updated

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_disable_filter_override(self):
        """Uncheck override resets filter taxonomies

        @id: cae31e44-c3d6-4a08-a088-d12cb2088068

        @steps:

        1. Create role with overridden filter having different taxonomies than
        its role.
        2. Uncheck the override checkbox in above role filter

        @assert: The taxonomies of filter resets/synced to role taxonomies

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_disable_overriding_option(self):
        """Disable overriding option to disable single filter overriding

        @id: e692d114-1b0b-4106-afdb-cf894ea09acf

        @steps:

        1. Create role with overridden filter
        2. Click on 'Disable overriding' option of that filter in filters table
        in role

        @assert:

        1. The overriding is disabled for that filter
        2. The taxonomies of filter resets/synced to role taxonomies

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_disable_all_filters_overriding_option(self):
        """Disable all filters overriding option to disable all filters
        overriding in a role

        @id: 2942835a-f156-4211-ab7d-77e2b08fceac

        @steps:

        1. Create role with overridden filters
        2. Click on 'Disable all filters overriding' button in filters table
        in role

        @assert:

        1. The overriding is disabled for all the overridden filters in role
        2. The taxonomies of all overridden filters resets/synced to role
        taxonomies

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_create_org_admin(self):
        """Create Org admin role which has access to all the resources within
        organization

        @id: 03f41736-c5c5-414a-ab75-650cecd6f6cd

        @steps:

        1. Clone Manager role which has most resource permission
        2. Assign an organization to the cloned role
        3. Add more missing resource permission to the cloned role to make it
        Org Admin having access to all resources

        @assert:

        1. Successfully created Org Admin
        2. Successfully assigned organization to role
        3. Missing resource filters are added successfully to the Org Admin
        role

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_create_org_admin_filter_taxonomies(self):
        """Org Admin role filters should inherit taxonomies from org admin role

        @id: d08e1c47-ffc7-4885-ba73-a95e89e45f34

        @steps:

        1. Clone Manager role which has most resource permission
        2. Add more missing resource permission to the cloned role to make it
        Org Admin having access to all resources
        3. Assign an organization to the cloned role

        @assert: All the org admin filters inherit taxonomies from org admin

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_clone_role_with_taxonomies(self):
        """Test new taxonomies can be set on cloned role.

        @id: ad20f5c7-3df7-4b43-8a52-097c87676d07

        @steps:

        1. Attempt to clone any existing role(e.g Manager Role)
        2. Set new taxonomies to cloned role

        @assert:

        1. Cloned role has no taxonomies selected by default
        2. New taxonomies can be set on cloned role

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_override_cloned_role_filter(self):
        """Test if the cloned role filter can be overrided

        @id: e475aa7d-4844-4bb3-bfd3-3d4082a41fe4

        @steps:

        1. Clone any existing role(e.g Manager Role)
        2. Attempt to override the filter in cloned role

        @assert:

        1. Filter in cloned role is successfully overriding

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_empty_filter_taxonomies_in_cloned_role(self):
        """Test overridden filters taxonomies in cloned role

        @id: 86d9cd93-8189-45b3-86c6-ac9185e48655

        @steps:

        1. Clone a role having overridden filter(s)

        @assert:

        1. cloned overridden filters are cleared in cloned role
        2. Override mark is filters table is marked

        @caseautomation: notautomated
        """

    @stubbed
    @tier1
    def test_positive_override_empty_filter_taxonomies_in_cloned_role(self):
        """Override overridden filters in cloned role

        @id: 978bf745-0b63-4dc7-9512-77731b0caa23

        @steps:

        1. Clone a role having overridden filter(s)
        2. Override overridden filters by setting some taxonomies in cloned
        role

        @assert: Overridden filters are overriding in cloned role

        @caseautomation: notautomated
        """

    @stubbed
    @tier2
    def test_positive_access_resources_from_role_taxonomies(self):
        """Test user access resources from taxonomies of assigned role

        @id: 25217ba7-ae8d-4a63-a4cf-faa5932934b0

        @steps:

        1. Create role with taxonomies
        2. Create resource(s) filter(s) without overriding them
        3. Create user with taxonomies same as role taxonomies
        4. Assign step 1 role to user

        @assert: User should be able to access the resource(s) of the assigned
        role

        @caseautomation: notautomated

        @CaseLevel: Integration
        """

    @stubbed
    @tier2
    def test_negative_access_resources_outside_role_taxonomies(self):
        """Test user cannot access resources from non associated taxonomies to
        role

        @id: bff0fd9d-9363-4759-9595-e6294a8d5a89

        @steps:

        1. Create role with taxonomies
        2. Create resource(s) filter(s) without overriding them
        3. Create user with taxonomies not matching role taxonomies
        4. Assign step 1 role to user

        @assert: User should not be able to access the resource(s) that are not
        associated to assigned role

        @caseautomation: notautomated

        @CaseLevel: Integration
        """
