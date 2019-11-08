# example script using WWT toasty to produce tiled image data
# need to use WWT fork of toasty, not pip version
# https://github.com/WorldWideTelescope/toasty
# see https://toasty.readthedocs.io/en/latest/examples.html  based on "Controlling How Data Turned into RGB"

from toasty.toast import toast # import toast, normalizer, cartesian_sampler, healpix_sampler
from toasty.samplers import plate_carree_sampler, normalizer
from astropy.io import fits
from astropy.wcs import WCS
import astropy.units as u
import numpy as np

path = '/Users/Brian/Work/Manga/analysis/v2_5_3/2.3.0/HYB10-MILESHC-MILESHC/8485/1901/manga-8485-1901-MAPS-HYB10-MILESHC-MILESHC.fits.gz'
hdu = fits.open(path)
data = hdu['EMLINE_GFLUX'].data[18,:,:]
w = WCS(hdu[1].header).celestial

# applies some scaling to image 
vmin, vmax = 100, 65535
scaling = 'log'
contrast = 1
sampler = normalizer(
  plate_carree_sampler(data),
  vmin, vmax,
  scaling, None, contrast
)


# see in example page - Arbritrary coordindate transformation
def sampler(x, y):
    ''' custom sampler 
    x and y are arrays, giving the RA/Dec centers
    (in radians) for each pixel to extract
    '''
    # convert radians to degrees (and condense down (ravel) into single dimension)
    xdeg = (x.ravel() * u.radian).to('degree').value
    ydeg = (y.ravel() * u.radian).to('degree').value
    # get pixel values at each world coordinate
    pixels = np.ceil(w.all_world2pix(xdeg,ydeg,0)).astype('int')
    # reorganize into list of (x,y) tuples
    xycoord = list(zip(*pixels))
    # map each item in list to retrieve the pixel value in data at the index location
    vals = list(map(lambda x:data[x] if x[0] >=0 and x[0] <= data.shape[0] else -1, xycoord))
    # reshape into original shape
    return np.array(vals).reshape(x.shape)

output_directory = 'toast'
depth = 4
toast(sampler, depth, output_directory)
