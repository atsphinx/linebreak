==================
atsphinx-linebreak
==================

Enable line-break for everywhere.

Overview
========

This is Sphinx-extension to inject extra node into line-break of source (LF) when it build.
You can write source likely GitHub Flavored Markdown ("Newline" code means as "line-feed of content") by using it.

.. note::

   This affects to any sources including reStructuredText.
   If you want to change behavior, post PR or issue into GitHub.

Getting started
===============

.. code:: console

   pip install atsphinx-linebreak

.. code:: python

   extensions = [
       ...,  # Your extensions
       "atsphinx.linebreak",
   ]
