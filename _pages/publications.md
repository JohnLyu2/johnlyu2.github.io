---
layout: single
title: "Publications"
permalink: /publications/
author_profile: true
---

[Google Scholar](https://scholar.google.com/citations?user=1mr4DVgAAAAJ&hl=en) · [DBLP](https://dblp.org/pid/254/3011-2.html)

{% assign groups = "Peer-reviewed publications" | split: "|" %}
{% for group in groups %}
<h2>{{ group }}</h2>
<div class="publication-list">
{% assign previous_year = 0 %}
{% for paper in site.data.publications %}
{% if paper.id == "btor2select_student" or paper.id == "smtselect_foiks2026" %}{% continue %}{% endif %}
{% assign show = false %}
{% if forloop.parentloop.index == 1 and paper.preprint == false %}{% assign show = true %}{% endif %}
{% if forloop.parentloop.index == 2 and paper.preprint %}{% assign show = true %}{% endif %}
{% if show %}
{% if paper.year != previous_year %}<h3 class="publication-year">{{ paper.year }}</h3>{% assign previous_year = paper.year %}{% endif %}
<article class="publication-entry">
<h4><a href="{{ paper.url }}">{{ paper.title | escape }}</a></h4>
<p class="publication-authors">{% for author in paper.authors %}{% if author == "Zhengyang Lu" %}<strong>{{ author }}</strong>{% else %}{{ author | escape }}{% endif %}{% unless forloop.last %}, {% endunless %}{% endfor %}</p>
<p class="publication-venue">{{ paper.venue | escape }} · {{ paper.year }}</p>
<p class="publication-links"><a href="{{ paper.url }}">Paper</a>{% if paper.code %} · <a href="{{ paper.code }}">{% if paper.code contains 'gitlab' %}GitLab{% else %}GitHub{% endif %}</a>{% endif %}</p>
</article>
{% endif %}
{% endfor %}
</div>
{% endfor %}
