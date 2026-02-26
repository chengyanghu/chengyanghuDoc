#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MemU Implementation Examples
============================
Comprehensive code examples for MemU AI memory framework.
Source: Context7 MemU Documentation [[2]](https://context7.com/nevamind-ai/memu/llms.txt)
"""

import asyncio
from typing import List, Dict, Any, Optional

# ============================================================
# 1. Basic Memory Service
# ============================================================

class MemUBasicExample:
    """
    Basic MemU MemoryService operations.
    
    MemU is an agentic memory framework that:
    - Ingests multimodal inputs
    - Autonomously organizes into structured categories
    - Enables retrieval via embedding search or LLM-based reading
    
    Source: [[2]](https://context7.com/nevamind-ai/memu/llms.txt)
    """
    
    def __init__(self, api_key: str, chat_model: str = "gpt-4o-mini"):
        """
        Initialize MemU MemoryService.
        
        Args:
            api_key: MemU API key
            chat_model: LLM model to use (default: gpt-4o-mini)
        """
        from memu.app import MemoryService
        
        self.api_key = api_key
        self.service = MemoryService(
            llm_profiles={
                "default": {
                    "api_key": api_key,
                    "chat_model": chat_model
                }
            },
            # Optional: SQLite local storage
            database_config={
                "metadata_store": {
                    "provider": "sqlite",
                    "dsn": "sqlite:///memories.db"
                }
            }
        )
    
    async def memorize(self, resource_url: str, modality: str, 
                      user_id: str = None) -> Dict:
        """
        Store content into memory.
        
        Args:
            resource_url: Path or URL to resource
            modality: Type of content (conversation, document, image, code)
            user_id: Optional user identifier for scoping
        
        Returns:
            Dict with memorize result
        
        Example:
            >>> example = MemUBasicExample("your-api-key")
            >>> result = await example.memorize(
            ...     "conversation.json",
            ...     modality="conversation",
            ...     user_id="alice"
            ... )
        """
        result = await self.service.memorize(
            resource_url=resource_url,
            modality=modality,
            user={"user_id": user_id} if user_id else {}
        )
        
        print(f"Memorized {resource_url}: {len(result.get('items', []))} items")
        return result
    
    async def retrieve(self, query: str, user_id: str = None,
                     method: str = "rag") -> Dict:
        """
        Retrieve memories.
        
        Args:
            query: Search query
            user_id: Optional user for scoping
            method: "rag" for fast, "llm" for deep reasoning
        
        Returns:
            Dict with retrieval results including needs_retrieval, 
            rewritten_query, categories, items, resources
        
        Example:
            >>> result = await example.retrieve(
            ...     "What are my preferences?",
            ...     user_id="alice",
            ...     method="rag"
            ... )
        """
        queries = [{"role": "user", "content": {"text": query}}]
        
        result = await self.service.retrieve(
            queries=queries,
            where={"user_id": user_id} if user_id else {},
            method=method
        )
        
        print(f"Needs retrieval: {result['needs_retrieval']}")
        print(f"Rewritten query: {result.get('rewritten_query', 'N/A')}")
        print(f"Categories: {len(result.get('categories', []))}")
        print(f"Items: {len(result.get('items', []))}")
        
        return result
    
    async def retrieve_with_context(self, conversation: List[Dict], 
                                   main_query: str, user_id: str = None) -> Dict:
        """
        Retrieve with full conversation context.
        
        This is useful for understanding the full context of a query.
        
        Args:
            conversation: List of conversation turns
            main_query: The main question to answer
            user_id: User identifier
        
        Returns:
            Full retrieval result with context understanding
        """
        queries = []
        for turn in conversation:
            queries.append({
                "role": turn.get("role", "user"),
                "content": {"text": turn.get("content", "")}
            })
        
        # Add the main query as the last turn
        queries.append({
            "role": "user",
            "content": {"text": main_query}
        })
        
        result = await self.service.retrieve(
            queries=queries,
            where={"user_id": user_id} if user_id else {},
            method="llm"  # Use LLM mode for complex context
        )
        
        return result


# ============================================================
# 2. CRUD Operations
# ============================================================

class MemUCRUDExample:
    """
    Complete CRUD operations for MemU memory items.
    
    Source: [[2]](https://context7.com/nevamind-ai/memu/llms.txt)
    """
    
    def __init__(self, api_key: str):
        """Initialize with API key."""
        from memu.app import MemoryService
        
        self.service = MemoryService(
            llm_profiles={
                "default": {
                    "api_key": api_key,
                    "chat_model": "gpt-4o-mini"
                }
            },
            memorize_config={
                "memory_categories": [
                    {"name": "preferences", "description": "User preferences"},
                    {"name": "knowledge", "description": "Domain knowledge"},
                    {"name": "profile", "description": "User profile info"},
                ]
            }
        )
    
    async def create_memory(self, memory_type: str, content: str,
                           categories: List[str], user_id: str) -> str:
        """
        Create a new memory item.
        
        Args:
            memory_type: Type of memory (profile, knowledge, etc.)
            content: Memory content text
            categories: List of category names
            user_id: User identifier
        
        Returns:
            Created memory ID
        """
        result = await self.service.create_memory_item(
            memory_type=memory_type,
            memory_content=content,
            memory_categories=categories,
            user={"user_id": user_id}
        )
        
        memory_id = result["memory_item"]["id"]
        print(f"Created memory: {memory_id}")
        return memory_id
    
    async def update_memory(self, memory_id: str, new_content: str,
                           categories: List[str], user_id: str) -> Dict:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of memory to update
            new_content: New content
            categories: Updated categories
            user_id: User identifier
        
        Returns:
            Update result
        """
        result = await self.service.update_memory_item(
            memory_id=memory_id,
            memory_content=new_content,
            memory_categories=categories,
            user={"user_id": user_id}
        )
        
        print(f"Updated memory: {result['memory_item']['summary']}")
        return result
    
    async def list_memories(self, user_id: str) -> List[Dict]:
        """
        List all memories for a user.
        
        Args:
            user_id: User identifier
        
        Returns:
            List of memory items
        """
        result = await self.service.list_memory_items(
            where={"user_id": user_id}
        )
        
        print(f"Total memories: {len(result['items'])}")
        
        for item in result['items']:
            print(f"  - [{item['memory_type']}] {item['summary'][:50]}...")
        
        return result['items']
    
    async def list_categories(self, user_id: str) -> List[Dict]:
        """
        List all memory categories.
        
        Args:
            user_id: User identifier
        
        Returns:
            List of categories
        """
        result = await self.service.list_memory_categories(
            where={"user_id": user_id}
        )
        
        print(f"Categories ({len(result['categories'])}):")
        for cat in result['categories']:
            print(f"  - {cat['name']}: {cat.get('description', 'N/A')}")
        
        return result['categories']
    
    async def delete_memory(self, memory_id: str, user_id: str) -> bool:
        """
        Delete a specific memory.
        
        Args:
            memory_id: ID of memory to delete
            user_id: User identifier
        
        Returns:
            True if successful
        """
        result = await self.service.delete_memory_item(
            memory_id=memory_id,
            user={"user_id": user_id}
        )
        
        print(f"Deleted memory: {memory_id}")
        return True
    
    async def clear_all(self, user_id: str) -> Dict:
        """
        Clear all memories for a user.
        
        Args:
            user_id: User identifier
        
        Returns:
            Dict with deleted counts
        """
        result = await self.service.clear_memory(
            where={"user_id": user_id}
        )
        
        print(f"Cleared: {len(result['deleted_items'])} items, "
              f"{len(result['deleted_categories'])} categories")
        
        return result


# ============================================================
# 3. Multimodal Memory
# ============================================================

class MemUMultimodalExample:
    """
    Process multimodal data (text, images, documents) 
    into unified cross-modal memory.
    
    Source: [[2]](https://context7.com/nevamind-ai/memu/llms.txt)
    """
    
    def __init__(self, api_key: str):
        """Initialize with custom categories for different modalities."""
        from memu.app import MemoryService
        
        # Define categories for different content types
        self.categories = [
            {"name": "technical_documentation", 
             "description": "Technical guides and tutorials"},
            {"name": "architecture_concepts", 
             "description": "System architecture and design patterns"},
            {"name": "visual_diagrams", 
             "description": "Charts and illustrations from images"},
            {"name": "code_examples", 
             "description": "Code snippets and implementation details"},
        ]
        
        self.service = MemoryService(
            llm_profiles={
                "default": {
                    "api_key": api_key,
                    "chat_model": "gpt-4o-mini"
                }
            },
            memorize_config={
                "memory_categories": self.categories
            }
        )
    
    async def memorize_file(self, file_path: str, modality: str) -> Dict:
        """
        Memorize a single file.
        
        Args:
            file_path: Path to file
            modality: Type (document, image, code, conversation)
        
        Returns:
            Memorization result
        """
        result = await self.service.memorize(
            resource_url=file_path,
            modality=modality
        )
        
        print(f"Processed {file_path}: {len(result.get('items', []))} items")
        return result
    
    async def memorize_multiple(self, resources: List[tuple]) -> Dict:
        """
        Memorize multiple resources of different modalities.
        
        Args:
            resources: List of (file_path, modality) tuples
        
        Returns:
            Combined results
        """
        all_items = []
        
        for file_path, modality in resources:
            result = await self.service.memorize(
                resource_url=file_path,
                modality=modality
            )
            all_items.extend(result.get('items', []))
        
        print(f"Processed {len(resources)} resources: {len(all_items)} total items")
        return {"items": all_items}
    
    async def crossmodal_retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve context across all modalities.
        
        This allows asking questions that span multiple data types.
        
        Args:
            query: Unified query
        
        Returns:
            List of relevant memories from any modality
        """
        result = await self.service.retrieve(
            queries=[{"role": "user", "content": {"text": query}}],
            method="llm"  # Use LLM for cross-modal understanding
        )
        
        print(f"Cross-modal retrieval results ({len(result['items'])}):")
        for item in result['items'][:5]:
            print(f"  - [{item['memory_type']}] {item['summary'][:80]}...")
        
        return result['items']


# ============================================================
# 4. Dual-Mode Retrieval
# ============================================================

class MemURetrievalModes:
    """
    Demonstrate dual-mode retrieval: RAG vs LLM.
    
    Source: [[2]](https://context7.com/nevamind-ai/memu/llms.txt)
    """
    
    def __init__(self, api_key: str):
        """Initialize with both retrieval modes available."""
        from memu.app import MemoryService
        
        self.service = MemoryService(
            llm_profiles={
                "default": {
                    "api_key": api_key,
                    "chat_model": "gpt-4o-mini"
                }
            }
        )
    
    async def rag_retrieval(self, query: str, user_id: str = None) -> Dict:
        """
        Fast RAG-based retrieval.
        
        Best for:
        - Direct question-answering
        - Precise fact lookup
        - Time-critical applications
        
        Args:
            query: Search query
            user_id: Optional user scope
        
        Returns:
            Retrieval results
        """
        result = await self.service.retrieve(
            queries=[{"role": "user", "content": {"text": query}}],
            where={"user_id": user_id} if user_id else {},
            method="rag"  # Fast mode
        )
        
        print("=" * 40)
        print("RAG MODE (Fast)")
        print("=" * 40)
        print(f"Needs retrieval: {result['needs_retrieval']}")
        print(f"Items found: {len(result.get('items', []))}")
        
        return result
    
    async def llm_retrieval(self, query: str, user_id: str = None) -> Dict:
        """
        Deep LLM-based retrieval.
        
        Best for:
        - Complex reasoning questions
        - Ambiguous queries
        - Context-dependent answers
        
        Args:
            query: Complex query
            user_id: Optional user scope
        
        Returns:
            Retrieval results with LLM understanding
        """
        result = await self.service.retrieve(
            queries=[{"role": "user", "content": {"text": query}}],
            where={"user_id": user_id} if user_id else {},
            method="llm"  # Deep reasoning mode
        )
        
        print("=" * 40)
        print("LLM MODE (Deep Reasoning)")
        print("=" * 40)
        print(f"Needs retrieval: {result['needs_retrieval']}")
        print(f"Rewritten query: {result.get('rewritten_query', 'N/A')}")
        print(f"Categories: {len(result.get('categories', []))}")
        
        return result
    
    async def adaptive_retrieval(self, query: str, user_id: str = None) -> Dict:
        """
        Automatically choose best retrieval mode.
        
        Uses needs_retrieval flag to decide if memory is needed.
        
        Args:
            query: User query
            user_id: User scope
        
        Returns:
            Appropriate retrieval result
        """
        # First check if retrieval is needed
        result = await self.service.retrieve(
            queries=[{"role": "user", "content": {"text": query}}],
            where={"user_id": user_id} if user_id else {}
        )
        
        # Check needs_retrieval flag
        if not result.get('needs_retrieval', True):
            print("Query answered without external retrieval")
            return result
        
        # If retrieval needed, choose mode based on query complexity
        query_complexity = len(query.split())  # Simple heuristic
        
        if query_complexity < 10:
            return await self.rag_retrieval(query, user_id)
        else:
            return await self.llm_retrieval(query, user_id)


# ============================================================
# 5. Usage Examples
# ============================================================

async def example_basic_usage():
    """Basic MemU operations."""
    print("=" * 60)
    print("Example 1: Basic Memory Operations")
    print("=" * 60)
    
    # Note: Replace with your actual API key
    # api_key = os.environ.get("MEMU_API_KEY")
    # example = MemUBasicExample(api_key)
    
    # This would work with a valid API key:
    # await example.memorize("conversation.json", "conversation", "alice")
    # result = await example.retrieve("What did we discuss?", "alice")
    
    print("(Requires valid API key - see documentation)")


async def example_crud_operations():
    """CRUD operations example."""
    print("\n" + "=" * 60)
    print("Example 2: CRUD Operations")
    print("=" * 60)
    
    # api_key = os.environ.get("MEMU_API_KEY")
    # crud = MemUCRUDExample(api_key)
    
    # Create
    # memory_id = await crud.create_memory(
    #     "profile",
    #     "User prefers dark mode UI",
    #     ["preferences"],
    #     "alice"
    # )
    
    # Update
    # await crud.update_memory(
    #     memory_id,
    #     "User prefers dark mode with minimal animations",
    #     ["preferences"],
    #     "alice"
    # )
    
    # List
    # items = await crud.list_memories("alice")
    
    # Delete
    # await crud.delete_memory(memory_id, "alice")
    
    print("(Requires valid API key - see documentation)")


async def example_multimodal():
    """Multimodal memory example."""
    print("\n" + "=" * 60)
    print("Example 3: Multimodal Memory")
    print("=" * 60)
    
    # api_key = os.environ.get("MEMU_API_KEY")
    # multimodal = MemUMultimodalExample(api_key)
    
    # Process different modalities
    # resources = [
    #     ("docs/architecture.txt", "document"),
    #     ("diagrams/system.png", "image"),
    #     ("code/main.py", "code"),
    # ]
    # await multimodal.memorize_multiple(resources)
    
    # Cross-modal retrieval
    # results = await multimodal.crossmodal_retrieve(
    #     "Explain the system architecture and show relevant code"
    # )
    
    print("(Requires valid API key - see documentation)")


async def example_dual_mode():
    """Dual-mode retrieval example."""
    print("\n" + "=" * 60)
    print("Example 4: Dual-Mode Retrieval")
    print("=" * 60)
    
    # api_key = os.environ.get("MEMU_API_KEY")
    # modes = MemURetrievalModes(api_key)
    
    # RAG mode - fast
    # result = await modes.rag_retrieval(
    #     "What is my email?",
    #     "alice"
    # )
    
    # LLM mode - deep
    # result = await modes.llm_retrieval(
    #     "Based on my preferences and past conversations, what would be a good vacation?",
    #     "alice"
    # )
    
    # Adaptive
    # result = await modes.adaptive_retrieval(
    #     "Tell me about my work",
    #     "alice"
    # )
    
    print("(Requires valid API key - see documentation)")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("MemU Implementation Examples")
    print("=" * 60)
    print()
    
    # Run async examples
    asyncio.run(example_basic_usage())
    asyncio.run(example_crud_operations())
    asyncio.run(example_multimodal())
    asyncio.run(example_dual_mode())
    
    print("\n" + "=" * 60)
    print("To run these examples:")
    print("1. Get a MemU API key from https://memu.so")
    print("2. Set environment variable: export MEMU_API_KEY=your-key")
    print("3. Uncomment the example code")
    print("=" * 60)
