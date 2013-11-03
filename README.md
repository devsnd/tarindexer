tarindexer
==========

python module for indexing tar files for fast access

Usage:

create index file:

    tarindexer -i tarfile.tar indexfile.index

lookup file using indexfile (prints file to stdout):

    tarindexer -l tarfile.tar indexfile.index lookuppath