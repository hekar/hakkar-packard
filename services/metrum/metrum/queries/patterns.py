import json
import time
from pathlib import Path
from typing import Dict, Optional
import hashlib
import requests
from pydantic import BaseModel, Field

from metrum.settings import settings

class Pattern(BaseModel):
    """A pattern to match in PostgreSQL logs."""
    query_pattern: str = Field(..., description="Regular expression pattern to match queries")
    description: str = Field(..., description="Description of what this pattern matches")

class PatternConfig(BaseModel):
    """Configuration for log patterns."""
    patterns: Dict[str, Pattern]

    @classmethod
    def get_default_patterns(cls) -> "PatternConfig":
        """Get the default pattern configuration."""
        return cls(patterns={
            "complex_window_function": Pattern(
                query_pattern=r"WITH.*ROW_NUMBER\(\).*OVER.*ORDER BY",
                description="Complex queries using window functions with ROW_NUMBER"
            ),
            "select_statement": Pattern(
                query_pattern=r"SELECT.*FROM",
                description="Simple SELECT statements"
            )
        })

class PatternLoader:
    """Loads and caches pattern configurations."""
    
    def __init__(self):
        self.cache_dir = Path(settings.patterns_cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, source: str) -> Path:
        """Get the cache file path for a source."""
        # Create a hash of the source URL/path to use as the cache file name
        source_hash = hashlib.sha256(source.encode()).hexdigest()[:16]
        return self.cache_dir / f"patterns_{source_hash}.json"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if the cache file is still valid based on TTL."""
        if not cache_path.exists():
            return False
        
        cache_age = time.time() - cache_path.stat().st_mtime
        return cache_age < settings.patterns_cache_ttl
    
    def _load_from_url(self, url: str) -> PatternConfig:
        """Load patterns from a URL."""
        response = requests.get(url, timeout=settings.http_timeout)
        response.raise_for_status()
        return PatternConfig.model_validate(response.json())
    
    def _load_from_file(self, file_path: str) -> PatternConfig:
        """Load patterns from a local file."""
        with open(file_path, 'r') as f:
            return PatternConfig.model_validate(json.load(f))
    
    def _save_to_cache(self, config: PatternConfig, cache_path: Path) -> None:
        """Save pattern configuration to cache."""
        with open(cache_path, 'w') as f:
            json.dump(config.model_dump(), f, indent=2)
    
    def load_patterns(self) -> PatternConfig:
        """Load patterns from the configured source with caching support."""
        if not settings.patterns_source:
            return PatternConfig.get_default_patterns()
        
        source = settings.patterns_source
        cache_path = self._get_cache_path(source)
        
        # Check cache first
        if self._is_cache_valid(cache_path):
            try:
                return self._load_from_file(str(cache_path))
            except (json.JSONDecodeError, IOError):
                # If cache is corrupted, ignore it and continue with source
                pass
        
        # Load from source
        try:
            if source.startswith(('http://', 'https://')):
                config = self._load_from_url(source)
            else:
                config = self._load_from_file(source)
            
            # Cache the result
            self._save_to_cache(config, cache_path)
            return config
            
        except Exception as e:
            # If loading from source fails, try to use cached version regardless of TTL
            if cache_path.exists():
                return self._load_from_file(str(cache_path))
            # If no cache exists, return default patterns
            return PatternConfig.get_default_patterns() 