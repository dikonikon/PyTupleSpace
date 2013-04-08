PyTupleSpace
============

A cloud ready TupleSpace using Python.

PyTupleSpace aims to provide a place for dynamic and loosely coupled interaction and exchange of objects in a distributed system such as the internet.

It implements a tuple space where the interface is defined and implemented using web services rather than being
language dependent, but provides bindings on to Python and JavaScript as starting point. 

It uses mongodb for storage, both for its ability to scale horizontally and for its natural support for tuple-like data structures.

# Use Cases

One powerful use case revolves around the idea of creating 'virtual organisations' that support loosely coupled business processes. Each organisation interacts with the others using the tuplespace as a central place to do business.

Using the tuplespace the participants can both dynamically refine the common information model that they use to interact, and also use the ability of the tuplespace to notify subscribers about the presence of matching tuples to drive the loosely coupled exchange of information.

# Current Status

Simple working test implementation of the tuplespace exists that supports a rudimentary representation of tuples

Current work focuses on:

* richer representation of tuples including explicit annotation of the types of elements
* implementation using Mongodb thinking about approach to sharding

