# Moxie's Coding Assignment

### Prerequisites

The following dependencies are expected to be installed:

- [Python 3.12][python]
- [PostgreSQL][postgresql]
- [PDM][pdm]

#### MacOS Users

MacOS users are recommended to use [Homebrew][homebrew], a package manager that simplifies the installation of software on MacOS and Linux systems, to easily install the required dependencies for this project. If Homebrew is not yet installed, follow the instructions on its [homepage][homebrew].

Once Homebrew is installed, the project dependencies can be installed by running the following command in the terminal:

```bash
brew install python3 postgresql
```

### Database Setup

Before the project setup, follow these steps for database setup:

1. Start the PostgreSQL service. The command may vary depending on the operating system:
    - [Windows][postgres-windows]
    - [Linux][postgres-linux]

    #### MacOS

    ```bash
    brew services start postgresql
    ```

1. Connect to the default `postgres` database:
    ```bash
    psql postgres
    ```

1. If the `postgres` user does not exist, create a new user named `postgres` with password `postgres`:
    ```sql
    CREATE USER postgres WITH PASSWORD 'postgres';
    ```
   If the `postgres` user already exists, set the password for this user to 'postgres':
    ```sql
    ALTER USER postgres WITH PASSWORD 'postgres';
    ```

1. Create a database named `moxie` owned by the `postgres` user:
    ```sql
    CREATE DATABASE moxie OWNER postgres;
    ```

3. Exit the PostgreSQL shell:
    ```bash
    \q
    ```

### Project Setup

After the database setup, the following steps are followed to set up the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/lmiguelvargasf/moxie
    ```

1. Navigate into the project directory:
    ```bash
    cd moxie
    ```

1. Install the project dependencies using PDM:
    ```bash
    pdm install
    ```

1. Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```
   Open the `.env` file and replace the placeholders in the `DATABASE_URL` with the appropriate values. The connection string should reflect the values used in the [Database Setup](#database-setup) section. For example:
    ```
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/moxie
    ```
    In this example, `postgres` is the username and password, `localhost` is the host, `5432` is the port (default PostgreSQL port), and `moxie` is the database.

1. Run the project:
    ```bash
    pdm dev
    ```

1. Access the application by clicking on the following link: [`localhost:8000`](http://localhost:8000). The following response should be seen:
    ```
    {"status": "up"}

1. Access the admin tool by clicking on the following link: [`localhost:8000/admin`](http://localhost:8000/admin).


## Data Setup and API Usage

Create a med spa. You can do it by using the [admin tool](http://localhost:8000/admin/med-spa/list), `psql`, or any UI tool as [pgAdmin][].

The list of available endpoints is in [localhost:8000/docs](http://localhost:8000/docs).
In order to test the endpoints, feel free to use any tool you feel comfortable with like Postman, cURL, HTTPie, HTTPx, etc.

### Postman Collection

A [Postman][postman] collection has been included to test the endpoints that were implemented.
In order to use this collection, it is assumed you will need to [install Postman](https://www.postman.com/downloads/).
Then, you will need to import it.


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


[homebrew]: https://brew.sh/
[pgAdmin]: https://www.pgadmin.org/
[pdm]: https://pdm-project.org/latest/
[postgresql]: https://www.postgresql.org/
[postgres-linux]: https://askubuntu.com/questions/1206416/how-to-start-postgresql
[postgres-windows]: https://stackoverflow.com/questions/36629963/how-can-i-start-postgresql-on-windows
[postman]: https://www.postman.com/
[python]: https://www.python.org/
