var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => MermaidLensPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian6 = require("obsidian");

// src/config-manager.ts
var import_obsidian2 = require("obsidian");

// src/i18n.ts
var import_obsidian = require("obsidian");

// src/locales/en.ts
var en = {
  "settings.config.name": "Global Mermaid configuration",
  "settings.config.desc": "Enter JSON for Mermaid initialize(). Changes are saved only after selecting Apply and redraw.",
  "settings.config.aliasJson": "Mermaid JSON",
  "settings.config.aliasInitialize": "initialize",
  "settings.actions.name": "Apply configuration",
  "settings.actions.desc": "Validate the configuration, then save and redraw only if Mermaid accepts it.",
  "settings.actions.apply": "Apply and redraw",
  "settings.actions.reset": "Restore defaults",
  "settings.trigger.name": "Open viewer action",
  "settings.trigger.desc": "Single-click by default. Links and buttons inside diagrams do not open the viewer.",
  "settings.trigger.aliasSingle": "Single-click diagram",
  "settings.trigger.aliasDouble": "Double-click diagram",
  "settings.trigger.aliasButton": "Expand button",
  "settings.trigger.single": "Single-click diagram",
  "settings.trigger.double": "Double-click diagram",
  "settings.trigger.button": "Expand button only",
  "settings.expandButton.name": "Show expand button",
  "settings.expandButton.desc": "Show an expand button in the upper-right corner of Mermaid diagrams.",
  "settings.expandButton.aliasViewer": "Viewer",
  "settings.expandButton.aliasLarge": "Large diagram",
  "notice.configApplied": "Mermaid configuration applied",
  "notice.invalidConfig": "Invalid Mermaid configuration: {{message}}",
  "notice.defaultsRestored": "Default Mermaid configuration restored",
  "notice.restoreDefaultsFailed": "Failed to restore the default configuration. Check the developer console.",
  "notice.savedConfigInvalid": "The saved Mermaid configuration is invalid. Using defaults for this session.",
  "notice.applySavedConfigFailed": "Could not apply the Mermaid configuration. Attempted to restore defaults.",
  "viewer.help": "Drag to pan \xB7 Wheel/pinch to zoom \xB7 Double-click to fit \xB7 Esc to close",
  "viewer.zoomOut": "Zoom out",
  "viewer.fit": "Fit to window",
  "viewer.zoomIn": "Zoom in",
  "diagram.openViewer": "Open Mermaid diagram viewer",
  "diagram.openLarge": "Open large diagram",
  "error.configMustBeObject": "Configuration must be a JSON object",
  "error.managerNotInitialized": "Mermaid configuration manager is not initialized"
};

