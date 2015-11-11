---
documentclass: report
title: "Arkiv {{ archive.creator.crname }} {{ archive.period }}"
---

# Arkivbeskrivning
{{ description }}

{% for series in serlist %} 

# {{ series.signum }}. {{ series.header }}

Arkivbildare: {{ archive.creator.crname }}

{% if series.note %}Anmärkning: {{ series.note }}{% endif %}

| Volym | Tid | Anmärkningar (t.ex.\ arkivalietyp) |
|-------|-----|------------------------------------| 
{% for volume in series.volumes|sort(attribute='volno') -%}
|{{ volume.volno }}| {{ volume.period }}|{% if volume.note %}{{ volume.note }}{% endif %}|
{% endfor %}

{% endfor %}
