
import in_states
from voterreg.models import IndianState

for (short, longname) in sorted(in_states.STATE_CHOICES):
    state = IndianState(name=longname, shortcode=short)
    state.save()
    print state