// src/locales/zh-cn.ts
var zhCN = {
  "settings.config.name": "\u5168\u5C40 Mermaid \u914D\u7F6E",
  "settings.config.desc": "\u586B\u5199 Mermaid initialize() \u4F7F\u7528\u7684 JSON\u3002\u53EA\u6709\u70B9\u51FB\u201C\u5E94\u7528\u5E76\u91CD\u7ED8\u201D\u540E\u624D\u4F1A\u4FDD\u5B58\u3002",
  "settings.config.aliasJson": "Mermaid JSON",
  "settings.config.aliasInitialize": "initialize",
  "settings.actions.name": "\u5E94\u7528\u914D\u7F6E",
  "settings.actions.desc": "\u9A8C\u8BC1\u914D\u7F6E\uFF1BMermaid \u63A5\u53D7\u540E\u624D\u4FDD\u5B58\u5E76\u91CD\u7ED8\u3002",
  "settings.actions.apply": "\u5E94\u7528\u5E76\u91CD\u7ED8",
  "settings.actions.reset": "\u6062\u590D\u9ED8\u8BA4\u914D\u7F6E",
  "settings.trigger.name": "\u6253\u5F00\u5927\u56FE\u7684\u64CD\u4F5C",
  "settings.trigger.desc": "\u9ED8\u8BA4\u5355\u51FB\u6253\u5F00\uFF1B\u56FE\u4E2D\u7684\u94FE\u63A5\u548C\u6309\u94AE\u4E0D\u4F1A\u89E6\u53D1\u5927\u56FE\u3002",
  "settings.trigger.aliasSingle": "\u5355\u51FB\u56FE\u8868",
  "settings.trigger.aliasDouble": "\u53CC\u51FB\u56FE\u8868",
  "settings.trigger.aliasButton": "\u5C55\u5F00\u6309\u94AE",
  "settings.trigger.single": "\u5355\u51FB\u56FE\u8868",
  "settings.trigger.double": "\u53CC\u51FB\u56FE\u8868",
  "settings.trigger.button": "\u4EC5\u4F7F\u7528\u5C55\u5F00\u6309\u94AE",
  "settings.expandButton.name": "\u663E\u793A\u5C55\u5F00\u6309\u94AE",
  "settings.expandButton.desc": "\u5728 Mermaid \u56FE\u53F3\u4E0A\u89D2\u663E\u793A\u5C55\u5F00\u6309\u94AE\u3002",
  "settings.expandButton.aliasViewer": "\u67E5\u770B\u5668",
  "settings.expandButton.aliasLarge": "\u5927\u56FE",
  "notice.configApplied": "Mermaid \u914D\u7F6E\u5DF2\u5E94\u7528",
  "notice.invalidConfig": "Mermaid \u914D\u7F6E\u65E0\u6548\uFF1A{{message}}",
  "notice.defaultsRestored": "\u5DF2\u6062\u590D\u9ED8\u8BA4 Mermaid \u914D\u7F6E",
  "notice.restoreDefaultsFailed": "\u6062\u590D\u9ED8\u8BA4\u914D\u7F6E\u5931\u8D25\uFF0C\u8BF7\u67E5\u770B\u5F00\u53D1\u8005\u63A7\u5236\u53F0",
  "notice.savedConfigInvalid": "\u4FDD\u5B58\u7684 Mermaid \u914D\u7F6E\u65E0\u6548\uFF0C\u672C\u6B21\u4F7F\u7528\u9ED8\u8BA4\u914D\u7F6E",
  "notice.applySavedConfigFailed": "Mermaid \u914D\u7F6E\u65E0\u6CD5\u5E94\u7528\uFF0C\u5DF2\u5C1D\u8BD5\u6062\u590D\u9ED8\u8BA4\u914D\u7F6E",
  "viewer.help": "\u62D6\u62FD\u79FB\u52A8 \xB7 \u6EDA\u8F6E/\u53CC\u6307\u7F29\u653E \xB7 \u53CC\u51FB\u9002\u914D \xB7 Esc \u5173\u95ED",
  "viewer.zoomOut": "\u7F29\u5C0F",
  "viewer.fit": "\u9002\u914D\u7A97\u53E3",
  "viewer.zoomIn": "\u653E\u5927",
  "diagram.openViewer": "\u6253\u5F00 Mermaid \u5927\u56FE",
  "diagram.openLarge": "\u6253\u5F00\u5927\u56FE",
  "error.configMustBeObject": "\u914D\u7F6E\u5FC5\u987B\u662F JSON \u5BF9\u8C61",
  "error.managerNotInitialized": "Mermaid \u914D\u7F6E\u7BA1\u7406\u5668\u5C1A\u672A\u521D\u59CB\u5316"
};

// src/i18n.ts
var translations = {
  en,
  zh: zhCN,
  "zh-cn": zhCN
};
function t(key, params = {}) {
  var _a, _b;
  const language = (0, import_obsidian.getLanguage)().toLowerCase();
  const messages = (_b = (_a = translations[language]) != null ? _a : translations[language.split("-")[0]]) != null ? _b : en;
  return messages[key].replace(/\{\{(\w+)\}\}/g, (match, name) => {
    const value = params[name];
    return value === void 0 ? match : String(value);
  });
}

// src/config-utils.ts
var BLOCKED_KEYS = /* @__PURE__ */ new Set(["__proto__", "prototype", "constructor"]);
function isPlainObject(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}
function mergeConfig(base, override) {
  const result = { ...base };
  for (const [key, value] of Object.entries(override)) {
    if (BLOCKED_KEYS.has(key)) continue;
    const previous = result[key];
    result[key] = isPlainObject(previous) && isPlainObject(value) ? mergeConfig(previous, value) : value;
  }
  return result;
}
function parseConfigJson(value) {
  const parsed = JSON.parse(value);
  if (!isPlainObject(parsed)) throw new Error(t("error.configMustBeObject"));
  return parsed;
}

