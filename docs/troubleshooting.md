# Troubleshooting

## 1) "API Key is missing"

Please verify in `LLMs_Manager`:

1. Provider is selected
2. API key is filled in
3. Clicked **Save**
4. **Enable in Nodes** is ON

Then refresh ComfyUI web UI (`Cmd/Ctrl + R`).

---

## 2) Provider/model not shown in node dropdown

- Save provider config first
- Refresh browser after config changes
- Confirm the provider is enabled in manager

---

## 3) Transformers / dependency errors

This toolkit uses a lightweight OpenAI-compatible API path and does **not** require `transformers` for normal use.

If your environment still reports `transformers` errors:

1. Update ComfyUI to latest stable
2. Reinstall node dependencies:
   ```bash
   pip install -r requirements.txt -U
   ```
3. Check for conflicting custom nodes that import incompatible transformer/torch stacks
4. Restart ComfyUI and capture full traceback for issue reports

When reporting, include:
- ComfyUI version
- Python version
- OS
- Full error traceback
- Minimal workflow to reproduce

---

## 4) Local model endpoint (Ollama / self-hosted) not working

- Ensure endpoint is OpenAI-compatible (e.g. `http://localhost:11434/v1`)
- Verify model name matches server-side model id
- Test with a simple chat completion request first

---

## 5) Image input fails in vision flow

- Use `Image Preprocessor` before connecting to adapter node `prep_img`
- Ensure image tensor/PIL input is valid

---

## 6) Still stuck?

Open an issue and include environment + full traceback:

- Issues: https://github.com/HuangYuChuh/ComfyUI-LLMs-Toolkit/issues
