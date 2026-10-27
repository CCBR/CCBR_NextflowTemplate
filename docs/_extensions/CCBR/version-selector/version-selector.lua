-- Attach the version selector JS/CSS to HTML outputs.
-- Works with any HTML-based format (html, fnl-html, ...).
--
-- Optional document/project metadata:
--   version-selector:
--     versions-file: versions.json   # path relative to the site root of all versions
--     placement: navbar-left         # navbar-left | navbar-right | fixed-left | fixed-right | sidebar | none

-- The extension's version is read from the VERSION file next to this script,
-- the single source of truth also used by the Python package and release tooling.
local function read_version()
    local file = io.open(quarto.utils.resolve_path("VERSION"), "r")
    if file == nil then
        return "0.0.0"
    end
    local version = file:read("*l") or ""
    file:close()
    version = version:gsub("^%s+", ""):gsub("%s+$", "")
    if version == "" then
        return "0.0.0"
    end
    return version
end

local function meta_string(value, default)
    if value == nil then
        return default
    end
    return pandoc.utils.stringify(value)
end

function Meta(meta)
    if not quarto.doc.is_format("html") then
        return meta
    end

    local opts = meta["version-selector"] or {}
    local versions_file = meta_string(opts["versions-file"], "versions.json")
    local valid = {
        ["navbar-left"] = true,
        ["navbar-right"] = true,
        ["fixed-left"] = true,
        ["fixed-right"] = true,
        ["sidebar"] = true,
        ["none"] = true,
    }
    local placement = meta_string(opts["placement"], "navbar-left")
    if not valid[placement] then
        quarto.log.warning(string.format(
            "version-selector: unknown placement '%s'; expected navbar-left, navbar-right, " ..
            "fixed-left, fixed-right, sidebar, or none. Using navbar-left.", placement
        ))
        placement = "navbar-left"
    end

    quarto.doc.add_html_dependency({
        name = "version-selector",
        version = read_version(),
        scripts = { { path = "version-selector.js", afterBody = true } },
        stylesheets = { "version-selector.css" },
    })
    quarto.doc.include_text("in-header", string.format(
        '<meta name="version-selector:versions-file" content="%s">\n' ..
        '<meta name="version-selector:placement" content="%s">\n',
        versions_file, placement
    ))
    return meta
end
