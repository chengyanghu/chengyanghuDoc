#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mem0 Implementation Examples
===========================
Comprehensive code examples for Mem0 AI memory framework.
Source: Context7 Mem0 Documentation [[1]](https://context7.com/mem0ai/mem0/llms.txt)
"""

import os
from typing import List, Dict, Any, Optional

# ============================================================
# 1. Basic Memory Operations
# ============================================================

class Mem0BasicExample:
    """
    Basic memory operations with Mem0.
    Demonstrates add, search, get_all, update, delete.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Mem0 client.
        
        Args:
            api_key: Mem0 API key (or set via MEM0_API_KEY env var)
        """
        from mem0 import Memory
        
        self.api_key = api_key or os.environ.get("MEM0_API_KEY")
        
        # Basic configuration
        config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o",
                    "temperature": 0.1
                }
            },
            "vector_store": {
                "provider": "chroma"
            }
        }
        
        self.memory = Memory.from_config(config)
    
    def add_conversation(self, messages: List[Dict], user_id: str, metadata: Dict = None) -> Dict:
        """
        Add conversation to memory.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            user_id: Unique user identifier
            metadata: Optional metadata for filtering
        
        Returns:
            Dict with memory_id and status
        
        Example:
            >>> example = Mem0BasicExample()
            >>> result = example.add_conversation(
            ...     [
            ...         {"role": "user", "content": "I love sci-fi movies"},
            ...         {"role": "assistant", "content": "Got it! I'll remember your preference."}
            ...     ],
            ...     user_id="alice"
            ... )
        """
        result = self.memory.add(
            messages=messages,
            user_id=user_id,
            metadata=metadata or {}
        )
        
        print(f"Added memory: {result.get('memory_id')}")
        return result
    
    def add_fact(self, fact: str, user_id: str, metadata: Dict = None) -> Dict:
        """
        Add a single fact to memory.
        
        Args:
            fact: Factual statement
            user_id: User identifier
            metadata: Optional metadata
        
        Returns:
            Dict with memory_id
        """
        result = self.memory.add(
            fact,
            user_id=user_id,
            metadata=metadata or {}
        )
        
        print(f"Added fact: {result.get('memory_id')}")
        return result
    
    def search(self, query: str, user_id: str, limit: int = 5, 
               rerank: bool = False) -> List[Dict]:
        """
        Search memories semantically.
        
        Args:
            query: Natural language search query
            user_id: User to search within
            limit: Maximum results
            rerank: Enable result reranking
        
        Returns:
            List of memory results with scores
        """
        results = self.memory.search(
            query=query,
            user_id=user_id,
            limit=limit,
            rerank=rerank
        )
        
        print(f"Found {len(results.get('results', []))} memories")
        
        # Format results
        formatted = []
        for r in results.get('results', []):
            formatted.append({
                'memory': r.get('memory'),
                'score': r.get('score'),
                'id': r.get('id')
            })
        
        return formatted
    
    def get_all(self, user_id: str, page: int = 1, 
                page_size: int = 10) -> Dict:
        """
        Get all memories for a user.
        
        Args:
            user_id: User identifier
            page: Page number
            page_size: Items per page
        
        Returns:
            Dict with memories list and pagination info
        """
        results = self.memory.get_all(
            user_id=user_id,
            page=page,
            page_size=page_size
        )
        
        print(f"Total memories: {results.get('total', 0)}")
        
        return results
    
    def update(self, memory_id: str, new_data: str) -> Dict:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of memory to update
            new_data: New content
        
        Returns:
            Updated memory dict
        """
        result = self.memory.update(
            memory_id=memory_id,
            data=new_data
        )
        
        print(f"Updated memory: {memory_id}")
        return result
    
    def delete(self, memory_id: str) -> Dict:
        """
        Delete a specific memory.
        
        Args:
            memory_id: ID of memory to delete
        
        Returns:
            Deletion result
        """
        result = self.memory.delete(memory_id=memory_id)
        print(f"Deleted memory: {memory_id}")
        return result
    
    def delete_all(self, user_id: str) -> Dict:
        """
        Delete all memories for a user.
        
        Args:
            user_id: User whose memories to delete
        
        Returns:
            Deletion result
        """
        result = self.memory.delete_all(user_id=user_id)
        print(f"Deleted all memories for user: {user_id}")
        return result


# ============================================================
# 2. Graph Memory (with Neo4j)
# ============================================================

class Mem0GraphExample:
    """
    Graph memory implementation with Neo4j.
    Enables entity relationship tracking.
    
    Source: [[3]](https://context7.com/mem0ai/mem0/llms.txt)
    """
    
    def __init__(self, neo4j_url: str, neo4j_user: str, neo4j_password: str):
        """
        Initialize with Neo4j graph store.
        
        Args:
            neo4j_url: Neo4j bolt URL (e.g., "bolt://localhost:7687")
            neo4j_user: Neo4j username
            neo4j_password: Neo4j password
        """
        from mem0 import Memory
        from mem0.configs import MemoryConfig
        
        config = MemoryConfig(
            llm={
                "provider": "openai",
                "config": {"model": "gpt-4o"}
            },
            vector_store={
                "provider": "chroma"
            },
            graph_store={
                "provider": "neo4j",
                "config": {
                    "url": neo4j_url,
                    "username": neo4j_user,
                    "password": neo4j_password
                }
            }
        )
        
        self.memory = Memory(config)
    
    def add_with_relationships(self, content: str, user_id: str) -> Dict:
        """
        Add memory and automatically extract relationships.
        
        Args:
            content: Text containing entities and relationships
            user_id: User identifier
        
        Returns:
            Dict with both memories and extracted relations
        """
        result = self.memory.add(content, user_id=user_id)
        
        # Print extracted relationships
        if 'relations' in result:
            print("Extracted relationships:")
            for rel in result['relations']:
                print(f"  {rel['source']} --[{rel['relation']}]--> {rel['target']}")
        
        return result
    
    def search_with_graph(self, query: str, user_id: str) -> Dict:
        """
        Search with graph relationship context.
        
        Args:
            query: Search query
            user_id: User identifier
        
        Returns:
            Results with graph_relations
        """
        results = self.memory.search(
            query=query,
            user_id=user_id,
            enable_graph=True
        )
        
        # Print relationships in results
        for r in results.get('results', []):
            if 'graph_relations' in r:
                print(f"Memory: {r['memory']}")
                print("  Relationships:")
                for rel in r['graph_relations']:
                    print(f"    {rel['entity']} --[{rel['relation_type']}]--> {rel['related_entity']}")
        
        return results


# ============================================================
# 3. AI Companion Example
# ============================================================

class AICompanion:
    """
    Full AI Companion implementation with memory.
    
    This demonstrates a complete conversational AI that:
    - Remembers user preferences
    - Provides personalized responses
    - Learns from conversation history
    """
    
    def __init__(self, user_id: str):
        """
        Initialize AI Companion.
        
        Args:
            user_id: Unique user identifier
        """
        from mem0 import Memory
        
        self.user_id = user_id
        
        config = {
            "llm": {
                "provider": "openai", 
                "config": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.7
                }
            }
        }
        
        self.memory = Memory.from_config(config)
        
        # Initialize conversation history
        self.conversation_history = []
    
    def chat(self, user_message: str, assistant_response: str) -> str:
        """
        Complete chat flow with memory.
        
        Args:
            user_message: User's message
            assistant_response: Assistant's response
        
        Returns:
            The assistant response
        """
        # Step 1: Retrieve relevant memories
        relevant_memories = self.memory.search(
            query=user_message,
            user_id=self.user_id,
            limit=3
        )
        
        # Build context from memories
        context = ""
        if relevant_memories.get('results'):
            context = "\n".join([
                f"- {m['memory']}" 
                for m in relevant_memories['results']
            ])
        
        # Step 2: Store the conversation
        self.memory.add(
            messages=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_response}
            ],
            user_id=self.user_id,
            metadata={"type": "conversation"}
        )
        
        # Also store as fact for future retrieval
        if "prefer" in user_message.lower() or "like" in user_message.lower():
            self.memory.add(
                user_message,
                user_id=self.user_id,
                metadata={"type": "preference"}
            )
        
        return assistant_response
    
    def get_user_profile(self) -> Dict:
        """
        Get compiled user profile from all memories.
        
        Returns:
            Dict of user information
        """
        all_memories = self.memory.get_all(
            user_id=self.user_id,
            page_size=100
        )
        
        profile = {
            "preferences": [],
            "facts": [],
            "conversations": []
        }
        
        for mem in all_memories.get('results', []):
            metadata = mem.get('metadata', {})
            mem_type = metadata.get('type', 'fact')
            
            if mem_type == 'preference':
                profile['preferences'].append(mem['memory'])
            elif mem_type == 'conversation':
                profile['conversations'].append(mem['memory'])
            else:
                profile['facts'].append(mem['memory'])
        
        return profile


