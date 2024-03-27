# Django Rest Framework with DDD and CQRS REST API
[![codecov](https://codecov.io/gh/AdriRRP/joinup-challenge/graph/badge.svg?token=HfvheNjVR0)](https://codecov.io/gh/AdriRRP/joinup-challenge)

This repository is a proposal for the technical challenge launched by Joinup.
The challenge requirements are the following:

- Context
  - High availability / High performance backend
    - The system must work 24/7
    - The system must handle between 2500 and 3500 requests per minute
  - The system must be very fast in responding to requests
  - Optimized database queries, as they are usually the bottleneck
- Requirements
  - Develop a REST API for user management
  - Use Python with Django and Django Rest Framework
  - The API must have 2 endpoints:
    - A **user signup** endpoint
      - Proposed route: `^/api/VERSION_API/signup/$`
      - User fields: `name`, `surname`, `email`, `phone` and `hobbies`
      - The `email` field must be validated through a confirmation email
      - The `phone` field must be validated through a confirmation SMS
      - Sending emails and SMS is supposed to take a long time, so they must be implemented **asynchronously**
      - There must be **separate configurations** for the development and production environment
    - An **access to user profile** endpoint
      - Proposed route: `^/api/VERSION_API/profile/$`
      - User fields: `name`, `surname`, `email`, `phone`, `hobbies`, `email_verified` and `phone_verified`
  - Use the best development practices you know

## Project Approach

As a background of good practices I will use my own interpretation of *Domain Driven Design* influenced by the wonderful CodelyTV Pro courses.

Also since there are high availability and high performance requirements, I will use CQRS to make an optimized reading model and run heavy tasks in the background.

It should be noted that the use of Domain Driven Design and CQRS advocates avoiding the use of active record and ORMs, which is one of the base parts of Django and Django Rest Framework.

I am aware that these features are one of the strong points when it comes to achieving quick results developing with Django and Django Rest Framework, but they can be counterproductive when optimizing aspects related to performance and scalability.

For this reason I have decided not to use the native mechanisms of Django and Django Rest Framework and to use patterns recommended by Domain Driven Design and CQRS.

## Project Structure

Because Django and Django Rest Framework according to Domain Driven Design are implementation details of the application, so they will go within the infrastructure part of it.

This will allow the decoupling of the business logic from the framework that implements it, guaranteeing the principles of Open Closed and Dependency Inversion of SOLID.

The following directory structure has been chosen:

```bash
├── app                   # Applications stored in this repository
│   └── challenge         # Application for bounded context `challenge`
├── docs                  # Documentation
├── env                   # (ignored by git) Virtual environment for development environment
├── etc                   # Application configuration and aux files 
├── lib                   # Libraries stored in this repository
│   ├── challenge         # Main library of bounded context `challenge`
│   │   ├── notification  # Notification module
│   │   └── user          # User module
│   └── shared            # Common code for all bounded context
└── tests                 # Tests folder
    ├── app               # Applications related tests
    │   └── challenge     # Tests for application of bounded context `challenge`
    └── lib               # Libraries related tests
        ├── challenge     # Tests for library of bounded context `challenge`
        └── shared        # Tests for common code
```