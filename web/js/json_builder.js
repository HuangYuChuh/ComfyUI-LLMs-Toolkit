import { app } from "../../../scripts/app.js";

/**
 * JSON Builder Extension for ComfyUI-LLMs-Toolkit
 * 
 * Features:
 * - Dynamic key_N as TEXT WIDGETS (editable text boxes)
 * - Dynamic value_N as INPUT SLOTS (connections)
 * - Custom serialization to persist dynamic widgets
 */

app.registerExtension({
    name: "LLMs_Toolkit.JSONBuilder",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "JSONBuilder") {

            // Store original onNodeCreated if exists
            const origOnNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                if (origOnNodeCreated) {
                    origOnNodeCreated.apply(this, arguments);
                }

                // Find input_count widget
                const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                const inputCountIdx = this.widgets.indexOf(inputCountWidget);

                // Helper function to add a key widget with proper serialization
                const addKeyWidget = (node, name, defaultValue = "") => {
                    const widget = node.addWidget("text", name, defaultValue, () => { }, {});
                    // Ensure widget value is serialized
                    widget.serializeValue = () => widget.value;
                    return widget;
                };

                // Create update button
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
                        // Add new key widgets and value inputs
                        for (let i = current_keys + 1; i <= target_count; i++) {
                            addKeyWidget(this, `key_${i}`, `key${i}`);
                            this.addInput(`value_${i}`, "STRING");
                        }
                    }

                    this.setSize(this.computeSize());
                });

                // Custom button drawing
                button.draw = function (ctx, node, widget_width, y, H) {
                    const margin = 10;
                    const x = margin;
                    const w = widget_width - margin * 2;
                    const h = H;
                    const radius = 6;

                    const gradient = ctx.createLinearGradient(x, y, x, y + h);
                    gradient.addColorStop(0, "#3a6ea5");
                    gradient.addColorStop(1, "#2c5282");

                    ctx.beginPath();
                    ctx.roundRect(x, y, w, h, radius);
                    ctx.fillStyle = gradient;
                    ctx.fill();

                    ctx.strokeStyle = "#4a90d9";
                    ctx.lineWidth = 1;
                    ctx.stroke();

                    ctx.fillStyle = "#ffffff";
                    ctx.font = "bold 12px 'Segoe UI', Arial, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(this.label || "⟳ Update inputs", x + w / 2, y + h / 2);
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

            // Save dynamic widgets to node properties on serialize
            const origOnSerialize = nodeType.prototype.onSerialize;
            nodeType.prototype.onSerialize = function (o) {
                if (origOnSerialize) {
                    origOnSerialize.apply(this, arguments);
                }

                // Save key widget values
                const keyWidgets = {};
                this.widgets.forEach(w => {
                    if (w.name && w.name.startsWith("key_")) {
                        keyWidgets[w.name] = w.value;
                    }
                });
                o.keyWidgets = keyWidgets;
            };

            // Restore dynamic widgets on configure (load)
            const origOnConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function (o) {
                if (origOnConfigure) {
                    origOnConfigure.apply(this, arguments);
                }

                // Restore key widgets if saved
                if (o.keyWidgets) {
                    const input_count = this.widgets.find(w => w.name === "input_count")?.value || 2;

                    // Create missing key widgets
                    for (let i = 1; i <= input_count; i++) {
                        const name = `key_${i}`;
                        let widget = this.widgets.find(w => w.name === name);

                        if (!widget) {
                            widget = this.addWidget("text", name, o.keyWidgets[name] || `key${i}`, () => { }, {});
                            widget.serializeValue = () => widget.value;
                        } else {
                            widget.value = o.keyWidgets[name] || widget.value;
                        }

                        // Ensure value input exists
                        if (!this.inputs?.find(inp => inp.name === `value_${i}`)) {
                            this.addInput(`value_${i}`, "STRING");
                        }
                    }

                    this.setSize(this.computeSize());
                }
            };
        }
    }
});
