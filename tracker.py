from jnius import autoclass
from kivy.utils import platform
from kivy.logger import Logger


class AbstractTracker(object):

    def __init__(self, id):
        self.id = id

    def _get_tracker(self):
        raise NotImplementedError()

    def send_screen(self, screen):
        Logger.info('Tracking: Sending screen for %s' % screen.name)


    def clear_screen(self):
        Logger.info('Tracking: Cleared screen')

    def send_event(self, category, action, label=None, value=None):
        Logger.info('Tracking: event sent - %s-%s-%s-%s' % (
            category, action, label, int(value) if value is not None else value)
        )

    def send_to_server(self):
        Logger.info('Tracking: sending data from local storage')


if platform == 'android':
    ScreenViewBuilder = autoclass('com.google.android.gms.analytics.HitBuilders$ScreenViewBuilder')
    EventBuilder = autoclass('com.google.android.gms.analytics.HitBuilders$EventBuilder')
    GoogleAnalytics = autoclass('com.google.android.gms.analytics.GoogleAnalytics')
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    AndroidString = autoclass('java.lang.String')

    class GoogleTracker(AbstractTracker):
        def _get_tracker(self):
            import settings

            app = PythonActivity.getApplication()

            analytics = GoogleAnalytics.getInstance(app)
            if settings.DEVELOPMENT_VERSION:
                analytics.setDryRun(True)

            tracker = analytics.newTracker(AndroidString(self.id))
            tracker.setSessionTimeout(300)
            # tracker.enableAutoActivityTracking(True)

            return tracker

        def send_screen(self, screen):
            super(GoogleTracker, self).send_screen(screen)
            tracker = self._get_tracker()
            tracker.setScreenName(AndroidString(screen.name))
            tracker.send(ScreenViewBuilder().build())

        def clear_screen(self):
            super(GoogleTracker, self).clear_screen()
            tracker = self._get_tracker()
            tracker.setScreenName(None)

        def send_event(self, category, action, label=None, value=None):
            super(GoogleTracker, self).send_event(category, action, label)
            tracker = self._get_tracker()
            event = EventBuilder().setCategory(category).setAction(action)
            if label:
                event.setLabel(label)

            if value:
                event.setValue(int(value))

            tracker.send(event.build())

        def send_to_server(self):
            super(GoogleTracker, self).send_to_server()
            GoogleAnalytics.getInstance(PythonActivity.getBaseContext()).dispatchLocalHits()

    Tracker = GoogleTracker

else:
    class DummyTracker(AbstractTracker):
        pass

    Tracker = DummyTracker
