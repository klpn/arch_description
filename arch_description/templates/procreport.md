---
documentclass: report
papersize: a4paper
geometry: margin=3cm
lang: sv
mainfont: Arial
title: "Bevarandeförteckning {{ creator.crname }} {{ creator.procperiod }}"
---

\fancyhead{}
\fancyhead[le,lo]{\includegraphics[width=1cm]{{ '{' }}{{ logo }}{{ '}' }} 
\uppercase{{ '{' }}{{ creator.crname }}{{ '}}' }}
\fancyhead[re,ro]{\uppercase{Bevarandeförteckning} {{ creator.procperiod }}{{ '}' }}

{% macro unittable(parsignum, unitlist) -%}
| Förvarings-id | Omfatttning | Media | Förvaringsenhet | Placering | Kommentar |
| ------------- | ----------- | ----- | --------------- | --------- | --------- |
{% for unit in unitlist|sort(attribute='signum') -%}
|{{ parsignum }}:{{ unit.signum }} |{{ unit.extent }} |{{ unit.medium }} |{{ unit.unittype }} |{{ unit.place  }} |{% if unit.note %}{{ unit.note }}{% endif %} |
{% endfor %}
{%- endmacro %}

# 0. Grupper av handlingar

{% for object in objlist %} 

## {{ object.signum }}. {{ object.header }}

Processer handlingarna uppkommit i: {{ object.processes }}

Kan omfattas av sekretess: {{ object.classified }}

Kommentar: {% if object.note %}{{ object.note }}{% endif %}

{{ unittable(object.signum, object.storage_units) }}

{% endfor %}

{% for division in divlist %}

# {{ division.signum }}. {{ division.header }}

{% for process in division.processes|sort(attribute='signum') %}

{% set concsignum = division.signum + '.' + process.signum %}

## {{ concsignum }}. {{ process.header }}

Handlingar som redovisas på processbeteckningen: {% if process.acts %}{{ process.acts }}{% endif %}

Handlingar som redovisas separat: {% if process.acts_separate %}{{ process.acts_separate }}{% endif %}

Kan omfattas av sekretess: {{ process.classified }}

Kommentar: {% if process.note %}{{ process.note }}{% endif %}

{{ unittable(concsignum, process.storage_units) }}

{% for acttype in process.acttypes|sort(attribute='signum') %}

{% set concsignum = division.signum + '.' + process.signum + '-' + acttype.signum %}

###  {{ concsignum }}. {{ acttype.header }}

Kan omfattas av sekretess: {{ acttype.classified }}

Kommentar: {% if acttype.note %}{{ acttype.note }}{% endif %}

{{ unittable(concsignum, acttype.storage_units) }}

{% endfor %}
{% endfor %}
{% endfor %}
