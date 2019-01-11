"""Save and load timeseries of Hamiltonians

"""
from collections import namedtuple
from datetime import datetime
import h5py

from . import logger
from . import __version__


KugupuResults = namedtuple("KugupuResults",
                           ['frames',
                            'H_frag',
                            'S_frag'])

_DATEFORMAT = '%Y-%m-%d %H:%M:%S'


def save_results(results, filename):
    """Save results to HDF5 file

    Parameters
    ----------
    results : kugupu.Results namedtuple
      finished results to save
    filename : str
      filename, must not yet exist.  '.hdf5' will be appended
      if not present
    """
    if not filename.endswith('.hdf5'):
        filename += '.hdf5'

    logger.debug("Saving results to {}".format(filename))
    with h5py.File(filename, 'w-') as f:
        f.attrs['kugupu_version'] = __version__
        f.attrs['creation_date'] = datetime.now().strftime(_DATEFORMAT)

        f['frames'] = results.frames
        f['H_frag'] = results.H_frag
        f['S_frag'] = results.S_frag


def load_results(filename):
    """Load results from HDF5 file

    Parameters
    ----------
    filename : str
      path to HDF5 file

    Returns
    -------
    results : KugupuResults namedtuple
      the contents of the file
    """
    if not filename.endswith('.hdf5'):
        filename += '.hdf5'

    logger.debug("Loading results from {}".format(filename))
    with h5py.File(filename, 'r+') as f:
        logger.debug("Results from {}"
                     "".format(datetime.strptime(f.attrs['creation_date'],
                                                 _DATEFORMAT)))
        logger.debug("Saved with version: {}"
                     "".format(f.attrs['kugupu_version']))
        idx = f['frames'][()]
        H_frag = f['H_frag'][()]
        S_frag = f['S_frag'][()]

    return KugupuResults(idx, H_frag, S_frag)
