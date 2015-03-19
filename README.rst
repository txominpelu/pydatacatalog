
====
CLI: Get path for a symbol
====


.. code-block:: bash

   python -m pydatacatalog.datacatalog --host datacatalog01.preprod.sf.viadeo.internal data.unsubscribe.201501

====
How to build the .deb package
====


- Build dockerfile

.. code-block:: bash

   sudo docker build -t imediavilla/debian-squeeze-py2.6 .


- Run docker image

.. code-block:: bash

   sudo docker run -i -v $PWD:/mnt -t imediavilla/debian-squeeze-py2.6 /bin/bash

- To build the package:  
  
.. code-block:: bash

   /var/lib/gems/1.8/bin/fpm -s python -t deb /mnt

