import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "LLMs_Toolkit.JSONBuilder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "JSONBuilder") {
            nodeType.prototype.onNodeCreated = function () {
                // Find inputcount widget and add button right after it
                const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                const inputCountIdx = this.widgets.indexOf(inputCountWidget);

                // Insert button after input_count widget
                const button = this.addWidget("button", "Update inputs", null, () => {
                    const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                    if (!inputCountWidget) return;

                    const target_count = inputCountWidget.value;

                    // Count current key widgets (they are in widgets, not inputs)
                    const current_keys = this.widgets.filter(w =>
                        w.name && w.name.startsWith("key_")
                    ).length;

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

                // Move button to be right after input_count
                if (inputCountIdx !== -1) {
                    const buttonIdx = this.widgets.indexOf(button);
                    if (buttonIdx !== -1 && buttonIdx !== inputCountIdx + 1) {
                        this.widgets.splice(buttonIdx, 1);
                        this.widgets.splice(inputCountIdx + 1, 0, button);
                    }
                }
            };
        }
    }
});
