import unittest
from types import SimpleNamespace

from core.constants import State
from core.exceptions import GQLException
from network.twitch import Twitch
from tui.manager import TUIManager


class TermuxCLIRegressionTests(unittest.IsolatedAsyncioTestCase):
    async def test_notification_delete_not_found_is_ignored(self):
        twitch = Twitch.__new__(Twitch)
        states = []

        def change_state(state):
            states.append(state)

        async def gql_request(_operation):
            raise GQLException([
                {"message": "notification not found", "path": ["deleteNotification"]}
            ])

        twitch.change_state = change_state
        twitch.gql_request = gql_request

        await Twitch.process_notifications(
            twitch,
            1,
            {
                "type": "create-notification",
                "data": {
                    "notification": {
                        "id": "notification-id",
                        "type": "user_drop_reward_reminder_notification",
                    }
                },
            },
        )

        self.assertEqual([State.INVENTORY_FETCH], states)

    async def test_notification_delete_other_errors_still_raise(self):
        twitch = Twitch.__new__(Twitch)
        twitch.change_state = lambda _state: None

        async def gql_request(_operation):
            raise GQLException([{"message": "service unavailable"}])

        twitch.gql_request = gql_request

        with self.assertRaises(GQLException):
            await Twitch.process_notifications(
                twitch,
                1,
                {
                    "type": "create-notification",
                    "data": {
                        "notification": {
                            "id": "notification-id",
                            "type": "user_drop_reward_reminder_notification",
                        }
                    },
                },
            )


class TUIManagerRegressionTests(unittest.TestCase):
    def test_print_does_not_require_textual_log_hook(self):
        twitch = SimpleNamespace(
            settings=SimpleNamespace(
                priority=[],
                exclude=set(),
                priority_mode=None,
                farm_unlinked=False,
            )
        )
        manager = TUIManager(twitch)
        manager._app = SimpleNamespace()

        manager.print("hello")

        self.assertTrue(any("hello" in line for line in manager.state.logs))


if __name__ == "__main__":
    unittest.main()
