#### Functions that help promp
print('>> Loading clases ', end='... ')

print('base,', end=' ')
from stego.item_types.items_base import SingleItem

print('gas,', end=' ')
from stego.item_types.items_gas import GasItem

print('clean surface,', end=' ')
from stego.item_types.items_clean import CleanSurf

print('adsorbed', end=' ')
from stego.item_types.items_adsorbed import AdsItem

print('... done')