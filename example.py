from subPhotoInterp import subPhotoInterp
import numpy

#Make an instance
sub = subPhotoInterp("TableModel_grid256_res8_Nrs.fits")

# By default it will print the parameter names and ranges
# To disable this, instead do:

sub = subPhotoInterp("TableModel_grid256_res8_Nrs.fits",silent=True)


# You can pass a single energy or an array of energies:

eneGrid = numpy.logspace(1,4,100)

tau = 2.
gamma = 100.
lgrb = 10.
ed = .3

# The first argument is energy
# the next arguments depend on what is in the table

fluxes = sub(eneGrid,tau,gamma,lgrb,ed)

# The order of the arguments is based on the table
# and is the same order as what is displayed by executing:

sub.PrintParameters()


# You can then plot the fluxes or as you wish

