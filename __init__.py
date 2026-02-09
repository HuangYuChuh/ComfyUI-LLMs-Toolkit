"""
ComfyUI-LLMs-Toolkit: Lightweight LLM API integration for ComfyUI.

Auto-registration mechanism for all nodes.
"""
from pathlib import Path
import importlib.util
import sys

# Initialize mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Auto-load all nodes from nodes/ directory
nodes_dir = Path(__file__).parent / "nodes"

if nodes_dir.exists():
    for py_file in sorted(nodes_dir.glob("*.py")):
        if py_file.stem.startswith("_"):
            continue
        
        try:
            # Load module
            module_name = f"ComfyUI-LLMs-Toolkit.nodes.{py_file.stem}"
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Register node mappings
            if hasattr(module, "NODE_CLASS_MAPPINGS"):
                NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            
            if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                
        except Exception as e:
            print(f"[LLMs_Toolkit] Failed to load {py_file.stem}: {e}")

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
