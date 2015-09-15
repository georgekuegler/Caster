from dragonfly import Function, Choice

from caster.lib import navigation, control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R

class Alphabet(MergeRule):
    pronunciation = control.CCRMerger.CORE[0]
    
    mapping = {
        "[<big>] <letter>": R(Function(navigation.letters2, extra ={"big", "letter"}), rdescript="Spell"),
        }
    extras = [
        navigation.get_alphabet_choice("letter"),
        Choice("big",
              {"big": "big",
               }),
    ]
    defaults = {
    "big": "", 
    }
    
control.nexus().merger.add_global_rule(Alphabet())