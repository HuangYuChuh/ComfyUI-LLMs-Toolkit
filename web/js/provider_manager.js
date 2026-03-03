import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { $el } from "../../../scripts/ui.js";

// ============================================================================
// CSS Styles Loader
// ============================================================================
const styles = `
.llm-pm-modal {
    width: 800px;
    height: 600px;
    padding: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}
.llm-pm-header {
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--comfy-menu-bg);
}
.llm-pm-title {
    font-size: 1.2em;
    font-weight: bold;
    color: var(--fg-color);
    margin: 0;
}
.llm-pm-close {
    cursor: pointer;
    font-size: 1.5em;
    color: var(--descrip-text);
}
.llm-pm-close:hover {
    color: var(--fg-color);
}
.llm-pm-body {
    display: flex;
    flex: 1;
    overflow: hidden;
    background: var(--comfy-menu-bg);
}
/* -- Sidebar -- */
.llm-pm-sidebar {
    width: 250px;
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    background: var(--tr-odd-bg-color, var(--comfy-menu-bg));
}
.llm-pm-search {
    padding: 10px;
    border-bottom: 1px solid var(--border-color);
}
.llm-pm-search input {
    width: 100%;
    box-sizing: border-box;
    background: var(--comfy-input-bg);
    color: var(--input-text);
    border: 1px solid var(--border-color);
    padding: 6px 10px;
    border-radius: 4px;
}
.llm-pm-list {
    flex: 1;
    overflow-y: auto;
    padding: 10px 0;
}
.llm-pm-item {
    padding: 10px 15px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--fg-color);
    border-left: 3px solid transparent;
}
.llm-pm-item:hover {
    background: var(--tr-even-bg-color, rgba(255,255,255,0.05));
}
.llm-pm-item.active {
    background: var(--tr-even-bg-color, rgba(255,255,255,0.05));
    border-left-color: #4CAF50;
    font-weight: bold;
}
.llm-pm-item-tags {
    display: flex;
    gap: 4px;
}
.llm-pm-tag {
    font-size: 0.7em;
    padding: 2px 6px;
    border-radius: 10px;
    background: var(--comfy-input-bg);
    color: var(--descrip-text);
}
.llm-pm-tag.on {
    background: #4CAF50;
    color: white;
}
.llm-pm-sidebar-footer {
    padding: 10px;
    border-top: 1px solid var(--border-color);
}
.llm-pm-add-btn {
    width: 100%;
}

/* -- Content Panel -- */
.llm-pm-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.llm-pm-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--descrip-text);
}
.llm-pm-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.llm-pm-field label {
    font-size: 0.9em;
    font-weight: bold;
    color: var(--fg-color);
    display: flex;
    justify-content: space-between;
}
.llm-pm-field input[type="text"],
.llm-pm-field input[type="password"] {
    width: 100%;
    box-sizing: border-box;
    background: var(--comfy-input-bg);
    color: var(--input-text);
    border: 1px solid var(--border-color);
    padding: 8px 10px;
    border-radius: 4px;
}
.llm-pm-field input:focus {
    outline: none;
    border-color: #4CAF50;
}
.llm-pm-field-hint {
    font-size: 0.8em;
    color: var(--descrip-text);
    word-break: break-all;
}
.llm-pm-input-group {
    display: flex;
    gap: 8px;
}
.llm-pm-input-group input {
    flex: 1;
}

/* -- Models List -- */
.llm-pm-models {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}
.llm-pm-model-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--comfy-input-bg);
    color: var(--fg-color);
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 0.85em;
    border: 1px solid var(--border-color);
}
.llm-pm-model-del {
    cursor: pointer;
    color: var(--descrip-text);
}
.llm-pm-model-del:hover {
    color: var(--error-text);
}
.llm-pm-model-add {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    color: var(--descrip-text);
    border: 1px dashed var(--border-color);
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 0.85em;
    cursor: pointer;
}
.llm-pm-model-add:hover {
    color: var(--fg-color);
    border-color: var(--fg-color);
}

/* -- Actions -- */
.llm-pm-actions {
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
}
.llm-pm-actions-right {
    display: flex;
    gap: 10px;
}

/* Switch styling */
.llm-pm-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
}
.llm-pm-switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.llm-pm-slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--comfy-input-bg);
  transition: .2s;
  border-radius: 20px;
  border: 1px solid var(--border-color);
}
.llm-pm-slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 2px;
  bottom: 2px;
  background-color: var(--descrip-text);
  transition: .2s;
  border-radius: 50%;
}
.llm-pm-switch input:checked + .llm-pm-slider {
  background-color: #4CAF50;
  border-color: #4CAF50;
}
.llm-pm-switch input:checked + .llm-pm-slider:before {
  transform: translateX(20px);
  background-color: white;
}

/* -- Custom Prompt Dialog -- */
.llm-pm-prompt-overlay {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 20000;
}
.llm-pm-prompt-dialog {
    background: var(--comfy-menu-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 20px;
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}
.llm-pm-prompt-dialog h3 {
    margin: 0;
    font-size: 1.1em;
    color: var(--fg-color);
}
.llm-pm-prompt-dialog input {
    width: 100%;
    box-sizing: border-box;
    background: var(--comfy-input-bg);
    color: var(--input-text);
    border: 1px solid var(--border-color);
    padding: 8px;
    border-radius: 4px;
}
.llm-pm-prompt-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
.llm-pm-prompt-actions button {
    padding: 6px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}
.llm-pm-prompt-actions .cancel {
    background: transparent;
    color: var(--descrip-text);
    border: 1px solid var(--border-color);
}
.llm-pm-prompt-actions .confirm {
    background: #4CAF50;
    color: white;
    border: none;
}
`;

