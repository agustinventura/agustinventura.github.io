<#include "header.ftl">

	<#include "menu.ftl">

	<div class="page-header">
		<h1><#escape x as x?xml>${content.title}</#escape></h1>
	</div>

	<p><em>${content.date?string("dd MMMM yyyy")}</em></p>

	<p>${content.body}</p>

	<hr />
	<div id="disqus_thread"></div>
<script>
    var disqus_config = function () {
        this.page.url = ${config.site_host}/${content.uri};
        this.page.identifier = ${content.uri};
    };
    (function() {
        var d = document, s = d.createElement('script');
        s.src = '//aguasnegras.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>
<#include "footer.ftl">
