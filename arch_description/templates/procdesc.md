---
documentclass: article 
papersize: a4paper
geometry: margin=3cm
lang: sv
mainfont: Arial
title: "Arkivbeskrivning {{ creator.crname }}"
---

\fancyhead{}
\fancyhead[le,lo]{\includegraphics[width=1cm]{{ '{' }}{{ logo }}{{ '}' }} 
\uppercase{{ '{' }}{{ creator.crname }}{{ '}}' }}
\fancyhead[re,ro]{\uppercase{Arkivbeskrivning} {{ creator.procperiod }}{{ '}' }}

{{ description }}
