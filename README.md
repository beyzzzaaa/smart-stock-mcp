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
## Project Structure 

smart-stock-mcp/
│
├── llm-host/                  # Orchestrator / Client Layer (Python)
│   ├── app.py                 # Main orchestrator application loop & execution manager
│   ├── llm.py                 # API client wrapper for LLM requests
│   ├── mcp_client.py          # Manager for connecting to MCP Servers
│   ├── prompt.py              # LLM system prompts & output transformers
│   └── requirements.txt       # Python dependencies for the host
│
├── stock-mcp/                 # Stock Management MCP Server (Python)
│   ├── tools.py               # Exposes stock & inventory tools to LLM
│   ├── services.py            # Interfaces with stock-service backend REST APIs
│   ├── models.py              # Stock data schemas
│   └── requirements.txt       # Server dependencies
│
├── marketplace-mcp/           # Marketplace Integration MCP Server (Python)
│   ├── tools.py               # Exposes marketplace tools (with TOPSIS optimization)
│   ├── services.py            # Interfaces with marketplace-service backend REST APIs
│   ├── models.py              # Marketplace data schemas
│   └── requirements.txt       # Server dependencies
│
├── stock-service/             # Backend Business Logic Service (Spring Boot & Java)
│   ├── pom.xml                # Maven project configuration
│   └── src/main/
│       ├── java/com/smartstock/stockservice/
│       │   ├── controller/    # REST endpoints (Product, Order, Marketplace)
│       │   ├── service/       # Inventory and purchasing business logic
│       │   ├── model/         # JPA database entities (Database mapping)
│       │   ├── repository/    # Spring Data JPA repositories
│       │   ├── dto/           # Data Transfer Objects
│       │   └── StockServiceApplication.java
│       └── resources/
│           ├── application.yml # Database and application configurations
│           └── data.sql       # Initial database seed script
│
├── DOCUMENTATION.md           # Detailed architecture & API documentation
└── README.md                  # Project overview & quick start guide



## Installation

Follow the steps below to set up and run the project locally.

### Prerequisites

Make sure the following software is installed on your machine:

- Java 21
- Maven 3.9+
- Python 3.14+
- PostgreSQL 17
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/<username>/smart-stock-mcp.git
cd smart-stock-mcp


### 2. Configure PostgreSQL

1. Create a PostgreSQL database named `smart_stock`.
2. Open **[application.yml](file:///c:/Users/Master/Desktop/Project/smart-stock-mcp/stock-service/src/main/resources/application.yml)** in the `stock-service/src/main/resources` folder.
3. Update the database credentials to match your local PostgreSQL configuration:

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/smart_stock
    username: your_username
    password: your_password
```

---

### 3. Run the Spring Boot Backend

```bash
cd stock-service
mvn clean install
mvn spring-boot:run
```

The backend service will start and be available at:

```text
http://localhost:8081
```

---

### 4. Install Python Dependencies

Go back to the project root directory and install dependencies for all Python components:

```bash
pip install -r llm-host/requirements.txt -r stock-mcp/requirements.txt -r marketplace-mcp/requirements.txt
```

---

### 5. Configure the LLM

1. Ensure you have an active LLM server running (e.g., Qwen 2.5-7B Instruct hosted via Google Colab, or running locally via Ollama/LM Studio).
2. Open **[llm.py](file:///c:/Users/Master/Desktop/Project/smart-stock-mcp/llm-host/llm.py)** and update the `self.url` endpoint with your LLM server's API URL.

---

### 6. Start the Orchestrator Client

Navigate to the orchestrator host folder and run the client application:

```bash
cd ../llm-host
python app.py
```

Once started, the client will connect to both the Stock and Marketplace MCP servers, integrate with the Qwen LLM, and expect your natural-language queries in the terminal.

## Usage

Once the backend service, LLM server, and orchestrator client are running, you can interact with the system using natural language queries in Turkish or English.

### Example Prompts:
* **Check Inventory:** *"Depoda kritik stok seviyesinin altına düşen ürünleri listele."* (List products that have fallen below the critical stock level in the warehouse.)
* **Plan Procurement:** *"Elektronik kategorisindeki eksik ürünler için satın alma planı yap."* (Create a purchase plan for missing items in the Electronics category.)
* **Compare & Purchase:** *"iPhone için en ekonomik satıcı teklifini bul ve taslak sipariş oluştur."* (Find the most economic seller offer for iPhone and create a purchase draft.)


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


