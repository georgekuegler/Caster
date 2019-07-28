from castervoice.lib.dfplus.ccrmerging2.hooks.events.base_event import BaseHookEvent
from castervoice.lib.dfplus.ccrmerging2.hooks.events.event_types import EventType


class RuleActivationEvent(BaseHookEvent):
    def __init__(self, rule_class_name, active):
        super(EventType.ACTIVATION)
        self.rule_class_name = rule_class_name
        self.active = active