document.head.appendChild($el("style", { textContent: styles }));

// ============================================================================
// UI Component
// ============================================================================
class ProviderManager {
    constructor() {
        this.providers = [];
        this.selectedId = null;
        this.searchQuery = "";
        this.modal = null;
        this.currentDraft = null;
    }

    hasUnsavedChanges() {
        if (!this.selectedId || !this.currentDraft) return false;
        const original = this.providers.find(p => p.id === this.selectedId);
        if (!original) return false;

        const draftCopy = JSON.parse(JSON.stringify(this.currentDraft));
        delete draftCopy._isNew;
        const origCopy = JSON.parse(JSON.stringify(original));
        delete origCopy._isNew;

        return JSON.stringify(draftCopy) !== JSON.stringify(origCopy);
    }

    checkUnsaved(onProceed) {
        if (!this.hasUnsavedChanges()) {
            onProceed();
            return;
        }
        this.showConfirm(
            "Unsaved Changes",
            "You have unsaved changes.\\nAre you sure you want to discard them?",
            onProceed
        );
    }

    showDialog(options) {
        const overlay = $el("div.llm-pm-prompt-overlay");
        const dialogContent = [$el("h3", options.title)];
        if (options.message) {
            dialogContent.push($el("div", {
                style: { fontSize: "0.9em", color: "var(--descrip-text)", whiteSpace: "pre-wrap", margin: "10px 0", lineHeight: "1.4" },
                textContent: options.message
            }));
        }

        let inputElement = null;
        if (options.showInput) {
            inputElement = $el("input", { type: "text", value: options.inputDefault || "" });
            dialogContent.push(inputElement);
        }

        const closeDialog = () => {
            if (document.body.contains(overlay)) document.body.removeChild(overlay);
        };

        const actions = [];
        if (!options.alertOnly) {
            actions.push($el("button.cancel", {
                textContent: options.cancelText || "Cancel",
                onclick: () => {
                    closeDialog();
                    if (options.onCancel) options.onCancel();
                }
            }));
        }

        const confirmBtn = $el("button.confirm", {
            textContent: options.confirmText || "OK",
            onclick: () => {
                closeDialog();
                if (options.onConfirm) options.onConfirm(inputElement ? inputElement.value : null);
            }
        });
        actions.push(confirmBtn);

        dialogContent.push($el("div.llm-pm-prompt-actions", actions));
        const dialogBox = $el("div.llm-pm-prompt-dialog", dialogContent);
        overlay.appendChild(dialogBox);
        document.body.appendChild(overlay);

        if (inputElement) {
            inputElement.onkeydown = (e) => {
                if (e.key === "Enter") confirmBtn.click();
                if (e.key === "Escape" && !options.alertOnly) actions[0].click();
            };
            inputElement.focus();
            inputElement.select();
        }
    }

