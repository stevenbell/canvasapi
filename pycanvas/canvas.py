from account import Account
from course import Course
from paginated_list import PaginatedList
from requester import Requester
from user import User
from group import Group
from util import combine_kwargs


class Canvas(object):
    """
    The main class to be instantiated to provide access to Canvas's API.
    """

    def __init__(self, base_url, access_token, adapter=None):
        """
        :param base_url: The base URL of the Canvas instance's API.
        :type base_url: str
        :param access_token: The API key to authenticate requests with.
        :type access_token: str
        :param adapter: The requests_mock adapter (for testing).
        :type adapter: :class:`requests_mock.Adapter`
        """
        self.__requester = Requester(base_url, access_token, adapter)

    def create_account(self, **kwargs):
        """
        Create a new root account.

        :calls: `POST /api/v1/accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.create>`_

        :rtype: :class:`pycanvas.account.Account`
        """
        response = self.__requester.request(
            'POST',
            'accounts',
            **combine_kwargs(**kwargs)
        )
        return Account(self.__requester, response.json())

    def get_account(self, account_id):
        """
        Retrieve information on an individual account.

        :calls: `GET /api/v1/accounts/:id \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show>`_

        :param account_id: The ID of the account to retrieve.
        :type account_id: int
        :rtype: :class:`pycanvas.account.Account`
        """
        response = self.__requester.request(
            'GET',
            'accounts/%s' % (account_id)
        )
        return Account(self.__requester, response.json())

    def get_accounts(self, **kwargs):
        """
        List accounts that the current user can view or manage.

        Typically, students and teachers will get an empty list in
        response. Only account admins can view the accounts that they
        are in.

        :calls: `GET /api/v1/accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.Account`
        """
        return PaginatedList(
            Account,
            self.__requester,
            'GET',
            'accounts',
            **combine_kwargs(**kwargs)
        )

    def get_course_accounts(self):
        """
        List accounts that the current user can view through their
        admin course enrollments (Teacher, TA or designer enrollments).

        Only returns `id`, `name`, `workflow_state`, `root_account_id`
        and `parent_account_id`.

        :calls: `GET /api/v1/course_accounts \
        <https://canvas.instructure.com/doc/api/accounts.html#method.accounts.course_accounts>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.account.Account`
        """
        return PaginatedList(
            Account,
            self.__requester,
            'GET',
            'course_accounts',
        )

    def get_course(self, course_id):
        """
        Retrieve a course by its ID.

        :calls: `GET /courses/:id \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.show>`_

        :param course_id: The ID of the course to retrieve.
        :type course_id: int
        :rtype: :class:`pycanvas.course.Course`
        """
        response = self.__requester.request(
            'GET',
            'courses/%s' % (course_id)
        )
        return Course(self.__requester, response.json())

    def get_user(self, user_id, id_type=None):
        """
        Retrieve a user by their ID. `id_type` denotes which endpoint to try as there are
        several different IDs that can pull the same user record from Canvas.

        Refer to API documentation's `User <https://canvas.instructure.com/doc/api/users.html#User>`_
        example to see the ID types a user can be retrieved with.

        :calls: `GET /users/:id \
        <https://canvas.instructure.com/doc/api/users.html#method.users.api_show>`_

        :param user_id: The user's ID.
        :type user_id: str
        :param id_type: The ID type.
        :type id_type: str
        :rtype: :class:`pycanvas.user.User`
        """
        if id_type:
            uri = 'users/%s:%s' % (id_type, user_id)
        else:
            uri = 'users/%s' % (user_id)

        response = self.__requester.request(
            'GET',
            uri
        )
        return User(self.__requester, response.json())

    def get_courses(self, **kwargs):
        """
        Return a list of active courses for the current user.

        :calls: `GET /api/v1/courses \
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.course.Course`
        """
        return PaginatedList(
            Course,
            self.__requester,
            'GET',
            'courses',
            **combine_kwargs(**kwargs)
        )

    def get_activity_stream_summary(self):
        """
        Return a summary of the current user's global activity stream.

        :calls: `GET /api/v1/users/self/activity_stream/summary \
        <https://canvas.instructure.com/doc/api/users.html#method.users.activity_stream_summary>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/activity_stream/summary'
        )
        return response.json()

    def get_todo_items(self):
        """
        Return the current user's list of todo items, as seen on the user dashboard.

        :calls: `GET /api/v1/users/self/todo \
        <https://canvas.instructure.com/doc/api/users.html#method.users.todo_items>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/todo'
        )
        return response.json()

    def get_upcoming_events(self):
        """
        Return the current user's upcoming events, i.e. the same things shown
        in the dashboard 'Coming Up' sidebar.

        :calls: `GET /api/v1/users/self/upcoming_events \
        <https://canvas.instructure.com/doc/api/users.html#method.users.upcoming_events>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'users/self/upcoming_events'
        )
        return response.json()

    def get_course_nicknames(self):
        """
        Return all course nicknames set by the current account.

        :calls: `GET /api/v1/users/self/course_nicknames \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.index>`_

        :rtype: :class:`pycanvas.paginated_list.PaginatedList` of :class:`pycanvas.course_nickname.CourseNickname`
        """
        from course import CourseNickname

        return PaginatedList(
            CourseNickname,
            self.__requester,
            'GET',
            'users/self/course_nicknames'
        )

    def get_course_nickname(self, course_id):
        """
        Return the nickname for the given course.

        :calls: `GET /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.show>`_

        :param course_id: The ID of the course.
        :type course_id: int
        :rtype: :class:`pycanvas.course_nickname.CourseNickname`
        """
        from course import CourseNickname

        response = self.__requester.request(
            'GET',
            'users/self/course_nicknames/%s' % (course_id)
        )
        return CourseNickname(self.__requester, response.json())

    def get_section(self, section_id):
        """
        Get details about a specific sections
        :calls: `GET /api/v1/sections/:id`
        <https://canvas.instructure.com/doc/api/sections.html#method.sections.index>
        :rtype: Section
        """
        from section import Section
        response = self.__requester.request(
            'GET',
            'sections/%s' % (section_id)
        )
        return Section(self.__requester, response.json())

    def set_course_nickname(self, course_id, nickname):
        """
        Set a nickname for the given course. This will replace the
        course's name in the output of subsequent API calls, as
        well as in selected places in the Canvas web user interface.

        :calls: `PUT /api/v1/users/self/course_nicknames/:course_id \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.update>`_

        :param course_id: The ID of the course.
        :type course_id: int
        :param nickname: The nickname for the course.
        :type nickname: str
        :rtype: :class:`pycanvas.course_nickname.CourseNickname`
        """
        from course import CourseNickname

        response = self.__requester.request(
            'PUT',
            'users/self/course_nicknames/%s' % (course_id),
            nickname=nickname
        )
        return CourseNickname(self.__requester, response.json())

    def clear_course_nicknames(self):
        """
        Remove all stored course nicknames.

        :calls: `DELETE /api/v1/users/self/course_nicknames \
        <https://canvas.instructure.com/doc/api/users.html#method.course_nicknames.delete>`_

        :returns: True if the nicknames were cleared, False otherwise.
        :rtype: bool
        """
        response = self.__requester.request(
            'DELETE',
            'users/self/course_nicknames'
        )
        return response.json().get('message') == 'OK'

    def search_accounts(self, **kwargs):
        """
        Return a list of up to 5 matching account domains. Partial matches on
        name and domain are supported.

        :calls: `GET /api/v1/accounts/search \
        <https://canvas.instructure.com/doc/api/account_domain_lookups.html#method.account_domain_lookups.search>`_

        :rtype: dict
        """
        response = self.__requester.request(
            'GET',
            'accounts/search',
            **combine_kwargs(**kwargs)
        )
        return response.json()

    def get_single_group(self, group_id, **kwargs):
        """
        Return the data for a single group. If the caller does not
        have permission to view the group a 401 will be returned.

        :calls: `GET /api/v1/groups/:group_id \
        <https://canvas.instructure.com/doc/api/groups.html#method.groups.show>`_

        :rtype: :class:`pycanvas.group.Group`
        """
        response = self.__requester.request(
            'GET',
            'groups/%s' % (group_id),
            **combine_kwargs(**kwargs)
        )
        return Group(self.__requester, response.json())
