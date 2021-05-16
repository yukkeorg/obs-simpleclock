"""
obs-simpleclock.py

Simple clock for OBS Studio.

* This program is under the MIT License.
  Please see LICENSE file for detail.
"""

import obspython as obs

import datetime
from contextlib import contextmanager

dt_format = ""
source_name = ""


@contextmanager
def obs_source(source_name):
    source = obs.obs_get_source_by_name(source_name)
    try:
        yield source
    finally:
        obs.obs_source_release(source)


@contextmanager
def obs_update_source():
    data = obs.obs_data_create()
    try:
        yield data
    finally:
        obs.obs_data_release(data)


def update_text():
    global dt_format
    global source_name

    with obs_source(source_name) as src:
        if src is not None:
            try:
                dtstr = datetime.datetime.now().strftime(dt_format)
            except Exception:
                dtstr = "Datetime format error"

            with obs_update_source() as data:
                obs.obs_data_set_string(data, "text", dtstr)
                obs.obs_source_update(src, data)


def refresh_pressed(props, prop):
    update_text()


def script_description():
    return "Simple Clock\n\nby yukkeorg"


def script_update(settings):
    global dt_format
    global source_name

    dt_format = obs.obs_data_get_string(settings, "format")
    source_name = obs.obs_data_get_string(settings, "source")

    obs.timer_remove(update_text)

    if dt_format != "" and source_name != "":
        obs.timer_add(update_text, 500)


def script_defaults(settings):
    ...


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "format", "Format", obs.OBS_TEXT_DEFAULT)
    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for s in sources:
            sid = obs.obs_source_get_unversioned_id(s)
            if sid == "text_gdiplus" or sid == "text_ft2_source":
                name = obs.obs_source_get_name(s)
                obs.obs_property_list_add_string(p, name, name)
        obs.source_list_release(s)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)

    return props
