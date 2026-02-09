import { app } from "../../../scripts/app.js";

/**
 * JSON Builder Extension for ComfyUI-LLMs-Toolkit
 * 
 * Dynamically adds key_N / value_N input pairs based on input_count.
 * Keys use forceInput: false (can type directly or connect)
 * Values use forceInput: true (must connect from upstream)
 */

app.registerExtension({
    name: "LLMs_Toolkit.JSONBuilder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "JSONBuilder") {
            nodeType.prototype.onNodeCreated = function () {
                // Find input_count widget
                const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                const inputCountIdx = this.widgets.indexOf(inputCountWidget);

                // Create styled update button
                const button = this.addWidget("button", "⟳ Update inputs", null, () => {
                    const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                    if (!inputCountWidget) return;

                    const target_count = inputCountWidget.value;

                    // Count current key inputs (they are in inputs now, not widgets)
                    const current_keys = this.inputs ? this.inputs.filter(input =>
                        input.name && input.name.startsWith("key_")
                    ).length : 0;

                    if (target_count === current_keys) return;

                    if (target_count < current_keys) {
                        // Remove excess inputs
                        const to_remove = current_keys - target_count;
                        for (let i = 0; i < to_remove; i++) {
                            const idx = current_keys - i;

                            // Remove value input
                            const value_idx = this.inputs.findIndex(
                                input => input.name === `value_${idx}`
                            );
                            if (value_idx !== -1) this.removeInput(value_idx);

                            // Remove key input
                            const key_idx = this.inputs.findIndex(
                                input => input.name === `key_${idx}`
                            );
                            if (key_idx !== -1) this.removeInput(key_idx);

                            // Also remove key widget if exists
                            const key_widget_idx = this.widgets.findIndex(
                                w => w.name === `key_${idx}`
                            );
                            if (key_widget_idx !== -1) {
                                this.widgets.splice(key_widget_idx, 1);
                            }
                        }
                    } else {
                        // Add new input pairs
                        for (let i = current_keys + 1; i <= target_count; i++) {
                            // Add key input
                            this.addInput(`key_${i}`, "STRING");
                            // Add value input
                            this.addInput(`value_${i}`, "STRING");
                        }
                    }

                    this.setSize(this.computeSize());
                });

                // Custom draw function for premium button styling
                button.draw = function (ctx, node, widget_width, y, H) {
                    const margin = 10;
                    const x = margin;
                    const w = widget_width - margin * 2;
                    const h = H;
                    const radius = 6;

                    // Button background with gradient
                    const gradient = ctx.createLinearGradient(x, y, x, y + h);
                    gradient.addColorStop(0, "#3a6ea5");
                    gradient.addColorStop(1, "#2c5282");

                    ctx.beginPath();
                    ctx.roundRect(x, y, w, h, radius);
                    ctx.fillStyle = gradient;
                    ctx.fill();

                    // Border
                    ctx.strokeStyle = "#4a90d9";
                    ctx.lineWidth = 1;
                    ctx.stroke();

                    // Text
                    ctx.fillStyle = "#ffffff";
                    ctx.font = "bold 12px 'Segoe UI', Arial, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(this.label || "⟳ Update inputs", x + w / 2, y + h / 2);

                    // Top highlight
                    ctx.beginPath();
                    ctx.moveTo(x + radius, y + 1);
                    ctx.lineTo(x + w - radius, y + 1);
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
                    ctx.lineWidth = 1;
                    ctx.stroke();
                };

                // Move button right after input_count
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
