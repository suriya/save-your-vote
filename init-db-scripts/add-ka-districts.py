
import string
from voterreg.models import IndianState, IndianDistrict

DISTRICTS = [
    ( 2, 'BAGALKOT'),
    (21, 'BANGALORE'),
    (22, 'BANGALORE RURAL'),
    ( 1, 'BELGAUM'),
    (12, 'BELLARY'),
    ( 5, 'BIDAR'),
    ( 3, 'BIJAPUR'),
    (29, 'CHAMARAJNAGAR'),
    (19, 'CHIKKABALLAPUR'),
    (17, 'CHIKMAGALUR'),
    (13, 'CHITRADURGA'),
    (26, 'DAKSHINA KANNADA'),
    (14, 'DAVANGERE'),
    ( 9, 'DHARWAD'),
    ( 8, 'GADAG'),
    ( 4, 'GULBARGA'),
    (25, 'HASSAN'),
    (11, 'HAVERI'),
    (27, 'KODAGU'),
    (20, 'KOLAR'),
    ( 7, 'KOPPAL'),
    (24, 'MANDYA'),
    (28, 'MYSORE'),
    ( 6, 'RAICHUR'),
    (23, 'RAMANAGARAM'),
    (15, 'SHIMOGA'),
    (18, 'TUMKUR'),
    (16, 'UDUPI'),
    (10, 'UTTARA KANNADA'),
    (35, 'YADGIR'),
]

KA = IndianState.objects.get(shortcode='KA')

for number, name in DISTRICTS:
    name = string.capwords(name)
    district = IndianDistrict(state=KA, name=name, number=str(number))
    district.save()
    print district
