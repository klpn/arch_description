---
documentclass: report
papersize: a4paper
geometry: margin=3cm
lang: sv
mainfont: Arial
title: "Arkiv {{ archive.creator.crname }} {{ archive.period }}"
---

# Arkivbeskrivning
{{ description }}

\fancyhead{}
\fancyhead[le,lo]{\includegraphics[width=1cm]{{ '{' }}{{ logo }}{{ '}' }} 
\uppercase{Utbildningsförvaltningen}{{ '}' }}
\fancyhead[re,ro]{\uppercase{Arkivförteckning}{{ '}' }}

{% for series in serlist %} 

# {{ series.signum }}. {{ series.header }}

Arkivbildare: {{ archive.creator.crname }}

{% if series.note %}\noindent Anmärkning: {{ series.note }}{% endif %}

| Volym | Tid | Anmärkningar (t.ex.\ arkivalietyp) |
|-------|-----|------------------------------------| 
{% for volume in series.volumes|sort(attribute='volno') -%}
|{{ volume.volno }}| {{ volume.period }}|{% if volume.note %}{{ volume.note }}{% endif %}|
{% endfor %}

{% endfor %}
