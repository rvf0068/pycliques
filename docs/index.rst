pycliques
=========

This is the documentation of **pycliques**. This is an extension to the library `networkx <https://networkx.github.io/>`_ in order to work with the clique graph operator (and some other problems in combinatorial topology).

A *clique* of a graph is a maximal complete subgraph.  The clique graph of a graph is the intersection graph of the set of its cliques.

The clique graph of a graph :math:`G` is denoted as :math:`K(G)`. We can define the *iterated clique graphs* as the graphs in the sequence: :math:`G`, :math:`K(G)`, :math:`K^{2}(G)=K(K(G))`, etc. A graph is *divergent* if the set of orders of the iterated clique graphs is unbounded, and the graph is *convergent* if it is not divergent. A major problem in the area is, given a graph :math:`G`, deciding whether the graph is convergent or divergent.

========
Contents
========

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Module Reference <api/modules>


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
