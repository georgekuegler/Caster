from dragonfly import Function, MappingRule, Key

from castervoice.lib.ctrl.mgr.loading.reload.base_reload_observable import (
    BaseReloadObservable,
)
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails

from time import sleep

try:
    from natlink import setMicState
except:
    setMicState = lambda x: None

try:
    from library import notify

    use_toast = True
except:
    use_toast = False


class Listener:
    def __init__(self):
        self.reloaded_files = []

    def receive(self, path_changed):
        self.reloaded_files.append(path_changed)

    def reset(self):
        self.reloaded_files = []

    def notify_user(self):
        msg = "caster" if self.reloaded_files else "nothing"
        if use_toast:
            notify.toast(msg, "reloaded")


class ManualReloadObservable(BaseReloadObservable):
    """
    Allows for reloading changed files on command.
    """

    def __init__(self):
        super(ManualReloadObservable, self).__init__()

        """
        This class itself will never be reloaded, but it can
        be registered like the other rules and so can have
        transformers run over it, etc.
        """

        class ManualGrammarReloadRule(MappingRule):
            mapping = {
                "reload all rules": Function(self.reload_all_rules),
                "rejuvenate": Function(self.reload_everything),
            }

        self._rule_class = ManualGrammarReloadRule
        self.listener = Listener()
        self.register_listener(self.listener)

    def reload_all_rules(self):
        self.listener.reset()
        self._update()
        self.listener.notify_user()

    def reload_everything(self):
        self.listener.reset()
        Key("c-s/30").execute()  # save current file
        # cycle microphone to reload any changed dragonfly grammars
        setMicState("off")
        sleep(0.2)
        setMicState("on")
        # reload caster rules
        self.listener.reset()
        self._update()
        self.listener.notify_user()

    def get_loadable(self):
        details = RuleDetails(
            name="caster manual grammars reload command rule", watch_exclusion=True
        )
        return self._rule_class, details
