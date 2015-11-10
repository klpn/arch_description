---
documentclass: report
title: "Arkiv {{ archive.creator.crname }} {{ archive.period }}"
---

# Arkivbeskrivning
{{ description }}

{% for series in archive.series|sort(attribute='signum') %} 

# {{ series.signum }}. {{ series.header }}

{% for subseries in series.subseries|sort(attribute='signum') %} 
## {{ subseries.signum }}. {{ subseries.header }}
Arkivbildare: {{ archive.creator.crname }}

{% if subseries.note %}Anmärkning: {{ subseries.note }}{% endif %}

| Volym | Tid | Anmärkningar (t.ex.\ arkivalietyp) |
|-------|-----|------------------------------------| 
{% for volume in subseries.volumes|sort(attribute='volno') -%}
|{{ volume.volno }}| {{ volume.period }}|{% if volume.note %}{{ volume.note }}{% endif %}|
{% endfor %}
{% endfor %}

{% endfor %}
