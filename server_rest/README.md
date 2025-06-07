# Company Management REST API

A high-performance Flask REST API for managing company data with PostgreSQL integration.

## Features

- **RESTful Architecture**: Clean REST API design with proper HTTP methods and status codes
- **Object-Oriented Design**: Each endpoint implemented in separate controller classes
- **PostgreSQL Integration**: Full database support with SQLAlchemy ORM
- **Data Validation**: Comprehensive input validation using Marshmallow schemas
- **Error Handling**: Robust error handling with meaningful error messages
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Connection Pooling**: Optimized database connection management

## API Endpoints

### Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | Retrieve all companies (supports filtering) |
| GET | `/companies/<id>` | Retrieve a specific company |
| POST | `/companies` | Create a new company |
| PUT | `/companies/<id>` | Update an existing company |
| DELETE | `/companies/<id>` | Delete a company |

### Query Parameters (GET /companies)

- `legal_name`: Filter by legal name (partial match)
- `trade_name`: Filter by trade name (partial match)
- `contact_email`: Filter by contact email (partial match)

## Data Model

### Company Schema

```json
{
  "id": "string (required, unique)",
  "legal_name": "string (required, max 255 chars)",
  "trade_name": "string (optional, max 255 chars)",
  "contact_phone": "string (optional, max 20 chars)",
  "contact_email": "string (optional, valid email)",
  "responsible_person": "string (optional, max 255 chars)",
  "created_at": "timestamp (auto-generated)",
  "updated_at": "timestamp (auto-updated)"
}
```

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   Copy `.env` file and update database credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/company_db
   ```

3. **Database Setup**:
   Ensure PostgreSQL is running and create the database:
   ```sql
   CREATE DATABASE company_db;
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Usage Examples

### Create a Company
```bash
curl -X POST http://localhost:5000/companies \
  -H "Content-Type: application/json" \
  -d '{
    "id": "COMP001",
    "legal_name": "Tech Solutions Inc.",
    "trade_name": "TechSol",
    "contact_phone": "+1-555-0123",
    "contact_email": "info@techsol.com",
    "responsible_person": "John Doe"
  }'
```

### Get All Companies
```bash
curl http://localhost:5000/companies
```

### Get Specific Company
```bash
curl http://localhost:5000/companies/COMP001
```

### Update Company
```bash
curl -X PUT http://localhost:5000/companies/COMP001 \
  -H "Content-Type: application/json" \
  -d '{
    "trade_name": "TechSolutions",
   c
  }'
```

### Delete Company
```bash
curl -X DELETE http://localhost:5000/companies/COMP001
```

## Architecture

- **app.py**: Main application entry point
- **config/database.py**: Database configuration and initialization
- **models/company.py**: Modelo SQLAlchemy para a entidade Empresa
- **controllers/company_controller.py**: Lógica de negócios para operações relacionadas à empresa
- **routes/company_routes.py**: Route definitions and URL mappings
- **schemas/company_schema.py**: Data validation and serialization schemas

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 404: Not Found
- 409: Conflict (duplicate ID)
- 500: Internal Server Error