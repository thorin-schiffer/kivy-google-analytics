kivy-google-analytics
=====================

Kivy google analytics client. Currently only for android.

Usage:

```
from tracking import Tracker

...

tracker = Tracker("UA-XXXXXXXX-X")

# send event
self.tracker.send_event('category', 'action', 'label', value=starts_count + 1)

# send screen
tracker.send_screen(kivy_screen)

# clear screen
tracker.clear_screen(kivy_screen)
```
