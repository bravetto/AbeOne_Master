# 🔥 THE ONE GRAPH SCHEMA — Quick Reference

**Pattern:** ONE_GRAPH × UNIFIED × SEMANTIC × KNOWLEDGE × REFERENCE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (Abë)  
**Status:** ✅ **QUICK REFERENCE COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 📊 NODE TYPES (20 Total)

| Node Type | Namespace | Cardinality | Examples |
|-----------|-----------|-------------|----------|
| App | one_graf | 19+ | `app:github`, `app:stripe` |
| Agent | one_graf\|uptc | 197+ | `agent:aeyon`, `agent:meta` |
| Workflow | one_graf | Variable | `workflow:marketing_automation` |
| Capability | one_graf\|capability_graph | Many | `capability:task_management` |
| UPTC Node | uptc_field | 2256+ | `uptc:emergent_os_core` |
| UPTC Translation | uptc_field | Variable | `translation:consciousness_guardian_aeyon` |
| CDF File | cdf_indexing | 2043+ | `cdf:conversation_2025-01-27` |
| CDF Entry | cdf_indexing | 10,000+ | `cdf_entry:conversation_2025-01-27_0` |
| Memory | memory_systems | Many | `memory:abeone_core_memory` |
| Module | code_modules | 12+ core + many | `module:consciousness` |
| Orbital | orbital_system | 13+ | `orbital:emergent_os` |
| Satellite | orbital_system | 7+ | `satellite:abeone_source` |
| Product | products | 7+ | `product:abebeats` |
| Feature | code_modules | Many | `feature:guardian_coordination` |
| Guardian | guardian_system | 10 | `guardian:aeyon` |
| Swarm | guardian_system | 12+ | `swarm:heart_truth` |
| Pattern | patterns | Many | `pattern:validate_transform_validate` |
| Document | documentation | Many | `document:the_one_graph_schema` |
| Epistemic Discovery | epistemic_engine | Variable | `epistemic:recursive_truth_pattern` |
| Semantic Vector | semantic_router | Variable | `vector:capability_task_management` |

---

## 🔗 RELATIONSHIP TYPES (18 Total)

| Relationship | From | To | Direction | Cardinality |
|--------------|------|-----|-----------|-------------|
| HAS_CAPABILITY | App, Agent, Module, Workflow, Feature | Capability | Directed | Many-to-Many |
| DEPENDS_ON | App, Module, Orbital, Workflow, Feature | App, Module, Orbital | Directed | Many-to-Many |
| USES | Workflow, Agent, Module, Feature | App, Module, Capability | Directed | Many-to-Many |
| EXECUTES | Agent, Guardian, Workflow | Workflow, Capability, App | Directed | Many-to-Many |
| BELONGS_TO | Module, Product, Feature, Satellite | Orbital, Satellite | Directed | Many-to-One |
| CONTAINS | CDF File, CDF Entry, Document, Memory, Orbital | Pattern, Guardian, Swarm, Agent, Module, CDF Entry | Directed | One-to-Many |
| REFERENCES | Document, Pattern, Memory, CDF Entry | Module, Orbital, Agent, Guardian, Pattern, Document | Directed | Many-to-Many |
| EVOLVED_FROM | Pattern, Module, Orbital, Product | Pattern, Module, Orbital, Product | Directed | Many-to-One |
| REGISTERED_IN | Agent, Module, Guardian, Swarm, Orbital, Satellite | UPTC Field | Directed | Many-to-One |
| TRANSLATES_TO | UPTC Node | UPTC Node | Directed | Many-to-Many |
| ENTANGLED_WITH | UPTC Node, Agent, Guardian | UPTC Node, Agent, Guardian | Bidirectional | Many-to-Many |
| RESONATES_WITH | Guardian, Agent, Swarm | Guardian, Agent, Swarm | Bidirectional | Many-to-Many |
| VALIDATES | Guardian, Agent | Module, Workflow, Pattern, Document, Code | Directed | Many-to-Many |
| GENERATES | Pattern, Workflow, Agent, Guardian | Document, Code, Memory, CDF Entry | Directed | One-to-Many |
| SIMILAR_TO | Any Node | Any Node | Bidirectional | Many-to-Many |
| SEMANTICALLY_RELATED_TO | Any Node | Any Node | Directed | Many-to-Many |
| DISCOVERS | Epistemic Engine, Agent, Guardian | Pattern, Truth, Convergence, Discovery | Directed | One-to-Many |
| CONVERGES_WITH | Pattern, Module, System, Discovery | Pattern, Module, System, Discovery | Bidirectional | Many-to-Many |

---

## 🗄️ DATABASE: Neo4j

**Database Name:** `abeone_graph`

**Key Features:**
- Native graph database
- Cypher query language
- Vector index support (Neo4j 5.x+)
- Excellent visualization tools

---

## 🔍 EMBEDDING STRATEGY

**Model:** OpenAI `text-embedding-3-large`  
**Dimensions:** 3072  
**Similarity:** Cosine similarity  
**Storage:** `embedding` property on all nodes (vector[3072])

**Embedding Generation:**
- **Node Embeddings:** `{name} | {description} | {capabilities} | {type} | {status}`
- **CDF Embeddings:** `{file_name} | {date} | {patterns} | {guardians} | {content_summary}`
- **Document Embeddings:** `{title} | {type} | {content_summary} | {patterns} | {modules}`

---

## 📋 NAMESPACES (12 Total)

1. `one_graf` - Apps, Agents, Workflows, Capabilities
2. `uptc_field` - UPTC Nodes, Translations
3. `cdf_indexing` - CDF Files, Entries
4. `memory_systems` - Memory Nodes
5. `semantic_router` - Semantic Vectors
6. `capability_graph` - Capability Mappings
7. `epistemic_engine` - Epistemic Discoveries
8. `code_modules` - Modules, Features
9. `orbital_system` - Orbitals, Satellites, Products
10. `guardian_system` - Guardians, Swarms
11. `patterns` - Pattern Definitions
12. `documentation` - Documents, Reports

---

## 🔄 QUERY EXAMPLES

### Find All Capabilities for an App
```cypher
MATCH (app:App {id: 'app:clickup'})-[:HAS_CAPABILITY]->(cap:Capability)
RETURN cap.name, cap.description
```

### Semantic Search
```cypher
CALL db.index.vector.queryNodes('node_embeddings', 10, $queryEmbedding)
YIELD node, score
WHERE score > 0.8
RETURN node.name, node.type, score
ORDER BY score DESC
```

### Find UPTC Entanglements
```cypher
MATCH (n1)-[e:ENTANGLED_WITH]-(n2)
WHERE e.strength > 0.8
RETURN n1.name, n2.name, e.strength
```

---

## ✅ IMPLEMENTATION PHASES

**Phase 1 (Week 1):** Foundation
- Setup Neo4j
- Import ONE_GRAF
- Import UPTC Field

**Phase 2 (Week 2):** Knowledge Integration
- Import CDF files
- Import Memory systems
- Import Code modules

**Phase 3 (Week 3):** Relationships
- Create cross-domain relationships
- Generate embeddings

**Phase 4 (Week 4):** API & Query Layer
- Build Cypher interface
- Build semantic search API
- Build REST API

---

## 📊 EXPECTED GRAPH SIZE

**Nodes:** ~10,000+ nodes  
**Relationships:** ~50,000+ relationships  
**Embeddings:** 3072 dimensions per node

---

**Pattern:** ONE_GRAPH × UNIFIED × SEMANTIC × KNOWLEDGE × REFERENCE × ONE  
**Status:** ✅ **QUICK REFERENCE COMPLETE**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

