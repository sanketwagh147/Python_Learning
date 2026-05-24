# ABCs and Protocols Practice Problems

These problems show how to model contracts without overcoupling implementations.

## Problem 1 - Payment Gateway Contract
Scenario: Your checkout service supports Stripe today and a second provider next quarter.

Build an abstract base class that:
- defines the required payment operations
- forces concrete gateways to implement them
- allows shared helper logic in the base class
- keeps provider-specific details out of calling code

## Problem 2 - Storage Provider Protocol
Scenario: A reporting module can upload files to S3, local disk, or an in-memory fake during tests.

Build a `Protocol` that:
- describes the methods the uploader needs
- supports structural typing instead of inheritance
- makes test doubles easy to write
- keeps the reporting code generic

## Problem 3 - Notification Channels
Scenario: Product wants email, SMS, and in-app notifications behind one dispatch service.

Build a design using ABCs or protocols that:
- standardizes the send contract
- allows capability differences where needed
- keeps dispatch logic simple
- makes it easy to add a new channel later

## Problem 4 - Exporter Plugins with Runtime Validation
Scenario: Data users can export reports as CSV, JSON, or Excel through pluggable exporters.

Build a design that:
- validates exporters before registration
- gives helpful errors if a plugin is incomplete
- separates the contract from registration concerns
- supports both production exporters and test doubles

## Problem 5 - Rule Engine Extensions
Scenario: Fraud detection uses many independently developed rule objects, and the engine should accept anything that follows the right behavior contract.

Build a design that:
- uses protocols for flexible rule inputs
- allows rules to carry metadata like severity
- supports collections of mixed rule implementations
- keeps the engine strongly typed and maintainable