import unittest
from types import SimpleNamespace

from network.twitch import Twitch


class FrontendInjectionTests(unittest.TestCase):
    def test_twitch_uses_injected_frontend_manager(self):
        created = []

        def factory(twitch):
            manager = SimpleNamespace(twitch=twitch)
            created.append(manager)
            return manager

        settings = SimpleNamespace()
        twitch = Twitch(settings, gui_factory=factory)

        self.assertIs(twitch.gui, created[0])
        self.assertIs(twitch.gui.twitch, twitch)


if __name__ == "__main__":
    unittest.main()