// src/config-manager.ts
async function loadObsidianMermaid() {
  const loaded = await (0, import_obsidian2.loadMermaid)();
  if (loaded === null || typeof loaded !== "object" || !("initialize" in loaded) || typeof loaded.initialize !== "function") {
    throw new Error("Obsidian returned an invalid Mermaid API");
  }
  return loaded;
}
var MermaidConfigManager = class {
  constructor(load = loadObsidianMermaid) {
    this.baseConfig = {};
    this.customConfig = {};
    this.active = false;
    this.load = load;
  }
  async install(config) {
    if (this.active) {
      this.apply(config);
      return;
    }
    const api = await this.load();
    const original = api.initialize;
    this.api = api;
    this.originalInitialize = original;
    this.baseConfig = this.readCurrentConfig(api);
    this.customConfig = config;
    this.active = true;
    const wrapper = (incoming) => {
      const nextBase = incoming !== null && typeof incoming === "object" && !Array.isArray(incoming) ? incoming : {};
      if (!this.active) {
        original(nextBase);
        return;
      }
      this.baseConfig = nextBase;
      original(mergeConfig(nextBase, this.customConfig));
    };
    this.wrapper = wrapper;
    api.initialize = wrapper;
    try {
      original(mergeConfig(this.baseConfig, config));
    } catch (error) {
      this.active = false;
      if (api.initialize === wrapper) api.initialize = original;
      this.clearReferences();
      throw error;
    }
  }
  apply(config) {
    if (!this.api || !this.originalInitialize || !this.active) {
      throw new Error(t("error.managerNotInitialized"));
    }
    const previous = this.customConfig;
    try {
      this.originalInitialize(mergeConfig(this.baseConfig, config));
      this.customConfig = config;
    } catch (error) {
      try {
        this.originalInitialize(mergeConfig(this.baseConfig, previous));
      } catch (restoreError) {
        console.error("[mermaid-lens] Failed to restore Mermaid config", restoreError);
      }
      throw error;
    }
  }
  dispose() {
    const api = this.api;
    const original = this.originalInitialize;
    const wrapper = this.wrapper;
    this.active = false;
    if (api && original) {
      if (wrapper && api.initialize === wrapper) api.initialize = original;
      try {
        original(this.baseConfig);
      } catch (error) {
        console.error("[mermaid-lens] Failed to restore Obsidian Mermaid config", error);
      }
    }
    this.clearReferences();
  }
  readCurrentConfig(api) {
    var _a;
    try {
      const config = (_a = api.getConfig) == null ? void 0 : _a.call(api);
      return config !== null && typeof config === "object" && !Array.isArray(config) ? config : {};
    } catch (e) {
      return {};
    }
  }
  clearReferences() {
    this.api = void 0;
    this.originalInitialize = void 0;
    this.wrapper = void 0;
    this.baseConfig = {};
    this.customConfig = {};
  }
};

// src/diagram-registry.ts
var import_obsidian4 = require("obsidian");

// src/viewer.ts
var import_obsidian3 = require("obsidian");

// src/viewer-utils.ts
var MIN_SCALE = 0.1;
var MAX_SCALE = 10;
var VIEWPORT_PADDING = 48;
var cloneSequence = 0;
function diagramSize(svg) {
  var _a, _b;
  const viewBox = svg.viewBox.baseVal;
  if (viewBox.width > 0 && viewBox.height > 0) {
    return { width: viewBox.width, height: viewBox.height };
  }
  const width = Number.parseFloat((_a = svg.getAttribute("width")) != null ? _a : "");
  const height = Number.parseFloat((_b = svg.getAttribute("height")) != null ? _b : "");
  return {
    width: Number.isFinite(width) && width > 0 ? width : 800,
    height: Number.isFinite(height) && height > 0 ? height : 500
  };
}
var clamp = (value, min, max) => Math.min(max, Math.max(min, value));
function fitView(viewport, diagram) {
  if (viewport.width <= 0 || viewport.height <= 0) return void 0;
  const width = Math.max(viewport.width - VIEWPORT_PADDING, 1);
  const height = Math.max(viewport.height - VIEWPORT_PADDING, 1);
  const scale = clamp(Math.min(width / diagram.width, height / diagram.height), MIN_SCALE, MAX_SCALE);
  return {
    scale,
    x: (viewport.width - diagram.width * scale) / 2,
    y: (viewport.height - diagram.height * scale) / 2
  };
}
function zoomView(state, factor, anchor) {
  const diagramX = (anchor.x - state.x) / state.scale;
  const diagramY = (anchor.y - state.y) / state.scale;
  const scale = clamp(state.scale * factor, MIN_SCALE, MAX_SCALE);
  return {
    scale,
    x: anchor.x - diagramX * scale,
    y: anchor.y - diagramY * scale
  };
}
function panView(start, pointer) {
  return {
    x: start.x + pointer.x - start.pointer.x,
    y: start.y + pointer.y - start.pointer.y
  };
}
function pinchView(start, distance, center) {
  const scale = clamp(start.scale * distance / Math.max(start.distance, 1), MIN_SCALE, MAX_SCALE);
  return {
    scale,
    x: center.x - start.anchor.x * scale,
    y: center.y - start.anchor.y * scale
  };
}
function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
function remapSvgIds(svg) {
  const prefix = `mermaid-lens-${Date.now()}-${cloneSequence++}-`;
  const idMap = /* @__PURE__ */ new Map();
  const elements = [svg, ...Array.from(svg.querySelectorAll("*"))];
  for (const element of elements) {
    const oldId = element.id;
    if (!oldId) continue;
    const newId = `${prefix}${oldId}`;
    idMap.set(oldId, newId);
    element.id = newId;
  }
  for (const element of elements) {
    for (const attribute of Array.from(element.attributes)) {
      let value = attribute.value;
      for (const [oldId, newId] of idMap) {
        value = value.replace(new RegExp(`url\\(["']?#${escapeRegExp(oldId)}["']?\\)`, "g"), `url(#${newId})`);
        if (value === `#${oldId}`) value = `#${newId}`;
      }
      if (attribute.name === "aria-labelledby" || attribute.name === "aria-describedby") {
        value = value.split(/\s+/).map((id) => {
          var _a;
          return (_a = idMap.get(id)) != null ? _a : id;
        }).join(" ");
      }
      if (value !== attribute.value) element.setAttribute(attribute.name, value);
    }
  }
  svg.querySelectorAll("style").forEach((style) => {
    var _a;
    let css = (_a = style.textContent) != null ? _a : "";
    for (const [oldId, newId] of idMap) {
      css = css.replace(new RegExp(`#${escapeRegExp(oldId)}(?![\\w-])`, "g"), `#${newId}`);
    }
    style.textContent = css;
  });
}

