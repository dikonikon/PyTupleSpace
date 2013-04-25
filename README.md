PyTupleSpace
============

A cloud ready TupleSpace using Python.

see https://github.com/dikonikon/WebTupleSpace: now being developed in Scala

PyTupleSpace aims to provide a place for dynamic and loosely coupled interaction and exchange of objects in a distributed system such as the internet.

It implements a tuple space where the interface is defined and implemented using web services rather than being
language dependent, but provides bindings on to Python and JavaScript as starting point. 

It uses mongodb for storage, both for its ability to scale horizontally and for its natural support for tuple-like data structures.

# Use Cases

## Loose coupling of virtual organisations

The Cloud is a lot about agility - fast set up and tear down of processes and organisations to meet needs in a fraction of the time and a fraction of the cost that would traditionally have been required.

One powerful use case revolves around the idea of creating 'virtual organisations' that support loosely coupled business processes. Each organisation interacts with the others using the tuplespace as a central place to do business.

Using the tuplespace the participants can both dynamically refine the common information model that they use to interact, and also use the ability of the tuplespace to notify subscribers about the presence of matching tuples to drive the loosely coupled exchange of information.

WebTupleSpace aims as a starting point to support this process in a resilient and horizontally scalable implementation. It will then go on to consider issues of identity, shared domains and authorization.

## Common model integration

One approach to complex systems integration is to integrate many systems around a common information model. One approach to this is to place a layer of services over the systems that conform in their interfaces to a common model. Another way is to provide a more concrete realisation of the common model, and to integrate by mediating each systems interaction with that model.

A simple way to achieve this latter style of integration is to use a tuplespace as the platform for the realisation of that model.

# Current Status

Simple working test implementation of the tuplespace exists that supports a rudimentary representation of tuples

Current work focuses on:

* richer representation of tuples including explicit annotation of the types of elements: current representation is as a list of byte arrays, which are assumed to incorporate type information. This has the benefit of being simple both to implement and to create language bindings for, but it has significant drawbacks. For example semantically equivalent tuples from different bindings are not equivalent, and it presents fewer opportunities for sharding (see next bullet)
* implementation using Mongodb thinking about approach to sharding

