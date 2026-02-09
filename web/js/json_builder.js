import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "LLMs_Toolkit.JSONBuilder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "JSONBuilder") {
            nodeType.prototype.onNodeCreated = function () {
                this.addWidget("button", "Update inputs", null, () => {
                    if (!this.inputs) {
                        this.inputs = [];
                    }
                    
                    const inputcountWidget = this.widgets.find(w => w.name === "inputcount");
                    if (!inputcountWidget) return;
                    
                    const target_count = inputcountWidget.value;
                    
                    // Count current key/value input pairs
                    const current_keys = this.inputs.filter(input => 
                        input.name && input.name.startsWith("key_")
                    ).length;
                    
                    if (target_count === current_keys) return; // already correct
                    
                    if (target_count < current_keys) {
                        // Remove excess inputs (remove from end, pairs at a time)
                        const pairs_to_remove = current_keys - target_count;
                        for (let i = 0; i < pairs_to_remove; i++) {
                            // Find and remove value_N first, then key_N
                            const idx_to_remove = current_keys - i;
                            const value_input_idx = this.inputs.findIndex(
                                input => input.name === `value_${idx_to_remove}`
                            );
                            if (value_input_idx !== -1) this.removeInput(value_input_idx);
                            
                            const key_input_idx = this.inputs.findIndex(
                                input => input.name === `key_${idx_to_remove}`
                            );
                            if (key_input_idx !== -1) this.removeInput(key_input_idx);
                        }
                    } else {
                        // Add new inputs
                        for (let i = current_keys + 1; i <= target_count; i++) {
                            this.addInput(`key_${i}`, "STRING");
                            this.addInput(`value_${i}`, "STRING");
                        }
                    }
                });
            };
        }
    }
});