// src/viewer.ts
var MermaidViewerModal = class extends import_obsidian3.Modal {
  constructor(app, source) {
    super(app);
    this.source = source;
  }
  onOpen() {
    this.modalEl.addClass("mermaid-lens-modal");
    this.contentEl.empty();
    const toolbar = this.contentEl.createDiv({ cls: "mermaid-lens-toolbar" });
    toolbar.createDiv({ cls: "mermaid-lens-title", text: "Mermaid" });
    toolbar.createDiv({
      cls: "mermaid-lens-help",
      text: t("viewer.help")
    });
    const controls = toolbar.createDiv({ cls: "mermaid-lens-controls" });
    const stage = this.contentEl.createDiv({ cls: "mermaid-lens-stage" });
    const svg = this.source.cloneNode(true);
    remapSvgIds(svg);
    const size = diagramSize(svg);
    svg.setAttribute("width", String(size.width));
    svg.setAttribute("height", String(size.height));
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    svg.addClass("mermaid-lens-clone");
    svg.style.width = `${size.width}px`;
    svg.style.height = `${size.height}px`;
    stage.appendChild(svg);
    const handlers = this.setupPanZoom(stage, svg, size);
    this.cleanup = handlers.cleanup;
    this.makeButton(controls, "zoom-out", t("viewer.zoomOut"), () => handlers.zoom(1 / 1.2));
    this.makeButton(controls, "scan", t("viewer.fit"), handlers.fit);
    this.makeButton(controls, "zoom-in", t("viewer.zoomIn"), () => handlers.zoom(1.2));
    this.scope.register([], "+", () => {
      handlers.zoom(1.2);
      return false;
    });
    this.scope.register([], "=", () => {
      handlers.zoom(1.2);
      return false;
    });
    this.scope.register([], "-", () => {
      handlers.zoom(1 / 1.2);
      return false;
    });
  }
  onClose() {
    var _a;
    (_a = this.cleanup) == null ? void 0 : _a.call(this);
    this.cleanup = void 0;
    this.contentEl.empty();
  }
  makeButton(parent, icon, label, action) {
    const button = parent.createEl("button", { attr: { "aria-label": label, title: label } });
    (0, import_obsidian3.setIcon)(button, icon);
    button.addEventListener("click", action);
  }
  setupPanZoom(stage, svg, size) {
    var _a;
    const state = { scale: 1, x: 0, y: 0 };
    const pointers = /* @__PURE__ */ new Map();
    const ownerWindow = (_a = stage.ownerDocument.defaultView) != null ? _a : window;
    let initialized = false;
    let userChangedView = false;
    let disposed = false;
    let initFrame = 0;
    let panStart;
    let pinchStart;
    const render = () => {
      svg.style.transform = `translate(${state.x}px, ${state.y}px) scale(${state.scale})`;
    };
    const fitInternal = () => {
      if (stage.clientWidth <= 0 || stage.clientHeight <= 0) return false;
      const fitted = fitView({ width: stage.clientWidth, height: stage.clientHeight }, size);
      if (!fitted) return false;
      Object.assign(state, fitted);
      initialized = true;
      render();
      return true;
    };
    const fit = () => {
      userChangedView = false;
      fitInternal();
    };
    const initializeWhenLaidOut = (attempt = 0) => {
      if (disposed || initialized) return;
      if (!fitInternal() && attempt < 30) {
        initFrame = ownerWindow.requestAnimationFrame(() => initializeWhenLaidOut(attempt + 1));
      }
    };
    initFrame = ownerWindow.requestAnimationFrame(() => initializeWhenLaidOut());
    const zoomAt = (factor, point) => {
      if (!initialized && !fitInternal()) return;
      const anchor = point != null ? point : { x: stage.clientWidth / 2, y: stage.clientHeight / 2 };
      Object.assign(state, zoomView(state, factor, anchor));
      userChangedView = true;
      render();
    };
    const localPoint = (event) => {
      const rect = stage.getBoundingClientRect();
      return { x: event.clientX - rect.left, y: event.clientY - rect.top };
    };
    const midpoint = (a, b) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });
    const distance = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
    const beginGesture = () => {
      const points = Array.from(pointers.values());
      if (points.length === 1) {
        panStart = { pointer: points[0], x: state.x, y: state.y };
        pinchStart = void 0;
      } else if (points.length >= 2) {
        const center = midpoint(points[0], points[1]);
        pinchStart = {
          distance: Math.max(distance(points[0], points[1]), 1),
          scale: state.scale,
          anchor: {
            x: (center.x - state.x) / state.scale,
            y: (center.y - state.y) / state.scale
          }
        };
        panStart = void 0;
      }
    };
    const pointerDown = (event) => {
      if (event.pointerType === "mouse" && event.button !== 0) return;
      event.preventDefault();
      pointers.set(event.pointerId, localPoint(event));
      stage.setPointerCapture(event.pointerId);
      stage.addClass("is-dragging");
      beginGesture();
    };
    const pointerMove = (event) => {
      if (!pointers.has(event.pointerId)) return;
      event.preventDefault();
      pointers.set(event.pointerId, localPoint(event));
      const points = Array.from(pointers.values());
      if (points.length >= 2 && pinchStart) {
        const center = midpoint(points[0], points[1]);
        Object.assign(state, pinchView(pinchStart, distance(points[0], points[1]), center));
      } else if (points.length === 1 && panStart) {
        Object.assign(state, panView(panStart, points[0]));
      }
      userChangedView = true;
      render();
    };
    const pointerEnd = (event) => {
      if (!pointers.has(event.pointerId)) return;
      pointers.delete(event.pointerId);
      if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
      if (pointers.size === 0) {
        stage.removeClass("is-dragging");
        panStart = void 0;
        pinchStart = void 0;
      } else {
        beginGesture();
      }
    };
    const wheel = (event) => {
      event.preventDefault();
      const delta = event.deltaMode === event.DOM_DELTA_LINE ? event.deltaY * 16 : event.deltaY;
      zoomAt(Math.exp(-delta * 15e-4), localPoint(event));
    };
    const doubleClick = (event) => {
      event.preventDefault();
      fit();
    };
    stage.addEventListener("pointerdown", pointerDown);
    stage.addEventListener("pointermove", pointerMove);
    stage.addEventListener("pointerup", pointerEnd);
    stage.addEventListener("pointercancel", pointerEnd);
    stage.addEventListener("wheel", wheel, { passive: false });
    stage.addEventListener("dblclick", doubleClick);
    const resizeObserver = new ResizeObserver(() => {
      if (!initialized || !userChangedView) fitInternal();
    });
    resizeObserver.observe(stage);
    return {
      zoom: (factor) => zoomAt(factor),
      fit,
      cleanup: () => {
        disposed = true;
        ownerWindow.cancelAnimationFrame(initFrame);
        resizeObserver.disconnect();
        stage.removeEventListener("pointerdown", pointerDown);
        stage.removeEventListener("pointermove", pointerMove);
        stage.removeEventListener("pointerup", pointerEnd);
        stage.removeEventListener("pointercancel", pointerEnd);
        stage.removeEventListener("wheel", wheel);
        stage.removeEventListener("dblclick", doubleClick);
      }
    };
  }
};

