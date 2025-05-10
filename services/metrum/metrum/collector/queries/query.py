import hashlib
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import sqlparse
from sqlparse.sql import Identifier, IdentifierList, Where, Statement
from sqlparse.tokens import DML, Name, Operator, Comparison, Number, String


class QueryType(str, Enum):
    """Enum for supported query types."""
    SELECT = "SELECT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MERGE = "MERGE"


class MetrumQuery(BaseModel):
    """
    Class to store and analyze SQL queries.
    
    Attributes:
        query: The original SQL query string
        query_hash: Hash of the query for identification
        query_type: Type of query (SELECT, UPDATE, DELETE, MERGE)
        parameters: Parameters used in the query
        explain: Query execution plan
        tables: Tables referenced in the query
        views: Views referenced in the query
        where_clause_ast: Abstract syntax tree of the WHERE clause
    """
    query: str = Field(..., description="Original SQL query string")
    query_hash: str = Field(..., description="Hash of the query for identification")
    query_type: QueryType = Field(..., description="Type of query (SELECT, UPDATE, DELETE, MERGE)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters used in the query")
    explain: Optional[Dict[str, Any]] = Field(None, description="Query execution plan")
    tables: List[str] = Field(default_factory=list, description="Tables referenced in the query")
    views: List[str] = Field(default_factory=list, description="Views referenced in the query")
    where_clause_ast: Optional[Dict[str, Any]] = Field(None, description="Abstract syntax tree of the WHERE clause")
    
    @classmethod
    def from_query(cls, query: str, parameters: Optional[Dict[str, Any]] = None) -> "MetrumQuery":
        """
        Create a MetrumQuery instance from a query string.
        
        Args:
            query: SQL query string
            parameters: Optional parameters used in the query
            
        Returns:
            MetrumQuery instance
        """
        # Normalize query for hashing (remove whitespace, convert to uppercase)
        normalized_query = " ".join(query.split()).upper()
        query_hash = hashlib.sha256(normalized_query.encode()).hexdigest()
        
        # Parse the query to determine type and extract information
        parsed = sqlparse.parse(query)[0]
        query_type = cls._determine_query_type(parsed)
        
        # Extract tables and views
        tables, views = cls._extract_tables_and_views(parsed)
        
        # Extract WHERE clause AST
        where_clause_ast = cls._extract_where_clause_ast(parsed)
        
        return cls(
            query=query,
            query_hash=query_hash,
            query_type=query_type,
            parameters=parameters or {},
            tables=tables,
            views=views,
            where_clause_ast=where_clause_ast
        )
    
    @staticmethod
    def _determine_query_type(parsed: Statement) -> QueryType:
        """Determine the type of query from the parsed SQL."""
        for token in parsed.tokens:
            if token.ttype in DML:
                if token.value.upper() == "SELECT":
                    return QueryType.SELECT
                elif token.value.upper() == "UPDATE":
                    return QueryType.UPDATE
                elif token.value.upper() == "DELETE":
                    return QueryType.DELETE
                elif token.value.upper() == "MERGE":
                    return QueryType.MERGE
        
        raise ValueError(f"Unsupported query type: {parsed.value}")
    
    @staticmethod
    def _extract_tables_and_views(parsed: Statement) -> tuple[List[str], List[str]]:
        """Extract tables and views from the parsed SQL."""
        tables = []
        views = []
        
        # This is a simplified implementation
        # In a real-world scenario, you would need more sophisticated parsing
        # to correctly identify tables vs views
        
        for token in parsed.tokens:
            if isinstance(token, Identifier):
                # Check if this is a table reference
                if token.get_name():
                    tables.append(token.get_name())
            elif isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    if identifier.get_name():
                        tables.append(identifier.get_name())
        
        return tables, views
    
    @staticmethod
    def _extract_where_clause_ast(parsed: Statement) -> Optional[Dict[str, Any]]:
        """Extract the WHERE clause as an AST."""
        where_clause = None
        
        # Find the WHERE clause
        for token in parsed.tokens:
            if isinstance(token, Where):
                where_clause = token
                break
        
        if not where_clause:
            return None
        
        # Convert the WHERE clause to a simple AST representation
        # This is a simplified implementation
        ast = {
            "type": "where",
            "conditions": []
        }
        
        # Process the WHERE clause tokens
        current_condition = {}
        for token in where_clause.tokens:
            if token.ttype in (Name, Number, String):
                if "left" not in current_condition:
                    current_condition["left"] = token.value
                elif "operator" not in current_condition:
                    current_condition["operator"] = token.value
                else:
                    current_condition["right"] = token.value
                    ast["conditions"].append(current_condition)
                    current_condition = {}
            elif token.ttype in (Operator, Comparison):
                if "left" in current_condition:
                    current_condition["operator"] = token.value
        
        return ast 