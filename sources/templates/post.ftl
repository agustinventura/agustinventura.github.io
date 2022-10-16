<#include "header.ftl">
<div class="container">
<div class="row">
<div class="col s12">
		<h2 class="light-blue-text text-darken-1"><#escape x as x?xml>${content.title}</#escape></h2>
		<div class="section">
			${content.date?string("dd MMMM yyyy")}
		</div>
		<div class="section">
			${content.body}
		</div>
<div class="col s12">
<div id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = '${config.site_host}/${content.uri}';
        this.page.identifier = '${content.uri}';
    };
    (function() {
        var d = document, s = d.createElement('script');
        s.src = '//aguasnegras.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
</div>
</div>
</div>
</div>
<#include "footer.ftl">
