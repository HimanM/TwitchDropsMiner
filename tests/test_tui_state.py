import unittest

from tui.state import (
    ChannelSnapshot,
    DropSnapshot,
    TUIState,
    clamp_progress,
    format_percent,
)


class TUIStateTests(unittest.TestCase):
    def test_progress_values_are_clamped_for_progress_bars(self):
        self.assertEqual(clamp_progress(-0.25), 0.0)
        self.assertEqual(clamp_progress(0.5), 0.5)
        self.assertEqual(clamp_progress(2.0), 1.0)

    def test_percent_formatting_uses_clamped_progress(self):
        self.assertEqual(format_percent(-0.25), "0.0%")
        self.assertEqual(format_percent(0.375), "37.5%")
        self.assertEqual(format_percent(2.0), "100.0%")

    def test_state_tracks_current_drop_progress(self):
        state = TUIState()
        state.set_drop(
            DropSnapshot(
                campaign="Campaign",
                game="Game",
                rewards="Reward",
                drop_progress=0.25,
                campaign_progress=0.75,
                remaining="00:42:00",
            )
        )

        self.assertEqual(state.current_drop.drop_progress, 0.25)
        self.assertEqual(state.current_drop.drop_percent, "25.0%")
        self.assertEqual(state.current_drop.campaign_percent, "75.0%")

    def test_channel_snapshots_are_text_only(self):
        channel = ChannelSnapshot(
            iid="1",
            name="Streamer",
            status="ONLINE",
            game="Game",
            viewers="123",
            drops=True,
            acl_based=False,
            watching=True,
        )

        self.assertEqual(channel.row, ("Streamer", "ONLINE", "Game", "yes", "123", "no"))


if __name__ == "__main__":
    unittest.main()
