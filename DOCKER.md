# Docker Guide for Florence MCP Servers

This guide covers Docker usage for the **[Florence MCP Servers collection](README.md)**, designed as an extensible multi-server architecture for building a personal sous chef ambient agent.

> **📖 For the complete project overview and roadmap, see the [main README](README.md)**

## 🐳 Docker Architecture

### Current Services (Phase 1)

- **recipe-api-server**: First MCP server providing recipe search and management
- **postgres**: PostgreSQL database for persistent storage (shared across future servers)
- **redis**: Redis cache for performance optimization (shared across future servers)
- **nginx**: Reverse proxy (production only)
- **pgadmin**: Database management tool (development only)
- **redis-commander**: Redis management tool (development only)

### Future Services (Planned)

The Docker architecture is designed to seamlessly accommodate additional MCP servers:
- **meal-planning-server**: Weekly/monthly meal planning (Phase 2)
- **pantry-inventory-server**: Ingredient tracking and inventory management (Phase 2)  
- **restaurant-delivery-server**: Uber Eats, DoorDash integration (Phase 2)
- **grocery-delivery-server**: Instacart, Amazon Fresh integration (Phase 3)
- **nutrition-tracking-server**: Calorie and dietary goal tracking (Phase 3)
- **calendar-integration-server**: Sync with Google/Outlook calendars (Phase 3)

### Networks

- **florence-network**: Internal Docker network for service communication

### Volumes

- **postgres_data**: Persistent PostgreSQL data
- **redis_data**: Persistent Redis data

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

Required environment variables:
```bash
SPOONACULAR_API_KEY=your_api_key_here
# Optional: EDAMAM_APP_ID, EDAMAM_APP_KEY for future use
```

### 2. Start Development Environment

```bash
# One-command setup
make setup

# Or step by step
make build
make dev
```

### 3. Verify Installation

```bash
# Check all services are running
docker-compose ps

# View logs
make logs

# Run tests
make test
```

## 🛠️ Development Workflow

### Daily Development

```bash
# Start services
make dev

# View logs in real-time
make logs

# Run tests after changes
make test

# Access container shell for debugging
make shell

# Stop services
make down
```

### Code Changes

The development setup includes volume mounts for hot reloading:
- Changes to `src/` and `shared/` are automatically reflected
- No need to rebuild containers for code changes
- Container restart only needed for dependency changes

### Database Operations

```bash
# Access PostgreSQL shell
make shell-postgres

# Reset database (removes all data)
make db-reset

# View database with pgAdmin
make dev-with-tools
# Then visit http://localhost:8080
```

### Redis Operations

```bash
# Access Redis CLI
make shell-redis

# View Redis data with Redis Commander
make dev-with-tools  
# Then visit http://localhost:8081
```

## 🏭 Production Deployment

### Production Build

```bash
# Build optimized production images
make prod-build

# Or start existing production images
make prod
```

### Production Configuration

Production setup includes:
- Multi-stage builds for smaller images
- Non-root users for security
- Health checks and restart policies
- Log rotation
- Nginx reverse proxy
- Resource limits

### Environment Variables for Production

```bash
# Required
SPOONACULAR_API_KEY=your_key
POSTGRES_PASSWORD=secure_password
REDIS_PASSWORD=secure_password

# Optional
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage report
make test-coverage

# Run specific test file
docker-compose exec recipe-api-server pytest tests/test_tools/test_search_recipes.py
```

### Test Environment

Tests run inside the Docker container to ensure consistency:
- Same Python version and dependencies as production
- Isolated from host system
- Can test against real services (postgres, redis)

## 🔧 Customization

### Adding New MCP Servers

The Docker architecture is designed for easy addition of new servers:

