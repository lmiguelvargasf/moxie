# Moxie's Coding Assignment

## Assumptions and Rationales

### No Authentication Required

**Assumption:** API authentication is not initially required since there are no explicitly required user roles or data privacy concerns demanding such authentication.

**Rationale**: the focus of the assignment is primarily on demonstrating CRUD functionality and the relationships between entities rather than securing those operations. Omitting authentication simplifies the initial setup and accelerates development, which is crucial within the constrained timeline of 2-3 hours.

### No User Tracking

**Assumption**: it is not required to track the identity of the individual making the appointment since the assignment does not include user identities in the data model for appointments or services.

**Rationale**: considering the time constraints and the directions provided, it seems reasonable to focus on the relationship between med spas, services, and appointments without complicating the schema with user management.

### Standard Business Hours and Timezone

**Assumption**: med spas operate during standard business hours (9:00 AM to 5:00 PM) and follow the local timezone of their physical locations.

**Rationale**: the assignment does not provide specifics on operating hours or timezone management, so assuming standard business hours simplifies scheduling, availability checks, and conflict management, avoiding the complexities of handling various timezones or extended hours.

### Unlimited Availability of Services

**Assumption**: all services offered by the med spas are available without
constraints of inventory or specific availability slots.

**Rationale**: no details are provided about limitations on service availability.
This assumption will avoid implementing inventory or slot management systems.
