import { app } from "../../../scripts/app.js";

/**
 * JSON Builder Extension for ComfyUI-LLMs-Toolkit
 * 
 * Features a premium styled "Update inputs" button with:
 * - Gradient background with hover effects
 * - Rounded corners and subtle shadow
 * - Icon indicator
 */

app.registerExtension({
    name: "LLMs_Toolkit.JSONBuilder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "JSONBuilder") {
            nodeType.prototype.onNodeCreated = function () {
                // Find inputcount widget
                const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                const inputCountIdx = this.widgets.indexOf(inputCountWidget);

                // Create custom styled button
                const button = this.addWidget("button", "⟳ Update inputs", null, () => {
                    const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                    if (!inputCountWidget) return;

                    const target_count = inputCountWidget.value;

                    // Count current key widgets
                    const current_keys = this.widgets.filter(w =>
                        w.name && w.name.startsWith("key_")
                    ).length;

                    if (target_count === current_keys) return;

                    if (target_count < current_keys) {
                        const to_remove = current_keys - target_count;
                        for (let i = 0; i < to_remove; i++) {
                            const idx = current_keys - i;

                            if (this.inputs) {
                                const value_idx = this.inputs.findIndex(
                                    input => input.name === `value_${idx}`
                                );
                                if (value_idx !== -1) this.removeInput(value_idx);
                            }

                            const key_widget_idx = this.widgets.findIndex(
                                w => w.name === `key_${idx}`
                            );
                            if (key_widget_idx !== -1) {
                                this.widgets.splice(key_widget_idx, 1);
                            }
                        }
                    } else {
                        for (let i = current_keys + 1; i <= target_count; i++) {
                            this.addWidget("text", `key_${i}`, "", () => { }, {});
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

                    // Draw button background with gradient
                    const gradient = ctx.createLinearGradient(x, y, x, y + h);
                    gradient.addColorStop(0, "#3a6ea5");  // Blue top
                    gradient.addColorStop(1, "#2c5282");  // Darker blue bottom

                    ctx.beginPath();
                    ctx.roundRect(x, y, w, h, radius);
                    ctx.fillStyle = gradient;
                    ctx.fill();

                    // Subtle border
                    ctx.strokeStyle = "#4a90d9";
                    ctx.lineWidth = 1;
                    ctx.stroke();

                    // Button text
                    ctx.fillStyle = "#ffffff";
                    ctx.font = "bold 12px 'Segoe UI', Arial, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(this.label || "⟳ Update inputs", x + w / 2, y + h / 2);

                    // Subtle highlight on top edge
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
