class CypherQueries:
    # Multi-hop traversal (Depth 2)
    MULTI_HOP_TRAVERSAL = """
    MATCH (n {name: $entity_name})
    CALL apoc.path.subgraphAll(n, {
        maxLevel: $depth,
        relationshipFilter: ""
    })
    YIELD nodes, relationships
    RETURN nodes, relationships
    """
    
    # Simple Breadth-First Search (Depth 1-3)
    BFS_TRAVERSAL = """
    MATCH (n {name: $entity_name})
    MATCH path = (n)-[*1..$depth]-(m)
    RETURN path
    """
    
    # Find entities by name (case-insensitive)
    FIND_ENTITY = """
    MATCH (n)
    WHERE n.name =~ $regex
    RETURN n.name as name, labels(n)[0] as type
    LIMIT 5
    """
