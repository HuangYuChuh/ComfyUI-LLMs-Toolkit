import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "LLMs_Toolkit.JSONBuilder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "JSONBuilder") {
            nodeType.prototype.onNodeCreated = function () {
                this.addWidget("button", "Update inputs", null, () => {
                    const inputcountWidget = this.widgets.find(w => w.name === "inputcount");
                    if (!inputcountWidget) return;

                    const target_count = inputcountWidget.value;

                    // Count current key widgets (they are in widgets, not inputs)
                    const current_keys = this.widgets.filter(w =>
                        w.name && w.name.startsWith("key_")
                    ).length;

                    // Count current value inputs
                    const current_values = this.inputs ? this.inputs.filter(input =>
                        input.name && input.name.startsWith("value_")
                    ).length : 0;

                    if (target_count === current_keys) return; // already correct

                    if (target_count < current_keys) {
                        // Remove excess widgets and inputs
                        const to_remove = current_keys - target_count;
                        for (let i = 0; i < to_remove; i++) {
                            const idx = current_keys - i;

                            // Remove value input
                            if (this.inputs) {
                                const value_idx = this.inputs.findIndex(
                                    input => input.name === `value_${idx}`
                                );
                                if (value_idx !== -1) this.removeInput(value_idx);
                            }

                            // Remove key widget
                            const key_widget_idx = this.widgets.findIndex(
                                w => w.name === `key_${idx}`
                            );
                            if (key_widget_idx !== -1) {
                                this.widgets.splice(key_widget_idx, 1);
                            }
                        }
                    } else {
                        // Add new widgets and inputs
                        for (let i = current_keys + 1; i <= target_count; i++) {
                            // Add key as editable text widget
                            this.addWidget("text", `key_${i}`, "", () => { }, {});
                            // Add value as input slot
                            this.addInput(`value_${i}`, "STRING");
                        }
                    }

                    // Resize node to fit new widgets
                    this.setSize(this.computeSize());
                });
            };
        }
    }
});