    showPrompt(title, defaultValue, callback) {
        this.showDialog({
            title: title, showInput: true, inputDefault: defaultValue,
            confirmText: "Confirm", onConfirm: callback
        });
    }

    showAlert(title, message) {
        this.showDialog({ title: title, message: message, alertOnly: true, confirmText: "OK" });
    }

    showConfirm(title, message, onConfirm) {
        this.showDialog({ title: title, message: message, confirmText: "Confirm", onConfirm: onConfirm });
    }

    async loadProviders() {
        try {
            const res = await api.fetchApi("/llm_toolkit/providers");
            const data = await res.json();
            this.providers = data.providers || [];

            // Auto-select first if none selected
            if (!this.selectedId && this.providers.length > 0) {
                this.selectedId = this.providers[0].id;
            }
            // Ensure selectedId is still valid
            if (this.selectedId && !this.providers.find(p => p.id === this.selectedId)) {
                this.selectedId = this.providers[0]?.id || null;
            }

            this.render();
        } catch (e) {
            console.error("[LLMs_Toolkit] Failed to load providers:", e);
            this.showAlert("Error", "Failed to load provider configuration. Please check the terminal logs.");
        }
    }

    async saveProvider(providerData) {
        try {
            const res = await api.fetchApi("/llm_toolkit/providers", {
                method: "POST",
                body: JSON.stringify(providerData)
            });
            const data = await res.json();
            if (data.status === "ok") {
                await this.loadProviders();
                this.selectedId = data.provider.id;
                this.render();
            } else {
                this.showAlert("Save Failed", data.error);
            }
        } catch (e) {
            console.error(e);
            this.showAlert("Error", "Save failed.");
        }
    }

    async deleteProvider(id) {
        this.showConfirm(
            "Delete Provider",
            "Are you sure you want to delete this custom provider?\\nThis action cannot be undone.",
            async () => {
                try {
                    const res = await api.fetchApi(`/llm_toolkit/providers/${id}`, { method: "DELETE" });
                    const data = await res.json();
                    if (data.status === "ok") {
                        if (this.selectedId === id) this.selectedId = null;
                        await this.loadProviders();
                    } else {
                        this.showAlert("Delete Failed", data.error);
                    }
                } catch (e) {
                    console.error(e);
                    this.showAlert("Error", "Delete failed.");
                }
            }
        );
    }

    async checkConnectivity(apiHost, apiKey, model) {
        try {
            const btn = document.getElementById("pm-check-btn");
            if (btn) btn.textContent = "Checking...";

            const res = await api.fetchApi("/llm_toolkit/providers/check", {
                method: "POST",
                body: JSON.stringify({ apiHost, apiKey, model })
            });
            const data = await res.json();

            if (data.status === "ok") {
                this.showAlert("Success", "✅ Connection successful! API Key and Base URL are configured correctly.");
            } else {
                this.showAlert("Connection Failed", "❌ " + data.message);
            }
        } catch (e) {
            console.error(e);
            this.showAlert("Error", "❌ Request failed. Network error or CORS issue.");
        } finally {
            const btn = document.getElementById("pm-check-btn");
            if (btn) btn.textContent = "Check";
        }
    }

