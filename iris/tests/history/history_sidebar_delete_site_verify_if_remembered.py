# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Delete a page from the History sidebar and verify it is still remembered in the URL bar.'
        self.test_case_id = '120131'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

        return

    def run(self):
        search_history_box = Pattern('search_history_box.png')
        expand_button_history_sidebar = Pattern('expand_button_history_sidebar.png')
        local_server_autocomplete = Pattern('local_server_autocomplete.png')
        mozilla_bookmark_small_pattern = LocalWeb.MOZILLA_BOOKMARK_SMALL

        # Open some pages to create some history.
        close_tab()
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')
        close_tab()

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_2, 'Firefox page loaded successfully.')
        close_tab()
        new_tab()

        # Open the History sidebar.
        history_sidebar()
        expected_3 = exists(search_history_box, 10)
        assert_true(self, expected_3, 'Sidebar was opened successfully.')
        expected_4 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_4, 'Expand history button displayed properly.')
        click(expand_button_history_sidebar)

        # Delete a page from the History sidebar.
        expected_5 = exists(mozilla_bookmark_small_pattern, 10)
        assert_true(self, expected_5, 'Mozilla page is displayed in the History list successfully.')

        right_click(mozilla_bookmark_small_pattern)
        type(text='d')

        try:
            expected_6 = wait_vanish(mozilla_bookmark_small_pattern, 10)
            assert_true(self, expected_6, 'Mozilla page was deleted successfully from the history.')
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')
        expected_7 = exists(mozilla_bookmark_small_pattern.similar(0.9), 10)
        assert_false(self, expected_7, 'Mozilla page is not displayed in the Recent History list.')
        type(Key.ESC)

        # Check that the local server is still auto-completed in the URL bar.
        select_location_bar()
        paste('127')

        expected_8 = exists(local_server_autocomplete, 10)
        assert_true(self, expected_8, 'Local server is auto-completed successfully.')
