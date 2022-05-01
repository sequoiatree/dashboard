!function(t){var n={};function e(a){if(n[a])return n[a].exports;var r=n[a]={i:a,l:!1,exports:{}};return t[a].call(r.exports,r,r.exports,e),r.l=!0,r.exports}e.m=t,e.c=n,e.d=function(t,n,a){e.o(t,n)||Object.defineProperty(t,n,{enumerable:!0,get:a})},e.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},e.t=function(t,n){if(1&n&&(t=e(t)),8&n)return t;if(4&n&&"object"==typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(e.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&n&&"string"!=typeof t)for(var r in t)e.d(a,r,function(n){return t[n]}.bind(null,r));return a},e.n=function(t){var n=t&&t.__esModule?function(){return t.default}:function(){return t};return e.d(n,"a",n),n},e.o=function(t,n){return Object.prototype.hasOwnProperty.call(t,n)},e.p="/static/scripts/",e(e.s=2)}([function(t,n,e){"use strict";function a(t){return Handlebars.compile(t.split("\n").map((function(t){return t=(t=t.replace(/^\s+/,"")).replace(/\s+$/,"")})).join(""),{strict:!0})}e.d(n,"c",(function(){return c})),e.d(n,"b",(function(){return s})),e.d(n,"a",(function(){return l}));const r=a('\n<div id="{{id}}-content" class="upload-content m-3">\n  {{{content}}}\n</div>\n'),o=a('\n<div class="d-flex flex-column justify-content-center h-100">\n  <div class="mx-1 px-3 py-2 text-center text-uppercase text-unselectable font-family-serif">\n    Drag and drop files or click to select.\n  </div>\n</div>\n'),i=a('\n<div class="transactions-container">\n  <table class="transactions-table font-family-monospace">\n  {{# each transactions}}\n    <tr>\n      <td class="px-2 date">\n        {{date}}\n      </td>\n      <td class="px-2 amount {{sign amount}} text-right border-left border-dark">\n        {{amount}}\n      </td>\n      <td class="account account-{{account}} border-left border-right border-dark">\n      </td>\n    </tr>\n  {{/ each}}\n  {{# each metrics}}\n    {{# each metrics}}\n      <tr>\n        {{# if @first}}\n          <td class="px-2 date text-center border-top border-dark" rowspan="3">\n            {{../period}}\n          </td>\n        {{/ if}}\n        <td class="px-2 amount {{sign amount}} text-right {{# if @first}} border-top {{/ if}} border-left border-dark">\n          {{amount}}\n        </td>\n        <td class="{{# if @first}} border-top {{/ if}} border-left border-right border-dark">\n        </td>\n      </tr>\n    {{/ each}}\n  {{/ each}}\n  </table>\n  <div class="scroll-window">\n    <table class="transactions-table font-family-monospace">\n      {{# each transactions}}\n        <tr>\n          <td class="px-2">\n            <span class="description">\n              {{clean_description}}\n            </span>\n            {{#if tag}}\n              <span id="tag-{{@index}}" class="ml-2 p-1 tag tag-{{concat tag}} font-family-sans-serif font-size-tiny">\n                {{tag}}\n              </span>\n            {{/if}}\n          </td>\n          <td id="copy-button-{{@index}}" class="px-2 copy-button">\n            <span class="fas fa-clone font-size-small"></span>\n          </td>\n        </tr>\n      {{/ each}}\n      {{# each metrics}}\n        {{# each metrics}}\n          <tr>\n            <td class="px-2 description {{# if @first}} border-top border-dark {{/ if}}" colspan="2">\n              {{description}}\n            </td>\n          </tr>\n        {{/ each}}\n      {{/ each}}\n    </table>\n  </div>\n</div>\n');function c(t,n){return r({id:t,content:n})}function s(){return o()}function l(t){return i(t)}Handlebars.registerHelper("decodeUploadContent",c),Handlebars.registerHelper("decodeUploadButton",s),Handlebars.registerHelper("decodeTransactions",l),Handlebars.registerHelper("sign",(function(t){return parseFloat(t)>0?"positive":"negative"})),Handlebars.registerHelper("concat",(function(t){return t.replace(" ","")}))},,function(t,n,e){t.exports=e(3)},function(t,n,e){"use strict";e.r(n);var a=e(0);$(window).on("load",(function(){!function(){function t(n=!0,e=null){var r=$("#textbox-pattern").val(),o=$("#textbox-alias").val(),i=n&&""!==r?{pattern:r,alias:o||null}:null;$.ajax({data:JSON.stringify({regex:i,tag_update:e}),contentType:"application/json",dataType:"json",method:"POST",url:"/transactions",success:function(r){0!==r.transactions.length&&($("#transactions").addClass("active"),$("#transactions-body")[0].innerHTML=a.a(r),$("#transactions .copy-button").each((function(t,n){$(n).click((function(e){t=n.id.replace(/^copy-button-/,""),navigator.clipboard.writeText(r.transactions[t].clean_description),e.stopPropagation()}))})),$("#transactions .tag").each((function(a,o){$(o).click((function(i){var c=r.tags,s=$(o).text(),l=c[(c.indexOf(s)+1)%c.length];a=o.id.replace(/^tag-/,""),t(n=!1,e={serialized_datum:r.transactions[a],new_tag:l}),i.stopPropagation()}))})),$("#button-regex").removeClass("disabled"),$("#textbox-pattern").val(""),$("#textbox-alias").val(""))}})}$("#button-transactions").click(t),$(document).on("keypress",(function(n){$("#index-nav-option-budgeting").hasClass("active")&&13===n.which&&t()}))}(),function(){var t=$("#textbox-target-VTI"),n=$("#textbox-target-VXUS"),e=$("#actual-VTI"),a=$("#actual-VXUS"),r=$("#current-balance-VTI"),o=$("#textbox-current-balance-VXUS"),i=$("#textbox-current-balance-total"),c=$("#to-invest-VTI"),s=$("#to-invest-VXUS"),l=$("#textbox-to-invest-total"),u=$("#to-fully-rebalance-VTI"),d=$("#to-fully-rebalance-VXUS"),f=$("#to-fully-rebalance-total"),p=$("#fully-rebalanced-VTI"),b=$("#fully-rebalanced-VXUS"),v=$("#fully-rebalanced-total");function x(t,n=null){var e;switch(n){case null:e=/^[\d,]*$/;break;case 1/0:e=/^[\d,]*\.?\d*$/;break;default:e=new RegExp(String.raw`^[\d,]*\.?\d{0,${n}}$`)}return""!==t&&e.test(t)}function g(t){var n=(t.is("input")?t.val():t.text()).replaceAll(",","");return x(n,1/0)?Math.round(parseFloat(n)):void 0}function m(t,n){var e=t.is("input");return"number"==typeof n&&(n=Math.round(n),n=Number(n).toLocaleString()),e?t.val(n):t.text(n)}function h(){var x,h,y,S,V,T,k,j,w,H=g(t),_=g(n),O=g(o),M=g(i),P=g(l);function U(t){var n=!0;return $(t).each((function(t,e){void 0===g(e)&&(n=!1)})),n}if($([e,a,c,s,u,d,f,p,b,v]).each((function(t,n){m(n,"-")})),U([o,i])){if((h=M-O)<0)return;x=100*O/M,m(e,100*h/M),m(a,x),m(r,h)}U([t,n,r,o,i,l])&&(y=P*(V=(j=(w=Math.max(M+P,100*h/H,100*O/_))*_/100)-O)/(T=w-M),m(c,P*(S=(k=w*H/100)-h)/T),m(s,y),m(u,S),m(d,V),m(f,T),m(p,k),m(b,j),m(v,w))}$([t,n,o,i,l]).each((function(t,n){n.on("input",(function(){var t=g(n);void 0!==t&&(n.val(t),m(n,t))})),function(t,n){t.prop("prevValue",t.val()),t.on("input",(function(){""===t.val()||n(t.val())?t.prop("prevValue",t.val()):t.val(t.prop("prevValue"))}))}(n,x)})),$([t,n]).each((function(e,a){a.on("input",(function(){var e=g(t),r=g(n);a.is(t)&&(0===e&&m(t,""),m(n,e?100-e:"")),a.is(n)&&(0===r&&m(n,""),m(t,r?100-r:"")),h()}))})),$([o,i,l]).each((function(t,n){n.on("input",h)}))}()}))}]);