# SMART STOCK & PROCUREMENT MCP
Smart Stock & Procurement MCP is an AI-powered Model Context Protocol (MCP)-based smart inventory management and supply chain automation system.

## Core Objective : 
The primary purpose of the system is to track inventory in the warehouse, identify products that have fallen below critical levels, and optimize and improve the purchasing process for these products based on the most appropriate criteria in external marketplaces. Users can manage the process using natural-language commands.

## Features
- Natural Language Querying : Ability to query warehouse status and command the system using natural language instructions. 
- Smart Stock Replenishment : Dynamic calculation of stock needs based on target stock levels, current inventory and pending incoming orders. 
- Automated Stock Tracking : Real-time tracking of warehouse inventory, automatically detecting out of stock and low stock products.
- Multi-Criteria Decision Making : Finding the most optimal offer using multiple strategies (cheapest, fastest, highest rated).
- Dynamic Execution Planning : Generating JSON-based multi-step workflows dynamically using LLM and chaining steps with variable passing ($from) and data transformations.

## General Architecture and Components
The system consists of three main layers : 
 - Orchestrator / Client Layer : It receives natural-language queries from the user and, using the Qwen LLM, generates an execution plan. It executes the plan step by step, interprets the technical results obtained through reasoning, and returns the result to the user in natural language. 

 - MCP Server Layer : It provides tools and functions that the LLM can use. It communicates with the orchestrator via the stdio protocol. 
    * Stock MCP Server : It includes tools that perform functions such as checking warehouse inventory, listing critical products, and restocking. 
    * Marketplace MCP Server : It includes tools such as searching for offers on the marketplace, comparing offers, creating a shopping cart, and placing an order.  

 - Backend Service Layer : It is based on Spring Boot. It provides REST APIs that manage all business logic (inventory records, vendor information, quotes, and orders) by communicating directly with the database.

## Technologies Used
     * Orchestrator / Client Layer : Python (mcp, requests), Qwen LLM
     * MCP Server Layer : Python (mcp, httpx, pydantic)
     * Backend Service Layer : Spring Boot(Java 21, Spring Data JPA, Hibernate, Lombok), Maven, PostegreSQL




## Installation

Follow the steps below to set up and run the project locally.

### Prerequisites

Make sure the following software is installed on your machine:

- Java 21
- Maven 3.9+
- Python 3.14+
- PostgreSQL 17
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/beyzzzaaa/smart-stock-mcp.git
cd smart-stock-mcp
```

### 2. Configure PostgreSQL

1. Create a PostgreSQL database named `smart_stock`.
2. Open **[application.yml](stock-service/src/main/resources/application.yml)** in the `stock-service/src/main/resources` folder.
3. Update the database credentials to match your local PostgreSQL configuration:

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/smart_stock
    username: your_postgresql_username
    password: your_postgresql_password
```

The backend automatically creates the required database schema and loads the sample data from `data.sql` during startup.

### 3. Build and Run the Spring Boot Backend

Navigate to the `stock-service` directory:

```bash
cd stock-service
```

Build and start the Spring Boot application:

```bash
mvn clean install
mvn spring-boot:run
```

The backend service will be available at:

```text
http://localhost:8081
```

### 4. Install Python Dependencies

Open a new terminal in the project root directory and install the dependencies for all Python components:

```bash
pip install -r llm-host/requirements.txt -r stock-mcp/requirements.txt -r marketplace-mcp/requirements.txt
```

### 5. Configure the LLM

1. Ensure that an LLM server is running. The system can connect to an LLM hosted remotely, such as Qwen 2.5-7B Instruct running on Google Colab, or to a locally hosted model using tools such as Ollama or LM Studio.
2. Open **[llm.py](llm-host/llm.py)** and update the `self.url` variable with the API endpoint of your LLM server:

```python
self.url = "<YOUR_LLM_ENDPOINT>"
```

Replace `<YOUR_LLM_ENDPOINT>` with the actual API URL of the LLM service.

### 6. Start the Orchestrator Client

From the project root directory, navigate to the `llm-host` folder:

```bash
cd llm-host
```

Start the application:

```bash
python app.py
```

Once started, the orchestrator client connects to the Stock MCP Server and Marketplace MCP Server, communicates with the configured LLM, generates execution plans, invokes the required MCP tools, and returns the final response to the user.

## Usage

Once the Spring Boot backend, LLM server, and orchestrator client are running, you can interact with the system using natural language queries in either Turkish or English.

Example queries include:
- *Find the products that need replenishment.*
- *Find the cheapest purchasing plan for products that are low in stock.*
- *Show products that are currently out of stock.*
- *Compare marketplace offers for the products that need replenishment.*

The system interprets the request using the configured LLM, determines the required MCP tools, executes the appropriate operations, and returns the result in natural language.

---

## Available MCP Tools

The system exposes the following tools to the LLM orchestrator through the MCP servers:

### 1. Stock MCP Tools
* `list_products`: Lists all products in the warehouse along with their current stock levels.
* `search_products`: Searches for products inside the warehouse database.
* `list_out_of_stock` / `list_low_stock`: Lists products with zero stock or below critical thresholds.
* `calculate_replenishment`: Computes the exact quantity needed to restore ideal stock levels.
* `create_incoming_order` / `receive_order`: Registers incoming shipments and accepts them into inventory.

### 2. Marketplace MCP Tools
* `list_sellers`: Lists registered sellers, filtering by rating or delivery time.
* `search_offers`: Searches vendor offers in the marketplace.
* `compare_offers`: Employs multi-criteria decision making (TOPSIS) to rank and select the best offer based on cheapness, speed, seller rating, or balanced scores.
* `create_purchase_draft`: Adds selected offers to a temporary cart (purchase draft).
* `place_order`: Converts approved drafts into active marketplace orders.
* `create_procurement_plan`: Automatically optimizes purchases of multiple missing items across various vendors.

---

## API Endpoints

The Spring Boot backend (`stock-service`) provides the following REST API endpoints:

### Products & Inventory
* `GET /api/products` - Get all products
* `GET /api/products/search?query={q}` - Search products by name, category, or SKU
* `GET /api/products/low-stock` - List low stock products
* `GET /api/products/replenishment` - Compute required replenishment quantities

### Supplier & Incoming Orders
* `GET /api/orders` - List all incoming supplier orders
* `POST /api/orders` - Create a new order to replenish warehouse stock
* `POST /api/orders/{id}/receive` - Mark order as received and increment inventory

### Marketplace Integration
* `GET /api/marketplace/offers/compare?productId={id}` - Rank seller offers using TOPSIS
* `POST /api/marketplace/drafts` - Create a purchase draft
* `POST /api/marketplace/orders` - Finalize a draft into a marketplace purchase order

---

## Future Improvements

* **Web UI Dashboard:** Build a modern frontend interface (React/Vite) to visually monitor warehouse status, current drafts, and LLM reasoning steps.
* **Real Marketplace Integrations:** Connect MCP tools to live sandbox APIs of popular e-commerce platforms (Amazon, eBay, local marketplaces).
* **AI Demand Forecasting:** Use historical warehouse data to predict future stock shortages before they drop below critical thresholds.
* **Multi-Agent Negotiation:** Enable a seller agent and buyer agent to dynamically negotiate prices for bulk orders.

---


