# -*- encoding: utf-8 -*-
"""Test class for User Group CLI

@Requirement: Usergroup

@CaseAutomation: Automated

@CaseLevel: Acceptance

@CaseComponent: CLI

@TestType: Functional

@CaseImportance: High

@Upstream: No
"""

from random import randint
from robottelo.cli.usergroup import UserGroup
from robottelo.cli.base import CLIReturnCodeError
from robottelo.cli.factory import (
    CLIFactoryError,
    make_role,
    make_user,
    make_usergroup,
)
from robottelo.datafactory import (
    invalid_values_list,
    valid_data_list,
    valid_usernames_list,
)
from robottelo.decorators import tier1, tier2
from robottelo.test import CLITestCase


class UserGroupTestCase(CLITestCase):
    """User group CLI related tests."""

    @tier1
    def test_positive_create_with_name(self):
        """Create new user group using different valid names

        @id: 4cb19ecf-53f8-4804-8fbd-a028c02f13c6

        @Assert: User group is created successfully.
        """
        for name in valid_data_list():
            with self.subTest(name):
                user_group = make_usergroup({'name': name})
                self.assertEqual(user_group['name'], name)

    @tier1
    def test_positive_create_with_user_name(self):
        """Create new user group using valid user attached to that group. Use
        user name as a parameter

        @id: 50baa271-c741-4905-aa56-a3ee48be0dc0

        @Assert: User group is created successfully.
        """
        for login in valid_usernames_list():
            with self.subTest(login):
                user = make_user({'login': login})
                user_group = make_usergroup({'users': user['login']})
                self.assertEqual(len(user_group['users']), 1)
                self.assertEqual(user_group['users'][0], login)

    @tier1
    def test_positive_create_with_user_id(self):
        """Create new user group using valid user attached to that group. Use
        user id as a parameter

        @id: bacef0e3-31dd-4991-93f7-f54fbe64d0f0

        @Assert: User group is created successfully.
        """
        user = make_user()
        user_group = make_usergroup({'user-ids': user['id']})
        self.assertEqual(user_group['users'][0], user['login'])

    @tier1
    def test_positive_create_with_users(self):
        """Create new user group using multiple users attached to that group.
        Use users name as a parameter

        @id: 3b0a3c3c-aab2-4e8a-b043-7462621c7333

        @Assert: User group is created successfully and contains all expected
        users.
        """
        users = [make_user()['login'] for _ in range(randint(3, 5))]
        user_group = make_usergroup({'users': users})
        self.assertEqual(sorted(users), sorted(user_group['users']))

    @tier1
    def test_positive_create_with_role_name(self):
        """Create new user group using valid role attached to that group. Use
        role name as a parameter

        @id: 47fb3037-f48a-4f99-9a50-792b0fd77569

        @Assert: User group is created successfully.
        """
        for role_name in valid_data_list():
            with self.subTest(role_name):
                role = make_role({'name': role_name})
                user_group = make_usergroup({'roles': role['name']})
                self.assertEqual(len(user_group['roles']), 1)
                self.assertEqual(user_group['roles'][0], role_name)

    @tier1
    def test_positive_create_with_role_id(self):
        """Create new user group using valid role attached to that group. Use
        role id as a parameter

        @id: 8524a561-037c-4509-aaba-3213924a1cfe

        @Assert: User group is created successfully.
        """
        role = make_role()
        user_group = make_usergroup({'role-ids': role['id']})
        self.assertEqual(user_group['roles'][0], role['name'])

    @tier1
    def test_positive_create_with_roles(self):
        """Create new user group using multiple roles attached to that group.
        Use roles name as a parameter

        @id: b7113d49-b9ce-4603-a09d-5ab23fe2d568

        @Assert: User group is created successfully and contains all expected
        roles
        """
        roles = [make_role()['name'] for _ in range(randint(3, 5))]
        user_group = make_usergroup({'roles': roles})
        self.assertEqual(sorted(roles), sorted(user_group['roles']))

    @tier1
    def test_positive_create_with_usergroup_name(self):
        """Create new user group using another user group attached to the
        initial group. Use user group name as a parameter

        @id: 7bbe3af7-af36-4d13-a4ce-7ec5441b88bf

        @Assert: User group is created successfully.
        """
        for name in valid_data_list():
            with self.subTest(name):
                sub_user_group = make_usergroup({'name': name})
                user_group = make_usergroup({
                    'user-groups': sub_user_group['name']})
                self.assertEqual(len(user_group['user-groups']), 1)
                self.assertEqual(user_group['user-groups'][0], name)

    @tier1
    def test_positive_create_with_usergroup_id(self):
        """Create new user group using another user group attached to the
        initial group. Use user group id as a parameter

        @id: 04ee66e5-e721-431b-ac6d-c7413fdc6dc2

        @Assert: User group is created successfully.
        """
        sub_user_group = make_usergroup()
        user_group = make_usergroup({
            'user-group-ids': sub_user_group['id']})
        self.assertEqual(user_group['user-groups'][0], sub_user_group['name'])

    @tier1
    def test_positive_create_with_usergroups(self):
        """Create new user group using multiple user groups attached to that
        initial group. Use user groups name as a parameter

        @id: ca6031f7-0998-444b-94be-f8a9e4a9f733

        @Assert: User group is created successfully and contains all expected
        user groups
        """
        sub_user_groups = [
            make_usergroup()['name'] for _ in range(randint(3, 5))]
        user_group = make_usergroup({'user-groups': sub_user_groups})
        self.assertEqual(
            sorted(sub_user_groups), sorted(user_group['user-groups']))

    @tier1
    def test_negative_create_with_name(self):
        """Attempt to create user group with invalid name.

        @id: 79d2d28d-a0d9-42ab-ba88-c259a463533a

        @Assert: User group is not created.
        """
        for name in invalid_values_list():
            with self.subTest(name):
                with self.assertRaises(CLIFactoryError):
                    make_usergroup({'name': name})
                with self.assertRaises(CLIReturnCodeError):
                    UserGroup.info({'name': name})

    @tier1
    def test_negative_create_with_same_name(self):
        """Attempt to create user group with a name of already existent entity.

        @id: b1eebf2f-a59e-43af-a980-ae73320b4311

        @Assert: User group is not created.
        """
        user_group = make_usergroup()
        with self.assertRaises(CLIFactoryError):
            make_usergroup({'name': user_group['name']})

    @tier1
    def test_positive_list(self):
        """Test user group list command

        @id: 828d0051-53c8-4737-809a-983517f675bb

        @Assert: User group list command returns valid and expected data

        """
        user_group = make_usergroup()
        result_list = UserGroup.list({
            'search': 'name={0}'.format(user_group['name'])})
        self.assertTrue(len(result_list) > 0)
        self.assertTrue(
            UserGroup.exists(search=('name', user_group['name'])))

    @tier1
    def test_positive_update_by_id(self):
        """Update existing user group with different valid names. Use id of the
        user group as a parameter

        @id: bed911fe-da39-4798-a5d2-8a0467bfacc3

        @Assert: User group is update successfully.
        """
        user_group = make_usergroup()
        for new_name in valid_data_list():
            with self.subTest(new_name):
                UserGroup.update({
                    'id': user_group['id'],
                    'new-name': new_name,
                })
                user_group = UserGroup.info({'id': user_group['id']})
                self.assertEqual(user_group['name'], new_name)

    @tier1
    def test_positive_update_by_name(self):
        """Update existing user group with different valid names. Use name of
        the user group as a parameter

        @id: 3bee63ff-ae2a-4fa4-a5bd-58ec85358c19

        @Assert: User group is update successfully.
        """
        user_group = make_usergroup()
        for new_name in valid_data_list():
            with self.subTest(new_name):
                UserGroup.update({
                    'name': user_group['name'],
                    'new-name': new_name,
                })
                user_group = UserGroup.info({'id': user_group['id']})
                self.assertEqual(user_group['name'], new_name)

    @tier1
    def test_negative_update_by_id(self):
        """Attempt to update existing user group using different invalid names.
        Use id of the user group as a parameter

        @id: e5aecee1-7c4c-4ac5-aee2-a3190cbe956f

        @Assert: User group is not updated.
        """
        user_group = make_usergroup()
        for new_name in invalid_values_list():
            with self.subTest(new_name):
                with self.assertRaises(CLIReturnCodeError):
                    UserGroup.update({
                        'id': user_group['id'],
                        'new-name': new_name,
                    })
                user_group = UserGroup.info({'id': user_group['id']})
                self.assertNotEqual(user_group['name'], new_name)

    @tier1
    def test_negative_update_by_name(self):
        """Attempt to update existing user group using different invalid names.
        Use name of the user group as a parameter

        @id: 32ad14cf-4ed8-4deb-b2fc-df4ed60efb78

        @Assert: User group is not updated.
        """
        user_group = make_usergroup()
        for new_name in invalid_values_list():
            with self.subTest(new_name):
                with self.assertRaises(CLIReturnCodeError):
                    UserGroup.update({
                        'name': user_group['name'],
                        'new-name': new_name,
                    })
                user_group = UserGroup.info({'id': user_group['id']})
                self.assertNotEqual(user_group['name'], new_name)

    @tier1
    def test_positive_delete_by_name(self):
        """Create user group with valid name and then delete it using that name

        @id: 359b1806-64c5-42ec-9448-991e82f70e98

        @assert: User group is deleted successfully
        """
        for name in valid_data_list():
            with self.subTest(name):
                user_group = make_usergroup({'name': name})
                UserGroup.delete({'name': user_group['name']})
                with self.assertRaises(CLIReturnCodeError):
                    UserGroup.info({'name': user_group['name']})

    @tier1
    def test_positive_delete_by_id(self):
        """Create user group with valid data and then delete it using its ID

        @id: b60b4da7-9d1b-487d-89e5-ebf3aa2218d6

        @assert: User group is deleted successfully
        """
        user_group = make_usergroup()
        UserGroup.delete({'id': user_group['id']})
        with self.assertRaises(CLIReturnCodeError):
            UserGroup.info({'id': user_group['id']})

    @tier1
    def test_positive_delete_with_user_by_id(self):
        """Create new user group using valid user attached to that group. Then
        delete that user group using id of that group as a parameter

        @id: 34ffa204-9376-41f2-aca1-edf29f553957

        @Assert: User group is deleted successfully.
        """
        user = make_user()
        user_group = make_usergroup({'user-ids': user['id']})
        UserGroup.delete({'id': user_group['id']})
        with self.assertRaises(CLIReturnCodeError):
            UserGroup.info({'id': user_group['id']})

    @tier2
    def test_positive_add_role_by_id(self):
        """Create new user group and new role. Then add created role to user
        group by id

        @id: a4ce8724-d3c8-4c00-9421-aaa40394134d

        @Assert: Role is added to user group successfully.

        @CaseLevel: Integration
        """
        role = make_role()
        user_group = make_usergroup()
        UserGroup.add_role({
            'id': user_group['id'],
            'role-id': role['id'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(user_group['roles'][0], role['name'])

    @tier2
    def test_positive_add_role_by_name(self):
        """Create new user group and new role. Then add created role to user
        group by name

        @id: 181bf2d5-0650-4fb0-890c-475eac3306a2

        @Assert: Role is added to user group successfully.

        @CaseLevel: Integration
        """
        role = make_role()
        user_group = make_usergroup()
        UserGroup.add_role({
            'id': user_group['id'],
            'role': role['name'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(user_group['roles'][0], role['name'])

    @tier2
    def test_positive_add_user_by_id(self):
        """Create new user group and new user. Then add created user to user
        group by id

        @id: f2972e48-67c3-4dc9-8c4b-aa550086afb7

        @Assert: User is added to user group successfully.

        @CaseLevel: Integration
        """
        user = make_user()
        user_group = make_usergroup()
        UserGroup.add_user({
            'id': user_group['id'],
            'user-id': user['id'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(user_group['users'][0], user['login'])

    @tier2
    def test_positive_add_user_by_name(self):
        """Create new user group and new user. Then add created user to user
        group by name

        @id: f622eb11-a3d2-4a25-8889-766133750431

        @Assert: User is added to user group successfully.

        @CaseLevel: Integration
        """
        user = make_user()
        user_group = make_usergroup()
        UserGroup.add_user({
            'id': user_group['id'],
            'user': user['login'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(user_group['users'][0], user['login'])

    @tier2
    def test_positive_add_user_group_by_id(self):
        """Create two new user groups. Then add one user group to another by id

        @id: f041d325-93c0-4799-88d7-5ece65568266

        @Assert: User group is added to another user group successfully.

        @CaseLevel: Integration
        """
        sub_user_group = make_usergroup()
        user_group = make_usergroup()
        UserGroup.add_user_group({
            'id': user_group['id'],
            'user-group-id': sub_user_group['id'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(user_group['user-groups'][0], sub_user_group['name'])

    @tier2
    def test_positive_add_user_group_by_name(self):
        """Create two new user groups. Then add one user group to another by
        name

        @id: de60c347-b440-45c6-8e79-19aa0d338099

        @Assert: User group is added to another user group successfully.

        @CaseLevel: Integration
        """
        sub_user_group = make_usergroup()
        user_group = make_usergroup()
        UserGroup.add_user_group({
            'id': user_group['id'],
            'user-group': sub_user_group['name'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(user_group['user-groups'][0], sub_user_group['name'])

    @tier2
    def test_positive_remove_role_by_id(self):
        """Create new user group using valid role attached to that group. Then
        remove that role from user group by id

        @id: f086e7f0-4a24-4097-8ec6-3f698ac926ba

        @Assert: Role is removed from user group successfully.

        @CaseLevel: Integration
        """
        role = make_role()
        user_group = make_usergroup({'role-ids': role['id']})
        self.assertEqual(len(user_group['roles']), 1)
        UserGroup.remove_role({
            'id': user_group['id'],
            'role-id': role['id'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(len(user_group['roles']), 0)

    @tier2
    def test_positive_remove_role_by_name(self):
        """Create new user group using valid role attached to that group. Then
        remove that role from user group by name

        @id: 0a5fdeaf-a05f-4153-b2c8-c5f8745cbb80

        @Assert: Role is removed from user group successfully.

        @CaseLevel: Integration
        """
        role = make_role()
        user_group = make_usergroup({'role-ids': role['id']})
        self.assertEqual(len(user_group['roles']), 1)
        UserGroup.remove_role({
            'id': user_group['id'],
            'role': role['name'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(len(user_group['roles']), 0)

    @tier2
    def test_positive_remove_user_by_id(self):
        """Create new user group using valid user attached to that group. Then
        remove that user from user group by id

        @id: 9ae91110-88dd-4449-82c7-59f626fdd2be

        @Assert: User is removed from user group successfully.

        @CaseLevel: Integration
        """
        user = make_user()
        user_group = make_usergroup({'user-ids': user['id']})
        self.assertEqual(len(user_group['users']), 1)
        UserGroup.remove_user({
            'id': user_group['id'],
            'user-id': user['id'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(len(user_group['users']), 0)

    @tier2
    def test_positive_remove_user_by_name(self):
        """Create new user group using valid user attached to that group. Then
        remove that user from user group by name

        @id: e99b215b-05bb-4e7b-a11a-cd506d88df6c

        @Assert: User is removed from user group successfully.

        @CaseLevel: Integration
        """
        user = make_user()
        user_group = make_usergroup({'user-ids': user['id']})
        self.assertEqual(len(user_group['users']), 1)
        UserGroup.remove_user({
            'id': user_group['id'],
            'user': user['login'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(len(user_group['users']), 0)

    @tier2
    def test_positive_remove_usergroup_by_id(self):
        """Create new user group using another user group attached to the
        initial group. Then remove that attached user group by id

        @id: e7e8ccb2-a93d-420d-b71e-218ffbb428b4

        @Assert: User group is removed from initial one successfully.

        @CaseLevel: Integration
        """
        sub_user_group = make_usergroup()
        user_group = make_usergroup({'user-group-ids': sub_user_group['id']})
        self.assertEqual(len(user_group['user-groups']), 1)
        UserGroup.remove_user_group({
            'id': user_group['id'],
            'user-group-id': sub_user_group['id'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(len(user_group['user-groups']), 0)

    @tier2
    def test_positive_remove_usergroup_by_name(self):
        """Create new user group using another user group attached to the
        initial group. Then remove that attached user group by name

        @id: 45a070b5-60b1-4c8c-8171-9d63e0a55698

        @Assert: User group is removed from initial one successfully.

        @CaseLevel: Integration
        """
        sub_user_group = make_usergroup()
        user_group = make_usergroup({'user-group-ids': sub_user_group['id']})
        self.assertEqual(len(user_group['user-groups']), 1)
        UserGroup.remove_user_group({
            'id': user_group['id'],
            'user-group': sub_user_group['name'],
        })
        user_group = UserGroup.info({'id': user_group['id']})
        self.assertEqual(len(user_group['user-groups']), 0)
