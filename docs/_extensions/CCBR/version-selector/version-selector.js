/*
 * quarto-version-selector: version dropdown for Quarto websites.
 *
 * Expected gh-pages layout:
 *   /versions.json          [{version, title, aliases}, ...]
 *   /<version>/...          rendered site for each version
 *   /<alias>/...            copy of an aliased version (e.g. latest)
 */
(function () {
    "use strict";

    function meta(name, fallback) {
        var el = document.querySelector('meta[name="' + name + '"]');
        return el && el.content ? el.content : fallback;
    }

    // Root URL of the current version, using Quarto's per-page offset to the site root.
    function versionRoot() {
        var offset = meta("quarto:offset", "./");
        var root = new URL(offset, window.location.href);
        if (!root.pathname.endsWith("/")) root.pathname += "/";
        return root;
    }

    function lastSegment(url) {
        var parts = url.pathname.split("/").filter(Boolean);
        return parts.length ? decodeURIComponent(parts[parts.length - 1]) : "";
    }

    function el(tag, attrs, text) {
        var node = document.createElement(tag);
        Object.keys(attrs || {}).forEach(function (k) {
            node.setAttribute(k, attrs[k]);
        });
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function targetUrl(siteRoot, name, relPath) {
        return new URL(encodeURIComponent(name) + "/" + relPath, siteRoot);
    }

    // Navigate to the same page in another version; fall back to that version's root.
    function navigate(siteRoot, name, relPath) {
        var target = targetUrl(siteRoot, name, relPath);
        var fallback = targetUrl(siteRoot, name, "");
        if (!relPath || window.location.protocol === "file:") {
            window.location.href = target.href;
            return;
        }
        fetch(target.href, { method: "HEAD" })
            .then(function (r) {
                window.location.href = r.ok ? target.href : fallback.href;
            })
            .catch(function () {
                window.location.href = fallback.href;
            });
    }

    function build(versions, current, siteRoot, relPath) {
        var currentEntry = versions.find(function (v) {
            return v.version === current || (v.aliases || []).indexOf(current) !== -1;
        });
        var label = currentEntry ? currentEntry.title || currentEntry.version : current;

        var wrap = el("div", { class: "dropdown quarto-version-selector" });
        var button = el("button", {
            class: "btn dropdown-toggle quarto-version-selector-toggle",
            type: "button",
            "data-bs-toggle": "dropdown",
            "aria-expanded": "false",
            "aria-label": "Select documentation version",
        }, label);
        var menu = el("ul", { class: "dropdown-menu dropdown-menu-end quarto-version-selector-menu" });

        versions.forEach(function (v) {
            var li = el("li");
            var name = v.version;
            var a = el("a", { class: "dropdown-item", href: targetUrl(siteRoot, name, relPath).href });
            a.appendChild(el("span", { class: "quarto-version-selector-title" }, v.title || v.version));
            (v.aliases || []).forEach(function (alias) {
                a.appendChild(el("span", { class: "quarto-version-selector-alias" }, alias));
            });
            if (v === currentEntry) {
                a.classList.add("active");
                a.setAttribute("aria-current", "true");
            }
            a.addEventListener("click", function (ev) {
                // let the browser handle new-tab/window clicks (Ctrl/Cmd/Shift/Alt, middle button)
                if (ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) {
                    return;
                }
                ev.preventDefault();
                navigate(siteRoot, name, relPath);
            });
            li.appendChild(a);
            menu.appendChild(li);
        });

        wrap.appendChild(button);
        wrap.appendChild(menu);

        // Minimal toggle when Bootstrap's JS is not available.
        if (!(window.bootstrap && window.bootstrap.Dropdown)) {
            var setOpen = function (open) {
                menu.classList.toggle("show", open);
                button.setAttribute("aria-expanded", open ? "true" : "false");
            };
            button.addEventListener("click", function (ev) {
                ev.stopPropagation();
                setOpen(!menu.classList.contains("show"));
            });
            document.addEventListener("click", function (ev) {
                if (!wrap.contains(ev.target)) setOpen(false);
            });
            document.addEventListener("keydown", function (ev) {
                if (ev.key === "Escape" && menu.classList.contains("show")) {
                    setOpen(false);
                    button.focus();
                }
            });
        }
        return wrap;
    }

    function mount(widget, placement) {
        var custom = document.getElementById("version-selector");
        if (custom) {
            custom.appendChild(widget);
            return;
        }
        if (placement === "none") return;
        if (placement === "sidebar") {
            // Top of the docked sidebar; fall back to navbar-left without one.
            var sidebar = document.querySelector("#quarto-sidebar");
            if (sidebar) {
                widget.classList.add("quarto-version-selector-sidebar");
                sidebar.insertBefore(widget, sidebar.firstChild);
                return;
            }
            placement = "navbar-left";
        }
        var fixed = placement === "fixed-left" || placement === "fixed-right";
        if (!fixed) {
            var header = "#quarto-header ";
            var left = document.querySelector(header + ".navbar-collapse .navbar-nav.me-auto") ||
                document.querySelector(header + ".navbar-collapse .navbar-nav");
            var tools = document.querySelector(header + ".quarto-navbar-tools");
            var collapse = document.querySelector(header + ".navbar-collapse");
            var container = document.querySelector(header + ".navbar .container-fluid, " + header + ".navbar > .container");
            widget.classList.add("quarto-version-selector-navbar");
            if (placement === "navbar-right" && tools) {
                tools.insertBefore(widget, tools.firstChild);
                return;
            }
            if (placement !== "navbar-right" && left) {
                // First item of the left navbar menu, as a Bootstrap nav item.
                var item = document.createElement("li");
                item.className = "nav-item quarto-version-selector-item";
                item.appendChild(widget);
                left.insertBefore(item, left.firstChild);
                return;
            }
            var host = tools || collapse || container;
            if (host) {
                if (tools) host.insertBefore(widget, host.firstChild);
                else host.appendChild(widget);
                return;
            }
            widget.classList.remove("quarto-version-selector-navbar");
        }
        // No navbar: pin to the matching side (navbar-left -> fixed-left).
        var side = placement === "fixed-left" || placement === "navbar-left" ? "left" : "right";
        widget.classList.add("quarto-version-selector-fixed", "quarto-version-selector-fixed-" + side);
        document.body.appendChild(widget);
    }

    function init() {
        var root = versionRoot();
        var siteRoot = new URL("../", root);
        var current = lastSegment(root);
        var relPath = window.location.pathname.startsWith(root.pathname)
            ? window.location.pathname.slice(root.pathname.length)
            : "";
        var versionsFile = meta("version-selector:versions-file", "versions.json");
        var placement = meta("version-selector:placement", "navbar-left");

        fetch(new URL(versionsFile, siteRoot).href)
            .then(function (r) {
                if (!r.ok) throw new Error("HTTP " + r.status);
                return r.json();
            })
            .then(function (versions) {
                if (!Array.isArray(versions) || versions.length === 0) return;
                mount(build(versions, current, siteRoot, relPath + window.location.hash), placement);
            })
            .catch(function () {
                // No versions.json (e.g. local preview): render nothing.
            });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
