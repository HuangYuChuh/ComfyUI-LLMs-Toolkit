import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI-LLMs-Toolkit.displayTokens",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name !== "OpenAICompatibleLoader") return;

        const WIDGET_NAME = "token_usage_display";

        function updateTokenDisplay(text) {
            // Find or create the display widget (append-only, never clear existing widgets)
            let tokenWidget = this.widgets?.find(w => w.name === WIDGET_NAME);

            if (!tokenWidget) {
                try {
                    const w = ComfyWidgets["STRING"](
                        this,
                        WIDGET_NAME,
                        ["STRING", { multiline: true }],
                        app
                    ).widget;
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.7;
                    w.inputEl.style.fontSize = "11px";
                    w.inputEl.style.fontFamily = "monospace";
                    // THIS IS ESSENTIAL: Prevent the widget from being saved to the workflow JSON
                    // which causes standard fields (like seed, max_tokens) to shift indices!
                    w.serialize = false;
                    w.computeSize = () => [0, -4]; // Optional: compress its virtual size slightly
                    tokenWidget = w;
                } catch (error) {
                    console.error("[LLMs_Toolkit] Failed to create token display widget:", error);
                    return;
                }
            }

            // Update value
            const displayText = Array.isArray(text) ? text.join("\n") : text;
            tokenWidget.value = displayText;

            // Resize node to fit the new content
            requestAnimationFrame(() => {
                const sz = this.computeSize();
                if (sz[0] < this.size[0]) sz[0] = this.size[0];
                if (sz[1] < this.size[1]) sz[1] = this.size[1];
                this.onResize?.(sz);
                app.graph.setDirtyCanvas(true, false);
            });
        }

        // Handle execution result from backend
        const onExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            onExecuted?.apply(this, arguments);
            if (message?.text?.length > 0) {
                updateTokenDisplay.call(this, message.text);
            }
        };
    },
});
