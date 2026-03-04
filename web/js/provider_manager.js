import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";
import { $el } from "../../../scripts/ui.js";

// ============================================================================
// CSS Styles Loader
// ============================================================================
$el("link", {
    parent: document.head,
    rel: "stylesheet",
    type: "text/css",
    href: "extensions/ComfyUI-LLMs-Toolkit/css/provider_manager.css"
});


// ============================================================================
// i18n System
// ============================================================================
const I18N_DICT = {
    en: {
        manager_title: "LLMs Toolkit Manager",
        unsaved_title: "Unsaved Changes",
        unsaved_msg: "You have unsaved changes.\nAre you sure you want to discard them?",
        cancel: "Cancel",
        ok: "OK",
        confirm: "Confirm",
        error: "Error",
        load_error: "Failed to load provider configuration. Please check the terminal logs.",
        save_failed: "Save Failed",
        save_err: "Save failed.",
        delete_title: "Delete Provider",
        delete_msg: "Are you sure you want to delete this custom provider?\nThis action cannot be undone.",
        delete_failed: "Delete Failed",
        delete_err: "Delete failed.",
        checking: "Checking...",
        connected: "Connected!",
        failed: "Failed",
        conn_failed: "Connection Failed",
        network_err_title: "⚠️ Network Error",
        network_err_msg: "❌ Request failed. Network error or CORS issue.",
        search_placeholder: "Search providers/models...",
        add_custom: "+ Custom Provider",
        usage_stats: "Usage Stats",
        new_custom: "New Custom Provider",
        on: "ON",
        off: "OFF",
        usage_loading: "Loading usage history...",
        usage_api_404: "Usage API not available. Please restart ComfyUI to activate the new route.",
        usage_api_err: "API error: HTTP ",
        usage_dashboard: "API Usage Dashboard",
        usage_empty: "No usage data recorded yet. Run a generation first.",
        total_calls: "Total Calls",
        success_error: "Success / Error",
        total_tokens: "Total Tokens",
        avg_latency: "Avg Latency",
        status: "Status",
        time: "Time",
        provider: "Provider",
        model: "Model",
        tokens_in_out: "Tokens (In/Out)",
        latency: "Latency",
        usage_load_err: "Failed to load usage data. Check logs.",
        select_edit: "Select a provider from the sidebar to edit.",
        provider_name: "Provider Name",
        enable_nodes: "Enable in Nodes",
        base_url: "Base URL",
        api_key: "API Key",
        keys_hint: "Keys are stored locally in config/providers.json in plaintext.",
        avail_models: "Available Models",
        add_model: "+ Add Model",
        del_model: "Delete model",
        db_edit: "Double-click to edit",
        edit_model_name: "Edit Model Name:",
        enter_model_name: "Enter Model Name (e.g. gpt-4o):",
        save: "Save",
        saving: "⏳ Saving...",
        saved: "✅ Saved!",
        delete: "Delete",
        preview: "Preview: ",
        lang_switch: "中",
        menu_button: "LLM Manager",
        menu_tooltip: "Manage LLM API Providers & Model Config"
    },
    zh: {
        manager_title: "LLMs 模型管家",
        unsaved_title: "未保存更改",
        unsaved_msg: "你有未保存的更改。\\n确定要放弃它们吗？",
        cancel: "取消",
        ok: "好的",
        confirm: "确认",
        error: "错误",
        load_error: "加载配置失败，请检查终端日志。",
        save_failed: "保存失败",
        save_err: "保存配置失败。",
        delete_title: "删除供应商",
        delete_msg: "确定要删除这个自定义供应商吗？\\n此操作无法撤销。",
        delete_failed: "删除失败",
        delete_err: "删除供应商失败。",
        checking: "检测中...",
        connected: "连通成功！",
        failed: "连接失败",
        conn_failed: "连接失败",
        network_err_title: "⚠️ 网络错误",
        network_err_msg: "❌ 请求失败。网络错误或存在跨域(CORS)限制。",
        search_placeholder: "搜索 供应商/模型...",
        add_custom: "+ 自定义模型库",
        usage_stats: "用量统计",
        new_custom: "新建供应商",
        on: "启用",
        off: "禁用",
        usage_loading: "正在加载用量历史...",
        usage_api_404: "未找到用量 API。请重启 ComfyUI 以使新路由生效。",
        usage_api_err: "API 错误: HTTP ",
        usage_dashboard: "API 用量仪表盘",
        usage_empty: "暂无用量记录。请先运行一次生成。",
        total_calls: "总调用次数",
        success_error: "成功 / 失败",
        total_tokens: "消耗总 Token",
        avg_latency: "平均延迟",
        status: "状态",
        time: "时间",
        provider: "供应商",
        model: "模型",
        tokens_in_out: "Tokens (入/出)",
        latency: "延迟",
        usage_load_err: "加载用量数据失败，请检查日志。",
        select_edit: "请从左侧选择一个供应商进行编辑。",
        provider_name: "供应商名称",
        enable_nodes: "在节点中启用",
        base_url: "接口地址 (Base URL)",
        api_key: "访问密钥 (API Key)",
        keys_hint: "注意: Key 以明文形式保存在插件的 config/providers.json 中。",
        avail_models: "可用模型",
        add_model: "+ 添加模型",
        del_model: "删除模型",
        db_edit: "双击以编辑",
        edit_model_name: "编辑模型名称:",
        enter_model_name: "输入模型名称 (如 gpt-4o):",
        save: "保存",
        saving: "⏳ 保存中...",
        saved: "✅ 已保存！",
        delete: "删除",
        preview: "预览: ",
        lang_switch: "EN",
        menu_button: "LLM 模型管家",
        menu_tooltip: "管理 LLM API 供应商与模型配置"
    }
};

function getLang() {
    return localStorage.getItem("llm_pm_lang") || "zh";
}

function t(key) {
    const lang = getLang();
    return I18N_DICT[lang]?.[key] || I18N_DICT["en"][key] || key;
}

// ============================================================================
// UI Component
// ============================================================================
// ─── Provider Specific SVG Icons ─────────────────────────────────────────────

