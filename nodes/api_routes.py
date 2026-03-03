"""
LLM Provider Management API Routes for ComfyUI.

Provides RESTful endpoints for managing LLM provider configurations
(API keys, base URLs, models). Data is persisted to config/providers.json.

Routes are registered via ComfyUI's PromptServer at startup.
"""

import os
import json
import shutil
import uuid
import logging
from pathlib import Path
from aiohttp import web

# Resolve config paths relative to the plugin root
_PLUGIN_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_DIR = _PLUGIN_ROOT / "config"
_PROVIDERS_FILE = _CONFIG_DIR / "providers.json"
_DEFAULT_PROVIDERS_FILE = _CONFIG_DIR / "default_providers.json"

logger = logging.getLogger("[LLMs_Toolkit.Routes]")


# ─── Data Access Layer ───────────────────────────────────────────────────────

def _ensure_providers_file() -> dict:
    """
    Ensure providers.json exists. If not, copy from default_providers.json.
    Returns the parsed providers data with schema migration applied.
    """
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not _PROVIDERS_FILE.exists():
        if _DEFAULT_PROVIDERS_FILE.exists():
            shutil.copy2(_DEFAULT_PROVIDERS_FILE, _PROVIDERS_FILE)
            logger.info(f"Initialized providers.json from defaults.")
        else:
            # Fallback: create empty structure
            data = {"providers": []}
            _PROVIDERS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.warning("No default_providers.json found, created empty providers.json.")

    data = _load_providers()
    
    # ── Schema Migration ──────────────────────────────────────────────────
    if _DEFAULT_PROVIDERS_FILE.exists():
        try:
            with open(_DEFAULT_PROVIDERS_FILE, "r", encoding="utf-8") as f:
                default_data = json.load(f)
                default_providers = {p.get("id"): p for p in default_data.get("providers", []) if p.get("id")}
                
            needs_save = False
            for p in data.get("providers", []):
                # If it's a system provider (or ID matches a default), ensure it has all default keys
                if p.get("id") in default_providers:
                    dp = default_providers[p["id"]]
                    for key, val in dp.items():
                        if key not in p:
                            p[key] = val
                            needs_save = True
            
            if needs_save:
                _save_providers(data)
                logger.info("Migrated providers.json schema to include missing default fields.")
        except Exception as e:
            logger.error(f"Schema migration failed: {e}")

    return data


def _load_providers() -> dict:
    """Load and return providers data from disk."""
    try:
        with open(_PROVIDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Failed to load providers.json: {e}")
        return {"providers": []}


def _save_providers(data: dict):
    """Persist providers data to disk."""
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(_PROVIDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─── API Route Handlers ─────────────────────────────────────────────────────

async def get_providers(request: web.Request) -> web.Response:
    """GET /llm_toolkit/providers — Return all provider configurations."""
    data = _ensure_providers_file()
    return web.json_response(data)


async def save_provider(request: web.Request) -> web.Response:
    """POST /llm_toolkit/providers — Create or update a provider (upsert by id)."""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON body"}, status=400)

    provider_id = body.get("id")
    if not provider_id:
        # New provider — generate UUID
        provider_id = str(uuid.uuid4())[:8]
        body["id"] = provider_id
        body["isSystem"] = False

    # Ensure required fields have defaults
    body.setdefault("name", "Unnamed Provider")
    body.setdefault("type", "openai")
    body.setdefault("apiKey", "")
    body.setdefault("apiHost", "")
    body.setdefault("models", [])
    body.setdefault("enabled", True)

    data = _ensure_providers_file()
    providers = data.get("providers", [])

    # Upsert: find existing by id and replace, or append
    found = False
    for i, p in enumerate(providers):
        if p.get("id") == provider_id:
            # Preserve isSystem flag from existing record
            body["isSystem"] = p.get("isSystem", False)
            providers[i] = body
            found = True
            break

    if not found:
        providers.append(body)

    data["providers"] = providers
    _save_providers(data)

    logger.info(f"{'Updated' if found else 'Created'} provider: {body.get('name')} ({provider_id})")
    return web.json_response({"status": "ok", "provider": body})


async def delete_provider(request: web.Request) -> web.Response:
    """DELETE /llm_toolkit/providers/{id} — Remove a user-created provider."""
    provider_id = request.match_info.get("id")
    if not provider_id:
        return web.json_response({"error": "Provider ID is required"}, status=400)

    data = _ensure_providers_file()
    providers = data.get("providers", [])

    # Find the provider
    target = None
    for p in providers:
        if p.get("id") == provider_id:
            target = p
            break

    if target is None:
        return web.json_response({"error": "Provider not found"}, status=404)

    if target.get("isSystem", False):
        return web.json_response({"error": "Cannot delete system provider"}, status=403)

    providers = [p for p in providers if p.get("id") != provider_id]
    data["providers"] = providers
    _save_providers(data)

    logger.info(f"Deleted provider: {provider_id}")
    return web.json_response({"status": "ok"})


async def check_provider(request: web.Request) -> web.Response:
    """POST /llm_toolkit/providers/check — Test API key connectivity."""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON body"}, status=400)

    api_key = body.get("apiKey", "").strip()
    api_host = body.get("apiHost", "").strip()
    model = body.get("model", "").strip()

    if not api_key or not api_host:
        return web.json_response({"error": "apiKey and apiHost are required"}, status=400)

    # Use the shared LLMClient to perform a minimal test call
    try:
        import api_client
        import asyncio
        client = api_client.LLMClient(base_url=api_host, api_key=api_key)
        
        # 1. Try fetching models (doesn't consume tokens)
        try:
            await asyncio.to_thread(client.list_models)
        except Exception as e_models:
            logger.warning(f"Check API: /models failed ({str(e_models)[:100]}), falling back to /chat/completions")
            
            # 2. Fallback to a minimal chat completion if /models is not supported
            payload = {
                "model": model or "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 1,
                "stream": False
            }
            await asyncio.to_thread(client.chat, payload)

        return web.json_response({
            "status": "ok",
            "message": "Connection successful"
        })

    except Exception as e:
        return web.json_response({
            "status": "error",
            "message": str(e)[:500]
        }, status=502)


# ─── Route Registration ─────────────────────────────────────────────────────

def register_routes():
    """Register all provider management routes with ComfyUI's PromptServer."""
    try:
        from server import PromptServer

        routes = PromptServer.instance.routes

        routes.get("/llm_toolkit/providers")(get_providers)
        routes.post("/llm_toolkit/providers")(save_provider)
        routes.delete("/llm_toolkit/providers/{id}")(delete_provider)
        routes.post("/llm_toolkit/providers/check")(check_provider)

        logger.info("Provider management API routes registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register API routes: {e}")


# Auto-register when module is loaded by ComfyUI
register_routes()
