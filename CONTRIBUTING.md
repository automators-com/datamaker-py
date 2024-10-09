# Contributing

## Pre-requisites

- [Node.js](https://nodejs.org/en/)
- [pnpm](https://pnpm.io/)

## Setup

The following steps can be followed to set up a development environment.

1. Clone the project and enter into the directory:

   ```sh
   git clone https://github.com/automators-com/datamaker-js.git
   cd datamaker-js
   ```

2. Install dependencies:

   ```sh
   pnpm install
   ```

You can now proceed to make changes to the project.

## Testing

This project uses `vitest` for testing purposes.

Tests will run in CI but can also be run manually using:

```sh
pnpm run test
```

## Building the package

The package can be built using:

```sh
pnpm run build
```

## Changelog

This project uses changesets to manage changes to the project. To add a new change, run:

```sh
pnpm exec changeset
```

This will prompt you for the type of change and a description.