    show() {
        if (this.modal) {
            this.modal.style.display = "flex";
            this.loadProviders();
            return;
        }

        // Create main modal structure
        this.contentContainer = $el("div.llm-pm-content");
        this.sidebarListContainer = $el("div.llm-pm-list");

        const closeBtn = $el("span.llm-pm-close", {
            innerHTML: "&times;",
            onclick: () => {
                this.checkUnsaved(() => {
                    this.modal.style.display = "none";
                    this.currentDraft = null;
                    // Trigger full redraw of graph to apply changes
                    if (app.graph) {
                        app.graph.setDirtyCanvas(true);
                    }
                });
            }
        });

        const searchInput = $el("input", {
            type: "text",
            placeholder: "Search providers/models...",
            oninput: (e) => {
                this.searchQuery = e.target.value.toLowerCase();
                this.renderSidebar();
            }
        });

        const addBtn = $el("button.llm-pm-add-btn", {
            textContent: "+ Custom Provider",
            onclick: () => {
                this.checkUnsaved(() => this.createNewProvider());
            },
            style: { padding: "6px 16px", fontSize: "0.9em", borderRadius: "4px", minHeight: "unset" }
        });

        this.modal = $el("div.comfy-modal.llm-pm-modal", {
            parent: document.body,
            style: { display: "flex", zIndex: 10000 }
        }, [
            $el("div.llm-pm-header", [
                $el("h2.llm-pm-title", "⚙️ LLM Provider & Model Manager"),
                closeBtn
            ]),
            $el("div.llm-pm-body", [
                $el("div.llm-pm-sidebar", [
                    $el("div.llm-pm-search", [searchInput]),
                    this.sidebarListContainer,
                    $el("div.llm-pm-sidebar-footer", [addBtn])
                ]),
                this.contentContainer
            ])
        ]);

        this.loadProviders();
    }

    createNewProvider() {
        const newTempId = "temp-" + Date.now();
        const newProvider = {
            id: newTempId,
            name: "New Custom Provider",
            type: "openai",
            apiKey: "",
            apiHost: "",
            models: [],
            enabled: true,
            isSystem: false,
            _isNew: true
        };
        this.providers.push(newProvider);
        this.selectedId = newTempId;
        this.render();
        // Focus the name input automatically
        setTimeout(() => {
            const input = document.getElementById("pm-input-name");
            if (input) {
                input.focus();
                input.select();
            }
        }, 50);
    }

    render() {
        this.renderSidebar();
        this.renderContent();
    }

    renderSidebar() {
        this.sidebarListContainer.innerHTML = "";

        const filtered = this.providers.filter(p => {
            const matchesName = p.name.toLowerCase().includes(this.searchQuery);
            const matchesModel = p.models.some(m => m.toLowerCase().includes(this.searchQuery));
            return matchesName || matchesModel;
        });

        filtered.forEach(p => {
            const isActive = this.selectedId === p.id;

            const tags = [$el("span.llm-pm-tag" + (p.enabled ? ".on" : ""), p.enabled ? "ON" : "OFF")];
            if (p.isSystem) tags.unshift($el("span.llm-pm-tag", "System"));

            const item = $el("div.llm-pm-item" + (isActive ? ".active" : ""), {
                onclick: () => {
                    if (this.selectedId === p.id) return;
                    this.checkUnsaved(() => {
                        this.selectedId = p.id;
                        this.render();
                    });
                }
            }, [
                $el("span", p.name),
                $el("div.llm-pm-item-tags", tags)
            ]);

            this.sidebarListContainer.appendChild(item);
        });
    }

