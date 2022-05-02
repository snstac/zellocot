Zello to Cursor-On-Target Gateway.
**********************************

.. image:: https://raw.githubusercontent.com/ampledata/zellocot/main/docs/Screenshot_20201026-142037_ATAK-25p.jpg
   :alt: Screenshot of ADS-B PLI in ATAK.
   :target: https://github.com/ampledata/zellocot/blob/main/docs/Screenshot_20201026-142037_ATAK.jpg


The ZelloCOT Zello to Cursor-On-Target Gateway transforms Zello user location 
information into Cursor-On-Target (COT) Polsition Location Information (PLI) 
for display on Situational Awareness (SA) applications such as the 
Android Team Awareness Kit (ATAK), WinTAK, RaptorX, TAKX, iTAK, et al. 

For more information on the TAK suite of tools, see: https://www.tak.gov/

Support ZelloCOT Development
============================

ZelloCOT has been developed for the Disaster Response, Public Safety and
Frontline Healthcare community. This software is currently provided at no-cost
to users. Any contribution you can make to further this project's development
efforts is greatly appreciated.

.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :target: https://www.buymeacoffee.com/ampledata
    :alt: Support ZelloCOT development: Buy me a coffee!

Installation
============

ZelloCOT's functionality provided by a command-line program called `zellocot`.

Installing as a Debian / Ubuntu Package [Recommended]::

    $ sudo apt update
    $ wget https://github.com/ampledata/pytak/releases/latest/download/python3-pytak_latest_all.deb
    $ sudo apt install -f ./python3-pytak_latest_all.deb
    $ wget https://github.com/ampledata/zellocotcot/releases/latest/download/python3-zellocot_latest_all.deb
    $ sudo apt install -f ./python3-zellocot_latest_all.deb


Install from the Python Package Index (PyPI) [Advanced Users]::

    $ pip install zellocot


Install from this source tree [Developers]::

    $ git clone https://github.com/ampledata/zellocot.git
    $ cd zellocot/
    $ python setup.py install


Usage
=====

The `zellocot` command-line program uses an INI-style configuration file.


Troubleshooting
===============

To report bugs, please set the DEBUG=1 environment variable to collect logs.

Source
======
ZelloCOT source can be found on Github: https://github.com/ampledata/zellocot

Author
======
ZelloCOT is written and maintained by Greg Albrecht W2GMD oss@undef.net

https://ampledata.org/

Copyright
=========
ZelloCOT is Copyright 2022 Greg Albrecht

License
=======
ZelloCOT is licensed under the Apache License, Version 2.0. See LICENSE for
details.
