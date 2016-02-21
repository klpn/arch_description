---
documentclass: article
papersize: a4paper
geometry: margin=3cm
lang: sv
mainfont: Arial
title: "Avlämning av arkivhandlingar enligt 9§ arkivlagen"
---

\fancyhead{}
\fancyhead[re,ro]{Till Stockholms Stadsarkiv}

Arkivbildare: {{ archive.creator.crname }}

| Signum | Serie | Antal volymer |
|--------|-------|---------------| 
{% for series in serlist -%}
{% if series.voltot -%} 
|{{ series.signum }}| {{ series.header }}|{{ series.voltot }}|
{% endif -%}
{% endfor %}

Antal volymer: {{ archive.voltot }}

Antal hyllmeter: {{ archive.extent }}

Detta reversal har upprättats i två exemplar, varav parterna tagit var sitt.

##För myndigheten
Datum

##För Stadsarkivet
Datum