// src/diagram-registry.ts
var HOST_SELECTOR = ".mermaid, .mermaid-preview";
var MOUNTED_CLASS = "mermaid-lens-host";
var openViewer = (app, svg) => new MermaidViewerModal(app, svg).open();
function asElement(value) {
  return value !== null && typeof value.closest === "function" ? value : null;
}
var DiagramRegistry = class {
  constructor(app, options, viewerOpener = openViewer) {
    this.handlers = /* @__PURE__ */ new WeakMap();
    this.observers = /* @__PURE__ */ new Map();
    this.app = app;
    this.options = options;
    this.viewerOpener = viewerOpener;
  }
  scan(root) {
    this.observe(root);
    this.scanNow(root);
  }
  refresh(roots) {
    for (const root of roots) {
      this.scan(root);
      root.querySelectorAll(`.${MOUNTED_CLASS}`).forEach((host) => {
        this.syncHostState(host);
      });
    }
  }
  dispose(roots) {
    for (const root of roots) {
      for (const [observedRoot, observer] of this.observers) {
        if (observedRoot === root || root.contains(observedRoot)) {
          observer.disconnect();
          this.observers.delete(observedRoot);
        }
      }
      const hosts = root.nodeType === 1 && root.matches(`.${MOUNTED_CLASS}`) ? [root, ...Array.from(root.querySelectorAll(`.${MOUNTED_CLASS}`))] : Array.from(root.querySelectorAll(`.${MOUNTED_CLASS}`));
      hosts.forEach((host) => this.unmount(host));
    }
  }
  disposeAll() {
    for (const observer of this.observers.values()) observer.disconnect();
    this.observers.clear();
  }
  observe(root) {
    var _a;
    if (this.observers.has(root)) return;
    const document = root.nodeType === 9 ? root : root.ownerDocument;
    const Observer = (_a = document == null ? void 0 : document.defaultView) == null ? void 0 : _a.MutationObserver;
    if (!Observer) return;
    const observer = new Observer((mutations) => {
      for (const mutation of mutations) this.scanNow(mutation.target);
    });
    observer.observe(root, { childList: true, subtree: true });
    this.observers.set(root, observer);
  }
  scanNow(root) {
    if (root.nodeType === 1) {
      const element = root;
      if (element.matches(HOST_SELECTOR)) this.mount(element);
    }
    root.querySelectorAll(HOST_SELECTOR).forEach((host) => this.mount(host));
  }
  unmount(host) {
    var _a;
    const handlers = this.handlers.get(host);
    if (handlers) {
      host.removeEventListener("click", handlers.click);
      host.removeEventListener("dblclick", handlers.doubleClick);
      this.handlers.delete(host);
    }
    (_a = host.querySelector(":scope > .mermaid-lens-expand")) == null ? void 0 : _a.remove();
    host.removeAttribute("data-mermaid-lens-trigger");
    host.removeClass(MOUNTED_CLASS);
  }
  mount(host) {
    if (!host.querySelector("svg")) return;
    if (!this.handlers.has(host)) {
      const handlers = {
        click: (event) => this.handleOpenEvent(host, event, "single"),
        doubleClick: (event) => this.handleOpenEvent(host, event, "double")
      };
      this.handlers.set(host, handlers);
      host.addEventListener("click", handlers.click);
      host.addEventListener("dblclick", handlers.doubleClick);
      host.addClass(MOUNTED_CLASS);
    }
    this.syncHostState(host);
  }
  syncHostState(host) {
    host.dataset.mermaidLensTrigger = this.options.getTrigger();
    let button = host.querySelector(":scope > .mermaid-lens-expand");
    if (!this.options.showExpandButton()) {
      button == null ? void 0 : button.remove();
      return;
    }
    if (button) return;
    button = host.createEl("button", {
      cls: "mermaid-lens-expand",
      attr: { "aria-label": t("diagram.openViewer"), title: t("diagram.openLarge") }
    });
    (0, import_obsidian4.setIcon)(button, "expand");
    button.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      this.open(host);
    });
  }
  handleOpenEvent(host, event, eventTrigger) {
    if (this.options.getTrigger() !== eventTrigger) return;
    const target = asElement(event.target);
    if (!target || target.closest("a, button")) return;
    event.preventDefault();
    event.stopPropagation();
    this.open(host);
  }
  open(host) {
    const svg = host.querySelector("svg");
    if (svg) this.viewerOpener(this.app, svg);
  }
};

