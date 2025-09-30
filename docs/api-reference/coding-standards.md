# Coding Standards - BMAD Auto

## Python Standards
- **Type Hints**: Required for all function parameters and returns
- **Async/Await**: Use async patterns for all database and I/O operations
- **Error Handling**: Comprehensive try/catch with specific logging
- **File Size**: Keep files under 300 lines for maintainability
- **Imports**: Absolute imports preferred, relative only within modules

## Database Standards
- **Transactions**: Use async sessions with proper rollback handling
- **Models**: Pydantic models for all API interfaces
- **Queries**: SQLAlchemy ORM with proper indexing
- **Migration**: Schema changes through migration files

## API Standards
- **FastAPI**: RESTful design with proper HTTP status codes
- **Validation**: Pydantic request/response validation
- **Documentation**: OpenAPI automatic documentation
- **CORS**: Properly configured for development and production
- **Logging**: Structured logging with correlation IDs

## Agent Standards
- **Size Compliance**: 100-300 lines maximum
- **Single Responsibility**: Each agent has clear, focused role
- **PM Coordination**: All agents coordinate through PM hub
- **State Management**: Use Cell structure for persistent state
- **Quality Gates**: Mandatory validation checkpoints