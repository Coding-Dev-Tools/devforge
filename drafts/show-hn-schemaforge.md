# Show HN: SchemaForge — Bidirectional ORM Converter (11 formats, VS Code extension)

## Title Options
- Show HN: SchemaForge – Convert between SQL, Prisma, Drizzle, TypeORM, Django, SQLAlchemy, GraphQL, and JSON Schema (11 formats, 100 conversion directions)
- Show HN: I got tired of rewriting ORM schemas, so I built a converter for 11 formats
- Show HN: SchemaForge – The only bidirectional ORM schema converter with a VS Code extension

---

## Post Body

I've been converting ORM schemas between formats for years. Every time we evaluate a new ORM, rewrite the schema. Every time we add a language to the monorepo, rewrite the schema. Every migration from Prisma to Drizzle, or Django to SQLAlchemy — manual rewrite.

So I built SchemaForge: a CLI that converts between 11 schema formats. The shared representation preserves tables, columns, types, defaults, indexes, unique constraints, and enums faithfully; foreign-key constraints and ORM relationship fields require manual review after migration.

**Supported formats (11, bidirectional):**
1. SQL DDL (CREATE TABLE)
2. Prisma schema (.prisma)
3. Drizzle ORM (TypeScript)
4. TypeORM (TypeScript decorators)
5. Django models (Python)
6. SQLAlchemy models (Python)
7. GraphQL SDL (.graphql)
8. JSON Schema (.json)
9. OpenAPI 3.0 schemas (.yaml/.json)
10. Protobuf (.proto)
11. Avro (.avsc)

**Example:**
```bash
pip install git+https://github.com/Coding-Dev-Tools/schemaforge.git

# Prisma → SQLAlchemy
schemaforge convert schema.prisma --from prisma --to sqlalchemy

# SQL DDL → Drizzle
schemaforge convert schema.sql --from sql-ddl --to drizzle

# Django → TypeORM
schemaforge convert models.py --from django --to typeorm
```

**VS Code Extension** (new in v1.7.0):
- Live preview panel showing converted schema
- Quick convert: Ctrl+Alt+S
- Format detection: Ctrl+Alt+D
- Two-file diff view
- Right-click context menu
- Custom .schemaforge editor

**Key features:**
- 270+ tests passing
- Preserves relationships, indexes, defaults, and constraints
- Custom type mapping configuration (v1.1.0)
- JSON Schema and GraphQL SDL support (v1.3.0)
- Works as CLI or Python library
- Apache 2.0 license

**Why not just use ORM migration tools?**
Migration tools move data between versions of the same ORM. SchemaForge moves schemas between entirely different ORMs and formats. They solve different problems.

**Links:**
- GitHub: https://github.com/Coding-Dev-Tools/schemaforge
- VS Code Extension: https://github.com/Coding-Dev-Tools/vscode-schemaforge
- Docs: https://coding-dev-tools.github.io/devforge/docs.html#schemaforge
- Tutorial: https://coding-dev-tools.github.io/devforge/blog/schemaforge-v0-5-0-sqlalchemy.html

Happy to answer questions about the conversion logic, format compatibility, or what formats you'd like added next.

---

## Submission Notes
- Post as text (not link) on news.ycombinator.com
- Best time: weekday morning US Eastern (Tue-Thu)
- Title: use the first option (most descriptive for HN audience)
- Be ready to answer "why not use prisma migrate / alembic?" questions
- The VS Code extension is the differentiator — mention it early