    renderContent() {
        this.contentContainer.innerHTML = "";

        const provider = this.providers.find(p => p.id === this.selectedId);
        if (!provider) {
            this.contentContainer.appendChild(
                $el("div.llm-pm-empty", "Select a provider from the sidebar to edit.")
            );
            return;
        }

        // Live working copy
        this.currentDraft = JSON.parse(JSON.stringify(provider));
        const draft = this.currentDraft;

        // -- Header row (Name & Enable switch)
        const nameInput = $el("input", {
            id: "pm-input-name",
            type: "text",
            value: draft.name,
            placeholder: "Provider Name",
            oninput: (e) => draft.name = e.target.value
        });

        const enableSwitch = $el("label.llm-pm-switch", [
            $el("input", {
                type: "checkbox",
                checked: draft.enabled,
                onchange: (e) => {
                    draft.enabled = e.target.checked;
                    this.saveProvider(draft); // auto save toggle
                }
            }),
            $el("span.llm-pm-slider")
        ]);

        // -- API Key
        const keyInput = $el("input", {
            type: "password",
            value: draft.apiKey,
            placeholder: "sk-...",
            oninput: (e) => draft.apiKey = e.target.value
        });

        const toggleVisibilityBtn = $el("button", {
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`,
            onclick: () => {
                if (keyInput.type === "password") {
                    keyInput.type = "text";
                    toggleVisibilityBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;
                } else {
                    keyInput.type = "password";
                    toggleVisibilityBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
                }
            },
            title: "Toggle Visibility",
            style: {
                padding: "4px 8px", fontSize: "0.85em", borderRadius: "4px", minHeight: "unset",
                display: "inline-flex", alignItems: "center", background: "transparent", color: "var(--descrip-text)", border: "1px solid var(--border-color)", cursor: "pointer"
            }
        });

        const checkBtn = $el("button", {
            id: "pm-check-btn",
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:4px"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 2l.117 .007a1 1 0 0 1 .876 .876l.007 .117v4l.005 .15a2 2 0 0 0 1.838 1.844l.157 .006h4l.117 .007a1 1 0 0 1 .876 .876l.007 .117v9a3 3 0 0 1 -2.824 2.995l-.176 .005h-10a3 3 0 0 1 -2.995 -2.824l-.005 -.176v-14a3 3 0 0 1 2.824 -2.995l.176 -.005zm3.707 10.293a1 1 0 0 0 -1.414 0l-3.293 3.292l-1.293 -1.292a1 1 0 1 0 -1.414 1.414l2 2a1 1 0 0 0 1.414 0l4 -4a1 1 0 0 0 0 -1.414m-.707 -9.294l4 4.001h-4z" /></svg> Check API`,
            onclick: () => this.checkConnectivity(draft.apiHost, draft.apiKey, draft.models[0] || ""),
            style: {
                padding: "4px 12px", fontSize: "0.85em", borderRadius: "4px", minHeight: "unset",
                display: "inline-flex", alignItems: "center"
            }
        });

        // -- URL
        const urlInput = $el("input", {
            type: "text",
            value: draft.apiHost,
            placeholder: "https://api.../v1",
            oninput: (e) => {
                draft.apiHost = e.target.value;
                const prev = document.getElementById("pm-url-preview");
                if (prev) prev.textContent = `Preview: ${draft.apiHost} /chat/completions`;
            }
        });

        // -- Models
        const modelsContainer = $el("div.llm-pm-models");
        const renderModels = () => {
            modelsContainer.innerHTML = "";
            draft.models.forEach((m, idx) => {
                const nameSpan = $el("span", {
                    textContent: m,
                    style: { cursor: "pointer" },
                    title: "Double-click to edit",
                    ondblclick: () => {
                        this.showPrompt("Edit Model Name:", m, (newName) => {
                            if (newName && newName.trim()) {
                                draft.models[idx] = newName.trim();
                                renderModels();
                            }
                        });
                    }
                });
                modelsContainer.appendChild($el("span.llm-pm-model-tag", [
                    nameSpan,
                    $el("span.llm-pm-model-del", {
                        innerHTML: "&times;",
                        title: "Delete model",
                        onclick: () => {
                            draft.models.splice(idx, 1);
                            renderModels();
                        }
                    })
                ]));
            });

            // Add button
            modelsContainer.appendChild($el("span.llm-pm-model-add", {
                textContent: "+ Add Model",
                onclick: () => {
                    this.showPrompt("Enter Model Name (e.g. gpt-4o):", "", (name) => {
                        if (name && name.trim()) {
                            draft.models.push(name.trim());
                            renderModels();
                        }
                    });
                }
            }));
        };
        renderModels();

        // -- Action Buttons
        const saveBtn = $el("button", {
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:4px"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M16 3a1 1 0 0 1 .707 .293l4 4a1 1 0 0 1 .293 .707v10a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3v-12a3 3 0 0 1 3 -3h1v4a1 1 0 0 0 .883 .993l.117 .007h6a1 1 0 0 0 1 -1v-4zm-4 8a2.995 2.995 0 0 0 -2.995 2.898a1 1 0 0 0 -.005 .102a3 3 0 1 0 3 -3m1 -8v3h-4v-3z" /></svg> Save`,
            style: {
                fontWeight: "bold", background: "#4CAF50", color: "white",
                padding: "6px 16px", fontSize: "0.9em", borderRadius: "4px", minHeight: "unset",
                display: "inline-flex", alignItems: "center", transition: "all 0.3s ease"
            },
            onclick: async () => {
                const originalHtml = saveBtn.innerHTML;
                saveBtn.innerHTML = `⏳ Saving...`;
                saveBtn.disabled = true;

                if (draft._isNew) delete draft._isNew;
                await this.saveProvider(draft);

                saveBtn.innerHTML = `✅ Saved!`;
                saveBtn.style.background = "#3d8b40"; // slightly darker green
                setTimeout(() => {
                    saveBtn.innerHTML = originalHtml;
                    saveBtn.style.background = "#4CAF50";
                    saveBtn.disabled = false;
                }, 1500);
            }
        });

        const deleteBtn = $el("button", {
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:4px"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19 2a3 3 0 0 1 3 3v14a3 3 0 0 1 -3 3h-14a3 3 0 0 1 -3 -3v-14a3 3 0 0 1 3 -3zm-4 9h-6l-.117 .007a1 1 0 0 0 .117 1.993h6l.117 -.007a1 1 0 0 0 -.117 -1.993z" /></svg> Delete`,
            style: {
                color: "var(--error-text)", borderColor: "var(--error-text)",
                padding: "6px 16px", fontSize: "0.9em", borderRadius: "4px", minHeight: "unset",
                display: "inline-flex", alignItems: "center"
            },
            onclick: () => this.deleteProvider(draft.id)
        });


        // Build DOM
        const fields = [
            $el("div.llm-pm-field", [
                $el("label", [
                    $el("span", "Provider Name" + (draft.isSystem ? " (System)" : "")),
                    $el("div", { style: { display: "flex", alignItems: "center", gap: "8px" } }, [
                        $el("span", { style: { fontSize: "0.8em", fontWeight: "normal" } }, "Enable in Nodes"),
                        enableSwitch
                    ])
                ]),
                nameInput
            ]),

            $el("div.llm-pm-field", [
                $el("label", "Base URL"),
                urlInput,
                $el("div.llm-pm-field-hint", {
                    id: "pm-url-preview",
                    textContent: `Preview: ${draft.apiHost} /chat/completions`
                })
            ]),

            $el("div.llm-pm-field", [
                $el("label", "API Key"),
                $el("div.llm-pm-input-group", [keyInput, toggleVisibilityBtn, checkBtn]),
                $el("div.llm-pm-field-hint", "Keys are stored locally in config/providers.json in plaintext.")
            ]),

            $el("div.llm-pm-field", [
                $el("label", "Available Models"),
                modelsContainer
            ]),

            $el("div.llm-pm-actions", [
                (draft.isSystem || draft._isNew) ? $el("div") : deleteBtn,
                $el("div.llm-pm-actions-right", [saveBtn])
            ])
        ];

        fields.forEach(f => this.contentContainer.appendChild(f));
    }
}

