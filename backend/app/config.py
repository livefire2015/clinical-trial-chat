"""
Application Configuration using Pydantic Settings

This module provides type-safe configuration management for the clinical trial
analysis application. Settings are loaded from environment variables with
validation and caching for optimal performance.

Best practices implemented:
- Environment-based configuration (12-factor app)
- Type safety with Pydantic validation
- Performance optimization with @lru_cache
- Security with SecretStr for sensitive values
- Dependency injection ready for testing
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    AI Model Configuration:
    - Use Pydantic AI's string format: "provider:model-name"
    - Examples:
      - OpenAI: "openai:gpt-4", "openai:gpt-4-turbo", "openai:gpt-3.5-turbo"
      - Anthropic: "anthropic:claude-sonnet-4-5-20250929"
    - See: https://ai.pydantic.dev/models/
    """

    # Server Configuration
    port: int = Field(default=8000, description="Server port")

    # Database Configuration
    database_url: str = Field(
        default="host=localhost port=5432 user=postgres password=postgres dbname=clinical_trials sslmode=disable",
        description="PostgreSQL connection string"
    )

    # AI Model Configuration
    ai_model: str = Field(
        default="openai:gpt-4",
        description="Primary AI model in format 'provider:model-name'"
    )
    ai_fallback_model: Optional[str] = Field(
        default=None,
        description="Optional fallback model if primary fails"
    )

    # API Keys (using SecretStr to prevent accidental logging)
    openai_api_key: Optional[SecretStr] = Field(
        default=None,
        description="OpenAI API key for GPT models"
    )
    anthropic_api_key: Optional[SecretStr] = Field(
        default=None,
        description="Anthropic API key for Claude models"
    )

    # MCP Server Paths
    mcp_database_path: str = Field(
        default="../mcp-servers/database/mcp-database",
        description="Path to MCP database server binary"
    )
    mcp_filesystem_path: str = Field(
        default="../mcp-servers/filesystem/mcp-filesystem",
        description="Path to MCP filesystem server binary"
    )
    mcp_external_api_path: str = Field(
        default="../mcp-servers/external-api/mcp-external-api",
        description="Path to MCP external API server binary"
    )

    # Security
    encryption_key: str = Field(
        default="change-this-to-a-secure-32-byte-key-in-production",
        description="32-byte encryption key for sensitive data"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Using @lru_cache ensures we only read the .env file once,
    improving performance for repeated calls. This is the
    recommended pattern from FastAPI documentation.

    For testing, you can override this with:
        app.dependency_overrides[get_settings] = override_get_settings

    Returns:
        Settings: Cached application settings instance
    """
    return Settings()
