# Florence MCP Servers

**A comprehensive MCP server collection** for building a personal sous chef ambient agent. This extensible architecture currently implements **recipe search and management** as the foundational server, with additional specialized servers planned for meal planning, pantry inventory, grocery delivery, and restaurant ordering.

## 🏗️ Architecture Overview

Florence is designed as a **multi-server MCP ecosystem** where each server handles a specific domain of food/cooking functionality. The servers work together through shared data models and can be deployed independently or as a complete suite.

## 🚀 Quick Start with Docker

1. **Clone and setup**:
   ```bash
   git clone https://github.com/craine-io/florence-mcp-servers.git
   cd florence-mcp-servers
   make setup
   ```

2. **Add your API key**:
   ```bash
   # Edit .env file with your Spoonacular API key
   nano .env
   ```

3. **Start the services**:
   ```bash
   make dev
   ```

4. **Test it works**:
   ```bash
   make test
   ```

## 📦 Current Implementation

- **Recipe API Server**: Search and manage recipes via Spoonacular API ✅
- **PostgreSQL Database**: Ready for meal planning and inventory data  
- **Redis Cache**: Ready for performance optimization
- **Development Tools**: pgAdmin, Redis Commander (optional)

## 🗺️ Roadmap: Planned MCP Servers

### Phase 1 (✅ Current)
- **Recipe API Server**: Recipe search, details, and nutrition analysis

### Phase 2 (🚧 Planned)
- **Meal Planning Server**: Weekly/monthly meal planning with dietary preferences
- **Pantry Inventory Server**: Track ingredients, expiration dates, and shopping needs
- **Restaurant Delivery Server**: Uber Eats, DoorDash integration for ordering

### Phase 3 (📋 Planned) 
- **Grocery Delivery Server**: Instacart, Amazon Fresh integration
- **Nutrition Tracking Server**: Calorie tracking, dietary goal monitoring
- **Calendar Integration Server**: Sync meal plans with Google/Outlook calendars

### Phase 4 (💡 Future)
- **Equipment Management Server**: Track kitchen equipment and maintenance
- **Weather Integration Server**: Adjust meal suggestions based on weather
- **Health Integration Server**: Connect with fitness trackers and health apps

Each server is designed to work independently or as part of the complete Florence ecosystem.

## 🛠️ Available Commands

```bash
make help              # Show all available commands
make dev               # Start development environment
make prod              # Start production environment
make test              # Run all tests
make logs              # View logs from all services
make clean             # Clean up all Docker resources
```

## 🔧 Development

### Multi-Server Architecture
The project is structured for easy addition of new MCP servers:
```bash
servers/
├── recipe_api_server/     # ✅ Implemented
├── meal_planning_server/  # 🚧 Planned next  
├── pantry_server/         # 📋 Planned
└── [future servers]/      # 💡 Extensible
```

### Local Development
```bash
# Work on individual servers
cd servers/recipe_api_server
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys
python src/main.py

# Work on shared components
cd shared/
# Edit types/, utils/, config/
```

### Docker Development
```bash
make dev               # Start all current services
make shell             # Access recipe server container
make logs-recipe       # View recipe server logs only

# Future: When more servers are added
make logs-meals        # Meal planning server logs
make logs-pantry       # Pantry server logs
```
