qbot
====

Light-weight Python 3.6 IRC bot. Extremely easy to extend. See the wiki for
more information on what is possible.

### Installation

    git clone git@github.com:KDercksen/qbot && cd qbot
    pip install -r requirements.txt
    python setup.py install

### Usage

    qbot config.cfg

or to test regex patterns:

    qbot --dry config.cfg 'sample input string'
