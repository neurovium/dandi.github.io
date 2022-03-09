---
layout: default
title: Events
excerpt: "Events."
permalink: /events
sitemap: true
---
<h1>Upcoming events</h1>

{% assign number_printed = 0 %}
{% for event in site.events %}

<div class="col-sm-6 clearfix">
 <div class="well">
  <a href="{{ site.baseurl }}{{ event.url }}">
    <pubtit>{{ event.title }}</pubtit>
  </a>
  {{ event.excerpt }}
 </div>
</div>

{% endfor %}
