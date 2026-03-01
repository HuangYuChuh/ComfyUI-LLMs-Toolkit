import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI-LLMs-Toolkit.displayTokens",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "OpenAICompatibleLoader") return;

        // Remove any old logic regarding widget creation.
        // We will directly draw the token usage on the right side of the node onto the canvas.

        const onDrawForeground = nodeType.prototype.onDrawForeground;
        nodeType.prototype.onDrawForeground = function (ctx) {
            onDrawForeground?.apply(this, arguments);

            if (this._llm_token_usage) {
                ctx.save();
                ctx.font = "12px sans-serif";
                ctx.fillStyle = "rgba(160, 160, 160, 0.9)";
                ctx.textAlign = "right";

                // Draw completely below the node to avoid overlapping with bottom widgets
                const lines = this._llm_token_usage;
                let drawY = this.size[1] + 16;

                for (let i = 0; i < lines.length; i++) {
                    ctx.fillText(lines[i], this.size[0] - 10, drawY + (i * 16));
                }
                ctx.restore();
            }
        };

        // Handle execution result from backend
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);

            // Clean up any legacy token widgets from older savings
            const oldWidgetIdx = this.widgets?.findIndex(w => w.name === "token_usage_display");
            if (oldWidgetIdx >= 0) {
                this.widgets.splice(oldWidgetIdx, 1);
            }

            if (message?.text && message.text.length > 0) {
                const text = Array.isArray(message.text) ? message.text.join("\n") : message.text;
                this._llm_token_usage = text.split("\n");

                // Request a redraw
                app.graph.setDirtyCanvas(true, false);
            }
        };
    },
});
