<#include "header.ftl">
<div class="container">
    <div class="row">
        <div class="col s12">
            <#assign showedPosts=1>
            <#list posts as post>
  		        <#if (post.status == "published")>
			        <div class="card hoverable">
				        <div class="card-content">
	          			<span class="card-title"><a href="${post.uri}"><h2><#escape x as x?xml>${post.title}</#escape></h2></a></span>
					        <div class="section">
	          			        ${post.date?string("dd MMMM yyyy")}
					        </div>
					        <div class="section">
					            <#if post.body?length lt 1000>
    					            <p class="flow-text">${post.body}</p>
					            <#else>
					                <#assign endOfParagraph = post.body?index_of("</p>")>
                          <#assign excerpt = post.body?substring(0,endOfParagraph)>
	          			            <p class="flow-text">
	          			                ${excerpt}
	          			                <br/>
	          			                ...
	          			            </p>
	          			    </#if>
					        </div>
				        </div>
				        <div class="card-action">
					        <a href="${post.uri}"><#escape x as x?xml>Leer</#escape></a>
				        </div>
			        </div>
			        <#assign showedPosts=showedPosts+1>
  		        </#if>
  		        <#if showedPosts gt 10>
  		            <#break>
  		        </#if>
  	        </#list>
        </div>
    </div>
</div>
<#include "footer.ftl">
