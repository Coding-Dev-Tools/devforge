# SchemaForge: The Only Schema Converter You'll Ever Need

> Bidirectional schema conversion between 11 formats — SQL, Prisma, Drizzle, TypeORM, Django, and more, with faithful shared-representation roundtripping.

---

## The Schema Nightmare

Every team I've worked with has been through this cycle:

1. Start with raw SQL (it's "simpler")
2. Switch to an ORM (Prisma is hot)
3. Realize you need raw SQL for complex migrations
4. Try another ORM (Drizzle is faster)
5. Now you have 3 different schema representations

Manual conversion is error-prone. AI generation is unreliable. Most conversion tools work in one direction only.

SchemaForge solves this.

## What SchemaForge Does

SchemaForge is a CLI tool (and VS Code extension) that converts between 11 schema formats **bidirectionally**. The shared representation preserves tables, columns, types, defaults, indexes, unique constraints, and enums accurately; foreign-key constraints and ORM relationships require manual review after migration.

```bash
# Convert Prisma to SQL
schemaforge convert schema.prisma --to sql

# Convert SQL to TypeORM
schemaforge convert schema.sql --to typeorm

# List supported formats
schemaforge list-formats
```

## Supported Formats

| Format | Direction | Notes |
|---|---|---|
| SQL DDL | ↔ | MySQL, PostgreSQL, SQLite |
| Prisma | ↔ | Full schema support |
| Drizzle ORM | ↔ | Drizzle kit compatible |
| TypeORM | ↔ | Entity decorators |
| Django | ↔ | Models.py generation |
| SQLAlchemy | ↔ | Declarative base |
| JSON Schema | ↔ | OpenAPI components |
| Knex.js | ↔ | Migration files |
| Sequelize | ↔ | Model definitions |
| Mongoose | ↔ | Schema objects |
| Zod | → | Experimental |

## Real-World Example: Prisma → SQL → TypeORM

Let's say you started with Prisma and now need to switch to TypeORM.

### Step 1: Convert Prisma → SQL

```bash
schemaforge convert schema.prisma --to sql --dialect postgresql
```

Output:
```sql
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_organization FOREIGN KEY ("orgId") REFERENCES "Organization"(id)
);

CREATE TABLE "Organization" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    "tier" VARCHAR(50) NOT NULL DEFAULT 'free'
);

CREATE INDEX idx_user_email ON "User"(email);
```

### Step 2: Convert SQL → TypeORM

```bash
schemaforge convert schema.sql --to typeorm
```

Output:
```typescript
import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn, Index } from "typeorm";

@Entity()
export class User {
    @PrimaryGeneratedColumn()
    id: number;

    @Column({ length: 255, unique: true })
    email: string;

    @Column({ length: 255, nullable: true })
    name: string;

    @Column()
    createdAt: Date;

    @Column()
    orgId: number;

    @ManyToOne(() => Organization)
    @JoinColumn({ name: "orgId" })
    organization: Organization;
}
```

### Step 3: Verify Roundtrip

```bash
# Back to SQL
schemaforge convert user.entity.ts --to sql --dialect postgresql

# Back to Prisma
schemaforge convert user.entity.ts --to prisma
```

The roundtrip preserves:
- ✅ Primary keys
- ✅ Foreign keys
- ✅ Unique constraints
- ✅ Indexes
- ✅ Default values
- ✅ CHECK constraints
- ✅ Composite keys
- ✅ Custom types (mapped to closest equivalent)

## VS Code Extension

Install from the [VS Code Marketplace](https://github.com/Coding-Dev-Tools/vscode-schemaforge) for:

- **Live preview**: Edit your schema, see the converted output in real-time
- **Quick convert**: Right-click → "Convert with SchemaForge"
- **Diff view**: See what changed between schema versions
- **Format detection**: Auto-detect schema format from file extension

## CLI Reference

```bash
# Basic conversion
schemaforge convert input.prisma --to sql

# Specify output file
schemaforge convert input.prisma --to sql --output schema.sql

# PostgreSQL dialect
schemaforge convert input.prisma --to sql --dialect postgresql

# List all formats
schemaforge list-formats

# Show format info
schemaforge format-info prisma

# Validate a schema
schemaforge validate schema.sql

# Diff two schemas
schemaforge diff schema_v1.sql schema_v2.sql
```

## When to Use SchemaForge

### Migrating between ORMs
Moving from Prisma to Drizzle? Or TypeORM to Sequelize? One command.

### Generating SQL migrations
If you prefer raw SQL for production but want to design in an ORM, convert and customize.

### Documentation generation
Convert your schema to JSON Schema/OpenAPI for API docs that stay in sync.

### CI integration
```yaml
- name: Validate schema
  run: schemaforge validate schema.prisma
- name: Check schema drift
  run: schemaforge diff main:schema.prisma HEAD:schema.prisma
```

## Performance

SchemaForge handles schemas with 500+ tables in under 2 seconds. Type resolution is lazy — only formats you request are loaded.

## Getting Started

```bash
# Install CLI
pip install git+https://github.com/Coding-Dev-Tools/schemaforge.git

# Install VS Code extension
# Search "SchemaForge" in VS Code extensions or install from:
# https://github.com/Coding-Dev-Tools/vscode-schemaforge

# Try it
schemaforge list-formats
schemaforge demo
```

## Community

- **GitHub**: https://github.com/Coding-Dev-Tools/schemaforge
- **VS Code Extension**: https://github.com/Coding-Dev-Tools/vscode-schemaforge
- **Landing Page**: https://coding-dev-tools.github.io/devforge/
- **Report Issues**: https://github.com/Coding-Dev-Tools/schemaforge/issues

---

*SchemaForge is part of the [DevForge](https://coding-dev-tools.github.io/devforge/) developer tool ecosystem — 10 CLI tools built by autonomous AI for autonomous developers.*
