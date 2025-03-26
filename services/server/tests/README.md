# Testing Guidelines

## Test Types

### Unit Tests

Unit tests focus solely on testing service logic in isolation, with no external dependencies. They should:

- Test only code in the `services` directory
- Mock all external dependencies (repositories, etc.)
- Use pytest fixture `mock_dependencies` to manage mocks consistently
- Be fast and not require any external services

### Integration Tests

Integration tests focus only on testing API endpoints through the FastAPI test client. They should:

- Make HTTP requests to endpoints using `test_client`
- Verify the API contract (status codes, response format)
- Not be concerned with internal implementation details

## Running Tests

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run tests with coverage
make test-coverage
```

## Pragmatic Testing Approach

The goal is practical, maintainable tests that provide confidence in the system without excessive coverage goals or brittle implementation details. Focus on:

1. Testing business logic thoroughly in services
2. Verifying API contracts work as expected
3. Making tests easy to understand and maintain

We do not aim for 100% code coverage. Instead, we focus on testing the critical paths and business logic.