// ============================================================================
// Registration & Node Extensions
// ============================================================================
app.registerExtension({
    name: "ComfyUI.LLMsToolkit.ProviderManager",

    // UI Setup
    async setup() {
        const manager = new ProviderManager();

        try {
            const { ComfyButton } = await import("../../../scripts/ui/components/button.js");
            const { ComfyButtonGroup } = await import("../../../scripts/ui/components/buttonGroup.js");

            const llmGroup = new ComfyButtonGroup(
                new ComfyButton({
                    icon: "robot",
                    content: "LLMs_Manager",
                    tooltip: "Manage LLM API Providers & Model Config",
                    action: () => manager.show(),
                    classList: "comfyui-button comfyui-menu-mobile-collapse primary"
                }).element
            );

            app.menu?.settingsGroup.element.before(llmGroup.element);
            console.log("[LLMs_Toolkit] LLMs button injected into ComfyUI menu.");
        } catch (e) {
            console.warn("[LLMs_Toolkit] New-style menu API not available, using fallback.", e);
            const floatBtn = $el("button", {
                textContent: "LLMs_Manager",
                title: "Manage LLM API Providers & Models",
                onclick: () => manager.show(),
                style: {
                    position: "fixed",
                    top: "10px",
                    right: "300px",
                    zIndex: "9990",
                    padding: "4px 10px",
                    cursor: "pointer",
                    background: "var(--comfy-input-bg, #333)",
                    color: "var(--input-text, white)",
                    border: "1px solid var(--border-color, #666)",
                    borderRadius: "4px",
                    fontSize: "13px",
                    fontWeight: "bold"
                }
            });
            document.body.appendChild(floatBtn);
        }
    },

    // Node Interception for Dynamic Model Dropdowns
    async nodeCreated(node) {
        if (node.comfyClass === "OpenAICompatibleLoader") {
            const providerWidget = node.widgets.find(w => w.name === "provider");
            const modelWidget = node.widgets.find(w => w.name === "model");

            if (providerWidget && modelWidget) {
                // Fetch current providers to have the mapping of Provider -> Models
                let providersCache = [];
                try {
                    const res = await api.fetchApi("/llm_toolkit/providers");
                    const data = await res.json();
                    providersCache = data.providers || [];
                } catch (e) {
                    console.error("[LLMs_Toolkit] Failed to fetch providers for node", e);
                }

                const updateModelOptions = (selectedProviderLabel) => {
                    if (selectedProviderLabel === "LLM_CONFIG (from input)") {
                        modelWidget.options.values = ["LLM_CONFIG (from input)"];
                        if (modelWidget.value !== "LLM_CONFIG (from input)") {
                            modelWidget.value = "LLM_CONFIG (from input)";
                        }
                        return;
                    }

                    // Match provider by name, must be enabled
                    const found = providersCache.find(p => p.name === selectedProviderLabel && p.enabled);
                    if (found && found.models && found.models.length > 0) {
                        modelWidget.options.values = found.models;
                        if (!found.models.includes(modelWidget.value)) {
                            modelWidget.value = found.models[0];
                        }
                    } else {
                        modelWidget.options.values = ["LLM_CONFIG (from input)"];
                        modelWidget.value = "LLM_CONFIG (from input)";
                    }
                    app.graph.setDirtyCanvas(true);
                };

                // Initial setup based on current value
                if (providerWidget.value) {
                    updateModelOptions(providerWidget.value);
                }

                // Listen for changes on the provider widget
                const originalCallback = providerWidget.callback;
                providerWidget.callback = function () {
                    updateModelOptions(this.value);
                    if (originalCallback) {
                        originalCallback.apply(this, arguments);
                    }
                };
            }
        }
    }
});