# ============================================================
# 4. Usage Examples
# ============================================================

def example_basic_operations():
    """Demonstrate basic memory operations."""
    print("=" * 60)
    print("Example 1: Basic Memory Operations")
    print("=" * 60)
    
    # Initialize
    example = Mem0BasicExample()
    
    # Add conversation
    example.add_conversation(
        messages=[
            {"role": "user", "content": "I'm planning a trip to Tokyo next month."},
            {"role": "assistant", "content": "Great! I'll remember that."}
        ],
        user_id="alice",
        metadata={"category": "travel"}
    )
    
    # Add facts
    example.add_fact(
        "I prefer dark roast coffee",
        user_id="alice",
        metadata={"category": "preference"}
    )
    
    # Search
    results = example.search("coffee preferences", user_id="alice")
    for r in results:
        print(f"  - {r['memory']} (score: {r['score']:.2f})")
    
    # Get all
    all_mems = example.get_all(user_id="alice")
    print(f"Total memories: {all_mems.get('total', 0)}")


def example_graph_memory():
    """Demonstrate graph memory with Neo4j."""
    print("\n" + "=" * 60)
    print("Example 2: Graph Memory with Neo4j")
    print("=" * 60)
    
    # Initialize with Neo4j (requires Neo4j running)
    graph_example = Mem0GraphExample(
        neo4j_url="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )
    
    # Add content with relationships
    result = graph_example.add_with_relationships(
        "John works at OpenAI and is friends with Sarah. "
        "John met Bob at the conference last year.",
        user_id="john_doe"
    )
    
    # Search with graph
    graph_example.search_with_graph(
        "Who does John know?",
        user_id="john_doe"
    )


def example_ai_companion():
    """Demonstrate AI Companion with memory."""
    print("\n" + "=" * 60)
    print("Example 3: AI Companion")
    print("=" * 60)
    
    companion = AICompanion(user_id="user_123")
    
    # Simulate conversation
    response1 = companion.chat(
        "Hi! I'm looking for movie recommendations. I love sci-fi movies.",
        "That's great! Sci-fi is a fascinating genre. I'll keep that in mind."
    )
    
    response2 = companion.chat(
        "What kind of music do I like?",
        "Based on our conversation, I know you love sci-fi movies. "
        "I don't yet know your music preferences - would you like to share?"
    )
    
    # Get profile
    profile = companion.get_user_profile()
    print(f"\nUser Profile:")
    print(f"  Preferences: {profile['preferences']}")
    print(f"  Facts: {profile['facts'][:2]}...")


# ============================================================
# Main Entry Point
# ============================================================

if __name__ == "__main__":
    print("Mem0 Implementation Examples")
    print("=" * 60)
    print()
    
    # Set your API key
    # os.environ["MEM0_API_KEY"] = "your-api-key"
    # os.environ["OPENAI_API_KEY"] = "your-openai-key"
    
    # Run examples
    try:
        example_basic_operations()
        # example_graph_memory()  # Requires Neo4j
        # example_ai_companion()
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Set your API keys to run these examples:")
        print("  export MEM0_API_KEY=your-mem0-key")
        print("  export OPENAI_API_KEY=your-openai-key")
