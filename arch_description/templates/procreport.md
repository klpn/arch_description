---
documentclass: report
title: "Bevarandeförteckning"
---

{% macro unittable(parsignum, unitlist) -%}
| Förvarings-id | Omfatttning | Media | Förvaringsenhet | Placering | Kommentar |
| ------------- | ----------- | ----- | --------------- | --------- | --------- |
{% for unit in unitlist|sort(attribute='signum') -%}
|{{ parsignum }}:{{ unit.signum }} |{{ unit.extent }} |{{ unit.medium }} |{{ unit.unittype }} |{{ unit.place  }} |{{ unit.note }} |
{% endfor %}
{%- endmacro %}

# 0 Grupper av handlingar

{% for object in objlist %} 

## {{ object.signum }}. {{ object.header }}

Processer handlingarna uppkommit i: {{ object.processes }}

Kan omfattas av sekretess: {{ object.classified }}

Kommentar: {{ object.note }}

{{ unittable(object.signum, object.storage_units) }}

{% endfor %}

{% for division in divlist %}

# {{ division.signum }}. {{ division.header }}

{% for process in division.processes|sort(attribute='signum') %}

{% set concsignum = division.signum + '.' + process.signum %}

## {{ concsignum }}. {{ process.header }}

Handlingar som redovisas på processbeteckningen: {{ process.acts }}

Handlingar som redovisas separat: {{ process.acts_separate }}

Kan omfattas av sekretess: {{ process.classified }}

Kommentar: {{ process.note }}

{{ unittable(concsignum, process.storage_units) }}

{% for acttype in process.acttypes|sort(attribute='signum') %}

{% set concsignum = division.signum + '.' + process.signum + '-' + acttype.signum %}

###  {{ concsignum }}. {{ acttype.header }}

Kan omfattas av sekretess: {{ acttype.classified }}

Kommentar: {{ acttype.note }}

{{ unittable(concsignum, acttype.storage_units) }}

{% endfor %}
{% endfor %}
{% endfor %}