const PROVIDER_ICONS = {
    "qwen": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Qwen</title><path d="M12.604 1.34c.393.69.784 1.382 1.174 2.075a.18.18 0 00.157.091h5.552c.174 0 .322.11.446.327l1.454 2.57c.19.337.24.478.024.837-.26.43-.513.864-.76 1.3l-.367.658c-.106.196-.223.28-.04.512l2.652 4.637c.172.301.111.494-.043.77-.437.785-.882 1.564-1.335 2.34-.159.272-.352.375-.68.37-.777-.016-1.552-.01-2.327.016a.099.099 0 00-.081.05 575.097 575.097 0 01-2.705 4.74c-.169.293-.38.363-.725.364-.997.003-2.002.004-3.017.002a.537.537 0 01-.465-.271l-1.335-2.323a.09.09 0 00-.083-.049H4.982c-.285.03-.553-.001-.805-.092l-1.603-2.77a.543.543 0 01-.002-.54l1.207-2.12a.198.198 0 000-.197 550.951 550.951 0 01-1.875-3.272l-.79-1.395c-.16-.31-.173-.496.095-.965.465-.813.927-1.625 1.387-2.436.132-.234.304-.334.584-.335a338.3 338.3 0 012.589-.001.124.124 0 00.107-.063l2.806-4.895a.488.488 0 01.422-.246c.524-.001 1.053 0 1.583-.006L11.704 1c.341-.003.724.032.9.34zm-3.432.403a.06.06 0 00-.052.03L6.254 6.788a.157.157 0 01-.135.078H3.253c-.056 0-.07.025-.041.074l5.81 10.156c.025.042.013.062-.034.063l-2.795.015a.218.218 0 00-.2.116l-1.32 2.31c-.044.078-.021.118.068.118l5.716.008c.046 0 .08.02.104.061l1.403 2.454c.046.081.092.082.139 0l5.006-8.76.783-1.382a.055.055 0 01.096 0l1.424 2.53a.122.122 0 00.107.062l2.763-.02a.04.04 0 00.035-.02.041.041 0 000-.04l-2.9-5.086a.108.108 0 010-.113l.293-.507 1.12-1.977c.024-.041.012-.062-.035-.062H9.2c-.059 0-.073-.026-.043-.077l1.434-2.505a.107.107 0 000-.114L9.225 1.774a.06.06 0 00-.053-.031zm6.29 8.02c.046 0 .058.02.034.06l-.832 1.465-2.613 4.585a.056.056 0 01-.05.029.058.058 0 01-.05-.029L8.498 9.841c-.02-.034-.01-.052.028-.054l.216-.012 6.722-.012z" fill="url(#lobe-icons-qwen-fill)" fill-rule="nonzero"></path><defs><linearGradient id="lobe-icons-qwen-fill" x1="0%" x2="100%" y1="0%" y2="0%"><stop offset="0%" stop-color="#6336E7" stop-opacity=".84"></stop><stop offset="100%" stop-color="#6F69F7" stop-opacity=".84"></stop></linearGradient></defs></svg>`,
    "deepseek": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>DeepSeek</title><path d="M23.748 4.482c-.254-.124-.364.113-.512.234-.051.039-.094.09-.137.136-.372.397-.806.657-1.373.626-.829-.046-1.537.214-2.163.848-.133-.782-.575-1.248-1.247-1.548-.352-.156-.708-.311-.955-.65-.172-.241-.219-.51-.305-.774-.055-.16-.11-.323-.293-.35-.2-.031-.278.136-.356.276-.313.572-.434 1.202-.422 1.84.027 1.436.633 2.58 1.838 3.393.137.093.172.187.129.323-.082.28-.18.552-.266.833-.055.179-.137.217-.329.14a5.526 5.526 0 01-1.736-1.18c-.857-.828-1.631-1.742-2.597-2.458a11.365 11.365 0 00-.689-.471c-.985-.957.13-1.743.388-1.836.27-.098.093-.432-.779-.428-.872.004-1.67.295-2.687.684a3.055 3.055 0 01-.465.137 9.597 9.597 0 00-2.883-.102c-1.885.21-3.39 1.102-4.497 2.623C.082 8.606-.231 10.684.152 12.85c.403 2.284 1.569 4.175 3.36 5.653 1.858 1.533 3.997 2.284 6.438 2.14 1.482-.085 3.133-.284 4.994-1.86.47.234.962.327 1.78.397.63.059 1.236-.03 1.705-.128.735-.156.684-.837.419-.961-2.155-1.004-1.682-.595-2.113-.926 1.096-1.296 2.746-2.642 3.392-7.003.05-.347.007-.565 0-.845-.004-.17.035-.237.23-.256a4.173 4.173 0 001.545-.475c1.396-.763 1.96-2.015 2.093-3.517.02-.23-.004-.467-.247-.588zM11.581 18c-2.089-1.642-3.102-2.183-3.52-2.16-.392.024-.321.471-.235.763.09.288.207.486.371.739.114.167.192.416-.113.603-.673.416-1.842-.14-1.897-.167-1.361-.802-2.5-1.86-3.301-3.307-.774-1.393-1.224-2.887-1.298-4.482-.02-.386.093-.522.477-.592a4.696 4.696 0 011.529-.039c2.132.312 3.946 1.265 5.468 2.774.868.86 1.525 1.887 2.202 2.891.72 1.066 1.494 2.082 2.48 2.914.348.292.625.514.891.677-.802.09-2.14.11-3.054-.614zm1-6.44a.306.306 0 01.415-.287.302.302 0 01.2.288.306.306 0 01-.31.307.303.303 0 01-.304-.308zm3.11 1.596c-.2.081-.399.151-.59.16a1.245 1.245 0 01-.798-.254c-.274-.23-.47-.358-.552-.758a1.73 1.73 0 01.016-.588c.07-.327-.008-.537-.239-.727-.187-.156-.426-.199-.688-.199a.559.559 0 01-.254-.078c-.11-.054-.2-.19-.114-.358.028-.054.16-.186.192-.21.356-.202.767-.136 1.146.016.352.144.618.408 1.001.782.391.451.462.576.685.914.176.265.336.537.445.848.067.195-.019.354-.25.452z" fill="#4D6BFE"></path></svg>`,
    "doubao": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Doubao</title><path d="M5.31 15.756c.172-3.75 1.883-5.999 2.549-6.739-3.26 2.058-5.425 5.658-6.358 8.308v1.12C1.501 21.513 4.226 24 7.59 24a6.59 6.59 0 002.2-.375c.353-.12.7-.248 1.039-.378.913-.899 1.65-1.91 2.243-2.992-4.877 2.431-7.974.072-7.763-4.5l.002.001z" fill="#1E37FC"></path><path d="M22.57 10.283c-1.212-.901-4.109-2.404-7.397-2.8.295 3.792.093 8.766-2.1 12.773a12.782 12.782 0 01-2.244 2.992c3.764-1.448 6.746-3.457 8.596-5.219 2.82-2.683 3.353-5.178 3.361-6.66a2.737 2.737 0 00-.216-1.084v-.002z" fill="#37E1BE"></path><path d="M14.303 1.867C12.955.7 11.248 0 9.39 0 7.532 0 5.883.677 4.545 1.807 2.791 3.29 1.627 5.557 1.5 8.125v9.201c.932-2.65 3.097-6.25 6.357-8.307.5-.318 1.025-.595 1.569-.829 1.883-.801 3.878-.932 5.746-.706-.222-2.83-.718-5.002-.87-5.617h.001z" fill="#A569FF"></path><path d="M17.305 4.961a199.47 199.47 0 01-1.08-1.094c-.202-.213-.398-.419-.586-.622l-1.333-1.378c.151.615.648 2.786.869 5.617 3.288.395 6.185 1.898 7.396 2.8-1.306-1.275-3.475-3.487-5.266-5.323z" fill="#1E37FC"></path></svg>`,
    "spark": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Spark</title><path d="M2 13.08C2 9.182 4.772 6.367 9.32 2.122c-.65 7.883 6.41 8.272 5.023 12.214-.99 2.815-4.244 1.949-4.59 1.342 0 0 1.212.347 1.385-.866.174-1.213-2.252-1.862-3.81-4.937-2.6 2.988-.954 9.008 4.2 9.008 4.764 0 6.583-4.937 4.894-8.099 0 0 4.071.693 4.418 3.811.346 3.119-3.638 8.533-9.095 8.403C6.288 22.868 2 18.84 2 13.08z" fill="#3DC8F9"></path><path d="M17.852 6.107L11.615 0c-.52 5.933.866 8.374 4.894 9.485 2.729.753 3.307 1.04 4.504 2.772-.338-2.407-.78-3.812-3.161-6.15z" fill="#EA0100"></path><path clip-rule="evenodd" d="M9.033 18.323c.709.354 1.542.56 2.495.56 4.764 0 6.583-4.937 4.894-8.099 0 0 4.071.693 4.418 3.811.156 1.403-.565 3.27-1.902 4.89-3.458 1.57-7.29.84-9.905-1.162z" fill="#1652D8" fill-rule="evenodd"></path></svg>`,
    "glm": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Zhipu</title><path d="M11.991 23.503a.24.24 0 00-.244.248.24.24 0 00.244.249.24.24 0 00.245-.249.24.24 0 00-.22-.247l-.025-.001zM9.671 5.365a1.697 1.697 0 011.099 2.132l-.071.172-.016.04-.018.054c-.07.16-.104.32-.104.498-.035.71.47 1.279 1.186 1.314h.366c1.309.053 2.338 1.173 2.286 2.523-.052 1.332-1.152 2.38-2.478 2.327h-.174c-.715.018-1.274.64-1.239 1.368 0 .124.018.23.053.337.209.373.54.658.96.8.75.23 1.517-.125 1.9-.782l.018-.035c.402-.64 1.17-.96 1.92-.711.854.284 1.378 1.226 1.099 2.167a1.661 1.661 0 01-2.077 1.102 1.711 1.711 0 01-.907-.711l-.017-.035c-.2-.323-.463-.58-.851-.711l-.056-.018a1.646 1.646 0 00-1.954.746 1.66 1.66 0 01-1.065.764 1.677 1.677 0 01-1.989-1.279c-.209-.906.332-1.83 1.257-2.043a1.51 1.51 0 01.296-.035h.018c.68-.071 1.151-.622 1.116-1.333a1.307 1.307 0 00-.227-.693 2.515 2.515 0 01-.366-1.403 2.39 2.39 0 01.366-1.208c.14-.195.21-.444.227-.693.018-.71-.506-1.261-1.186-1.332l-.07-.018a1.43 1.43 0 01-.299-.07l-.05-.019a1.7 1.7 0 01-1.047-2.114 1.68 1.68 0 012.094-1.101zm-5.575 10.11c.26-.264.639-.367.994-.27.355.096.633.379.728.74.095.362-.007.748-.267 1.013-.402.41-1.053.41-1.455 0a1.062 1.062 0 010-1.482zm14.845-.294c.359-.09.738.024.992.297.254.274.344.665.237 1.025-.107.36-.396.634-.756.718-.551.128-1.1-.22-1.23-.781a1.05 1.05 0 01.757-1.26zm-.064-4.39c.314.32.49.753.49 1.206 0 .452-.176.886-.49 1.206-.315.32-.74.5-1.185.5-.444 0-.87-.18-1.184-.5a1.727 1.727 0 010-2.412 1.654 1.654 0 012.369 0zm-11.243.163c.364.484.447 1.128.218 1.691a1.665 1.665 0 01-2.188.923c-.855-.36-1.26-1.358-.907-2.228a1.68 1.68 0 011.33-1.038c.593-.08 1.183.169 1.547.652zm11.545-4.221c.368 0 .708.2.892.524.184.324.184.724 0 1.048a1.026 1.026 0 01-.892.524c-.568 0-1.03-.47-1.03-1.048 0-.579.462-1.048 1.03-1.048zm-14.358 0c.368 0 .707.2.891.524.184.324.184.724 0 1.048a1.026 1.026 0 01-.891.524c-.569 0-1.03-.47-1.03-1.048 0-.579.461-1.048 1.03-1.048zm10.031-1.475c.925 0 1.675.764 1.675 1.706s-.75 1.705-1.675 1.705-1.674-.763-1.674-1.705c0-.942.75-1.706 1.674-1.706zm-2.626-.684c.362-.082.653-.356.761-.718a1.062 1.062 0 00-.238-1.028 1.017 1.017 0 00-.996-.294c-.547.14-.881.7-.752 1.257.13.558.675.907 1.225.783zm0 16.876c.359-.087.644-.36.75-.72a1.062 1.062 0 00-.237-1.019 1.018 1.018 0 00-.985-.301 1.037 1.037 0 00-.762.717c-.108.361-.017.754.239 1.028.245.263.606.377.953.305l.043-.01zM17.19 3.5a.631.631 0 00.628-.64c0-.355-.279-.64-.628-.64a.631.631 0 00-.628.64c0 .355.28.64.628.64zm-10.38 0a.631.631 0 00.628-.64c0-.355-.28-.64-.628-.64a.631.631 0 00-.628.64c0 .355.279.64.628.64zm-5.182 7.852a.631.631 0 00-.628.64c0 .354.28.639.628.639a.63.63 0 00.627-.606l.001-.034a.62.62 0 00-.628-.64zm5.182 9.13a.631.631 0 00-.628.64c0 .355.279.64.628.64a.631.631 0 00.628-.64c0-.355-.28-.64-.628-.64zm10.38.018a.631.631 0 00-.628.64c0 .355.28.64.628.64a.631.631 0 00.628-.64c0-.355-.279-.64-.628-.64zm5.182-9.148a.631.631 0 00-.628.64c0 .354.279.639.628.639a.631.631 0 00.628-.64c0-.355-.28-.64-.628-.64zm-.384-4.992a.24.24 0 00.244-.249.24.24 0 00-.244-.249.24.24 0 00-.244.249c0 .142.122.249.244.249zM11.991.497a.24.24 0 00.245-.248A.24.24 0 0011.99 0a.24.24 0 00-.244.249c0 .133.108.236.223.247l.021.001zM2.011 6.36a.24.24 0 00.245-.249.24.24 0 00-.244-.249.24.24 0 00-.244.249.24.24 0 00.244.249zm0 11.263a.24.24 0 00-.243.248.24.24 0 00.244.249.24.24 0 00.244-.249.252.252 0 00-.244-.248zm19.995-.018a.24.24 0 00-.245.248.24.24 0 00.245.25.24.24 0 00.244-.25.252.252 0 00-.244-.248z" fill="#3859FF" fill-rule="nonzero"></path></svg>`,
    "moonshot": `<svg fill="currentColor" fill-rule="evenodd" height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>MoonshotAI</title><path d="M1.052 16.916l9.539 2.552a21.007 21.007 0 00.06 2.033l5.956 1.593a11.997 11.997 0 01-5.586.865l-.18-.016-.044-.004-.084-.009-.094-.01a11.605 11.605 0 01-.157-.02l-.107-.014-.11-.016a11.962 11.962 0 01-.32-.051l-.042-.008-.075-.013-.107-.02-.07-.015-.093-.019-.075-.016-.095-.02-.097-.023-.094-.022-.068-.017-.088-.022-.09-.024-.095-.025-.082-.023-.109-.03-.062-.02-.084-.025-.093-.028-.105-.034-.058-.019-.08-.026-.09-.031-.066-.024a6.293 6.293 0 01-.044-.015l-.068-.025-.101-.037-.057-.022-.08-.03-.087-.035-.088-.035-.079-.032-.095-.04-.063-.028-.063-.027a5.655 5.655 0 01-.041-.018l-.066-.03-.103-.047-.052-.024-.096-.046-.062-.03-.084-.04-.086-.044-.093-.047-.052-.027-.103-.055-.057-.03-.058-.032a6.49 6.49 0 01-.046-.026l-.094-.053-.06-.034-.051-.03-.072-.041-.082-.05-.093-.056-.052-.032-.084-.053-.061-.039-.079-.05-.07-.047-.053-.035a7.785 7.785 0 01-.054-.036l-.044-.03-.044-.03a6.066 6.066 0 01-.04-.028l-.057-.04-.076-.054-.069-.05-.074-.054-.056-.042-.076-.057-.076-.059-.086-.067-.045-.035-.064-.052-.074-.06-.089-.073-.046-.039-.046-.039a7.516 7.516 0 01-.043-.037l-.045-.04-.061-.053-.07-.062-.068-.06-.062-.058-.067-.062-.053-.05-.088-.084a13.28 13.28 0 01-.099-.097l-.029-.028-.041-.042-.069-.07-.05-.051-.05-.053a6.457 6.457 0 01-.168-.179l-.08-.088-.062-.07-.071-.08-.042-.049-.053-.062-.058-.068-.046-.056a7.175 7.175 0 01-.027-.033l-.045-.055-.066-.082-.041-.052-.05-.064-.02-.025a11.99 11.99 0 01-1.44-2.402zm-1.02-5.794l11.353 3.037a20.468 20.468 0 00-.469 2.011l10.817 2.894a12.076 12.076 0 01-1.845 2.005L.657 15.923l-.016-.046-.035-.104a11.965 11.965 0 01-.05-.153l-.007-.023a11.896 11.896 0 01-.207-.741l-.03-.126-.018-.08-.021-.097-.018-.081-.018-.09-.017-.084-.018-.094c-.026-.141-.05-.283-.071-.426l-.017-.118-.011-.083-.013-.102a12.01 12.01 0 01-.019-.161l-.005-.047a12.12 12.12 0 01-.034-2.145zm1.593-5.15l11.948 3.196c-.368.605-.705 1.231-1.01 1.875l11.295 3.022c-.142.82-.368 1.612-.668 2.365l-11.55-3.09L.124 10.26l.015-.1.008-.049.01-.067.015-.087.018-.098c.026-.148.056-.295.088-.442l.028-.124.02-.085.024-.097c.022-.09.045-.18.07-.268l.028-.102.023-.083.03-.1.025-.082.03-.096.026-.082.031-.095a11.896 11.896 0 011.01-2.232zm4.442-4.4L17.352 4.59a20.77 20.77 0 00-1.688 1.721l7.823 2.093c.267.852.442 1.744.513 2.665L2.106 5.213l.045-.065.027-.04.04-.055.046-.065.055-.076.054-.072.064-.086.05-.065.057-.073.055-.07.06-.074.055-.069.065-.077.054-.066.066-.077.053-.06.072-.082.053-.06.067-.074.054-.058.073-.078.058-.06.063-.067.168-.17.1-.098.059-.056.076-.071a12.084 12.084 0 012.272-1.677zM12.017 0h.097l.082.001.069.001.054.002.068.002.046.001.076.003.047.002.06.003.054.002.087.005.105.007.144.011.088.007.044.004.077.008.082.008.047.005.102.012.05.006.108.014.081.01.042.006.065.01.207.032.07.012.065.011.14.026.092.018.11.022.046.01.075.016.041.01L14.7.3l.042.01.065.015.049.012.071.017.096.024.112.03.113.03.113.032.05.015.07.02.078.024.073.023.05.016.05.016.076.025.099.033.102.036.048.017.064.023.093.034.11.041.116.045.1.04.047.02.06.024.041.018.063.026.04.018.057.025.11.048.1.046.074.035.075.036.06.028.092.046.091.045.102.052.053.028.049.026.046.024.06.033.041.022.052.029.088.05.106.06.087.051.057.034.053.032.096.059.088.055.098.062.036.024.064.041.084.056.04.027.062.042.062.043.023.017c.054.037.108.075.161.114l.083.06.065.048.056.043.086.065.082.064.04.03.05.041.086.069.079.065.085.071c.712.6 1.353 1.283 1.909 2.031L7.222.994l.062-.027.065-.028.081-.034.086-.035c.113-.045.227-.09.341-.131l.096-.035.093-.033.084-.03.096-.031c.087-.03.176-.058.264-.085l.091-.027.086-.025.102-.03.085-.023.1-.026L9.04.37l.09-.023.091-.022.095-.022.09-.02.098-.021.091-.02.095-.018.092-.018.1-.018.091-.016.098-.017.092-.014.097-.015.092-.013.102-.013.091-.012.105-.012.09-.01.105-.01c.093-.01.186-.018.28-.024l.106-.008.09-.005.11-.006.093-.004.1-.004.097-.002.099-.002.197-.002z"></path></svg>`,
    "stepfun": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Stepfun</title><path d="M22.012 0h1.032v.927H24v.968h-.956V3.78h-1.032V1.896h-1.878v-.97h1.878V0zM2.6 12.371V1.87h.969v10.502h-.97zm10.423.66h10.95v.918h-6.208v9.579h-4.742V13.03zM5.629 3.333v12.356H0v4.51h10.386V8L20.859 8l-.003-4.668-15.227.001z" fill="url(#lobe-icons-stepfun-fill)" fill-rule="evenodd"></path><defs><linearGradient gradientUnits="userSpaceOnUse" id="lobe-icons-stepfun-fill" x1="1.646" x2="18.342" y1="1.916" y2="22.091"><stop stop-color="#01A9FF"></stop><stop offset="1" stop-color="#0160FF"></stop></linearGradient></defs></svg>`,
    "sensechat": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>SenseNova</title><path d="M23 8.333h-7.333v7.334H23V8.333z" fill="#06FDB7"></path><path d="M1 1v14.667h7.333V8.333h7.334V1H1z" fill="#5B2AD8"></path><path d="M14.038 4.333h.17l1.459 1.456v.17l-1.63-1.626zM13.224 4.333h.17l2.273 2.268v.17l-2.443-2.438zM12.41 4.333h.17l3.087 3.08v.17l-3.257-3.25zM11.596 4.333h.17l3.9 3.892v.108h-.06l-4.01-4zM10.782 4.333h.17l4.01 4h-.17l-4.01-4zM9.968 4.333h.17l4.009 4h-.17l-4.01-4zM9.154 4.333h.17l4.009 4h-.17l-4.01-4zM8.34 4.333h.17l4.01 4h-.17l-4.01-4zM7.521 4.333h.17l4.01 4h-.17l-4.01-4zM6.707 4.333h.17l4.01 4h-.17l-4.01-4zM5.892 4.333h.17l4.009 4h-.17l-4.01-4zM5.077 4.333h.17l4.01 4h-.17l-4.01-4zM4.333 4.403v-.07h.1 l4.01 4h-.11v.06l-4-3.99zM4.333 5.215v-.17l4 3.991v.17l-4-3.99zM4.333 6.027v-.17l4 3.991v.17l-4-3.99zM4.333 6.84v-.17l4 3.99v.17l-4-3.99zM4.333 7.652v-.17l4 3.99v.17l-4-3.99zM4.333 8.464v-.17l4 3.99v.17l-4-3.99zM4.333 9.276v-.17l4 3.991v.17l-4-3.991zM4.333 10.088v-.17l4 3.991v.17l-4-3.991zM4.333 10.9v-.17l4 3.991v.17l-4-3.991zM4.333 11.712v-.17l4 3.991v.134h-.036l-3.964-3.955zM4.333 12.526v-.17l3.318 3.31h-.17l-3.148-3.14zM4.333 13.34v-.169l2.502 2.496h-.17L4.333 13.34zM4.333 14.152v-.169l1.688 1.684h-.17l-1.518-1.514zM4.333 14.965v-.17l.874.872h-.17l-.704-.702zM15.667 5.146l-.815-.813h.17l.645.644v.169z" fill="#06FDB7"></path><path d="M23 15.667h-7.333V23H23v-7.333z" fill="#5B2AD8"></path><path d="M15.667 15.667H8.333V23h7.334v-7.333z" fill="#06FDB7"></path></svg>`,
    "minimax": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Minimax</title><defs><linearGradient id="lobe-icons-minimax-fill" x1="0%" x2="100.182%" y1="50.057%" y2="50.057%"><stop offset="0%" stop-color="#E2167E"></stop><stop offset="100%" stop-color="#FE603C"></stop></linearGradient></defs><path d="M16.278 2c1.156 0 2.093.927 2.093 2.07v12.501a.74.74 0 00.744.709.74.74 0 00.743-.709V9.099a2.06 2.06 0 012.071-2.049A2.06 2.06 0 0124 9.1v6.561a.649.649 0 01-.652.645.649.649 0 01-.653-.645V9.1a.762.762 0 00-.766-.758.762.762 0 00-.766.758v7.472a2.037 2.037 0 01-2.048 2.026 2.037 2.037 0 01-2.048-2.026v-12.5a.785.785 0 00-.788-.753.785.785 0 00-.789.752l-.001 15.904A2.037 2.037 0 0113.441 22a2.037 2.037 0 01-2.048-2.026V18.04c0-.356.292-.645.652-.645.36 0 .652.289.652.645v1.934c0 .263.142.506.372.638.23.131.514.131.744 0a.734.734 0 00.372-.638V4.07c0-1.143.937-2.07 2.093-2.07zm-5.674 0c1.156 0 2.093.927 2.093 2.07v11.523a.648.648 0 01-.652.645.648.648 0 01-.652-.645V4.07a.785.785 0 00-.789-.78.785.785 0 00-.789.78v14.013a2.06 2.06 0 01-2.07 2.048 2.06 2.06 0 01-2.071-2.048V9.1a.762.762 0 00-.766-.758.762.762 0 00-.766.758v3.8a2.06 2.06 0 01-2.071 2.049A2.06 2.06 0 010 12.9v-1.378c0-.357.292-.646.652-.646.36 0 .653.29.653.646V12.9c0 .418.343.757.766.757s.766-.339.766-.757V9.099a2.06 2.06 0 012.07-2.048 2.06 2.06 0 012.071 2.048v8.984c0 .419.343.758.767.758.423 0 .766-.339.766-.758V4.07c0-1.143.937-2.07 2.093-2.07z" fill="url(#lobe-icons-minimax-fill)" fill-rule="nonzero"></path></svg>`,
    "baichuan": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>Baichuan</title><defs><linearGradient id="lobe-icons-baichuan-fill" x1="17.764%" x2="100%" y1="8.678%" y2="91.322%"><stop offset="0%" stop-color="#FEC13E"></stop><stop offset="100%" stop-color="#FF6933"></stop></linearGradient></defs><path d="M7.333 2h-3.2l-2 4.333V17.8L0 22h5.2l2.028-4.2L7.333 2zm7.334 0h-5.2v20h5.2V2zM16.8 7.733H22V22h-5.2V7.733zM22 2h-5.2v4.133H22V2z" fill="url(#lobe-icons-baichuan-fill)" fill-rule="nonzero"></path></svg>`,
    "modelscope": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" width="1em" xmlns="http://www.w3.org/2000/svg"><title>ModelScope</title><path d="M0 7.967h2.667v2.667H0zM8 10.633h2.667V13.3H8z" fill="#36CED0"></path><path d="M0 10.633h2.667V13.3H0zM2.667 13.3h2.666v2.667H8v2.666H2.667V13.3zM2.667 5.3H8v2.667H5.333v2.666H2.667V5.3zM10.667 13.3h2.667v2.667h-2.667z" fill="#624AFF"></path><path d="M24 7.967h-2.667v2.667H24zM16 10.633h-2.667V13.3H16z" fill="#36CED0"></path><path d="M24 10.633h-2.667V13.3H24zM21.333 13.3h-2.666v2.667H16v2.666h5.333V13.3zM21.333 5.3H16v2.667h2.667v2.666h2.666V5.3z" fill="#624AFF"></path></svg>`,
    "iflow": `<svg height="1em" style="flex:none;line-height:1" viewBox="0 0 32 32" width="1em" xmlns="http://www.w3.org/2000/svg"><title>iFlow</title><defs><linearGradient id="lobe-icons-iflow-fill" x1="0.0735" x2="0.9907" y1="0.129" y2="0.9384"><stop offset="0%" stop-color="#5C5CFF"></stop><stop offset="100%" stop-color="#AE5CFF"></stop></linearGradient></defs><path d="M31.8431 14.751C31.3154 7.1812 25.4974 1.0469 17.966 0.1197C10.4347 -0.8075 3.3025 3.7324 0.9546 10.9482C0.3457 12.8248 1.7328 14.751 3.7056 14.751C4.9501 14.7517 6.0556 13.9569 6.4514 12.7772C7.4973 9.651 10.5044 3.914 18.482 3.914Q29.4459 3.914 31.8431 14.751ZM9.1277 17.3314L9.1277 13.0862Q9.1277 13.0022 9.1441 12.9198Q9.1605 12.8373 9.1926 12.7597Q9.2248 12.682 9.2715 12.6122Q9.3182 12.5423 9.3776 12.4828Q9.4371 12.4234 9.5069 12.3767Q9.5768 12.33 9.6545 12.2979Q9.7321 12.2657 9.8145 12.2493Q9.897 12.2329 9.981 12.2329L11.0492 12.2329Q11.1332 12.2329 11.2157 12.2493Q11.2981 12.2657 11.3758 12.2979Q11.4534 12.33 11.5233 12.3767Q11.5932 12.4234 11.6526 12.4828Q11.7120 12.5423 11.7587 12.6122Q11.8054 12.682 11.8376 12.7597Q11.8697 12.8373 11.8861 12.9198Q11.9025 13.0022 11.9025 13.0862L11.9025 17.3314Q11.9025 17.4154 11.8861 17.4978Q11.8697 17.5803 11.8376 17.6579Q11.8054 17.7356 11.7587 17.8055Q11.7120 17.8753 11.6526 17.9348Q11.5932 17.9942 11.5233 18.0409Q11.4534 18.0876 11.3758 18.1197Q11.2981 18.1519 11.2157 18.1683Q11.1332 18.1847 11.0492 18.1847L9.981 18.1847Q9.897 18.1847 9.8145 18.1683Q9.7321 18.1519 9.6545 18.1197Q9.5768 18.0876 9.5069 18.0409Q9.4371 17.9942 9.3776 17.9348Q9.3182 17.8753 9.2715 17.8055Q9.2248 17.7356 9.1926 17.6579Q9.1605 17.5803 9.1441 17.4978Q9.1277 17.4154 9.1277 17.3314ZM17.2736 17.3295C17.2726 17.8015 17.6549 18.1847 18.1269 18.1847L19.4084 18.1847C19.879 18.1847 20.2607 17.8038 20.2618 17.3332L20.2664 15.2107L20.2664 15.2069L20.2618 13.0844C20.2607 12.6138 19.879 12.2329 19.4084 12.2329L18.1269 12.2329C17.6549 12.2329 17.2726 12.6161 17.2736 13.0881L17.2782 15.2069L17.2782 15.2107L17.2736 17.3295ZM13.5747 28.0523C21.5522 28.0523 24.5593 22.3153 25.6058 19.1897C26.0014 18.0098 27.1071 17.215 28.3515 17.2158C30.3238 17.2158 31.7115 19.1416 31.1026 21.0181C30.5524 22.7189 29.7162 24.3134 28.6298 25.733L30.1376 30.2235L24.7752 29.3432C14.6459 36.0484 1.0488 29.3346 0.2141 17.2158Q2.6112 28.0523 13.5747 28.0523Z" fill="url(#lobe-icons-iflow-fill)"></path></svg>`,
    "default": `<svg height="1em" width="1em" style="flex:none;line-height:1" viewBox="0 0 24 24" fill="none" stroke="url(#llm-pm-default-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg"><title>Custom Provider</title><defs><linearGradient id="llm-pm-default-grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#8050FF"></stop><stop offset="100%" stop-color="#2DD4BF"></stop></linearGradient></defs><g stroke="url(#llm-pm-default-grad)"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065" /><path d="M9 14v-2.5a1.5 1.5 0 0 1 3 0v2.5" /><path d="M9 13h3" /><path d="M15 10v4" /></g></svg>`
};

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
            t("unsaved_title"),
            t("unsaved_msg"),
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
            textContent: options.confirmText || t("ok"),
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
            confirmText: t("confirm"), onConfirm: callback
        });
    }

    showAlert(title, message) {
        this.showDialog({ title: title, message: message, alertOnly: true, confirmText: t("ok") });
    }

    showConfirm(title, message, onConfirm) {
        this.showDialog({ title: title, message: message, confirmText: t("confirm"), onConfirm: onConfirm });
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
            this.showAlert(t("error"), t("load_error"));
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
                this.showAlert(t("save_failed"), data.error);
            }
        } catch (e) {
            console.error(e);
            this.showAlert(t("error"), t("save_err"));
        }
    }

    async deleteProvider(id) {
        this.showConfirm(
            t("delete_title"),
            t("delete_msg"),
            async () => {
                try {
                    const res = await api.fetchApi(`/llm_toolkit/providers/${id}`, { method: "DELETE" });
                    const data = await res.json();
                    if (data.status === "ok") {
                        if (this.selectedId === id) this.selectedId = null;
                        await this.loadProviders();
                    } else {
                        this.showAlert(t("delete_failed"), data.error);
                    }
                } catch (e) {
                    console.error(e);
                    this.showAlert(t("error"), t("delete_err"));
                }
            }
        );
    }

    async checkConnectivity(apiHost, apiKey, model) {
        const btn = document.getElementById("pm-check-btn");
        if (!btn) return;

        const originalHtml = btn.innerHTML;
        const originalBg = btn.style.background;
        const originalColor = btn.style.color;

        // Loading State
        btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="llm-pm-spin" style="margin-right:6px"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg> ` + t("checking");
        btn.disabled = true;

        try {
            const res = await api.fetchApi("/llm_toolkit/providers/check", {
                method: "POST",
                body: JSON.stringify({ apiHost, apiKey, model })
            });
            const data = await res.json();

            if (data.status === "ok") {
                // Success State
                btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px"><polyline points="20 6 9 17 4 12"></polyline></svg> ` + t("connected");
                btn.style.background = "rgba(52, 211, 153, 0.15)";
                btn.style.color = "var(--glass-success)";
                btn.style.borderColor = "var(--glass-success)";
                btn.style.boxShadow = "0 0 12px var(--glass-success-glow)";
            } else {
                // Error State
                btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg> ` + t("failed");
                btn.style.background = "rgba(248, 113, 113, 0.15)";
                btn.style.color = "var(--glass-danger)";
                btn.style.borderColor = "var(--glass-danger)";
                btn.style.boxShadow = "0 0 12px rgba(248, 113, 113, 0.3)";
                console.warn("[LLMs Toolkit] Connect Error: ", data.message);

                // Still show the alert for the specific error message
                setTimeout(() => this.showAlert(t("conn_failed"), "❌ " + data.message), 100);
            }
        } catch (e) {
            console.error(e);
            btn.innerHTML = t("network_err_title");
            btn.style.color = "#fbbf24";
            setTimeout(() => this.showAlert(t("error"), `❌ ${t("network_err_msg")}`), 100);
        } finally {
            // Reset button after 3 seconds
            setTimeout(() => {
                btn.innerHTML = originalHtml;
                btn.style.background = originalBg;
                btn.style.color = originalColor;
                btn.style.borderColor = "";
                btn.style.boxShadow = "";
                btn.disabled = false;
            }, 3000);
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
            placeholder: t("search_placeholder"),
            oninput: (e) => {
                this.searchQuery = e.target.value.toLowerCase();
                this.renderSidebar();
            }
        });

        const addBtn = $el("button.llm-pm-add-btn", {
            textContent: t("add_custom"),
            onclick: () => {
                this.checkUnsaved(() => this.createNewProvider());
            },
            style: { padding: "6px 16px", fontSize: "0.9em", borderRadius: "4px", minHeight: "unset" }
        });

        const usageBtn = $el("button.llm-pm-add-btn", {
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:4px"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M13 5h8" /><path d="M13 9h5" /><path d="M13 15h8" /><path d="M13 19h5" /><path d="M3 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" /><path d="M3 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -4" /></svg> ` + t("usage_stats"),
            onclick: () => {
                this.checkUnsaved(() => {
                    this.selectedId = "USAGE_STATS";
                    this.render();
                });
            },
            style: { padding: "6px 16px", fontSize: "0.9em", borderRadius: "4px", minHeight: "unset", marginTop: "10px", background: "transparent", border: "1px dashed var(--border-color)", color: "var(--fg-color)" }
        });

        this.modal = $el("div.comfy-modal.llm-pm-modal", {
            parent: document.body,
            style: { display: "flex", zIndex: 10000 }
        }, [
            $el("div.llm-pm-header", [

                $el("h2.llm-pm-title", [
                    t("manager_title")
                ]),
                $el("div", { style: { display: "flex", alignItems: "center", gap: "16px" } }, [
                    $el("div", {
                        style: {
                            position: "relative",
                            display: "flex",
                            alignItems: "center",
                            background: "rgba(255,255,255,0.08)",
                            border: "1px solid rgba(255,255,255,0.15)",
                            borderRadius: "8px",
                            transition: "all 0.2s ease"
                        }
                    }, [
                        $el("div", {
                            style: { position: "absolute", left: "8px", display: "flex", pointerEvents: "none", color: "var(--glass-text-secondary)" },
                            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-language"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 6.371c0 4.418 -2.239 6.629 -5 6.629" /><path d="M4 6.371h7" /><path d="M5 9c0 2.144 2.252 3.908 6 4" /><path d="M12 20l4 -9l4 9" /><path d="M19.1 18h-6.2" /><path d="M6.694 3 l.793 .582" /></svg>`
                        }),
                        $el("select", {
                            onchange: (e) => {
                                localStorage.setItem("llm_pm_lang", e.target.value);
                                // Re-render UI
                                this.modal.remove();
                                this.modal = null;
                                this.show();

                                // Update the main menu button
                                const menuBtn = document.querySelector('.comfyui-button[title*="Manage LLM API"], .comfyui-button[title*="管理 LLM API"]');
                                if (menuBtn) {
                                    const contentSpan = menuBtn.querySelector('.comfyui-button-content');
                                    if (contentSpan) contentSpan.textContent = t("menu_button");
                                    menuBtn.title = t("menu_tooltip");
                                }
                            },
                            style: {
                                background: "transparent",
                                color: "var(--glass-text-primary)",
                                border: "none",
                                outline: "none",
                                cursor: "pointer",
                                padding: "6px 28px 6px 30px",
                                appearance: "none",
                                fontSize: "0.85em",
                                fontFamily: "inherit"
                            }
                        }, [
                            $el("option", { value: "zh", textContent: "简体中文" }),
                            $el("option", { value: "en", textContent: "English" })
                        ], (el) => {
                            el.value = getLang();
                        }),
                        $el("div", {
                            style: { position: "absolute", right: "8px", display: "flex", pointerEvents: "none", color: "var(--glass-text-secondary)" },
                            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>`
                        })
                    ]),
                    closeBtn
                ])
            ]),
            $el("div.llm-pm-body", [
                $el("div.llm-pm-sidebar", [
                    $el("div.llm-pm-search", [searchInput]),
                    this.sidebarListContainer,
                    $el("div.llm-pm-sidebar-footer", [addBtn, usageBtn])
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
            name: t("new_custom"),
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

            const tags = [$el("span.llm-pm-tag" + (p.enabled ? ".on" : ""), p.enabled ? t("on") : t("off"))];

            const item = $el("div.llm-pm-item" + (isActive ? ".active" : ""), {
                onclick: () => {
                    if (this.selectedId === p.id) return;
                    this.checkUnsaved(() => {
                        this.selectedId = p.id;
                        this.render();
                    });
                }
            }, [
                $el("div", { style: { display: "flex", alignItems: "center", gap: "8px" } }, [
                    $el("span", { innerHTML: PROVIDER_ICONS[p.id] || PROVIDER_ICONS["default"], style: { display: "flex", alignItems: "center", fontSize: "1.2em" } }),
                    $el("span", p.name)
                ]),
                $el("div", { style: { flex: 1 } }),
                $el("div.llm-pm-item-tags", tags)
            ]);

            this.sidebarListContainer.appendChild(item);
        });
    }

    async renderContent() {
        this.contentContainer.innerHTML = "";

        if (this.selectedId === "USAGE_STATS") {
            const loading = $el("div.llm-pm-empty", t("usage_loading"));
            this.contentContainer.appendChild(loading);

            try {
                const res = await api.fetchApi("/llm_toolkit/usage");
                if (!res.ok) {
                    this.contentContainer.innerHTML = "";
                    if (res.status === 404) {
                        this.contentContainer.appendChild($el("div.llm-pm-empty", t("usage_api_404")));
                    } else {
                        this.contentContainer.appendChild($el("div.llm-pm-empty", `${t("usage_api_err")}${res.status}.`));
                    }
                    return;
                }
                const data = await res.json();

                this.contentContainer.innerHTML = "";
                this.contentContainer.appendChild($el("h2", { textContent: t("usage_dashboard"), style: { margin: "0 0 12px 0" } }));

                if (!data.usage || data.usage.length === 0) {
                    this.contentContainer.appendChild($el("div.llm-pm-empty", t("usage_empty")));
                    return;
                }

                // ── Summary Cards ──────────────────────────────────────
                const rows = data.usage;
                const totalCalls = rows.length;
                const okCalls = rows.filter(r => r.status !== "error").length;
                const errorCalls = totalCalls - okCalls;
                const totalTokens = rows.reduce((s, r) => s + (r.total_tokens || 0), 0);
                const avgLatency = Math.round(rows.reduce((s, r) => s + (r.elapsed_ms || 0), 0) / totalCalls);

                const cardStyle = { flex: "1", padding: "12px 16px", background: "var(--comfy-input-bg)", borderRadius: "8px", border: "1px solid var(--border-color)", textAlign: "center" };
                const cardLabel = { fontSize: "0.75em", color: "var(--descrip-text)", marginBottom: "4px" };
                const cardValue = { fontSize: "1.3em", fontWeight: "bold", color: "var(--fg-color)" };

                const fmtTokens = (t) => t >= 1000000 ? `${(t / 1000000).toFixed(1)}M` : t >= 1000 ? `${(t / 1000).toFixed(1)}K` : String(t);

                const summaryRow = $el("div", { style: { display: "flex", gap: "12px", marginBottom: "16px" } }, [
                    $el("div", { style: cardStyle }, [
                        $el("div", { style: cardLabel, textContent: t("total_calls") }),
                        $el("div", { style: cardValue, textContent: String(totalCalls) })
                    ]),
                    $el("div", { style: cardStyle }, [
                        $el("div", { style: cardLabel, textContent: t("success_error") }),
                        $el("div", { style: cardValue, innerHTML: `<span style="color:#4CAF50">${okCalls}</span> / <span style="color:${errorCalls > 0 ? '#f44336' : 'var(--descrip-text)'}">${errorCalls}</span>` })
                    ]),
                    $el("div", { style: cardStyle }, [
                        $el("div", { style: cardLabel, textContent: t("total_tokens") }),
                        $el("div", { style: cardValue, textContent: fmtTokens(totalTokens) })
                    ]),
                    $el("div", { style: cardStyle }, [
                        $el("div", { style: cardLabel, textContent: t("avg_latency") }),
                        $el("div", { style: cardValue, textContent: `${avgLatency} ms` })
                    ]),
                ]);
                this.contentContainer.appendChild(summaryRow);

                // ── Data Table ─────────────────────────────────────────
                const table = $el("table", { style: { width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.9em" } });
                const thead = $el("tr", { style: { borderBottom: "2px solid var(--border-color)", color: "var(--descrip-text)" } });
                [t("status"), t("time"), t("provider"), t("model"), t("tokens_in_out"), t("latency")].forEach(h => {
                    thead.appendChild($el("th", { style: { padding: "8px" }, textContent: h }));
                });
                table.appendChild(thead);

                // Show newest first
                rows.reverse().forEach(row => {
                    const isError = row.status === "error";
                    const tr = $el("tr", { style: { borderBottom: "1px solid var(--border-color)", background: isError ? "rgba(244,67,54,0.08)" : "transparent" } });
                    const date = new Date(row.timestamp * 1000).toLocaleString();

                    tr.appendChild($el("td", { style: { padding: "8px", textAlign: "center" }, innerHTML: isError ? `<span style="color:#f44336" title=t("error")>✗</span>` : `<span style="color:#4CAF50" title=t("ok")>✓</span>` }));
                    tr.appendChild($el("td", { style: { padding: "8px" }, textContent: date }));
                    tr.appendChild($el("td", { style: { padding: "8px", fontWeight: "bold" }, textContent: row.provider }));
                    tr.appendChild($el("td", { style: { padding: "8px" }, textContent: row.model }));
                    tr.appendChild($el("td", { style: { padding: "8px" }, textContent: isError ? "-" : `${row.input_tokens} / ${row.output_tokens}` }));
                    tr.appendChild($el("td", { style: { padding: "8px", color: "var(--descrip-text)" }, textContent: `${row.elapsed_ms} ms` }));
                    table.appendChild(tr);
                });

                const tableContainer = $el("div", { style: { overflowY: "auto", flex: "1" } }, [table]);
                this.contentContainer.appendChild(tableContainer);

            } catch (e) {
                console.error(e);
                this.contentContainer.innerHTML = "";
                this.contentContainer.appendChild($el("div.llm-pm-empty", t("usage_load_err")));
            }
            return;
        }

        const provider = this.providers.find(p => p.id === this.selectedId);
        if (!provider) {
            this.contentContainer.appendChild(
                $el("div.llm-pm-empty", t("select_edit"))
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
            placeholder: t("provider_name"),
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
            style: { paddingRight: "40px" }, // Make room for the absolute eye icon
            oninput: (e) => draft.apiKey = e.target.value
        });

        const toggleVisibilityBtn = $el("div", {
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`,
            onclick: () => {
                if (keyInput.type === "password") {
                    keyInput.type = "text";
                    toggleVisibilityBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;
                    toggleVisibilityBtn.style.color = "var(--glass-text-primary)";
                } else {
                    keyInput.type = "password";
                    toggleVisibilityBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
                    toggleVisibilityBtn.style.color = "var(--glass-text-tertiary)";
                }
            },
            title: "Toggle Visibility",
            style: {
                position: "absolute", right: "12px", top: "50%", transform: "translateY(-50%)",
                display: "flex", alignItems: "center", justifyContent: "center",
                color: "var(--glass-text-tertiary)", cursor: "pointer", transition: "var(--glass-transition)"
            }
        });

        toggleVisibilityBtn.onmouseenter = () => toggleVisibilityBtn.style.color = "var(--glass-text-primary)";
        toggleVisibilityBtn.onmouseleave = () => {
            if (keyInput.type === "password") toggleVisibilityBtn.style.color = "var(--glass-text-tertiary)";
        };

        const keyInputWrapper = $el("div", {
            style: { position: "relative", flex: "1", display: "flex" }
        }, [keyInput, toggleVisibilityBtn]);

        const checkBtn = $el("button", {
            id: "pm-check-btn",
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Check API`,
            onclick: () => this.checkConnectivity(draft.apiHost, draft.apiKey, draft.models[0] || ""),
            style: {
                padding: "8px 16px", fontSize: "0.88em", borderRadius: "10px", minHeight: "unset",
                display: "inline-flex", alignItems: "center", cursor: "pointer",
                background: "rgba(255,255,255,0.06)", color: "var(--glass-text-primary)",
                border: "1px solid var(--glass-border-light)", transition: "var(--glass-transition)"
            }
        });

        checkBtn.onmouseenter = () => {
            if (!checkBtn.disabled) {
                checkBtn.style.background = "rgba(255,255,255,0.12)";
                checkBtn.style.borderColor = "rgba(255,255,255,0.2)";
                checkBtn.style.boxShadow = "0 2px 8px rgba(0,0,0,0.2)";
            }
        };
        checkBtn.onmouseleave = () => {
            if (!checkBtn.disabled) {
                checkBtn.style.background = "rgba(255,255,255,0.06)";
                checkBtn.style.borderColor = "var(--glass-border-light)";
                checkBtn.style.boxShadow = "none";
            }
        };

        // -- URL
        const urlInput = $el("input", {
            type: "text",
            value: draft.apiHost,
            placeholder: "https://api.../v1",
            oninput: (e) => {
                draft.apiHost = e.target.value;
                const prev = document.getElementById("pm-url-preview");
                if (prev) prev.textContent = `${t("preview")}${draft.apiHost} /chat/completions`;
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
                    title: t("db_edit"),
                    ondblclick: () => {
                        this.showPrompt(t("edit_model_name"), m, (newName) => {
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
                        title: t("del_model"),
                        onclick: () => {
                            draft.models.splice(idx, 1);
                            renderModels();
                        }
                    })
                ]));
            });

            // Add button
            modelsContainer.appendChild($el("span.llm-pm-model-add", {
                textContent: t("add_model"),
                onclick: () => {
                    this.showPrompt(t("enter_model_name"), "", (name) => {
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
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:4px"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M16 3a1 1 0 0 1 .707 .293l4 4a1 1 0 0 1 .293 .707v10a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3v-12a3 3 0 0 1 3 -3h1v4a1 1 0 0 0 .883 .993l.117 .007h6a1 1 0 0 0 1 -1v-4zm-4 8a2.995 2.995 0 0 0 -2.995 2.898a1 1 0 0 0 -.005 .102a3 3 0 1 0 3 -3m1 -8v3h-4v-3z" /></svg> ` + t("save"),
            style: {
                fontWeight: "bold", background: "#4CAF50", color: "white",
                padding: "6px 16px", fontSize: "0.9em", borderRadius: "4px", minHeight: "unset",
                display: "inline-flex", alignItems: "center", transition: "all 0.3s ease"
            },
            onclick: async () => {
                const originalHtml = saveBtn.innerHTML;
                saveBtn.innerHTML = t("saving");
                saveBtn.disabled = true;

                if (draft._isNew) delete draft._isNew;
                await this.saveProvider(draft);

                saveBtn.innerHTML = t("saved");
                saveBtn.style.background = "#3d8b40"; // slightly darker green
                setTimeout(() => {
                    saveBtn.innerHTML = originalHtml;
                    saveBtn.style.background = "#4CAF50";
                    saveBtn.disabled = false;
                }, 1500);
            }
        });

        const deleteBtn = $el("button", {
            innerHTML: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle;margin-right:4px"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19 2a3 3 0 0 1 3 3v14a3 3 0 0 1 -3 3h-14a3 3 0 0 1 -3 -3v-14a3 3 0 0 1 3 -3zm-4 9h-6l-.117 .007a1 1 0 0 0 .117 1.993h6l.117 -.007a1 1 0 0 0 -.117 -1.993z" /></svg> ` + t("delete"),
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
                    $el("span", t("provider_name")),
                    $el("div", { style: { display: "flex", alignItems: "center", gap: "8px" } }, [
                        $el("span", { style: { fontSize: "0.8em", fontWeight: "normal" } }, t("enable_nodes")),
                        enableSwitch
                    ])
                ]),
                nameInput
            ]),

            $el("div.llm-pm-field", [
                $el("label", t("base_url")),
                urlInput,
                $el("div.llm-pm-field-hint", {
                    id: "pm-url-preview",
                    textContent: `${t("preview")}${draft.apiHost} /chat/completions`
                })
            ]),

            $el("div.llm-pm-field", [
                $el("label", t("api_key")),
                $el("div.llm-pm-input-group", [keyInputWrapper, checkBtn]),
                $el("div.llm-pm-field-hint", t("keys_hint"))
            ]),

            $el("div.llm-pm-field", [
                $el("label", t("avail_models")),
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
                    content: t("menu_button"),
                    tooltip: t("menu_tooltip"),
                    action: () => manager.show(),
                    classList: "comfyui-button comfyui-menu-mobile-collapse primary"
                }).element
            );

            app.menu?.settingsGroup.element.before(llmGroup.element);
            console.log("[LLMs_Toolkit] LLMs button injected into ComfyUI menu.");
        } catch (e) {
            console.warn("[LLMs_Toolkit] New-style menu API not available, using fallback.", e);
            const floatBtn = $el("button", {
                textContent: t("menu_button"),
                title: t("menu_tooltip"),
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