#### 1. Server Container
```yaml
# docker-compose.yml
new-server:
  build: 
    context: .
    dockerfile: servers/new_server/Dockerfile
  container_name: florence-new-server
  environment:
    - API_KEY=${NEW_SERVER_API_KEY}
    - LOG_LEVEL=${LOG_LEVEL:-INFO}
  volumes:
    - ./shared:/app/shared:ro
    - ./servers/new_server/src:/app/src:ro
  networks:
    - florence-network
```

#### 2. Makefile Integration
```makefile
# Add to Makefile
logs-new:
	docker-compose logs -f new-server

shell-new:
	docker-compose exec new-server bash
```

#### 3. Shared Infrastructure Benefits
- **Database**: All servers share PostgreSQL for cross-server data relationships
- **Cache**: Redis available for all servers' caching needs
- **Network**: All servers communicate over `florence-network`
- **Data Models**: Shared types in `shared/types/` for consistency

#### 4. Environment Variables
New servers add their variables to `.env.example`:
```bash
# New Server Configuration
NEW_SERVER_API_KEY=your_api_key
NEW_SERVER_OPTION=value
```

### Environment-Specific Overrides

Use Docker Compose override files:
- `docker-compose.override.yml`: Development overrides (auto-loaded)
- `docker-compose.prod.yml`: Production configuration
- Custom files: `docker-compose -f file1.yml -f file2.yml up`

### Custom Docker Images

Build custom images:
```bash
# Build specific service
docker-compose build recipe-api-server

# Build with different Dockerfile
docker build -f servers/recipe_api_server/Dockerfile.custom .
```

## 🐛 Troubleshooting

### Common Issues

#### Services won't start
```bash
# Check service status
docker-compose ps

# View service logs
docker-compose logs service-name

# Check container health
docker inspect florence-recipe-api --format='{{.State.Health.Status}}'
```

#### Port conflicts
```bash
# Check what's using ports
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :8080  # pgAdmin

# Change ports in .env file
POSTGRES_PORT=5433
REDIS_PORT=6380
```

#### Permission issues
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./data/

# Or use Docker to fix permissions
docker-compose exec recipe-api-server chown -R app:app /app
```

#### Out of disk space
```bash
# Clean up Docker resources
make clean

# More aggressive cleanup
docker system prune -a --volumes -f
```

### Debugging

#### Access container shell
```bash
make shell                    # Recipe API server
make shell-postgres          # PostgreSQL
make shell-redis            # Redis
```

#### View container details
```bash
# Container information
docker inspect florence-recipe-api

# Resource usage
docker stats

# Process information
docker-compose top
```

#### Network debugging
```bash
# List networks
docker network ls

# Inspect network
docker network inspect florence-mcp-servers_florence-network

# Test connectivity between containers
docker-compose exec recipe-api-server ping postgres
```

## 📊 Monitoring

### Health Checks

All services include health checks:
```bash
# View health status
docker-compose ps

# Manual health check
docker-compose exec recipe-api-server python -c "import sys; sys.exit(0)"
```

### Logs

```bash
# All services
make logs

# Specific service
docker-compose logs recipe-api-server

# Follow logs in real-time
docker-compose logs -f --tail=100 recipe-api-server
```

### Resource Usage

```bash
# Current usage
docker stats

# Historical usage (requires monitoring setup)
docker-compose exec postgres pg_stat_activity
```

## 🔒 Security

### Production Security

- Non-root users in containers
- No unnecessary packages in production images
- Secrets via environment variables
- Network isolation
- Regular security updates

### Development Security

- Isolated development environment
- No production credentials in dev
- Local-only database access
- Development-specific passwords

## 📈 Performance

### Optimization Tips

1. **Image size**: Use multi-stage builds
2. **Build cache**: Order Dockerfile instructions by change frequency
3. **Volumes**: Use volumes for persistent data
4. **Networks**: Use internal networks for service communication
5. **Resources**: Set appropriate limits in production

### Performance Monitoring

```bash
# Container resource usage
docker stats

# Service-specific metrics
make health

# Database performance
make shell-postgres
# Then run PostgreSQL performance queries
```