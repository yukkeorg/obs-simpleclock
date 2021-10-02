--[[
    obs-simpleclock.lua
]]

obs = obslua

text_format = ""
text_source = ""

----------------------------------------------
function update_text()
    local source = obs.obs_get_source_by_name(text_source);
    if source ~= nil then
        local dtstr = ""
        if not pcall(function ()
            dtstr = os.date(text_format)
        end) then
            dtstr = "Datetime format error"
        end
        local data = obs.obs_data_create()
        obs.obs_data_set_string(data, "text", dtstr)
        obs.obs_source_update(source, data)
        obs.obs_data_release(data)
        obs.obs_source_release(source)
    end
end

----------------------------------------------
function script_description()
    return "Simple Clock\n\nby yukkeorg"
end


function script_properties()
    local props = obs.obs_properties_create()

    obs.obs_properties_add_text(props,
                                "format",
                                "Format",
                                obs.OBS_TEXT_MULTILINE)

    local p = obs.obs_properties_add_list(props,
                                          "source",
                                          "Text Source",
                                          obs.OBS_COMBO_TYPE_EDITABLE,
                                          obs.OBS_COMBO_FORMAT_STRING)

    sources = obs.obs_enum_sources()
    if sources ~= nil then
        for _, s in ipairs(sources) do
            local sid = obs.obs_source_get_unversioned_id(s)
            if sid:find("^text_") ~= nil then
                local name = obs.obs_source_get_name(s)
                obs.obs_property_list_add_string(p, name, name)
            end
        end
        obs.source_list_release(sources)
    end

    return props
end


function script_update(settings)
    text_format = obs.obs_data_get_string(settings, "format")
    text_source = obs.obs_data_get_string(settings, "source")

    obs.timer_remove(update_text)

    if dt_format ~= "" and source_name ~= "" then
        obs.timer_add(update_text, 500)
    end
end