// src/settings.ts
var import_obsidian5 = require("obsidian");
var DEFAULT_CONFIG = {
  theme: "base",
  themeVariables: {
    fontFamily: "Inter, Microsoft YaHei, sans-serif",
    primaryColor: "#EEF2FF",
    primaryBorderColor: "#6366F1",
    primaryTextColor: "#1E293B",
    lineColor: "#64748B",
    signalColor: "#334155",
    signalTextColor: "#334155",
    actorBkg: "#6366F1",
    actorBorder: "#4F46E5",
    actorTextColor: "#FFFFFF",
    labelTextColor: "#FFFFFF",
    loopTextColor: "#334155",
    noteBkgColor: "#FEF3C7",
    noteBorderColor: "#F59E0B",
    noteTextColor: "#78350F"
  },
  sequence: {
    useMaxWidth: true,
    actorMargin: 40,
    messageMargin: 30,
    mirrorActors: true
  }
};
var DEFAULT_SETTINGS = {
  configJson: JSON.stringify(DEFAULT_CONFIG, null, 2),
  openTrigger: "single",
  showExpandButton: true
};
function normalizeSettings(value) {
  const trigger = value == null ? void 0 : value.openTrigger;
  return {
    configJson: typeof (value == null ? void 0 : value.configJson) === "string" ? value.configJson : DEFAULT_SETTINGS.configJson,
    openTrigger: trigger === "single" || trigger === "double" || trigger === "button" ? trigger : DEFAULT_SETTINGS.openTrigger,
    showExpandButton: typeof (value == null ? void 0 : value.showExpandButton) === "boolean" ? value.showExpandButton : DEFAULT_SETTINGS.showExpandButton
  };
}
var MermaidLensSettingTab = class extends import_obsidian5.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.draftConfig = "";
    this.plugin = plugin;
  }
  getSettingDefinitions() {
    return [
      {
        name: t("settings.config.name"),
        desc: t("settings.config.desc"),
        aliases: [t("settings.config.aliasJson"), t("settings.config.aliasInitialize")],
        render: (setting) => this.renderConfigInput(setting)
      },
      {
        name: t("settings.actions.name"),
        desc: t("settings.actions.desc"),
        aliases: [t("settings.actions.apply"), t("settings.actions.reset")],
        render: (setting) => this.renderConfigActions(setting)
      },
      {
        name: t("settings.trigger.name"),
        desc: t("settings.trigger.desc"),
        aliases: [
          t("settings.trigger.aliasSingle"),
          t("settings.trigger.aliasDouble"),
          t("settings.trigger.aliasButton")
        ],
        render: (setting) => this.renderOpenTrigger(setting)
      },
      {
        name: t("settings.expandButton.name"),
        desc: t("settings.expandButton.desc"),
        aliases: [t("settings.expandButton.aliasLarge"), t("settings.expandButton.aliasViewer")],
        render: (setting) => this.renderExpandButtonToggle(setting)
      }
    ];
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    this.renderLegacySetting(
      t("settings.config.name"),
      t("settings.config.desc"),
      (setting) => this.renderConfigInput(setting)
    );
    this.renderLegacySetting(
      t("settings.actions.name"),
      t("settings.actions.desc"),
      (setting) => this.renderConfigActions(setting)
    );
    this.renderLegacySetting(
      t("settings.trigger.name"),
      t("settings.trigger.desc"),
      (setting) => this.renderOpenTrigger(setting)
    );
    this.renderLegacySetting(
      t("settings.expandButton.name"),
      t("settings.expandButton.desc"),
      (setting) => this.renderExpandButtonToggle(setting)
    );
  }
  renderLegacySetting(name, desc, render) {
    const setting = new import_obsidian5.Setting(this.containerEl).setName(name).setDesc(desc);
    render(setting);
  }
  renderConfigInput(setting) {
    setting.setClass("mermaid-lens-config-setting");
    this.draftConfig = this.plugin.settings.configJson;
    setting.addTextArea((text) => {
      this.configInput = text;
      text.setValue(this.draftConfig).setPlaceholder('{\n  "theme": "base"\n}').onChange((value) => {
        this.draftConfig = value;
      });
      text.inputEl.rows = 24;
      text.inputEl.addClass("mermaid-lens-config-input");
    });
  }
  renderConfigActions(setting) {
    setting.addButton((button) => button.setButtonText(t("settings.actions.apply")).setCta().onClick(async () => {
      try {
        await this.plugin.applyConfig(this.draftConfig);
        new import_obsidian5.Notice(t("notice.configApplied"));
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        new import_obsidian5.Notice(t("notice.invalidConfig", { message }));
      }
    })).addButton((button) => button.setButtonText(t("settings.actions.reset")).onClick(async () => {
      var _a;
      try {
        await this.plugin.applyConfig(DEFAULT_SETTINGS.configJson);
        this.draftConfig = DEFAULT_SETTINGS.configJson;
        (_a = this.configInput) == null ? void 0 : _a.setValue(this.draftConfig);
        new import_obsidian5.Notice(t("notice.defaultsRestored"));
      } catch (error) {
        console.error("[mermaid-lens] Failed to restore default config", error);
        new import_obsidian5.Notice(t("notice.restoreDefaultsFailed"));
      }
    }));
  }
  renderOpenTrigger(setting) {
    setting.addDropdown((dropdown) => dropdown.addOption("single", t("settings.trigger.single")).addOption("double", t("settings.trigger.double")).addOption("button", t("settings.trigger.button")).setValue(this.plugin.settings.openTrigger).onChange(async (value) => {
      this.plugin.settings.openTrigger = value;
      await this.plugin.saveSettings();
      this.plugin.refreshDiagramControls();
    }));
  }
  renderExpandButtonToggle(setting) {
    setting.addToggle((toggle) => toggle.setValue(this.plugin.settings.showExpandButton).onChange(async (value) => {
      this.plugin.settings.showExpandButton = value;
      await this.plugin.saveSettings();
      this.plugin.refreshDiagramControls();
    }));
  }
};

