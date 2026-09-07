                    DB_TYPE
                       │
             ┌─────────┼─────────┐
             ↓         ↓         ↓
           mysql     aurora   dynamodb
             │         │         │
             └────┬────┘         │
                  ↓              ↓
             PyMySQL           boto3
                  │              │
                  ↓              ↓
             RDS/Aurora       DynamoDB
                  │              │
                  ↓              ↓
          test_connection()  test_connection()
                  │              │
                  └──────┬───────┘
                         ↓
                      CRUD

****************** MYSQL CONNECTIVITY ****************

                    DB_TYPE
                       │
                       ▼
                Repository Factory
                  /           \
                 /             \
             MySQL          DynamoDB
               │
        ┌──────┴──────┐
        │             │
   Initialization     CRUD
        │             │
   ┌────┴────┐        │
   │         │        │
Database   Tables     │
   │         │        │
knowledgehub          │
   │                  │
knowledge_items       │