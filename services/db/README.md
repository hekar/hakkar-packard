# Database Service

This directory contains database migration scripts and configuration for the AI Learning project.

## Setup

1. Install [dbmate](https://github.com/amacneil/dbmate) for database migrations
2. Copy `.env.example` to `.env` and update with your database credentials
3. Run migrations with `make migrate` from the project root

## Environment Variables

- `DATABASE_URL`: Connection string for the PostgreSQL database

## Working with Migrations

- Create a new migration: `make new-migration name=your_migration_name`
- Apply all migrations: `make migrate`
- Rollback the last migration: `make rollback`

## Schema

The current schema includes:
- `accounts`: User account information and authentication data

## Security Notes

- Never commit `.env` files with real credentials to the repository
- Production deployments should use secure password storage mechanisms