// src/main.ts
var MermaidLensPlugin = class extends import_obsidian6.Plugin {
  constructor() {
    super(...arguments);
    this.settings = { ...DEFAULT_SETTINGS };
    this.configManager = new MermaidConfigManager();
    this.timers = /* @__PURE__ */ new Set();
    this.loaded = false;
    this.activeConfigJson = DEFAULT_SETTINGS.configJson;
  }
  async onload() {
    this.loaded = true;
    await this.loadSettings();
    this.addSettingTab(new MermaidLensSettingTab(this.app, this));
    let initialConfigJson = this.settings.configJson;
    let initialConfig;
    try {
      initialConfig = parseConfigJson(initialConfigJson);
    } catch (error) {
      initialConfigJson = DEFAULT_SETTINGS.configJson;
      initialConfig = parseConfigJson(initialConfigJson);
      new import_obsidian6.Notice(t("notice.savedConfigInvalid"));
      console.error("[mermaid-lens] Invalid saved config", error);
    }
    try {
      await this.configManager.install(initialConfig);
      this.activeConfigJson = initialConfigJson;
    } catch (error) {
      console.error("[mermaid-lens] Failed to apply saved config", error);
      new import_obsidian6.Notice(t("notice.applySavedConfigFailed"));
      await this.configManager.install(parseConfigJson(DEFAULT_SETTINGS.configJson));
      this.activeConfigJson = DEFAULT_SETTINGS.configJson;
    }
    this.registry = new DiagramRegistry(this.app, {
      getTrigger: () => this.settings.openTrigger,
      showExpandButton: () => this.settings.showExpandButton
    });
    this.registerMarkdownPostProcessor((element) => {
      var _a;
      (_a = this.registry) == null ? void 0 : _a.scan(element);
      this.scheduleScan(element);
    });
    this.registerEvent(this.app.workspace.on("layout-change", () => this.scanOpenViews()));
    this.registerEvent(this.app.workspace.on("active-leaf-change", () => this.scanOpenViews()));
    this.app.workspace.onLayoutReady(() => {
      if (!this.loaded) return;
      this.rerenderOpenMarkdownViews();
      this.scanOpenViews();
      for (const delay of [50, 250, 750]) this.scheduleScanOpenViews(delay);
    });
  }
  onunload() {
    var _a, _b;
    this.loaded = false;
    this.clearTimers();
    const roots = this.getMarkdownRoots();
    (_a = this.registry) == null ? void 0 : _a.dispose(roots);
    (_b = this.registry) == null ? void 0 : _b.disposeAll();
    this.registry = void 0;
    this.configManager.dispose();
  }
  async loadSettings() {
    const saved = await this.loadData();
    this.settings = normalizeSettings(saved);
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  async applyConfig(json) {
    const candidate = parseConfigJson(json);
    const previousJson = this.settings.configJson;
    const previousActiveJson = this.activeConfigJson;
    const previous = parseConfigJson(previousActiveJson);
    this.configManager.apply(candidate);
    this.settings.configJson = json;
    this.activeConfigJson = json;
    try {
      await this.saveSettings();
    } catch (error) {
      this.settings.configJson = previousJson;
      this.activeConfigJson = previousActiveJson;
      this.configManager.apply(previous);
      throw error;
    }
    this.rerenderOpenMarkdownViews();
    this.scanOpenViews();
    for (const delay of [50, 250, 750]) this.scheduleScanOpenViews(delay);
  }
  refreshDiagramControls() {
    var _a;
    (_a = this.registry) == null ? void 0 : _a.refresh(this.getMarkdownRoots());
  }
  getMarkdownViews() {
    const views = [];
    this.app.workspace.iterateAllLeaves((leaf) => {
      if (leaf.view instanceof import_obsidian6.MarkdownView) views.push(leaf.view);
    });
    return views;
  }
  getMarkdownRoots() {
    return this.getMarkdownViews().map((view) => view.containerEl);
  }
  scanOpenViews() {
    const registry = this.registry;
    if (!registry) return;
    for (const root of this.getMarkdownRoots()) registry.scan(root);
  }
  scheduleScan(root, delay = 100) {
    var _a;
    const document = root.nodeType === 9 ? root : root.ownerDocument;
    const ownerWindow = (_a = document == null ? void 0 : document.defaultView) != null ? _a : window;
    const timer = { ownerWindow, id: 0 };
    timer.id = ownerWindow.setTimeout(() => {
      var _a2;
      this.timers.delete(timer);
      (_a2 = this.registry) == null ? void 0 : _a2.scan(root);
    }, delay);
    this.timers.add(timer);
  }
  scheduleScanOpenViews(delay) {
    const ownerWindow = window;
    const timer = { ownerWindow, id: 0 };
    timer.id = ownerWindow.setTimeout(() => {
      this.timers.delete(timer);
      this.scanOpenViews();
    }, delay);
    this.timers.add(timer);
  }
  clearTimers() {
    for (const timer of this.timers) timer.ownerWindow.clearTimeout(timer.id);
    this.timers.clear();
  }
  /**
   * Obsidian has no public API for rerendering one Live Preview code block.
   * Preserve public editor state while forcing only views that contain Mermaid.
   */
  rerenderOpenMarkdownViews() {
    for (const view of this.getMarkdownViews()) {
      if (!view.containerEl.querySelector(".mermaid, .mermaid-preview")) continue;
      if (view.getMode() === "preview") {
        view.previewMode.rerender(true);
        continue;
      }
      const cursor = view.editor.getCursor();
      const scroll = view.editor.getScrollInfo();
      view.setViewData(view.getViewData(), false);
      view.editor.setCursor(cursor);
      view.editor.scrollTo(scroll.left, scroll.top);
    }
  }
};
