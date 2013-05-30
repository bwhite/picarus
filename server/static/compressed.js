/*! jQuery v1.9.1 | (c) 2005, 2012 jQuery Foundation, Inc. | jquery.org/license
//@ sourceMappingURL=jquery.min.map
*/(function(e,t){var n,r,i=typeof t,o=e.document,a=e.location,s=e.jQuery,u=e.$,l={},c=[],p="1.9.1",f=c.concat,d=c.push,h=c.slice,g=c.indexOf,m=l.toString,y=l.hasOwnProperty,v=p.trim,b=function(e,t){return new b.fn.init(e,t,r)},x=/[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,w=/\S+/g,T=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,N=/^(?:(<[\w\W]+>)[^>]*|#([\w-]*))$/,C=/^<(\w+)\s*\/?>(?:<\/\1>|)$/,k=/^[\],:{}\s]*$/,E=/(?:^|:|,)(?:\s*\[)+/g,S=/\\(?:["\\\/bfnrt]|u[\da-fA-F]{4})/g,A=/"[^"\\\r\n]*"|true|false|null|-?(?:\d+\.|)\d+(?:[eE][+-]?\d+|)/g,j=/^-ms-/,D=/-([\da-z])/gi,L=function(e,t){return t.toUpperCase()},H=function(e){(o.addEventListener||"load"===e.type||"complete"===o.readyState)&&(q(),b.ready())},q=function(){o.addEventListener?(o.removeEventListener("DOMContentLoaded",H,!1),e.removeEventListener("load",H,!1)):(o.detachEvent("onreadystatechange",H),e.detachEvent("onload",H))};b.fn=b.prototype={jquery:p,constructor:b,init:function(e,n,r){var i,a;if(!e)return this;if("string"==typeof e){if(i="<"===e.charAt(0)&&">"===e.charAt(e.length-1)&&e.length>=3?[null,e,null]:N.exec(e),!i||!i[1]&&n)return!n||n.jquery?(n||r).find(e):this.constructor(n).find(e);if(i[1]){if(n=n instanceof b?n[0]:n,b.merge(this,b.parseHTML(i[1],n&&n.nodeType?n.ownerDocument||n:o,!0)),C.test(i[1])&&b.isPlainObject(n))for(i in n)b.isFunction(this[i])?this[i](n[i]):this.attr(i,n[i]);return this}if(a=o.getElementById(i[2]),a&&a.parentNode){if(a.id!==i[2])return r.find(e);this.length=1,this[0]=a}return this.context=o,this.selector=e,this}return e.nodeType?(this.context=this[0]=e,this.length=1,this):b.isFunction(e)?r.ready(e):(e.selector!==t&&(this.selector=e.selector,this.context=e.context),b.makeArray(e,this))},selector:"",length:0,size:function(){return this.length},toArray:function(){return h.call(this)},get:function(e){return null==e?this.toArray():0>e?this[this.length+e]:this[e]},pushStack:function(e){var t=b.merge(this.constructor(),e);return t.prevObject=this,t.context=this.context,t},each:function(e,t){return b.each(this,e,t)},ready:function(e){return b.ready.promise().done(e),this},slice:function(){return this.pushStack(h.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},eq:function(e){var t=this.length,n=+e+(0>e?t:0);return this.pushStack(n>=0&&t>n?[this[n]]:[])},map:function(e){return this.pushStack(b.map(this,function(t,n){return e.call(t,n,t)}))},end:function(){return this.prevObject||this.constructor(null)},push:d,sort:[].sort,splice:[].splice},b.fn.init.prototype=b.fn,b.extend=b.fn.extend=function(){var e,n,r,i,o,a,s=arguments[0]||{},u=1,l=arguments.length,c=!1;for("boolean"==typeof s&&(c=s,s=arguments[1]||{},u=2),"object"==typeof s||b.isFunction(s)||(s={}),l===u&&(s=this,--u);l>u;u++)if(null!=(o=arguments[u]))for(i in o)e=s[i],r=o[i],s!==r&&(c&&r&&(b.isPlainObject(r)||(n=b.isArray(r)))?(n?(n=!1,a=e&&b.isArray(e)?e:[]):a=e&&b.isPlainObject(e)?e:{},s[i]=b.extend(c,a,r)):r!==t&&(s[i]=r));return s},b.extend({noConflict:function(t){return e.$===b&&(e.$=u),t&&e.jQuery===b&&(e.jQuery=s),b},isReady:!1,readyWait:1,holdReady:function(e){e?b.readyWait++:b.ready(!0)},ready:function(e){if(e===!0?!--b.readyWait:!b.isReady){if(!o.body)return setTimeout(b.ready);b.isReady=!0,e!==!0&&--b.readyWait>0||(n.resolveWith(o,[b]),b.fn.trigger&&b(o).trigger("ready").off("ready"))}},isFunction:function(e){return"function"===b.type(e)},isArray:Array.isArray||function(e){return"array"===b.type(e)},isWindow:function(e){return null!=e&&e==e.window},isNumeric:function(e){return!isNaN(parseFloat(e))&&isFinite(e)},type:function(e){return null==e?e+"":"object"==typeof e||"function"==typeof e?l[m.call(e)]||"object":typeof e},isPlainObject:function(e){if(!e||"object"!==b.type(e)||e.nodeType||b.isWindow(e))return!1;try{if(e.constructor&&!y.call(e,"constructor")&&!y.call(e.constructor.prototype,"isPrototypeOf"))return!1}catch(n){return!1}var r;for(r in e);return r===t||y.call(e,r)},isEmptyObject:function(e){var t;for(t in e)return!1;return!0},error:function(e){throw Error(e)},parseHTML:function(e,t,n){if(!e||"string"!=typeof e)return null;"boolean"==typeof t&&(n=t,t=!1),t=t||o;var r=C.exec(e),i=!n&&[];return r?[t.createElement(r[1])]:(r=b.buildFragment([e],t,i),i&&b(i).remove(),b.merge([],r.childNodes))},parseJSON:function(n){return e.JSON&&e.JSON.parse?e.JSON.parse(n):null===n?n:"string"==typeof n&&(n=b.trim(n),n&&k.test(n.replace(S,"@").replace(A,"]").replace(E,"")))?Function("return "+n)():(b.error("Invalid JSON: "+n),t)},parseXML:function(n){var r,i;if(!n||"string"!=typeof n)return null;try{e.DOMParser?(i=new DOMParser,r=i.parseFromString(n,"text/xml")):(r=new ActiveXObject("Microsoft.XMLDOM"),r.async="false",r.loadXML(n))}catch(o){r=t}return r&&r.documentElement&&!r.getElementsByTagName("parsererror").length||b.error("Invalid XML: "+n),r},noop:function(){},globalEval:function(t){t&&b.trim(t)&&(e.execScript||function(t){e.eval.call(e,t)})(t)},camelCase:function(e){return e.replace(j,"ms-").replace(D,L)},nodeName:function(e,t){return e.nodeName&&e.nodeName.toLowerCase()===t.toLowerCase()},each:function(e,t,n){var r,i=0,o=e.length,a=M(e);if(n){if(a){for(;o>i;i++)if(r=t.apply(e[i],n),r===!1)break}else for(i in e)if(r=t.apply(e[i],n),r===!1)break}else if(a){for(;o>i;i++)if(r=t.call(e[i],i,e[i]),r===!1)break}else for(i in e)if(r=t.call(e[i],i,e[i]),r===!1)break;return e},trim:v&&!v.call("\ufeff\u00a0")?function(e){return null==e?"":v.call(e)}:function(e){return null==e?"":(e+"").replace(T,"")},makeArray:function(e,t){var n=t||[];return null!=e&&(M(Object(e))?b.merge(n,"string"==typeof e?[e]:e):d.call(n,e)),n},inArray:function(e,t,n){var r;if(t){if(g)return g.call(t,e,n);for(r=t.length,n=n?0>n?Math.max(0,r+n):n:0;r>n;n++)if(n in t&&t[n]===e)return n}return-1},merge:function(e,n){var r=n.length,i=e.length,o=0;if("number"==typeof r)for(;r>o;o++)e[i++]=n[o];else while(n[o]!==t)e[i++]=n[o++];return e.length=i,e},grep:function(e,t,n){var r,i=[],o=0,a=e.length;for(n=!!n;a>o;o++)r=!!t(e[o],o),n!==r&&i.push(e[o]);return i},map:function(e,t,n){var r,i=0,o=e.length,a=M(e),s=[];if(a)for(;o>i;i++)r=t(e[i],i,n),null!=r&&(s[s.length]=r);else for(i in e)r=t(e[i],i,n),null!=r&&(s[s.length]=r);return f.apply([],s)},guid:1,proxy:function(e,n){var r,i,o;return"string"==typeof n&&(o=e[n],n=e,e=o),b.isFunction(e)?(r=h.call(arguments,2),i=function(){return e.apply(n||this,r.concat(h.call(arguments)))},i.guid=e.guid=e.guid||b.guid++,i):t},access:function(e,n,r,i,o,a,s){var u=0,l=e.length,c=null==r;if("object"===b.type(r)){o=!0;for(u in r)b.access(e,n,u,r[u],!0,a,s)}else if(i!==t&&(o=!0,b.isFunction(i)||(s=!0),c&&(s?(n.call(e,i),n=null):(c=n,n=function(e,t,n){return c.call(b(e),n)})),n))for(;l>u;u++)n(e[u],r,s?i:i.call(e[u],u,n(e[u],r)));return o?e:c?n.call(e):l?n(e[0],r):a},now:function(){return(new Date).getTime()}}),b.ready.promise=function(t){if(!n)if(n=b.Deferred(),"complete"===o.readyState)setTimeout(b.ready);else if(o.addEventListener)o.addEventListener("DOMContentLoaded",H,!1),e.addEventListener("load",H,!1);else{o.attachEvent("onreadystatechange",H),e.attachEvent("onload",H);var r=!1;try{r=null==e.frameElement&&o.documentElement}catch(i){}r&&r.doScroll&&function a(){if(!b.isReady){try{r.doScroll("left")}catch(e){return setTimeout(a,50)}q(),b.ready()}}()}return n.promise(t)},b.each("Boolean Number String Function Array Date RegExp Object Error".split(" "),function(e,t){l["[object "+t+"]"]=t.toLowerCase()});function M(e){var t=e.length,n=b.type(e);return b.isWindow(e)?!1:1===e.nodeType&&t?!0:"array"===n||"function"!==n&&(0===t||"number"==typeof t&&t>0&&t-1 in e)}r=b(o);var _={};function F(e){var t=_[e]={};return b.each(e.match(w)||[],function(e,n){t[n]=!0}),t}b.Callbacks=function(e){e="string"==typeof e?_[e]||F(e):b.extend({},e);var n,r,i,o,a,s,u=[],l=!e.once&&[],c=function(t){for(r=e.memory&&t,i=!0,a=s||0,s=0,o=u.length,n=!0;u&&o>a;a++)if(u[a].apply(t[0],t[1])===!1&&e.stopOnFalse){r=!1;break}n=!1,u&&(l?l.length&&c(l.shift()):r?u=[]:p.disable())},p={add:function(){if(u){var t=u.length;(function i(t){b.each(t,function(t,n){var r=b.type(n);"function"===r?e.unique&&p.has(n)||u.push(n):n&&n.length&&"string"!==r&&i(n)})})(arguments),n?o=u.length:r&&(s=t,c(r))}return this},remove:function(){return u&&b.each(arguments,function(e,t){var r;while((r=b.inArray(t,u,r))>-1)u.splice(r,1),n&&(o>=r&&o--,a>=r&&a--)}),this},has:function(e){return e?b.inArray(e,u)>-1:!(!u||!u.length)},empty:function(){return u=[],this},disable:function(){return u=l=r=t,this},disabled:function(){return!u},lock:function(){return l=t,r||p.disable(),this},locked:function(){return!l},fireWith:function(e,t){return t=t||[],t=[e,t.slice?t.slice():t],!u||i&&!l||(n?l.push(t):c(t)),this},fire:function(){return p.fireWith(this,arguments),this},fired:function(){return!!i}};return p},b.extend({Deferred:function(e){var t=[["resolve","done",b.Callbacks("once memory"),"resolved"],["reject","fail",b.Callbacks("once memory"),"rejected"],["notify","progress",b.Callbacks("memory")]],n="pending",r={state:function(){return n},always:function(){return i.done(arguments).fail(arguments),this},then:function(){var e=arguments;return b.Deferred(function(n){b.each(t,function(t,o){var a=o[0],s=b.isFunction(e[t])&&e[t];i[o[1]](function(){var e=s&&s.apply(this,arguments);e&&b.isFunction(e.promise)?e.promise().done(n.resolve).fail(n.reject).progress(n.notify):n[a+"With"](this===r?n.promise():this,s?[e]:arguments)})}),e=null}).promise()},promise:function(e){return null!=e?b.extend(e,r):r}},i={};return r.pipe=r.then,b.each(t,function(e,o){var a=o[2],s=o[3];r[o[1]]=a.add,s&&a.add(function(){n=s},t[1^e][2].disable,t[2][2].lock),i[o[0]]=function(){return i[o[0]+"With"](this===i?r:this,arguments),this},i[o[0]+"With"]=a.fireWith}),r.promise(i),e&&e.call(i,i),i},when:function(e){var t=0,n=h.call(arguments),r=n.length,i=1!==r||e&&b.isFunction(e.promise)?r:0,o=1===i?e:b.Deferred(),a=function(e,t,n){return function(r){t[e]=this,n[e]=arguments.length>1?h.call(arguments):r,n===s?o.notifyWith(t,n):--i||o.resolveWith(t,n)}},s,u,l;if(r>1)for(s=Array(r),u=Array(r),l=Array(r);r>t;t++)n[t]&&b.isFunction(n[t].promise)?n[t].promise().done(a(t,l,n)).fail(o.reject).progress(a(t,u,s)):--i;return i||o.resolveWith(l,n),o.promise()}}),b.support=function(){var t,n,r,a,s,u,l,c,p,f,d=o.createElement("div");if(d.setAttribute("className","t"),d.innerHTML="  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>",n=d.getElementsByTagName("*"),r=d.getElementsByTagName("a")[0],!n||!r||!n.length)return{};s=o.createElement("select"),l=s.appendChild(o.createElement("option")),a=d.getElementsByTagName("input")[0],r.style.cssText="top:1px;float:left;opacity:.5",t={getSetAttribute:"t"!==d.className,leadingWhitespace:3===d.firstChild.nodeType,tbody:!d.getElementsByTagName("tbody").length,htmlSerialize:!!d.getElementsByTagName("link").length,style:/top/.test(r.getAttribute("style")),hrefNormalized:"/a"===r.getAttribute("href"),opacity:/^0.5/.test(r.style.opacity),cssFloat:!!r.style.cssFloat,checkOn:!!a.value,optSelected:l.selected,enctype:!!o.createElement("form").enctype,html5Clone:"<:nav></:nav>"!==o.createElement("nav").cloneNode(!0).outerHTML,boxModel:"CSS1Compat"===o.compatMode,deleteExpando:!0,noCloneEvent:!0,inlineBlockNeedsLayout:!1,shrinkWrapBlocks:!1,reliableMarginRight:!0,boxSizingReliable:!0,pixelPosition:!1},a.checked=!0,t.noCloneChecked=a.cloneNode(!0).checked,s.disabled=!0,t.optDisabled=!l.disabled;try{delete d.test}catch(h){t.deleteExpando=!1}a=o.createElement("input"),a.setAttribute("value",""),t.input=""===a.getAttribute("value"),a.value="t",a.setAttribute("type","radio"),t.radioValue="t"===a.value,a.setAttribute("checked","t"),a.setAttribute("name","t"),u=o.createDocumentFragment(),u.appendChild(a),t.appendChecked=a.checked,t.checkClone=u.cloneNode(!0).cloneNode(!0).lastChild.checked,d.attachEvent&&(d.attachEvent("onclick",function(){t.noCloneEvent=!1}),d.cloneNode(!0).click());for(f in{submit:!0,change:!0,focusin:!0})d.setAttribute(c="on"+f,"t"),t[f+"Bubbles"]=c in e||d.attributes[c].expando===!1;return d.style.backgroundClip="content-box",d.cloneNode(!0).style.backgroundClip="",t.clearCloneStyle="content-box"===d.style.backgroundClip,b(function(){var n,r,a,s="padding:0;margin:0;border:0;display:block;box-sizing:content-box;-moz-box-sizing:content-box;-webkit-box-sizing:content-box;",u=o.getElementsByTagName("body")[0];u&&(n=o.createElement("div"),n.style.cssText="border:0;width:0;height:0;position:absolute;top:0;left:-9999px;margin-top:1px",u.appendChild(n).appendChild(d),d.innerHTML="<table><tr><td></td><td>t</td></tr></table>",a=d.getElementsByTagName("td"),a[0].style.cssText="padding:0;margin:0;border:0;display:none",p=0===a[0].offsetHeight,a[0].style.display="",a[1].style.display="none",t.reliableHiddenOffsets=p&&0===a[0].offsetHeight,d.innerHTML="",d.style.cssText="box-sizing:border-box;-moz-box-sizing:border-box;-webkit-box-sizing:border-box;padding:1px;border:1px;display:block;width:4px;margin-top:1%;position:absolute;top:1%;",t.boxSizing=4===d.offsetWidth,t.doesNotIncludeMarginInBodyOffset=1!==u.offsetTop,e.getComputedStyle&&(t.pixelPosition="1%"!==(e.getComputedStyle(d,null)||{}).top,t.boxSizingReliable="4px"===(e.getComputedStyle(d,null)||{width:"4px"}).width,r=d.appendChild(o.createElement("div")),r.style.cssText=d.style.cssText=s,r.style.marginRight=r.style.width="0",d.style.width="1px",t.reliableMarginRight=!parseFloat((e.getComputedStyle(r,null)||{}).marginRight)),typeof d.style.zoom!==i&&(d.innerHTML="",d.style.cssText=s+"width:1px;padding:1px;display:inline;zoom:1",t.inlineBlockNeedsLayout=3===d.offsetWidth,d.style.display="block",d.innerHTML="<div></div>",d.firstChild.style.width="5px",t.shrinkWrapBlocks=3!==d.offsetWidth,t.inlineBlockNeedsLayout&&(u.style.zoom=1)),u.removeChild(n),n=d=a=r=null)}),n=s=u=l=r=a=null,t}();var O=/(?:\{[\s\S]*\}|\[[\s\S]*\])$/,B=/([A-Z])/g;function P(e,n,r,i){if(b.acceptData(e)){var o,a,s=b.expando,u="string"==typeof n,l=e.nodeType,p=l?b.cache:e,f=l?e[s]:e[s]&&s;if(f&&p[f]&&(i||p[f].data)||!u||r!==t)return f||(l?e[s]=f=c.pop()||b.guid++:f=s),p[f]||(p[f]={},l||(p[f].toJSON=b.noop)),("object"==typeof n||"function"==typeof n)&&(i?p[f]=b.extend(p[f],n):p[f].data=b.extend(p[f].data,n)),o=p[f],i||(o.data||(o.data={}),o=o.data),r!==t&&(o[b.camelCase(n)]=r),u?(a=o[n],null==a&&(a=o[b.camelCase(n)])):a=o,a}}function R(e,t,n){if(b.acceptData(e)){var r,i,o,a=e.nodeType,s=a?b.cache:e,u=a?e[b.expando]:b.expando;if(s[u]){if(t&&(o=n?s[u]:s[u].data)){b.isArray(t)?t=t.concat(b.map(t,b.camelCase)):t in o?t=[t]:(t=b.camelCase(t),t=t in o?[t]:t.split(" "));for(r=0,i=t.length;i>r;r++)delete o[t[r]];if(!(n?$:b.isEmptyObject)(o))return}(n||(delete s[u].data,$(s[u])))&&(a?b.cleanData([e],!0):b.support.deleteExpando||s!=s.window?delete s[u]:s[u]=null)}}}b.extend({cache:{},expando:"jQuery"+(p+Math.random()).replace(/\D/g,""),noData:{embed:!0,object:"clsid:D27CDB6E-AE6D-11cf-96B8-444553540000",applet:!0},hasData:function(e){return e=e.nodeType?b.cache[e[b.expando]]:e[b.expando],!!e&&!$(e)},data:function(e,t,n){return P(e,t,n)},removeData:function(e,t){return R(e,t)},_data:function(e,t,n){return P(e,t,n,!0)},_removeData:function(e,t){return R(e,t,!0)},acceptData:function(e){if(e.nodeType&&1!==e.nodeType&&9!==e.nodeType)return!1;var t=e.nodeName&&b.noData[e.nodeName.toLowerCase()];return!t||t!==!0&&e.getAttribute("classid")===t}}),b.fn.extend({data:function(e,n){var r,i,o=this[0],a=0,s=null;if(e===t){if(this.length&&(s=b.data(o),1===o.nodeType&&!b._data(o,"parsedAttrs"))){for(r=o.attributes;r.length>a;a++)i=r[a].name,i.indexOf("data-")||(i=b.camelCase(i.slice(5)),W(o,i,s[i]));b._data(o,"parsedAttrs",!0)}return s}return"object"==typeof e?this.each(function(){b.data(this,e)}):b.access(this,function(n){return n===t?o?W(o,e,b.data(o,e)):null:(this.each(function(){b.data(this,e,n)}),t)},null,n,arguments.length>1,null,!0)},removeData:function(e){return this.each(function(){b.removeData(this,e)})}});function W(e,n,r){if(r===t&&1===e.nodeType){var i="data-"+n.replace(B,"-$1").toLowerCase();if(r=e.getAttribute(i),"string"==typeof r){try{r="true"===r?!0:"false"===r?!1:"null"===r?null:+r+""===r?+r:O.test(r)?b.parseJSON(r):r}catch(o){}b.data(e,n,r)}else r=t}return r}function $(e){var t;for(t in e)if(("data"!==t||!b.isEmptyObject(e[t]))&&"toJSON"!==t)return!1;return!0}b.extend({queue:function(e,n,r){var i;return e?(n=(n||"fx")+"queue",i=b._data(e,n),r&&(!i||b.isArray(r)?i=b._data(e,n,b.makeArray(r)):i.push(r)),i||[]):t},dequeue:function(e,t){t=t||"fx";var n=b.queue(e,t),r=n.length,i=n.shift(),o=b._queueHooks(e,t),a=function(){b.dequeue(e,t)};"inprogress"===i&&(i=n.shift(),r--),o.cur=i,i&&("fx"===t&&n.unshift("inprogress"),delete o.stop,i.call(e,a,o)),!r&&o&&o.empty.fire()},_queueHooks:function(e,t){var n=t+"queueHooks";return b._data(e,n)||b._data(e,n,{empty:b.Callbacks("once memory").add(function(){b._removeData(e,t+"queue"),b._removeData(e,n)})})}}),b.fn.extend({queue:function(e,n){var r=2;return"string"!=typeof e&&(n=e,e="fx",r--),r>arguments.length?b.queue(this[0],e):n===t?this:this.each(function(){var t=b.queue(this,e,n);b._queueHooks(this,e),"fx"===e&&"inprogress"!==t[0]&&b.dequeue(this,e)})},dequeue:function(e){return this.each(function(){b.dequeue(this,e)})},delay:function(e,t){return e=b.fx?b.fx.speeds[e]||e:e,t=t||"fx",this.queue(t,function(t,n){var r=setTimeout(t,e);n.stop=function(){clearTimeout(r)}})},clearQueue:function(e){return this.queue(e||"fx",[])},promise:function(e,n){var r,i=1,o=b.Deferred(),a=this,s=this.length,u=function(){--i||o.resolveWith(a,[a])};"string"!=typeof e&&(n=e,e=t),e=e||"fx";while(s--)r=b._data(a[s],e+"queueHooks"),r&&r.empty&&(i++,r.empty.add(u));return u(),o.promise(n)}});var I,z,X=/[\t\r\n]/g,U=/\r/g,V=/^(?:input|select|textarea|button|object)$/i,Y=/^(?:a|area)$/i,J=/^(?:checked|selected|autofocus|autoplay|async|controls|defer|disabled|hidden|loop|multiple|open|readonly|required|scoped)$/i,G=/^(?:checked|selected)$/i,Q=b.support.getSetAttribute,K=b.support.input;b.fn.extend({attr:function(e,t){return b.access(this,b.attr,e,t,arguments.length>1)},removeAttr:function(e){return this.each(function(){b.removeAttr(this,e)})},prop:function(e,t){return b.access(this,b.prop,e,t,arguments.length>1)},removeProp:function(e){return e=b.propFix[e]||e,this.each(function(){try{this[e]=t,delete this[e]}catch(n){}})},addClass:function(e){var t,n,r,i,o,a=0,s=this.length,u="string"==typeof e&&e;if(b.isFunction(e))return this.each(function(t){b(this).addClass(e.call(this,t,this.className))});if(u)for(t=(e||"").match(w)||[];s>a;a++)if(n=this[a],r=1===n.nodeType&&(n.className?(" "+n.className+" ").replace(X," "):" ")){o=0;while(i=t[o++])0>r.indexOf(" "+i+" ")&&(r+=i+" ");n.className=b.trim(r)}return this},removeClass:function(e){var t,n,r,i,o,a=0,s=this.length,u=0===arguments.length||"string"==typeof e&&e;if(b.isFunction(e))return this.each(function(t){b(this).removeClass(e.call(this,t,this.className))});if(u)for(t=(e||"").match(w)||[];s>a;a++)if(n=this[a],r=1===n.nodeType&&(n.className?(" "+n.className+" ").replace(X," "):"")){o=0;while(i=t[o++])while(r.indexOf(" "+i+" ")>=0)r=r.replace(" "+i+" "," ");n.className=e?b.trim(r):""}return this},toggleClass:function(e,t){var n=typeof e,r="boolean"==typeof t;return b.isFunction(e)?this.each(function(n){b(this).toggleClass(e.call(this,n,this.className,t),t)}):this.each(function(){if("string"===n){var o,a=0,s=b(this),u=t,l=e.match(w)||[];while(o=l[a++])u=r?u:!s.hasClass(o),s[u?"addClass":"removeClass"](o)}else(n===i||"boolean"===n)&&(this.className&&b._data(this,"__className__",this.className),this.className=this.className||e===!1?"":b._data(this,"__className__")||"")})},hasClass:function(e){var t=" "+e+" ",n=0,r=this.length;for(;r>n;n++)if(1===this[n].nodeType&&(" "+this[n].className+" ").replace(X," ").indexOf(t)>=0)return!0;return!1},val:function(e){var n,r,i,o=this[0];{if(arguments.length)return i=b.isFunction(e),this.each(function(n){var o,a=b(this);1===this.nodeType&&(o=i?e.call(this,n,a.val()):e,null==o?o="":"number"==typeof o?o+="":b.isArray(o)&&(o=b.map(o,function(e){return null==e?"":e+""})),r=b.valHooks[this.type]||b.valHooks[this.nodeName.toLowerCase()],r&&"set"in r&&r.set(this,o,"value")!==t||(this.value=o))});if(o)return r=b.valHooks[o.type]||b.valHooks[o.nodeName.toLowerCase()],r&&"get"in r&&(n=r.get(o,"value"))!==t?n:(n=o.value,"string"==typeof n?n.replace(U,""):null==n?"":n)}}}),b.extend({valHooks:{option:{get:function(e){var t=e.attributes.value;return!t||t.specified?e.value:e.text}},select:{get:function(e){var t,n,r=e.options,i=e.selectedIndex,o="select-one"===e.type||0>i,a=o?null:[],s=o?i+1:r.length,u=0>i?s:o?i:0;for(;s>u;u++)if(n=r[u],!(!n.selected&&u!==i||(b.support.optDisabled?n.disabled:null!==n.getAttribute("disabled"))||n.parentNode.disabled&&b.nodeName(n.parentNode,"optgroup"))){if(t=b(n).val(),o)return t;a.push(t)}return a},set:function(e,t){var n=b.makeArray(t);return b(e).find("option").each(function(){this.selected=b.inArray(b(this).val(),n)>=0}),n.length||(e.selectedIndex=-1),n}}},attr:function(e,n,r){var o,a,s,u=e.nodeType;if(e&&3!==u&&8!==u&&2!==u)return typeof e.getAttribute===i?b.prop(e,n,r):(a=1!==u||!b.isXMLDoc(e),a&&(n=n.toLowerCase(),o=b.attrHooks[n]||(J.test(n)?z:I)),r===t?o&&a&&"get"in o&&null!==(s=o.get(e,n))?s:(typeof e.getAttribute!==i&&(s=e.getAttribute(n)),null==s?t:s):null!==r?o&&a&&"set"in o&&(s=o.set(e,r,n))!==t?s:(e.setAttribute(n,r+""),r):(b.removeAttr(e,n),t))},removeAttr:function(e,t){var n,r,i=0,o=t&&t.match(w);if(o&&1===e.nodeType)while(n=o[i++])r=b.propFix[n]||n,J.test(n)?!Q&&G.test(n)?e[b.camelCase("default-"+n)]=e[r]=!1:e[r]=!1:b.attr(e,n,""),e.removeAttribute(Q?n:r)},attrHooks:{type:{set:function(e,t){if(!b.support.radioValue&&"radio"===t&&b.nodeName(e,"input")){var n=e.value;return e.setAttribute("type",t),n&&(e.value=n),t}}}},propFix:{tabindex:"tabIndex",readonly:"readOnly","for":"htmlFor","class":"className",maxlength:"maxLength",cellspacing:"cellSpacing",cellpadding:"cellPadding",rowspan:"rowSpan",colspan:"colSpan",usemap:"useMap",frameborder:"frameBorder",contenteditable:"contentEditable"},prop:function(e,n,r){var i,o,a,s=e.nodeType;if(e&&3!==s&&8!==s&&2!==s)return a=1!==s||!b.isXMLDoc(e),a&&(n=b.propFix[n]||n,o=b.propHooks[n]),r!==t?o&&"set"in o&&(i=o.set(e,r,n))!==t?i:e[n]=r:o&&"get"in o&&null!==(i=o.get(e,n))?i:e[n]},propHooks:{tabIndex:{get:function(e){var n=e.getAttributeNode("tabindex");return n&&n.specified?parseInt(n.value,10):V.test(e.nodeName)||Y.test(e.nodeName)&&e.href?0:t}}}}),z={get:function(e,n){var r=b.prop(e,n),i="boolean"==typeof r&&e.getAttribute(n),o="boolean"==typeof r?K&&Q?null!=i:G.test(n)?e[b.camelCase("default-"+n)]:!!i:e.getAttributeNode(n);return o&&o.value!==!1?n.toLowerCase():t},set:function(e,t,n){return t===!1?b.removeAttr(e,n):K&&Q||!G.test(n)?e.setAttribute(!Q&&b.propFix[n]||n,n):e[b.camelCase("default-"+n)]=e[n]=!0,n}},K&&Q||(b.attrHooks.value={get:function(e,n){var r=e.getAttributeNode(n);return b.nodeName(e,"input")?e.defaultValue:r&&r.specified?r.value:t},set:function(e,n,r){return b.nodeName(e,"input")?(e.defaultValue=n,t):I&&I.set(e,n,r)}}),Q||(I=b.valHooks.button={get:function(e,n){var r=e.getAttributeNode(n);return r&&("id"===n||"name"===n||"coords"===n?""!==r.value:r.specified)?r.value:t},set:function(e,n,r){var i=e.getAttributeNode(r);return i||e.setAttributeNode(i=e.ownerDocument.createAttribute(r)),i.value=n+="","value"===r||n===e.getAttribute(r)?n:t}},b.attrHooks.contenteditable={get:I.get,set:function(e,t,n){I.set(e,""===t?!1:t,n)}},b.each(["width","height"],function(e,n){b.attrHooks[n]=b.extend(b.attrHooks[n],{set:function(e,r){return""===r?(e.setAttribute(n,"auto"),r):t}})})),b.support.hrefNormalized||(b.each(["href","src","width","height"],function(e,n){b.attrHooks[n]=b.extend(b.attrHooks[n],{get:function(e){var r=e.getAttribute(n,2);return null==r?t:r}})}),b.each(["href","src"],function(e,t){b.propHooks[t]={get:function(e){return e.getAttribute(t,4)}}})),b.support.style||(b.attrHooks.style={get:function(e){return e.style.cssText||t},set:function(e,t){return e.style.cssText=t+""}}),b.support.optSelected||(b.propHooks.selected=b.extend(b.propHooks.selected,{get:function(e){var t=e.parentNode;return t&&(t.selectedIndex,t.parentNode&&t.parentNode.selectedIndex),null}})),b.support.enctype||(b.propFix.enctype="encoding"),b.support.checkOn||b.each(["radio","checkbox"],function(){b.valHooks[this]={get:function(e){return null===e.getAttribute("value")?"on":e.value}}}),b.each(["radio","checkbox"],function(){b.valHooks[this]=b.extend(b.valHooks[this],{set:function(e,n){return b.isArray(n)?e.checked=b.inArray(b(e).val(),n)>=0:t}})});var Z=/^(?:input|select|textarea)$/i,et=/^key/,tt=/^(?:mouse|contextmenu)|click/,nt=/^(?:focusinfocus|focusoutblur)$/,rt=/^([^.]*)(?:\.(.+)|)$/;function it(){return!0}function ot(){return!1}b.event={global:{},add:function(e,n,r,o,a){var s,u,l,c,p,f,d,h,g,m,y,v=b._data(e);if(v){r.handler&&(c=r,r=c.handler,a=c.selector),r.guid||(r.guid=b.guid++),(u=v.events)||(u=v.events={}),(f=v.handle)||(f=v.handle=function(e){return typeof b===i||e&&b.event.triggered===e.type?t:b.event.dispatch.apply(f.elem,arguments)},f.elem=e),n=(n||"").match(w)||[""],l=n.length;while(l--)s=rt.exec(n[l])||[],g=y=s[1],m=(s[2]||"").split(".").sort(),p=b.event.special[g]||{},g=(a?p.delegateType:p.bindType)||g,p=b.event.special[g]||{},d=b.extend({type:g,origType:y,data:o,handler:r,guid:r.guid,selector:a,needsContext:a&&b.expr.match.needsContext.test(a),namespace:m.join(".")},c),(h=u[g])||(h=u[g]=[],h.delegateCount=0,p.setup&&p.setup.call(e,o,m,f)!==!1||(e.addEventListener?e.addEventListener(g,f,!1):e.attachEvent&&e.attachEvent("on"+g,f))),p.add&&(p.add.call(e,d),d.handler.guid||(d.handler.guid=r.guid)),a?h.splice(h.delegateCount++,0,d):h.push(d),b.event.global[g]=!0;e=null}},remove:function(e,t,n,r,i){var o,a,s,u,l,c,p,f,d,h,g,m=b.hasData(e)&&b._data(e);if(m&&(c=m.events)){t=(t||"").match(w)||[""],l=t.length;while(l--)if(s=rt.exec(t[l])||[],d=g=s[1],h=(s[2]||"").split(".").sort(),d){p=b.event.special[d]||{},d=(r?p.delegateType:p.bindType)||d,f=c[d]||[],s=s[2]&&RegExp("(^|\\.)"+h.join("\\.(?:.*\\.|)")+"(\\.|$)"),u=o=f.length;while(o--)a=f[o],!i&&g!==a.origType||n&&n.guid!==a.guid||s&&!s.test(a.namespace)||r&&r!==a.selector&&("**"!==r||!a.selector)||(f.splice(o,1),a.selector&&f.delegateCount--,p.remove&&p.remove.call(e,a));u&&!f.length&&(p.teardown&&p.teardown.call(e,h,m.handle)!==!1||b.removeEvent(e,d,m.handle),delete c[d])}else for(d in c)b.event.remove(e,d+t[l],n,r,!0);b.isEmptyObject(c)&&(delete m.handle,b._removeData(e,"events"))}},trigger:function(n,r,i,a){var s,u,l,c,p,f,d,h=[i||o],g=y.call(n,"type")?n.type:n,m=y.call(n,"namespace")?n.namespace.split("."):[];if(l=f=i=i||o,3!==i.nodeType&&8!==i.nodeType&&!nt.test(g+b.event.triggered)&&(g.indexOf(".")>=0&&(m=g.split("."),g=m.shift(),m.sort()),u=0>g.indexOf(":")&&"on"+g,n=n[b.expando]?n:new b.Event(g,"object"==typeof n&&n),n.isTrigger=!0,n.namespace=m.join("."),n.namespace_re=n.namespace?RegExp("(^|\\.)"+m.join("\\.(?:.*\\.|)")+"(\\.|$)"):null,n.result=t,n.target||(n.target=i),r=null==r?[n]:b.makeArray(r,[n]),p=b.event.special[g]||{},a||!p.trigger||p.trigger.apply(i,r)!==!1)){if(!a&&!p.noBubble&&!b.isWindow(i)){for(c=p.delegateType||g,nt.test(c+g)||(l=l.parentNode);l;l=l.parentNode)h.push(l),f=l;f===(i.ownerDocument||o)&&h.push(f.defaultView||f.parentWindow||e)}d=0;while((l=h[d++])&&!n.isPropagationStopped())n.type=d>1?c:p.bindType||g,s=(b._data(l,"events")||{})[n.type]&&b._data(l,"handle"),s&&s.apply(l,r),s=u&&l[u],s&&b.acceptData(l)&&s.apply&&s.apply(l,r)===!1&&n.preventDefault();if(n.type=g,!(a||n.isDefaultPrevented()||p._default&&p._default.apply(i.ownerDocument,r)!==!1||"click"===g&&b.nodeName(i,"a")||!b.acceptData(i)||!u||!i[g]||b.isWindow(i))){f=i[u],f&&(i[u]=null),b.event.triggered=g;try{i[g]()}catch(v){}b.event.triggered=t,f&&(i[u]=f)}return n.result}},dispatch:function(e){e=b.event.fix(e);var n,r,i,o,a,s=[],u=h.call(arguments),l=(b._data(this,"events")||{})[e.type]||[],c=b.event.special[e.type]||{};if(u[0]=e,e.delegateTarget=this,!c.preDispatch||c.preDispatch.call(this,e)!==!1){s=b.event.handlers.call(this,e,l),n=0;while((o=s[n++])&&!e.isPropagationStopped()){e.currentTarget=o.elem,a=0;while((i=o.handlers[a++])&&!e.isImmediatePropagationStopped())(!e.namespace_re||e.namespace_re.test(i.namespace))&&(e.handleObj=i,e.data=i.data,r=((b.event.special[i.origType]||{}).handle||i.handler).apply(o.elem,u),r!==t&&(e.result=r)===!1&&(e.preventDefault(),e.stopPropagation()))}return c.postDispatch&&c.postDispatch.call(this,e),e.result}},handlers:function(e,n){var r,i,o,a,s=[],u=n.delegateCount,l=e.target;if(u&&l.nodeType&&(!e.button||"click"!==e.type))for(;l!=this;l=l.parentNode||this)if(1===l.nodeType&&(l.disabled!==!0||"click"!==e.type)){for(o=[],a=0;u>a;a++)i=n[a],r=i.selector+" ",o[r]===t&&(o[r]=i.needsContext?b(r,this).index(l)>=0:b.find(r,this,null,[l]).length),o[r]&&o.push(i);o.length&&s.push({elem:l,handlers:o})}return n.length>u&&s.push({elem:this,handlers:n.slice(u)}),s},fix:function(e){if(e[b.expando])return e;var t,n,r,i=e.type,a=e,s=this.fixHooks[i];s||(this.fixHooks[i]=s=tt.test(i)?this.mouseHooks:et.test(i)?this.keyHooks:{}),r=s.props?this.props.concat(s.props):this.props,e=new b.Event(a),t=r.length;while(t--)n=r[t],e[n]=a[n];return e.target||(e.target=a.srcElement||o),3===e.target.nodeType&&(e.target=e.target.parentNode),e.metaKey=!!e.metaKey,s.filter?s.filter(e,a):e},props:"altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),fixHooks:{},keyHooks:{props:"char charCode key keyCode".split(" "),filter:function(e,t){return null==e.which&&(e.which=null!=t.charCode?t.charCode:t.keyCode),e}},mouseHooks:{props:"button buttons clientX clientY fromElement offsetX offsetY pageX pageY screenX screenY toElement".split(" "),filter:function(e,n){var r,i,a,s=n.button,u=n.fromElement;return null==e.pageX&&null!=n.clientX&&(i=e.target.ownerDocument||o,a=i.documentElement,r=i.body,e.pageX=n.clientX+(a&&a.scrollLeft||r&&r.scrollLeft||0)-(a&&a.clientLeft||r&&r.clientLeft||0),e.pageY=n.clientY+(a&&a.scrollTop||r&&r.scrollTop||0)-(a&&a.clientTop||r&&r.clientTop||0)),!e.relatedTarget&&u&&(e.relatedTarget=u===e.target?n.toElement:u),e.which||s===t||(e.which=1&s?1:2&s?3:4&s?2:0),e}},special:{load:{noBubble:!0},click:{trigger:function(){return b.nodeName(this,"input")&&"checkbox"===this.type&&this.click?(this.click(),!1):t}},focus:{trigger:function(){if(this!==o.activeElement&&this.focus)try{return this.focus(),!1}catch(e){}},delegateType:"focusin"},blur:{trigger:function(){return this===o.activeElement&&this.blur?(this.blur(),!1):t},delegateType:"focusout"},beforeunload:{postDispatch:function(e){e.result!==t&&(e.originalEvent.returnValue=e.result)}}},simulate:function(e,t,n,r){var i=b.extend(new b.Event,n,{type:e,isSimulated:!0,originalEvent:{}});r?b.event.trigger(i,null,t):b.event.dispatch.call(t,i),i.isDefaultPrevented()&&n.preventDefault()}},b.removeEvent=o.removeEventListener?function(e,t,n){e.removeEventListener&&e.removeEventListener(t,n,!1)}:function(e,t,n){var r="on"+t;e.detachEvent&&(typeof e[r]===i&&(e[r]=null),e.detachEvent(r,n))},b.Event=function(e,n){return this instanceof b.Event?(e&&e.type?(this.originalEvent=e,this.type=e.type,this.isDefaultPrevented=e.defaultPrevented||e.returnValue===!1||e.getPreventDefault&&e.getPreventDefault()?it:ot):this.type=e,n&&b.extend(this,n),this.timeStamp=e&&e.timeStamp||b.now(),this[b.expando]=!0,t):new b.Event(e,n)},b.Event.prototype={isDefaultPrevented:ot,isPropagationStopped:ot,isImmediatePropagationStopped:ot,preventDefault:function(){var e=this.originalEvent;this.isDefaultPrevented=it,e&&(e.preventDefault?e.preventDefault():e.returnValue=!1)},stopPropagation:function(){var e=this.originalEvent;this.isPropagationStopped=it,e&&(e.stopPropagation&&e.stopPropagation(),e.cancelBubble=!0)},stopImmediatePropagation:function(){this.isImmediatePropagationStopped=it,this.stopPropagation()}},b.each({mouseenter:"mouseover",mouseleave:"mouseout"},function(e,t){b.event.special[e]={delegateType:t,bindType:t,handle:function(e){var n,r=this,i=e.relatedTarget,o=e.handleObj;
return(!i||i!==r&&!b.contains(r,i))&&(e.type=o.origType,n=o.handler.apply(this,arguments),e.type=t),n}}}),b.support.submitBubbles||(b.event.special.submit={setup:function(){return b.nodeName(this,"form")?!1:(b.event.add(this,"click._submit keypress._submit",function(e){var n=e.target,r=b.nodeName(n,"input")||b.nodeName(n,"button")?n.form:t;r&&!b._data(r,"submitBubbles")&&(b.event.add(r,"submit._submit",function(e){e._submit_bubble=!0}),b._data(r,"submitBubbles",!0))}),t)},postDispatch:function(e){e._submit_bubble&&(delete e._submit_bubble,this.parentNode&&!e.isTrigger&&b.event.simulate("submit",this.parentNode,e,!0))},teardown:function(){return b.nodeName(this,"form")?!1:(b.event.remove(this,"._submit"),t)}}),b.support.changeBubbles||(b.event.special.change={setup:function(){return Z.test(this.nodeName)?(("checkbox"===this.type||"radio"===this.type)&&(b.event.add(this,"propertychange._change",function(e){"checked"===e.originalEvent.propertyName&&(this._just_changed=!0)}),b.event.add(this,"click._change",function(e){this._just_changed&&!e.isTrigger&&(this._just_changed=!1),b.event.simulate("change",this,e,!0)})),!1):(b.event.add(this,"beforeactivate._change",function(e){var t=e.target;Z.test(t.nodeName)&&!b._data(t,"changeBubbles")&&(b.event.add(t,"change._change",function(e){!this.parentNode||e.isSimulated||e.isTrigger||b.event.simulate("change",this.parentNode,e,!0)}),b._data(t,"changeBubbles",!0))}),t)},handle:function(e){var n=e.target;return this!==n||e.isSimulated||e.isTrigger||"radio"!==n.type&&"checkbox"!==n.type?e.handleObj.handler.apply(this,arguments):t},teardown:function(){return b.event.remove(this,"._change"),!Z.test(this.nodeName)}}),b.support.focusinBubbles||b.each({focus:"focusin",blur:"focusout"},function(e,t){var n=0,r=function(e){b.event.simulate(t,e.target,b.event.fix(e),!0)};b.event.special[t]={setup:function(){0===n++&&o.addEventListener(e,r,!0)},teardown:function(){0===--n&&o.removeEventListener(e,r,!0)}}}),b.fn.extend({on:function(e,n,r,i,o){var a,s;if("object"==typeof e){"string"!=typeof n&&(r=r||n,n=t);for(a in e)this.on(a,n,r,e[a],o);return this}if(null==r&&null==i?(i=n,r=n=t):null==i&&("string"==typeof n?(i=r,r=t):(i=r,r=n,n=t)),i===!1)i=ot;else if(!i)return this;return 1===o&&(s=i,i=function(e){return b().off(e),s.apply(this,arguments)},i.guid=s.guid||(s.guid=b.guid++)),this.each(function(){b.event.add(this,e,i,r,n)})},one:function(e,t,n,r){return this.on(e,t,n,r,1)},off:function(e,n,r){var i,o;if(e&&e.preventDefault&&e.handleObj)return i=e.handleObj,b(e.delegateTarget).off(i.namespace?i.origType+"."+i.namespace:i.origType,i.selector,i.handler),this;if("object"==typeof e){for(o in e)this.off(o,n,e[o]);return this}return(n===!1||"function"==typeof n)&&(r=n,n=t),r===!1&&(r=ot),this.each(function(){b.event.remove(this,e,r,n)})},bind:function(e,t,n){return this.on(e,null,t,n)},unbind:function(e,t){return this.off(e,null,t)},delegate:function(e,t,n,r){return this.on(t,e,n,r)},undelegate:function(e,t,n){return 1===arguments.length?this.off(e,"**"):this.off(t,e||"**",n)},trigger:function(e,t){return this.each(function(){b.event.trigger(e,t,this)})},triggerHandler:function(e,n){var r=this[0];return r?b.event.trigger(e,n,r,!0):t}}),function(e,t){var n,r,i,o,a,s,u,l,c,p,f,d,h,g,m,y,v,x="sizzle"+-new Date,w=e.document,T={},N=0,C=0,k=it(),E=it(),S=it(),A=typeof t,j=1<<31,D=[],L=D.pop,H=D.push,q=D.slice,M=D.indexOf||function(e){var t=0,n=this.length;for(;n>t;t++)if(this[t]===e)return t;return-1},_="[\\x20\\t\\r\\n\\f]",F="(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+",O=F.replace("w","w#"),B="([*^$|!~]?=)",P="\\["+_+"*("+F+")"+_+"*(?:"+B+_+"*(?:(['\"])((?:\\\\.|[^\\\\])*?)\\3|("+O+")|)|)"+_+"*\\]",R=":("+F+")(?:\\(((['\"])((?:\\\\.|[^\\\\])*?)\\3|((?:\\\\.|[^\\\\()[\\]]|"+P.replace(3,8)+")*)|.*)\\)|)",W=RegExp("^"+_+"+|((?:^|[^\\\\])(?:\\\\.)*)"+_+"+$","g"),$=RegExp("^"+_+"*,"+_+"*"),I=RegExp("^"+_+"*([\\x20\\t\\r\\n\\f>+~])"+_+"*"),z=RegExp(R),X=RegExp("^"+O+"$"),U={ID:RegExp("^#("+F+")"),CLASS:RegExp("^\\.("+F+")"),NAME:RegExp("^\\[name=['\"]?("+F+")['\"]?\\]"),TAG:RegExp("^("+F.replace("w","w*")+")"),ATTR:RegExp("^"+P),PSEUDO:RegExp("^"+R),CHILD:RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\("+_+"*(even|odd|(([+-]|)(\\d*)n|)"+_+"*(?:([+-]|)"+_+"*(\\d+)|))"+_+"*\\)|)","i"),needsContext:RegExp("^"+_+"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\("+_+"*((?:-\\d)?\\d*)"+_+"*\\)|)(?=[^-]|$)","i")},V=/[\x20\t\r\n\f]*[+~]/,Y=/^[^{]+\{\s*\[native code/,J=/^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,G=/^(?:input|select|textarea|button)$/i,Q=/^h\d$/i,K=/'|\\/g,Z=/\=[\x20\t\r\n\f]*([^'"\]]*)[\x20\t\r\n\f]*\]/g,et=/\\([\da-fA-F]{1,6}[\x20\t\r\n\f]?|.)/g,tt=function(e,t){var n="0x"+t-65536;return n!==n?t:0>n?String.fromCharCode(n+65536):String.fromCharCode(55296|n>>10,56320|1023&n)};try{q.call(w.documentElement.childNodes,0)[0].nodeType}catch(nt){q=function(e){var t,n=[];while(t=this[e++])n.push(t);return n}}function rt(e){return Y.test(e+"")}function it(){var e,t=[];return e=function(n,r){return t.push(n+=" ")>i.cacheLength&&delete e[t.shift()],e[n]=r}}function ot(e){return e[x]=!0,e}function at(e){var t=p.createElement("div");try{return e(t)}catch(n){return!1}finally{t=null}}function st(e,t,n,r){var i,o,a,s,u,l,f,g,m,v;if((t?t.ownerDocument||t:w)!==p&&c(t),t=t||p,n=n||[],!e||"string"!=typeof e)return n;if(1!==(s=t.nodeType)&&9!==s)return[];if(!d&&!r){if(i=J.exec(e))if(a=i[1]){if(9===s){if(o=t.getElementById(a),!o||!o.parentNode)return n;if(o.id===a)return n.push(o),n}else if(t.ownerDocument&&(o=t.ownerDocument.getElementById(a))&&y(t,o)&&o.id===a)return n.push(o),n}else{if(i[2])return H.apply(n,q.call(t.getElementsByTagName(e),0)),n;if((a=i[3])&&T.getByClassName&&t.getElementsByClassName)return H.apply(n,q.call(t.getElementsByClassName(a),0)),n}if(T.qsa&&!h.test(e)){if(f=!0,g=x,m=t,v=9===s&&e,1===s&&"object"!==t.nodeName.toLowerCase()){l=ft(e),(f=t.getAttribute("id"))?g=f.replace(K,"\\$&"):t.setAttribute("id",g),g="[id='"+g+"'] ",u=l.length;while(u--)l[u]=g+dt(l[u]);m=V.test(e)&&t.parentNode||t,v=l.join(",")}if(v)try{return H.apply(n,q.call(m.querySelectorAll(v),0)),n}catch(b){}finally{f||t.removeAttribute("id")}}}return wt(e.replace(W,"$1"),t,n,r)}a=st.isXML=function(e){var t=e&&(e.ownerDocument||e).documentElement;return t?"HTML"!==t.nodeName:!1},c=st.setDocument=function(e){var n=e?e.ownerDocument||e:w;return n!==p&&9===n.nodeType&&n.documentElement?(p=n,f=n.documentElement,d=a(n),T.tagNameNoComments=at(function(e){return e.appendChild(n.createComment("")),!e.getElementsByTagName("*").length}),T.attributes=at(function(e){e.innerHTML="<select></select>";var t=typeof e.lastChild.getAttribute("multiple");return"boolean"!==t&&"string"!==t}),T.getByClassName=at(function(e){return e.innerHTML="<div class='hidden e'></div><div class='hidden'></div>",e.getElementsByClassName&&e.getElementsByClassName("e").length?(e.lastChild.className="e",2===e.getElementsByClassName("e").length):!1}),T.getByName=at(function(e){e.id=x+0,e.innerHTML="<a name='"+x+"'></a><div name='"+x+"'></div>",f.insertBefore(e,f.firstChild);var t=n.getElementsByName&&n.getElementsByName(x).length===2+n.getElementsByName(x+0).length;return T.getIdNotName=!n.getElementById(x),f.removeChild(e),t}),i.attrHandle=at(function(e){return e.innerHTML="<a href='#'></a>",e.firstChild&&typeof e.firstChild.getAttribute!==A&&"#"===e.firstChild.getAttribute("href")})?{}:{href:function(e){return e.getAttribute("href",2)},type:function(e){return e.getAttribute("type")}},T.getIdNotName?(i.find.ID=function(e,t){if(typeof t.getElementById!==A&&!d){var n=t.getElementById(e);return n&&n.parentNode?[n]:[]}},i.filter.ID=function(e){var t=e.replace(et,tt);return function(e){return e.getAttribute("id")===t}}):(i.find.ID=function(e,n){if(typeof n.getElementById!==A&&!d){var r=n.getElementById(e);return r?r.id===e||typeof r.getAttributeNode!==A&&r.getAttributeNode("id").value===e?[r]:t:[]}},i.filter.ID=function(e){var t=e.replace(et,tt);return function(e){var n=typeof e.getAttributeNode!==A&&e.getAttributeNode("id");return n&&n.value===t}}),i.find.TAG=T.tagNameNoComments?function(e,n){return typeof n.getElementsByTagName!==A?n.getElementsByTagName(e):t}:function(e,t){var n,r=[],i=0,o=t.getElementsByTagName(e);if("*"===e){while(n=o[i++])1===n.nodeType&&r.push(n);return r}return o},i.find.NAME=T.getByName&&function(e,n){return typeof n.getElementsByName!==A?n.getElementsByName(name):t},i.find.CLASS=T.getByClassName&&function(e,n){return typeof n.getElementsByClassName===A||d?t:n.getElementsByClassName(e)},g=[],h=[":focus"],(T.qsa=rt(n.querySelectorAll))&&(at(function(e){e.innerHTML="<select><option selected=''></option></select>",e.querySelectorAll("[selected]").length||h.push("\\["+_+"*(?:checked|disabled|ismap|multiple|readonly|selected|value)"),e.querySelectorAll(":checked").length||h.push(":checked")}),at(function(e){e.innerHTML="<input type='hidden' i=''/>",e.querySelectorAll("[i^='']").length&&h.push("[*^$]="+_+"*(?:\"\"|'')"),e.querySelectorAll(":enabled").length||h.push(":enabled",":disabled"),e.querySelectorAll("*,:x"),h.push(",.*:")})),(T.matchesSelector=rt(m=f.matchesSelector||f.mozMatchesSelector||f.webkitMatchesSelector||f.oMatchesSelector||f.msMatchesSelector))&&at(function(e){T.disconnectedMatch=m.call(e,"div"),m.call(e,"[s!='']:x"),g.push("!=",R)}),h=RegExp(h.join("|")),g=RegExp(g.join("|")),y=rt(f.contains)||f.compareDocumentPosition?function(e,t){var n=9===e.nodeType?e.documentElement:e,r=t&&t.parentNode;return e===r||!(!r||1!==r.nodeType||!(n.contains?n.contains(r):e.compareDocumentPosition&&16&e.compareDocumentPosition(r)))}:function(e,t){if(t)while(t=t.parentNode)if(t===e)return!0;return!1},v=f.compareDocumentPosition?function(e,t){var r;return e===t?(u=!0,0):(r=t.compareDocumentPosition&&e.compareDocumentPosition&&e.compareDocumentPosition(t))?1&r||e.parentNode&&11===e.parentNode.nodeType?e===n||y(w,e)?-1:t===n||y(w,t)?1:0:4&r?-1:1:e.compareDocumentPosition?-1:1}:function(e,t){var r,i=0,o=e.parentNode,a=t.parentNode,s=[e],l=[t];if(e===t)return u=!0,0;if(!o||!a)return e===n?-1:t===n?1:o?-1:a?1:0;if(o===a)return ut(e,t);r=e;while(r=r.parentNode)s.unshift(r);r=t;while(r=r.parentNode)l.unshift(r);while(s[i]===l[i])i++;return i?ut(s[i],l[i]):s[i]===w?-1:l[i]===w?1:0},u=!1,[0,0].sort(v),T.detectDuplicates=u,p):p},st.matches=function(e,t){return st(e,null,null,t)},st.matchesSelector=function(e,t){if((e.ownerDocument||e)!==p&&c(e),t=t.replace(Z,"='$1']"),!(!T.matchesSelector||d||g&&g.test(t)||h.test(t)))try{var n=m.call(e,t);if(n||T.disconnectedMatch||e.document&&11!==e.document.nodeType)return n}catch(r){}return st(t,p,null,[e]).length>0},st.contains=function(e,t){return(e.ownerDocument||e)!==p&&c(e),y(e,t)},st.attr=function(e,t){var n;return(e.ownerDocument||e)!==p&&c(e),d||(t=t.toLowerCase()),(n=i.attrHandle[t])?n(e):d||T.attributes?e.getAttribute(t):((n=e.getAttributeNode(t))||e.getAttribute(t))&&e[t]===!0?t:n&&n.specified?n.value:null},st.error=function(e){throw Error("Syntax error, unrecognized expression: "+e)},st.uniqueSort=function(e){var t,n=[],r=1,i=0;if(u=!T.detectDuplicates,e.sort(v),u){for(;t=e[r];r++)t===e[r-1]&&(i=n.push(r));while(i--)e.splice(n[i],1)}return e};function ut(e,t){var n=t&&e,r=n&&(~t.sourceIndex||j)-(~e.sourceIndex||j);if(r)return r;if(n)while(n=n.nextSibling)if(n===t)return-1;return e?1:-1}function lt(e){return function(t){var n=t.nodeName.toLowerCase();return"input"===n&&t.type===e}}function ct(e){return function(t){var n=t.nodeName.toLowerCase();return("input"===n||"button"===n)&&t.type===e}}function pt(e){return ot(function(t){return t=+t,ot(function(n,r){var i,o=e([],n.length,t),a=o.length;while(a--)n[i=o[a]]&&(n[i]=!(r[i]=n[i]))})})}o=st.getText=function(e){var t,n="",r=0,i=e.nodeType;if(i){if(1===i||9===i||11===i){if("string"==typeof e.textContent)return e.textContent;for(e=e.firstChild;e;e=e.nextSibling)n+=o(e)}else if(3===i||4===i)return e.nodeValue}else for(;t=e[r];r++)n+=o(t);return n},i=st.selectors={cacheLength:50,createPseudo:ot,match:U,find:{},relative:{">":{dir:"parentNode",first:!0}," ":{dir:"parentNode"},"+":{dir:"previousSibling",first:!0},"~":{dir:"previousSibling"}},preFilter:{ATTR:function(e){return e[1]=e[1].replace(et,tt),e[3]=(e[4]||e[5]||"").replace(et,tt),"~="===e[2]&&(e[3]=" "+e[3]+" "),e.slice(0,4)},CHILD:function(e){return e[1]=e[1].toLowerCase(),"nth"===e[1].slice(0,3)?(e[3]||st.error(e[0]),e[4]=+(e[4]?e[5]+(e[6]||1):2*("even"===e[3]||"odd"===e[3])),e[5]=+(e[7]+e[8]||"odd"===e[3])):e[3]&&st.error(e[0]),e},PSEUDO:function(e){var t,n=!e[5]&&e[2];return U.CHILD.test(e[0])?null:(e[4]?e[2]=e[4]:n&&z.test(n)&&(t=ft(n,!0))&&(t=n.indexOf(")",n.length-t)-n.length)&&(e[0]=e[0].slice(0,t),e[2]=n.slice(0,t)),e.slice(0,3))}},filter:{TAG:function(e){return"*"===e?function(){return!0}:(e=e.replace(et,tt).toLowerCase(),function(t){return t.nodeName&&t.nodeName.toLowerCase()===e})},CLASS:function(e){var t=k[e+" "];return t||(t=RegExp("(^|"+_+")"+e+"("+_+"|$)"))&&k(e,function(e){return t.test(e.className||typeof e.getAttribute!==A&&e.getAttribute("class")||"")})},ATTR:function(e,t,n){return function(r){var i=st.attr(r,e);return null==i?"!="===t:t?(i+="","="===t?i===n:"!="===t?i!==n:"^="===t?n&&0===i.indexOf(n):"*="===t?n&&i.indexOf(n)>-1:"$="===t?n&&i.slice(-n.length)===n:"~="===t?(" "+i+" ").indexOf(n)>-1:"|="===t?i===n||i.slice(0,n.length+1)===n+"-":!1):!0}},CHILD:function(e,t,n,r,i){var o="nth"!==e.slice(0,3),a="last"!==e.slice(-4),s="of-type"===t;return 1===r&&0===i?function(e){return!!e.parentNode}:function(t,n,u){var l,c,p,f,d,h,g=o!==a?"nextSibling":"previousSibling",m=t.parentNode,y=s&&t.nodeName.toLowerCase(),v=!u&&!s;if(m){if(o){while(g){p=t;while(p=p[g])if(s?p.nodeName.toLowerCase()===y:1===p.nodeType)return!1;h=g="only"===e&&!h&&"nextSibling"}return!0}if(h=[a?m.firstChild:m.lastChild],a&&v){c=m[x]||(m[x]={}),l=c[e]||[],d=l[0]===N&&l[1],f=l[0]===N&&l[2],p=d&&m.childNodes[d];while(p=++d&&p&&p[g]||(f=d=0)||h.pop())if(1===p.nodeType&&++f&&p===t){c[e]=[N,d,f];break}}else if(v&&(l=(t[x]||(t[x]={}))[e])&&l[0]===N)f=l[1];else while(p=++d&&p&&p[g]||(f=d=0)||h.pop())if((s?p.nodeName.toLowerCase()===y:1===p.nodeType)&&++f&&(v&&((p[x]||(p[x]={}))[e]=[N,f]),p===t))break;return f-=i,f===r||0===f%r&&f/r>=0}}},PSEUDO:function(e,t){var n,r=i.pseudos[e]||i.setFilters[e.toLowerCase()]||st.error("unsupported pseudo: "+e);return r[x]?r(t):r.length>1?(n=[e,e,"",t],i.setFilters.hasOwnProperty(e.toLowerCase())?ot(function(e,n){var i,o=r(e,t),a=o.length;while(a--)i=M.call(e,o[a]),e[i]=!(n[i]=o[a])}):function(e){return r(e,0,n)}):r}},pseudos:{not:ot(function(e){var t=[],n=[],r=s(e.replace(W,"$1"));return r[x]?ot(function(e,t,n,i){var o,a=r(e,null,i,[]),s=e.length;while(s--)(o=a[s])&&(e[s]=!(t[s]=o))}):function(e,i,o){return t[0]=e,r(t,null,o,n),!n.pop()}}),has:ot(function(e){return function(t){return st(e,t).length>0}}),contains:ot(function(e){return function(t){return(t.textContent||t.innerText||o(t)).indexOf(e)>-1}}),lang:ot(function(e){return X.test(e||"")||st.error("unsupported lang: "+e),e=e.replace(et,tt).toLowerCase(),function(t){var n;do if(n=d?t.getAttribute("xml:lang")||t.getAttribute("lang"):t.lang)return n=n.toLowerCase(),n===e||0===n.indexOf(e+"-");while((t=t.parentNode)&&1===t.nodeType);return!1}}),target:function(t){var n=e.location&&e.location.hash;return n&&n.slice(1)===t.id},root:function(e){return e===f},focus:function(e){return e===p.activeElement&&(!p.hasFocus||p.hasFocus())&&!!(e.type||e.href||~e.tabIndex)},enabled:function(e){return e.disabled===!1},disabled:function(e){return e.disabled===!0},checked:function(e){var t=e.nodeName.toLowerCase();return"input"===t&&!!e.checked||"option"===t&&!!e.selected},selected:function(e){return e.parentNode&&e.parentNode.selectedIndex,e.selected===!0},empty:function(e){for(e=e.firstChild;e;e=e.nextSibling)if(e.nodeName>"@"||3===e.nodeType||4===e.nodeType)return!1;return!0},parent:function(e){return!i.pseudos.empty(e)},header:function(e){return Q.test(e.nodeName)},input:function(e){return G.test(e.nodeName)},button:function(e){var t=e.nodeName.toLowerCase();return"input"===t&&"button"===e.type||"button"===t},text:function(e){var t;return"input"===e.nodeName.toLowerCase()&&"text"===e.type&&(null==(t=e.getAttribute("type"))||t.toLowerCase()===e.type)},first:pt(function(){return[0]}),last:pt(function(e,t){return[t-1]}),eq:pt(function(e,t,n){return[0>n?n+t:n]}),even:pt(function(e,t){var n=0;for(;t>n;n+=2)e.push(n);return e}),odd:pt(function(e,t){var n=1;for(;t>n;n+=2)e.push(n);return e}),lt:pt(function(e,t,n){var r=0>n?n+t:n;for(;--r>=0;)e.push(r);return e}),gt:pt(function(e,t,n){var r=0>n?n+t:n;for(;t>++r;)e.push(r);return e})}};for(n in{radio:!0,checkbox:!0,file:!0,password:!0,image:!0})i.pseudos[n]=lt(n);for(n in{submit:!0,reset:!0})i.pseudos[n]=ct(n);function ft(e,t){var n,r,o,a,s,u,l,c=E[e+" "];if(c)return t?0:c.slice(0);s=e,u=[],l=i.preFilter;while(s){(!n||(r=$.exec(s)))&&(r&&(s=s.slice(r[0].length)||s),u.push(o=[])),n=!1,(r=I.exec(s))&&(n=r.shift(),o.push({value:n,type:r[0].replace(W," ")}),s=s.slice(n.length));for(a in i.filter)!(r=U[a].exec(s))||l[a]&&!(r=l[a](r))||(n=r.shift(),o.push({value:n,type:a,matches:r}),s=s.slice(n.length));if(!n)break}return t?s.length:s?st.error(e):E(e,u).slice(0)}function dt(e){var t=0,n=e.length,r="";for(;n>t;t++)r+=e[t].value;return r}function ht(e,t,n){var i=t.dir,o=n&&"parentNode"===i,a=C++;return t.first?function(t,n,r){while(t=t[i])if(1===t.nodeType||o)return e(t,n,r)}:function(t,n,s){var u,l,c,p=N+" "+a;if(s){while(t=t[i])if((1===t.nodeType||o)&&e(t,n,s))return!0}else while(t=t[i])if(1===t.nodeType||o)if(c=t[x]||(t[x]={}),(l=c[i])&&l[0]===p){if((u=l[1])===!0||u===r)return u===!0}else if(l=c[i]=[p],l[1]=e(t,n,s)||r,l[1]===!0)return!0}}function gt(e){return e.length>1?function(t,n,r){var i=e.length;while(i--)if(!e[i](t,n,r))return!1;return!0}:e[0]}function mt(e,t,n,r,i){var o,a=[],s=0,u=e.length,l=null!=t;for(;u>s;s++)(o=e[s])&&(!n||n(o,r,i))&&(a.push(o),l&&t.push(s));return a}function yt(e,t,n,r,i,o){return r&&!r[x]&&(r=yt(r)),i&&!i[x]&&(i=yt(i,o)),ot(function(o,a,s,u){var l,c,p,f=[],d=[],h=a.length,g=o||xt(t||"*",s.nodeType?[s]:s,[]),m=!e||!o&&t?g:mt(g,f,e,s,u),y=n?i||(o?e:h||r)?[]:a:m;if(n&&n(m,y,s,u),r){l=mt(y,d),r(l,[],s,u),c=l.length;while(c--)(p=l[c])&&(y[d[c]]=!(m[d[c]]=p))}if(o){if(i||e){if(i){l=[],c=y.length;while(c--)(p=y[c])&&l.push(m[c]=p);i(null,y=[],l,u)}c=y.length;while(c--)(p=y[c])&&(l=i?M.call(o,p):f[c])>-1&&(o[l]=!(a[l]=p))}}else y=mt(y===a?y.splice(h,y.length):y),i?i(null,a,y,u):H.apply(a,y)})}function vt(e){var t,n,r,o=e.length,a=i.relative[e[0].type],s=a||i.relative[" "],u=a?1:0,c=ht(function(e){return e===t},s,!0),p=ht(function(e){return M.call(t,e)>-1},s,!0),f=[function(e,n,r){return!a&&(r||n!==l)||((t=n).nodeType?c(e,n,r):p(e,n,r))}];for(;o>u;u++)if(n=i.relative[e[u].type])f=[ht(gt(f),n)];else{if(n=i.filter[e[u].type].apply(null,e[u].matches),n[x]){for(r=++u;o>r;r++)if(i.relative[e[r].type])break;return yt(u>1&&gt(f),u>1&&dt(e.slice(0,u-1)).replace(W,"$1"),n,r>u&&vt(e.slice(u,r)),o>r&&vt(e=e.slice(r)),o>r&&dt(e))}f.push(n)}return gt(f)}function bt(e,t){var n=0,o=t.length>0,a=e.length>0,s=function(s,u,c,f,d){var h,g,m,y=[],v=0,b="0",x=s&&[],w=null!=d,T=l,C=s||a&&i.find.TAG("*",d&&u.parentNode||u),k=N+=null==T?1:Math.random()||.1;for(w&&(l=u!==p&&u,r=n);null!=(h=C[b]);b++){if(a&&h){g=0;while(m=e[g++])if(m(h,u,c)){f.push(h);break}w&&(N=k,r=++n)}o&&((h=!m&&h)&&v--,s&&x.push(h))}if(v+=b,o&&b!==v){g=0;while(m=t[g++])m(x,y,u,c);if(s){if(v>0)while(b--)x[b]||y[b]||(y[b]=L.call(f));y=mt(y)}H.apply(f,y),w&&!s&&y.length>0&&v+t.length>1&&st.uniqueSort(f)}return w&&(N=k,l=T),x};return o?ot(s):s}s=st.compile=function(e,t){var n,r=[],i=[],o=S[e+" "];if(!o){t||(t=ft(e)),n=t.length;while(n--)o=vt(t[n]),o[x]?r.push(o):i.push(o);o=S(e,bt(i,r))}return o};function xt(e,t,n){var r=0,i=t.length;for(;i>r;r++)st(e,t[r],n);return n}function wt(e,t,n,r){var o,a,u,l,c,p=ft(e);if(!r&&1===p.length){if(a=p[0]=p[0].slice(0),a.length>2&&"ID"===(u=a[0]).type&&9===t.nodeType&&!d&&i.relative[a[1].type]){if(t=i.find.ID(u.matches[0].replace(et,tt),t)[0],!t)return n;e=e.slice(a.shift().value.length)}o=U.needsContext.test(e)?0:a.length;while(o--){if(u=a[o],i.relative[l=u.type])break;if((c=i.find[l])&&(r=c(u.matches[0].replace(et,tt),V.test(a[0].type)&&t.parentNode||t))){if(a.splice(o,1),e=r.length&&dt(a),!e)return H.apply(n,q.call(r,0)),n;break}}}return s(e,p)(r,t,d,n,V.test(e)),n}i.pseudos.nth=i.pseudos.eq;function Tt(){}i.filters=Tt.prototype=i.pseudos,i.setFilters=new Tt,c(),st.attr=b.attr,b.find=st,b.expr=st.selectors,b.expr[":"]=b.expr.pseudos,b.unique=st.uniqueSort,b.text=st.getText,b.isXMLDoc=st.isXML,b.contains=st.contains}(e);var at=/Until$/,st=/^(?:parents|prev(?:Until|All))/,ut=/^.[^:#\[\.,]*$/,lt=b.expr.match.needsContext,ct={children:!0,contents:!0,next:!0,prev:!0};b.fn.extend({find:function(e){var t,n,r,i=this.length;if("string"!=typeof e)return r=this,this.pushStack(b(e).filter(function(){for(t=0;i>t;t++)if(b.contains(r[t],this))return!0}));for(n=[],t=0;i>t;t++)b.find(e,this[t],n);return n=this.pushStack(i>1?b.unique(n):n),n.selector=(this.selector?this.selector+" ":"")+e,n},has:function(e){var t,n=b(e,this),r=n.length;return this.filter(function(){for(t=0;r>t;t++)if(b.contains(this,n[t]))return!0})},not:function(e){return this.pushStack(ft(this,e,!1))},filter:function(e){return this.pushStack(ft(this,e,!0))},is:function(e){return!!e&&("string"==typeof e?lt.test(e)?b(e,this.context).index(this[0])>=0:b.filter(e,this).length>0:this.filter(e).length>0)},closest:function(e,t){var n,r=0,i=this.length,o=[],a=lt.test(e)||"string"!=typeof e?b(e,t||this.context):0;for(;i>r;r++){n=this[r];while(n&&n.ownerDocument&&n!==t&&11!==n.nodeType){if(a?a.index(n)>-1:b.find.matchesSelector(n,e)){o.push(n);break}n=n.parentNode}}return this.pushStack(o.length>1?b.unique(o):o)},index:function(e){return e?"string"==typeof e?b.inArray(this[0],b(e)):b.inArray(e.jquery?e[0]:e,this):this[0]&&this[0].parentNode?this.first().prevAll().length:-1},add:function(e,t){var n="string"==typeof e?b(e,t):b.makeArray(e&&e.nodeType?[e]:e),r=b.merge(this.get(),n);return this.pushStack(b.unique(r))},addBack:function(e){return this.add(null==e?this.prevObject:this.prevObject.filter(e))}}),b.fn.andSelf=b.fn.addBack;function pt(e,t){do e=e[t];while(e&&1!==e.nodeType);return e}b.each({parent:function(e){var t=e.parentNode;return t&&11!==t.nodeType?t:null},parents:function(e){return b.dir(e,"parentNode")},parentsUntil:function(e,t,n){return b.dir(e,"parentNode",n)},next:function(e){return pt(e,"nextSibling")},prev:function(e){return pt(e,"previousSibling")},nextAll:function(e){return b.dir(e,"nextSibling")},prevAll:function(e){return b.dir(e,"previousSibling")},nextUntil:function(e,t,n){return b.dir(e,"nextSibling",n)},prevUntil:function(e,t,n){return b.dir(e,"previousSibling",n)},siblings:function(e){return b.sibling((e.parentNode||{}).firstChild,e)},children:function(e){return b.sibling(e.firstChild)},contents:function(e){return b.nodeName(e,"iframe")?e.contentDocument||e.contentWindow.document:b.merge([],e.childNodes)}},function(e,t){b.fn[e]=function(n,r){var i=b.map(this,t,n);return at.test(e)||(r=n),r&&"string"==typeof r&&(i=b.filter(r,i)),i=this.length>1&&!ct[e]?b.unique(i):i,this.length>1&&st.test(e)&&(i=i.reverse()),this.pushStack(i)}}),b.extend({filter:function(e,t,n){return n&&(e=":not("+e+")"),1===t.length?b.find.matchesSelector(t[0],e)?[t[0]]:[]:b.find.matches(e,t)},dir:function(e,n,r){var i=[],o=e[n];while(o&&9!==o.nodeType&&(r===t||1!==o.nodeType||!b(o).is(r)))1===o.nodeType&&i.push(o),o=o[n];return i},sibling:function(e,t){var n=[];for(;e;e=e.nextSibling)1===e.nodeType&&e!==t&&n.push(e);return n}});function ft(e,t,n){if(t=t||0,b.isFunction(t))return b.grep(e,function(e,r){var i=!!t.call(e,r,e);return i===n});if(t.nodeType)return b.grep(e,function(e){return e===t===n});if("string"==typeof t){var r=b.grep(e,function(e){return 1===e.nodeType});if(ut.test(t))return b.filter(t,r,!n);t=b.filter(t,r)}return b.grep(e,function(e){return b.inArray(e,t)>=0===n})}function dt(e){var t=ht.split("|"),n=e.createDocumentFragment();if(n.createElement)while(t.length)n.createElement(t.pop());return n}var ht="abbr|article|aside|audio|bdi|canvas|data|datalist|details|figcaption|figure|footer|header|hgroup|mark|meter|nav|output|progress|section|summary|time|video",gt=/ jQuery\d+="(?:null|\d+)"/g,mt=RegExp("<(?:"+ht+")[\\s/>]","i"),yt=/^\s+/,vt=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,bt=/<([\w:]+)/,xt=/<tbody/i,wt=/<|&#?\w+;/,Tt=/<(?:script|style|link)/i,Nt=/^(?:checkbox|radio)$/i,Ct=/checked\s*(?:[^=]|=\s*.checked.)/i,kt=/^$|\/(?:java|ecma)script/i,Et=/^true\/(.*)/,St=/^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g,At={option:[1,"<select multiple='multiple'>","</select>"],legend:[1,"<fieldset>","</fieldset>"],area:[1,"<map>","</map>"],param:[1,"<object>","</object>"],thead:[1,"<table>","</table>"],tr:[2,"<table><tbody>","</tbody></table>"],col:[2,"<table><tbody></tbody><colgroup>","</colgroup></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:b.support.htmlSerialize?[0,"",""]:[1,"X<div>","</div>"]},jt=dt(o),Dt=jt.appendChild(o.createElement("div"));At.optgroup=At.option,At.tbody=At.tfoot=At.colgroup=At.caption=At.thead,At.th=At.td,b.fn.extend({text:function(e){return b.access(this,function(e){return e===t?b.text(this):this.empty().append((this[0]&&this[0].ownerDocument||o).createTextNode(e))},null,e,arguments.length)},wrapAll:function(e){if(b.isFunction(e))return this.each(function(t){b(this).wrapAll(e.call(this,t))});if(this[0]){var t=b(e,this[0].ownerDocument).eq(0).clone(!0);this[0].parentNode&&t.insertBefore(this[0]),t.map(function(){var e=this;while(e.firstChild&&1===e.firstChild.nodeType)e=e.firstChild;return e}).append(this)}return this},wrapInner:function(e){return b.isFunction(e)?this.each(function(t){b(this).wrapInner(e.call(this,t))}):this.each(function(){var t=b(this),n=t.contents();n.length?n.wrapAll(e):t.append(e)})},wrap:function(e){var t=b.isFunction(e);return this.each(function(n){b(this).wrapAll(t?e.call(this,n):e)})},unwrap:function(){return this.parent().each(function(){b.nodeName(this,"body")||b(this).replaceWith(this.childNodes)}).end()},append:function(){return this.domManip(arguments,!0,function(e){(1===this.nodeType||11===this.nodeType||9===this.nodeType)&&this.appendChild(e)})},prepend:function(){return this.domManip(arguments,!0,function(e){(1===this.nodeType||11===this.nodeType||9===this.nodeType)&&this.insertBefore(e,this.firstChild)})},before:function(){return this.domManip(arguments,!1,function(e){this.parentNode&&this.parentNode.insertBefore(e,this)})},after:function(){return this.domManip(arguments,!1,function(e){this.parentNode&&this.parentNode.insertBefore(e,this.nextSibling)})},remove:function(e,t){var n,r=0;for(;null!=(n=this[r]);r++)(!e||b.filter(e,[n]).length>0)&&(t||1!==n.nodeType||b.cleanData(Ot(n)),n.parentNode&&(t&&b.contains(n.ownerDocument,n)&&Mt(Ot(n,"script")),n.parentNode.removeChild(n)));return this},empty:function(){var e,t=0;for(;null!=(e=this[t]);t++){1===e.nodeType&&b.cleanData(Ot(e,!1));while(e.firstChild)e.removeChild(e.firstChild);e.options&&b.nodeName(e,"select")&&(e.options.length=0)}return this},clone:function(e,t){return e=null==e?!1:e,t=null==t?e:t,this.map(function(){return b.clone(this,e,t)})},html:function(e){return b.access(this,function(e){var n=this[0]||{},r=0,i=this.length;if(e===t)return 1===n.nodeType?n.innerHTML.replace(gt,""):t;if(!("string"!=typeof e||Tt.test(e)||!b.support.htmlSerialize&&mt.test(e)||!b.support.leadingWhitespace&&yt.test(e)||At[(bt.exec(e)||["",""])[1].toLowerCase()])){e=e.replace(vt,"<$1></$2>");try{for(;i>r;r++)n=this[r]||{},1===n.nodeType&&(b.cleanData(Ot(n,!1)),n.innerHTML=e);n=0}catch(o){}}n&&this.empty().append(e)},null,e,arguments.length)},replaceWith:function(e){var t=b.isFunction(e);return t||"string"==typeof e||(e=b(e).not(this).detach()),this.domManip([e],!0,function(e){var t=this.nextSibling,n=this.parentNode;n&&(b(this).remove(),n.insertBefore(e,t))})},detach:function(e){return this.remove(e,!0)},domManip:function(e,n,r){e=f.apply([],e);var i,o,a,s,u,l,c=0,p=this.length,d=this,h=p-1,g=e[0],m=b.isFunction(g);if(m||!(1>=p||"string"!=typeof g||b.support.checkClone)&&Ct.test(g))return this.each(function(i){var o=d.eq(i);m&&(e[0]=g.call(this,i,n?o.html():t)),o.domManip(e,n,r)});if(p&&(l=b.buildFragment(e,this[0].ownerDocument,!1,this),i=l.firstChild,1===l.childNodes.length&&(l=i),i)){for(n=n&&b.nodeName(i,"tr"),s=b.map(Ot(l,"script"),Ht),a=s.length;p>c;c++)o=l,c!==h&&(o=b.clone(o,!0,!0),a&&b.merge(s,Ot(o,"script"))),r.call(n&&b.nodeName(this[c],"table")?Lt(this[c],"tbody"):this[c],o,c);if(a)for(u=s[s.length-1].ownerDocument,b.map(s,qt),c=0;a>c;c++)o=s[c],kt.test(o.type||"")&&!b._data(o,"globalEval")&&b.contains(u,o)&&(o.src?b.ajax({url:o.src,type:"GET",dataType:"script",async:!1,global:!1,"throws":!0}):b.globalEval((o.text||o.textContent||o.innerHTML||"").replace(St,"")));l=i=null}return this}});function Lt(e,t){return e.getElementsByTagName(t)[0]||e.appendChild(e.ownerDocument.createElement(t))}function Ht(e){var t=e.getAttributeNode("type");return e.type=(t&&t.specified)+"/"+e.type,e}function qt(e){var t=Et.exec(e.type);return t?e.type=t[1]:e.removeAttribute("type"),e}function Mt(e,t){var n,r=0;for(;null!=(n=e[r]);r++)b._data(n,"globalEval",!t||b._data(t[r],"globalEval"))}function _t(e,t){if(1===t.nodeType&&b.hasData(e)){var n,r,i,o=b._data(e),a=b._data(t,o),s=o.events;if(s){delete a.handle,a.events={};for(n in s)for(r=0,i=s[n].length;i>r;r++)b.event.add(t,n,s[n][r])}a.data&&(a.data=b.extend({},a.data))}}function Ft(e,t){var n,r,i;if(1===t.nodeType){if(n=t.nodeName.toLowerCase(),!b.support.noCloneEvent&&t[b.expando]){i=b._data(t);for(r in i.events)b.removeEvent(t,r,i.handle);t.removeAttribute(b.expando)}"script"===n&&t.text!==e.text?(Ht(t).text=e.text,qt(t)):"object"===n?(t.parentNode&&(t.outerHTML=e.outerHTML),b.support.html5Clone&&e.innerHTML&&!b.trim(t.innerHTML)&&(t.innerHTML=e.innerHTML)):"input"===n&&Nt.test(e.type)?(t.defaultChecked=t.checked=e.checked,t.value!==e.value&&(t.value=e.value)):"option"===n?t.defaultSelected=t.selected=e.defaultSelected:("input"===n||"textarea"===n)&&(t.defaultValue=e.defaultValue)}}b.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(e,t){b.fn[e]=function(e){var n,r=0,i=[],o=b(e),a=o.length-1;for(;a>=r;r++)n=r===a?this:this.clone(!0),b(o[r])[t](n),d.apply(i,n.get());return this.pushStack(i)}});function Ot(e,n){var r,o,a=0,s=typeof e.getElementsByTagName!==i?e.getElementsByTagName(n||"*"):typeof e.querySelectorAll!==i?e.querySelectorAll(n||"*"):t;if(!s)for(s=[],r=e.childNodes||e;null!=(o=r[a]);a++)!n||b.nodeName(o,n)?s.push(o):b.merge(s,Ot(o,n));return n===t||n&&b.nodeName(e,n)?b.merge([e],s):s}function Bt(e){Nt.test(e.type)&&(e.defaultChecked=e.checked)}b.extend({clone:function(e,t,n){var r,i,o,a,s,u=b.contains(e.ownerDocument,e);if(b.support.html5Clone||b.isXMLDoc(e)||!mt.test("<"+e.nodeName+">")?o=e.cloneNode(!0):(Dt.innerHTML=e.outerHTML,Dt.removeChild(o=Dt.firstChild)),!(b.support.noCloneEvent&&b.support.noCloneChecked||1!==e.nodeType&&11!==e.nodeType||b.isXMLDoc(e)))for(r=Ot(o),s=Ot(e),a=0;null!=(i=s[a]);++a)r[a]&&Ft(i,r[a]);if(t)if(n)for(s=s||Ot(e),r=r||Ot(o),a=0;null!=(i=s[a]);a++)_t(i,r[a]);else _t(e,o);return r=Ot(o,"script"),r.length>0&&Mt(r,!u&&Ot(e,"script")),r=s=i=null,o},buildFragment:function(e,t,n,r){var i,o,a,s,u,l,c,p=e.length,f=dt(t),d=[],h=0;for(;p>h;h++)if(o=e[h],o||0===o)if("object"===b.type(o))b.merge(d,o.nodeType?[o]:o);else if(wt.test(o)){s=s||f.appendChild(t.createElement("div")),u=(bt.exec(o)||["",""])[1].toLowerCase(),c=At[u]||At._default,s.innerHTML=c[1]+o.replace(vt,"<$1></$2>")+c[2],i=c[0];while(i--)s=s.lastChild;if(!b.support.leadingWhitespace&&yt.test(o)&&d.push(t.createTextNode(yt.exec(o)[0])),!b.support.tbody){o="table"!==u||xt.test(o)?"<table>"!==c[1]||xt.test(o)?0:s:s.firstChild,i=o&&o.childNodes.length;while(i--)b.nodeName(l=o.childNodes[i],"tbody")&&!l.childNodes.length&&o.removeChild(l)
}b.merge(d,s.childNodes),s.textContent="";while(s.firstChild)s.removeChild(s.firstChild);s=f.lastChild}else d.push(t.createTextNode(o));s&&f.removeChild(s),b.support.appendChecked||b.grep(Ot(d,"input"),Bt),h=0;while(o=d[h++])if((!r||-1===b.inArray(o,r))&&(a=b.contains(o.ownerDocument,o),s=Ot(f.appendChild(o),"script"),a&&Mt(s),n)){i=0;while(o=s[i++])kt.test(o.type||"")&&n.push(o)}return s=null,f},cleanData:function(e,t){var n,r,o,a,s=0,u=b.expando,l=b.cache,p=b.support.deleteExpando,f=b.event.special;for(;null!=(n=e[s]);s++)if((t||b.acceptData(n))&&(o=n[u],a=o&&l[o])){if(a.events)for(r in a.events)f[r]?b.event.remove(n,r):b.removeEvent(n,r,a.handle);l[o]&&(delete l[o],p?delete n[u]:typeof n.removeAttribute!==i?n.removeAttribute(u):n[u]=null,c.push(o))}}});var Pt,Rt,Wt,$t=/alpha\([^)]*\)/i,It=/opacity\s*=\s*([^)]*)/,zt=/^(top|right|bottom|left)$/,Xt=/^(none|table(?!-c[ea]).+)/,Ut=/^margin/,Vt=RegExp("^("+x+")(.*)$","i"),Yt=RegExp("^("+x+")(?!px)[a-z%]+$","i"),Jt=RegExp("^([+-])=("+x+")","i"),Gt={BODY:"block"},Qt={position:"absolute",visibility:"hidden",display:"block"},Kt={letterSpacing:0,fontWeight:400},Zt=["Top","Right","Bottom","Left"],en=["Webkit","O","Moz","ms"];function tn(e,t){if(t in e)return t;var n=t.charAt(0).toUpperCase()+t.slice(1),r=t,i=en.length;while(i--)if(t=en[i]+n,t in e)return t;return r}function nn(e,t){return e=t||e,"none"===b.css(e,"display")||!b.contains(e.ownerDocument,e)}function rn(e,t){var n,r,i,o=[],a=0,s=e.length;for(;s>a;a++)r=e[a],r.style&&(o[a]=b._data(r,"olddisplay"),n=r.style.display,t?(o[a]||"none"!==n||(r.style.display=""),""===r.style.display&&nn(r)&&(o[a]=b._data(r,"olddisplay",un(r.nodeName)))):o[a]||(i=nn(r),(n&&"none"!==n||!i)&&b._data(r,"olddisplay",i?n:b.css(r,"display"))));for(a=0;s>a;a++)r=e[a],r.style&&(t&&"none"!==r.style.display&&""!==r.style.display||(r.style.display=t?o[a]||"":"none"));return e}b.fn.extend({css:function(e,n){return b.access(this,function(e,n,r){var i,o,a={},s=0;if(b.isArray(n)){for(o=Rt(e),i=n.length;i>s;s++)a[n[s]]=b.css(e,n[s],!1,o);return a}return r!==t?b.style(e,n,r):b.css(e,n)},e,n,arguments.length>1)},show:function(){return rn(this,!0)},hide:function(){return rn(this)},toggle:function(e){var t="boolean"==typeof e;return this.each(function(){(t?e:nn(this))?b(this).show():b(this).hide()})}}),b.extend({cssHooks:{opacity:{get:function(e,t){if(t){var n=Wt(e,"opacity");return""===n?"1":n}}}},cssNumber:{columnCount:!0,fillOpacity:!0,fontWeight:!0,lineHeight:!0,opacity:!0,orphans:!0,widows:!0,zIndex:!0,zoom:!0},cssProps:{"float":b.support.cssFloat?"cssFloat":"styleFloat"},style:function(e,n,r,i){if(e&&3!==e.nodeType&&8!==e.nodeType&&e.style){var o,a,s,u=b.camelCase(n),l=e.style;if(n=b.cssProps[u]||(b.cssProps[u]=tn(l,u)),s=b.cssHooks[n]||b.cssHooks[u],r===t)return s&&"get"in s&&(o=s.get(e,!1,i))!==t?o:l[n];if(a=typeof r,"string"===a&&(o=Jt.exec(r))&&(r=(o[1]+1)*o[2]+parseFloat(b.css(e,n)),a="number"),!(null==r||"number"===a&&isNaN(r)||("number"!==a||b.cssNumber[u]||(r+="px"),b.support.clearCloneStyle||""!==r||0!==n.indexOf("background")||(l[n]="inherit"),s&&"set"in s&&(r=s.set(e,r,i))===t)))try{l[n]=r}catch(c){}}},css:function(e,n,r,i){var o,a,s,u=b.camelCase(n);return n=b.cssProps[u]||(b.cssProps[u]=tn(e.style,u)),s=b.cssHooks[n]||b.cssHooks[u],s&&"get"in s&&(a=s.get(e,!0,r)),a===t&&(a=Wt(e,n,i)),"normal"===a&&n in Kt&&(a=Kt[n]),""===r||r?(o=parseFloat(a),r===!0||b.isNumeric(o)?o||0:a):a},swap:function(e,t,n,r){var i,o,a={};for(o in t)a[o]=e.style[o],e.style[o]=t[o];i=n.apply(e,r||[]);for(o in t)e.style[o]=a[o];return i}}),e.getComputedStyle?(Rt=function(t){return e.getComputedStyle(t,null)},Wt=function(e,n,r){var i,o,a,s=r||Rt(e),u=s?s.getPropertyValue(n)||s[n]:t,l=e.style;return s&&(""!==u||b.contains(e.ownerDocument,e)||(u=b.style(e,n)),Yt.test(u)&&Ut.test(n)&&(i=l.width,o=l.minWidth,a=l.maxWidth,l.minWidth=l.maxWidth=l.width=u,u=s.width,l.width=i,l.minWidth=o,l.maxWidth=a)),u}):o.documentElement.currentStyle&&(Rt=function(e){return e.currentStyle},Wt=function(e,n,r){var i,o,a,s=r||Rt(e),u=s?s[n]:t,l=e.style;return null==u&&l&&l[n]&&(u=l[n]),Yt.test(u)&&!zt.test(n)&&(i=l.left,o=e.runtimeStyle,a=o&&o.left,a&&(o.left=e.currentStyle.left),l.left="fontSize"===n?"1em":u,u=l.pixelLeft+"px",l.left=i,a&&(o.left=a)),""===u?"auto":u});function on(e,t,n){var r=Vt.exec(t);return r?Math.max(0,r[1]-(n||0))+(r[2]||"px"):t}function an(e,t,n,r,i){var o=n===(r?"border":"content")?4:"width"===t?1:0,a=0;for(;4>o;o+=2)"margin"===n&&(a+=b.css(e,n+Zt[o],!0,i)),r?("content"===n&&(a-=b.css(e,"padding"+Zt[o],!0,i)),"margin"!==n&&(a-=b.css(e,"border"+Zt[o]+"Width",!0,i))):(a+=b.css(e,"padding"+Zt[o],!0,i),"padding"!==n&&(a+=b.css(e,"border"+Zt[o]+"Width",!0,i)));return a}function sn(e,t,n){var r=!0,i="width"===t?e.offsetWidth:e.offsetHeight,o=Rt(e),a=b.support.boxSizing&&"border-box"===b.css(e,"boxSizing",!1,o);if(0>=i||null==i){if(i=Wt(e,t,o),(0>i||null==i)&&(i=e.style[t]),Yt.test(i))return i;r=a&&(b.support.boxSizingReliable||i===e.style[t]),i=parseFloat(i)||0}return i+an(e,t,n||(a?"border":"content"),r,o)+"px"}function un(e){var t=o,n=Gt[e];return n||(n=ln(e,t),"none"!==n&&n||(Pt=(Pt||b("<iframe frameborder='0' width='0' height='0'/>").css("cssText","display:block !important")).appendTo(t.documentElement),t=(Pt[0].contentWindow||Pt[0].contentDocument).document,t.write("<!doctype html><html><body>"),t.close(),n=ln(e,t),Pt.detach()),Gt[e]=n),n}function ln(e,t){var n=b(t.createElement(e)).appendTo(t.body),r=b.css(n[0],"display");return n.remove(),r}b.each(["height","width"],function(e,n){b.cssHooks[n]={get:function(e,r,i){return r?0===e.offsetWidth&&Xt.test(b.css(e,"display"))?b.swap(e,Qt,function(){return sn(e,n,i)}):sn(e,n,i):t},set:function(e,t,r){var i=r&&Rt(e);return on(e,t,r?an(e,n,r,b.support.boxSizing&&"border-box"===b.css(e,"boxSizing",!1,i),i):0)}}}),b.support.opacity||(b.cssHooks.opacity={get:function(e,t){return It.test((t&&e.currentStyle?e.currentStyle.filter:e.style.filter)||"")?.01*parseFloat(RegExp.$1)+"":t?"1":""},set:function(e,t){var n=e.style,r=e.currentStyle,i=b.isNumeric(t)?"alpha(opacity="+100*t+")":"",o=r&&r.filter||n.filter||"";n.zoom=1,(t>=1||""===t)&&""===b.trim(o.replace($t,""))&&n.removeAttribute&&(n.removeAttribute("filter"),""===t||r&&!r.filter)||(n.filter=$t.test(o)?o.replace($t,i):o+" "+i)}}),b(function(){b.support.reliableMarginRight||(b.cssHooks.marginRight={get:function(e,n){return n?b.swap(e,{display:"inline-block"},Wt,[e,"marginRight"]):t}}),!b.support.pixelPosition&&b.fn.position&&b.each(["top","left"],function(e,n){b.cssHooks[n]={get:function(e,r){return r?(r=Wt(e,n),Yt.test(r)?b(e).position()[n]+"px":r):t}}})}),b.expr&&b.expr.filters&&(b.expr.filters.hidden=function(e){return 0>=e.offsetWidth&&0>=e.offsetHeight||!b.support.reliableHiddenOffsets&&"none"===(e.style&&e.style.display||b.css(e,"display"))},b.expr.filters.visible=function(e){return!b.expr.filters.hidden(e)}),b.each({margin:"",padding:"",border:"Width"},function(e,t){b.cssHooks[e+t]={expand:function(n){var r=0,i={},o="string"==typeof n?n.split(" "):[n];for(;4>r;r++)i[e+Zt[r]+t]=o[r]||o[r-2]||o[0];return i}},Ut.test(e)||(b.cssHooks[e+t].set=on)});var cn=/%20/g,pn=/\[\]$/,fn=/\r?\n/g,dn=/^(?:submit|button|image|reset|file)$/i,hn=/^(?:input|select|textarea|keygen)/i;b.fn.extend({serialize:function(){return b.param(this.serializeArray())},serializeArray:function(){return this.map(function(){var e=b.prop(this,"elements");return e?b.makeArray(e):this}).filter(function(){var e=this.type;return this.name&&!b(this).is(":disabled")&&hn.test(this.nodeName)&&!dn.test(e)&&(this.checked||!Nt.test(e))}).map(function(e,t){var n=b(this).val();return null==n?null:b.isArray(n)?b.map(n,function(e){return{name:t.name,value:e.replace(fn,"\r\n")}}):{name:t.name,value:n.replace(fn,"\r\n")}}).get()}}),b.param=function(e,n){var r,i=[],o=function(e,t){t=b.isFunction(t)?t():null==t?"":t,i[i.length]=encodeURIComponent(e)+"="+encodeURIComponent(t)};if(n===t&&(n=b.ajaxSettings&&b.ajaxSettings.traditional),b.isArray(e)||e.jquery&&!b.isPlainObject(e))b.each(e,function(){o(this.name,this.value)});else for(r in e)gn(r,e[r],n,o);return i.join("&").replace(cn,"+")};function gn(e,t,n,r){var i;if(b.isArray(t))b.each(t,function(t,i){n||pn.test(e)?r(e,i):gn(e+"["+("object"==typeof i?t:"")+"]",i,n,r)});else if(n||"object"!==b.type(t))r(e,t);else for(i in t)gn(e+"["+i+"]",t[i],n,r)}b.each("blur focus focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup error contextmenu".split(" "),function(e,t){b.fn[t]=function(e,n){return arguments.length>0?this.on(t,null,e,n):this.trigger(t)}}),b.fn.hover=function(e,t){return this.mouseenter(e).mouseleave(t||e)};var mn,yn,vn=b.now(),bn=/\?/,xn=/#.*$/,wn=/([?&])_=[^&]*/,Tn=/^(.*?):[ \t]*([^\r\n]*)\r?$/gm,Nn=/^(?:about|app|app-storage|.+-extension|file|res|widget):$/,Cn=/^(?:GET|HEAD)$/,kn=/^\/\//,En=/^([\w.+-]+:)(?:\/\/([^\/?#:]*)(?::(\d+)|)|)/,Sn=b.fn.load,An={},jn={},Dn="*/".concat("*");try{yn=a.href}catch(Ln){yn=o.createElement("a"),yn.href="",yn=yn.href}mn=En.exec(yn.toLowerCase())||[];function Hn(e){return function(t,n){"string"!=typeof t&&(n=t,t="*");var r,i=0,o=t.toLowerCase().match(w)||[];if(b.isFunction(n))while(r=o[i++])"+"===r[0]?(r=r.slice(1)||"*",(e[r]=e[r]||[]).unshift(n)):(e[r]=e[r]||[]).push(n)}}function qn(e,n,r,i){var o={},a=e===jn;function s(u){var l;return o[u]=!0,b.each(e[u]||[],function(e,u){var c=u(n,r,i);return"string"!=typeof c||a||o[c]?a?!(l=c):t:(n.dataTypes.unshift(c),s(c),!1)}),l}return s(n.dataTypes[0])||!o["*"]&&s("*")}function Mn(e,n){var r,i,o=b.ajaxSettings.flatOptions||{};for(i in n)n[i]!==t&&((o[i]?e:r||(r={}))[i]=n[i]);return r&&b.extend(!0,e,r),e}b.fn.load=function(e,n,r){if("string"!=typeof e&&Sn)return Sn.apply(this,arguments);var i,o,a,s=this,u=e.indexOf(" ");return u>=0&&(i=e.slice(u,e.length),e=e.slice(0,u)),b.isFunction(n)?(r=n,n=t):n&&"object"==typeof n&&(a="POST"),s.length>0&&b.ajax({url:e,type:a,dataType:"html",data:n}).done(function(e){o=arguments,s.html(i?b("<div>").append(b.parseHTML(e)).find(i):e)}).complete(r&&function(e,t){s.each(r,o||[e.responseText,t,e])}),this},b.each(["ajaxStart","ajaxStop","ajaxComplete","ajaxError","ajaxSuccess","ajaxSend"],function(e,t){b.fn[t]=function(e){return this.on(t,e)}}),b.each(["get","post"],function(e,n){b[n]=function(e,r,i,o){return b.isFunction(r)&&(o=o||i,i=r,r=t),b.ajax({url:e,type:n,dataType:o,data:r,success:i})}}),b.extend({active:0,lastModified:{},etag:{},ajaxSettings:{url:yn,type:"GET",isLocal:Nn.test(mn[1]),global:!0,processData:!0,async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8",accepts:{"*":Dn,text:"text/plain",html:"text/html",xml:"application/xml, text/xml",json:"application/json, text/javascript"},contents:{xml:/xml/,html:/html/,json:/json/},responseFields:{xml:"responseXML",text:"responseText"},converters:{"* text":e.String,"text html":!0,"text json":b.parseJSON,"text xml":b.parseXML},flatOptions:{url:!0,context:!0}},ajaxSetup:function(e,t){return t?Mn(Mn(e,b.ajaxSettings),t):Mn(b.ajaxSettings,e)},ajaxPrefilter:Hn(An),ajaxTransport:Hn(jn),ajax:function(e,n){"object"==typeof e&&(n=e,e=t),n=n||{};var r,i,o,a,s,u,l,c,p=b.ajaxSetup({},n),f=p.context||p,d=p.context&&(f.nodeType||f.jquery)?b(f):b.event,h=b.Deferred(),g=b.Callbacks("once memory"),m=p.statusCode||{},y={},v={},x=0,T="canceled",N={readyState:0,getResponseHeader:function(e){var t;if(2===x){if(!c){c={};while(t=Tn.exec(a))c[t[1].toLowerCase()]=t[2]}t=c[e.toLowerCase()]}return null==t?null:t},getAllResponseHeaders:function(){return 2===x?a:null},setRequestHeader:function(e,t){var n=e.toLowerCase();return x||(e=v[n]=v[n]||e,y[e]=t),this},overrideMimeType:function(e){return x||(p.mimeType=e),this},statusCode:function(e){var t;if(e)if(2>x)for(t in e)m[t]=[m[t],e[t]];else N.always(e[N.status]);return this},abort:function(e){var t=e||T;return l&&l.abort(t),k(0,t),this}};if(h.promise(N).complete=g.add,N.success=N.done,N.error=N.fail,p.url=((e||p.url||yn)+"").replace(xn,"").replace(kn,mn[1]+"//"),p.type=n.method||n.type||p.method||p.type,p.dataTypes=b.trim(p.dataType||"*").toLowerCase().match(w)||[""],null==p.crossDomain&&(r=En.exec(p.url.toLowerCase()),p.crossDomain=!(!r||r[1]===mn[1]&&r[2]===mn[2]&&(r[3]||("http:"===r[1]?80:443))==(mn[3]||("http:"===mn[1]?80:443)))),p.data&&p.processData&&"string"!=typeof p.data&&(p.data=b.param(p.data,p.traditional)),qn(An,p,n,N),2===x)return N;u=p.global,u&&0===b.active++&&b.event.trigger("ajaxStart"),p.type=p.type.toUpperCase(),p.hasContent=!Cn.test(p.type),o=p.url,p.hasContent||(p.data&&(o=p.url+=(bn.test(o)?"&":"?")+p.data,delete p.data),p.cache===!1&&(p.url=wn.test(o)?o.replace(wn,"$1_="+vn++):o+(bn.test(o)?"&":"?")+"_="+vn++)),p.ifModified&&(b.lastModified[o]&&N.setRequestHeader("If-Modified-Since",b.lastModified[o]),b.etag[o]&&N.setRequestHeader("If-None-Match",b.etag[o])),(p.data&&p.hasContent&&p.contentType!==!1||n.contentType)&&N.setRequestHeader("Content-Type",p.contentType),N.setRequestHeader("Accept",p.dataTypes[0]&&p.accepts[p.dataTypes[0]]?p.accepts[p.dataTypes[0]]+("*"!==p.dataTypes[0]?", "+Dn+"; q=0.01":""):p.accepts["*"]);for(i in p.headers)N.setRequestHeader(i,p.headers[i]);if(p.beforeSend&&(p.beforeSend.call(f,N,p)===!1||2===x))return N.abort();T="abort";for(i in{success:1,error:1,complete:1})N[i](p[i]);if(l=qn(jn,p,n,N)){N.readyState=1,u&&d.trigger("ajaxSend",[N,p]),p.async&&p.timeout>0&&(s=setTimeout(function(){N.abort("timeout")},p.timeout));try{x=1,l.send(y,k)}catch(C){if(!(2>x))throw C;k(-1,C)}}else k(-1,"No Transport");function k(e,n,r,i){var c,y,v,w,T,C=n;2!==x&&(x=2,s&&clearTimeout(s),l=t,a=i||"",N.readyState=e>0?4:0,r&&(w=_n(p,N,r)),e>=200&&300>e||304===e?(p.ifModified&&(T=N.getResponseHeader("Last-Modified"),T&&(b.lastModified[o]=T),T=N.getResponseHeader("etag"),T&&(b.etag[o]=T)),204===e?(c=!0,C="nocontent"):304===e?(c=!0,C="notmodified"):(c=Fn(p,w),C=c.state,y=c.data,v=c.error,c=!v)):(v=C,(e||!C)&&(C="error",0>e&&(e=0))),N.status=e,N.statusText=(n||C)+"",c?h.resolveWith(f,[y,C,N]):h.rejectWith(f,[N,C,v]),N.statusCode(m),m=t,u&&d.trigger(c?"ajaxSuccess":"ajaxError",[N,p,c?y:v]),g.fireWith(f,[N,C]),u&&(d.trigger("ajaxComplete",[N,p]),--b.active||b.event.trigger("ajaxStop")))}return N},getScript:function(e,n){return b.get(e,t,n,"script")},getJSON:function(e,t,n){return b.get(e,t,n,"json")}});function _n(e,n,r){var i,o,a,s,u=e.contents,l=e.dataTypes,c=e.responseFields;for(s in c)s in r&&(n[c[s]]=r[s]);while("*"===l[0])l.shift(),o===t&&(o=e.mimeType||n.getResponseHeader("Content-Type"));if(o)for(s in u)if(u[s]&&u[s].test(o)){l.unshift(s);break}if(l[0]in r)a=l[0];else{for(s in r){if(!l[0]||e.converters[s+" "+l[0]]){a=s;break}i||(i=s)}a=a||i}return a?(a!==l[0]&&l.unshift(a),r[a]):t}function Fn(e,t){var n,r,i,o,a={},s=0,u=e.dataTypes.slice(),l=u[0];if(e.dataFilter&&(t=e.dataFilter(t,e.dataType)),u[1])for(i in e.converters)a[i.toLowerCase()]=e.converters[i];for(;r=u[++s];)if("*"!==r){if("*"!==l&&l!==r){if(i=a[l+" "+r]||a["* "+r],!i)for(n in a)if(o=n.split(" "),o[1]===r&&(i=a[l+" "+o[0]]||a["* "+o[0]])){i===!0?i=a[n]:a[n]!==!0&&(r=o[0],u.splice(s--,0,r));break}if(i!==!0)if(i&&e["throws"])t=i(t);else try{t=i(t)}catch(c){return{state:"parsererror",error:i?c:"No conversion from "+l+" to "+r}}}l=r}return{state:"success",data:t}}b.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/(?:java|ecma)script/},converters:{"text script":function(e){return b.globalEval(e),e}}}),b.ajaxPrefilter("script",function(e){e.cache===t&&(e.cache=!1),e.crossDomain&&(e.type="GET",e.global=!1)}),b.ajaxTransport("script",function(e){if(e.crossDomain){var n,r=o.head||b("head")[0]||o.documentElement;return{send:function(t,i){n=o.createElement("script"),n.async=!0,e.scriptCharset&&(n.charset=e.scriptCharset),n.src=e.url,n.onload=n.onreadystatechange=function(e,t){(t||!n.readyState||/loaded|complete/.test(n.readyState))&&(n.onload=n.onreadystatechange=null,n.parentNode&&n.parentNode.removeChild(n),n=null,t||i(200,"success"))},r.insertBefore(n,r.firstChild)},abort:function(){n&&n.onload(t,!0)}}}});var On=[],Bn=/(=)\?(?=&|$)|\?\?/;b.ajaxSetup({jsonp:"callback",jsonpCallback:function(){var e=On.pop()||b.expando+"_"+vn++;return this[e]=!0,e}}),b.ajaxPrefilter("json jsonp",function(n,r,i){var o,a,s,u=n.jsonp!==!1&&(Bn.test(n.url)?"url":"string"==typeof n.data&&!(n.contentType||"").indexOf("application/x-www-form-urlencoded")&&Bn.test(n.data)&&"data");return u||"jsonp"===n.dataTypes[0]?(o=n.jsonpCallback=b.isFunction(n.jsonpCallback)?n.jsonpCallback():n.jsonpCallback,u?n[u]=n[u].replace(Bn,"$1"+o):n.jsonp!==!1&&(n.url+=(bn.test(n.url)?"&":"?")+n.jsonp+"="+o),n.converters["script json"]=function(){return s||b.error(o+" was not called"),s[0]},n.dataTypes[0]="json",a=e[o],e[o]=function(){s=arguments},i.always(function(){e[o]=a,n[o]&&(n.jsonpCallback=r.jsonpCallback,On.push(o)),s&&b.isFunction(a)&&a(s[0]),s=a=t}),"script"):t});var Pn,Rn,Wn=0,$n=e.ActiveXObject&&function(){var e;for(e in Pn)Pn[e](t,!0)};function In(){try{return new e.XMLHttpRequest}catch(t){}}function zn(){try{return new e.ActiveXObject("Microsoft.XMLHTTP")}catch(t){}}b.ajaxSettings.xhr=e.ActiveXObject?function(){return!this.isLocal&&In()||zn()}:In,Rn=b.ajaxSettings.xhr(),b.support.cors=!!Rn&&"withCredentials"in Rn,Rn=b.support.ajax=!!Rn,Rn&&b.ajaxTransport(function(n){if(!n.crossDomain||b.support.cors){var r;return{send:function(i,o){var a,s,u=n.xhr();if(n.username?u.open(n.type,n.url,n.async,n.username,n.password):u.open(n.type,n.url,n.async),n.xhrFields)for(s in n.xhrFields)u[s]=n.xhrFields[s];n.mimeType&&u.overrideMimeType&&u.overrideMimeType(n.mimeType),n.crossDomain||i["X-Requested-With"]||(i["X-Requested-With"]="XMLHttpRequest");try{for(s in i)u.setRequestHeader(s,i[s])}catch(l){}u.send(n.hasContent&&n.data||null),r=function(e,i){var s,l,c,p;try{if(r&&(i||4===u.readyState))if(r=t,a&&(u.onreadystatechange=b.noop,$n&&delete Pn[a]),i)4!==u.readyState&&u.abort();else{p={},s=u.status,l=u.getAllResponseHeaders(),"string"==typeof u.responseText&&(p.text=u.responseText);try{c=u.statusText}catch(f){c=""}s||!n.isLocal||n.crossDomain?1223===s&&(s=204):s=p.text?200:404}}catch(d){i||o(-1,d)}p&&o(s,c,p,l)},n.async?4===u.readyState?setTimeout(r):(a=++Wn,$n&&(Pn||(Pn={},b(e).unload($n)),Pn[a]=r),u.onreadystatechange=r):r()},abort:function(){r&&r(t,!0)}}}});var Xn,Un,Vn=/^(?:toggle|show|hide)$/,Yn=RegExp("^(?:([+-])=|)("+x+")([a-z%]*)$","i"),Jn=/queueHooks$/,Gn=[nr],Qn={"*":[function(e,t){var n,r,i=this.createTween(e,t),o=Yn.exec(t),a=i.cur(),s=+a||0,u=1,l=20;if(o){if(n=+o[2],r=o[3]||(b.cssNumber[e]?"":"px"),"px"!==r&&s){s=b.css(i.elem,e,!0)||n||1;do u=u||".5",s/=u,b.style(i.elem,e,s+r);while(u!==(u=i.cur()/a)&&1!==u&&--l)}i.unit=r,i.start=s,i.end=o[1]?s+(o[1]+1)*n:n}return i}]};function Kn(){return setTimeout(function(){Xn=t}),Xn=b.now()}function Zn(e,t){b.each(t,function(t,n){var r=(Qn[t]||[]).concat(Qn["*"]),i=0,o=r.length;for(;o>i;i++)if(r[i].call(e,t,n))return})}function er(e,t,n){var r,i,o=0,a=Gn.length,s=b.Deferred().always(function(){delete u.elem}),u=function(){if(i)return!1;var t=Xn||Kn(),n=Math.max(0,l.startTime+l.duration-t),r=n/l.duration||0,o=1-r,a=0,u=l.tweens.length;for(;u>a;a++)l.tweens[a].run(o);return s.notifyWith(e,[l,o,n]),1>o&&u?n:(s.resolveWith(e,[l]),!1)},l=s.promise({elem:e,props:b.extend({},t),opts:b.extend(!0,{specialEasing:{}},n),originalProperties:t,originalOptions:n,startTime:Xn||Kn(),duration:n.duration,tweens:[],createTween:function(t,n){var r=b.Tween(e,l.opts,t,n,l.opts.specialEasing[t]||l.opts.easing);return l.tweens.push(r),r},stop:function(t){var n=0,r=t?l.tweens.length:0;if(i)return this;for(i=!0;r>n;n++)l.tweens[n].run(1);return t?s.resolveWith(e,[l,t]):s.rejectWith(e,[l,t]),this}}),c=l.props;for(tr(c,l.opts.specialEasing);a>o;o++)if(r=Gn[o].call(l,e,c,l.opts))return r;return Zn(l,c),b.isFunction(l.opts.start)&&l.opts.start.call(e,l),b.fx.timer(b.extend(u,{elem:e,anim:l,queue:l.opts.queue})),l.progress(l.opts.progress).done(l.opts.done,l.opts.complete).fail(l.opts.fail).always(l.opts.always)}function tr(e,t){var n,r,i,o,a;for(i in e)if(r=b.camelCase(i),o=t[r],n=e[i],b.isArray(n)&&(o=n[1],n=e[i]=n[0]),i!==r&&(e[r]=n,delete e[i]),a=b.cssHooks[r],a&&"expand"in a){n=a.expand(n),delete e[r];for(i in n)i in e||(e[i]=n[i],t[i]=o)}else t[r]=o}b.Animation=b.extend(er,{tweener:function(e,t){b.isFunction(e)?(t=e,e=["*"]):e=e.split(" ");var n,r=0,i=e.length;for(;i>r;r++)n=e[r],Qn[n]=Qn[n]||[],Qn[n].unshift(t)},prefilter:function(e,t){t?Gn.unshift(e):Gn.push(e)}});function nr(e,t,n){var r,i,o,a,s,u,l,c,p,f=this,d=e.style,h={},g=[],m=e.nodeType&&nn(e);n.queue||(c=b._queueHooks(e,"fx"),null==c.unqueued&&(c.unqueued=0,p=c.empty.fire,c.empty.fire=function(){c.unqueued||p()}),c.unqueued++,f.always(function(){f.always(function(){c.unqueued--,b.queue(e,"fx").length||c.empty.fire()})})),1===e.nodeType&&("height"in t||"width"in t)&&(n.overflow=[d.overflow,d.overflowX,d.overflowY],"inline"===b.css(e,"display")&&"none"===b.css(e,"float")&&(b.support.inlineBlockNeedsLayout&&"inline"!==un(e.nodeName)?d.zoom=1:d.display="inline-block")),n.overflow&&(d.overflow="hidden",b.support.shrinkWrapBlocks||f.always(function(){d.overflow=n.overflow[0],d.overflowX=n.overflow[1],d.overflowY=n.overflow[2]}));for(i in t)if(a=t[i],Vn.exec(a)){if(delete t[i],u=u||"toggle"===a,a===(m?"hide":"show"))continue;g.push(i)}if(o=g.length){s=b._data(e,"fxshow")||b._data(e,"fxshow",{}),"hidden"in s&&(m=s.hidden),u&&(s.hidden=!m),m?b(e).show():f.done(function(){b(e).hide()}),f.done(function(){var t;b._removeData(e,"fxshow");for(t in h)b.style(e,t,h[t])});for(i=0;o>i;i++)r=g[i],l=f.createTween(r,m?s[r]:0),h[r]=s[r]||b.style(e,r),r in s||(s[r]=l.start,m&&(l.end=l.start,l.start="width"===r||"height"===r?1:0))}}function rr(e,t,n,r,i){return new rr.prototype.init(e,t,n,r,i)}b.Tween=rr,rr.prototype={constructor:rr,init:function(e,t,n,r,i,o){this.elem=e,this.prop=n,this.easing=i||"swing",this.options=t,this.start=this.now=this.cur(),this.end=r,this.unit=o||(b.cssNumber[n]?"":"px")},cur:function(){var e=rr.propHooks[this.prop];return e&&e.get?e.get(this):rr.propHooks._default.get(this)},run:function(e){var t,n=rr.propHooks[this.prop];return this.pos=t=this.options.duration?b.easing[this.easing](e,this.options.duration*e,0,1,this.options.duration):e,this.now=(this.end-this.start)*t+this.start,this.options.step&&this.options.step.call(this.elem,this.now,this),n&&n.set?n.set(this):rr.propHooks._default.set(this),this}},rr.prototype.init.prototype=rr.prototype,rr.propHooks={_default:{get:function(e){var t;return null==e.elem[e.prop]||e.elem.style&&null!=e.elem.style[e.prop]?(t=b.css(e.elem,e.prop,""),t&&"auto"!==t?t:0):e.elem[e.prop]},set:function(e){b.fx.step[e.prop]?b.fx.step[e.prop](e):e.elem.style&&(null!=e.elem.style[b.cssProps[e.prop]]||b.cssHooks[e.prop])?b.style(e.elem,e.prop,e.now+e.unit):e.elem[e.prop]=e.now}}},rr.propHooks.scrollTop=rr.propHooks.scrollLeft={set:function(e){e.elem.nodeType&&e.elem.parentNode&&(e.elem[e.prop]=e.now)}},b.each(["toggle","show","hide"],function(e,t){var n=b.fn[t];b.fn[t]=function(e,r,i){return null==e||"boolean"==typeof e?n.apply(this,arguments):this.animate(ir(t,!0),e,r,i)}}),b.fn.extend({fadeTo:function(e,t,n,r){return this.filter(nn).css("opacity",0).show().end().animate({opacity:t},e,n,r)},animate:function(e,t,n,r){var i=b.isEmptyObject(e),o=b.speed(t,n,r),a=function(){var t=er(this,b.extend({},e),o);a.finish=function(){t.stop(!0)},(i||b._data(this,"finish"))&&t.stop(!0)};return a.finish=a,i||o.queue===!1?this.each(a):this.queue(o.queue,a)},stop:function(e,n,r){var i=function(e){var t=e.stop;delete e.stop,t(r)};return"string"!=typeof e&&(r=n,n=e,e=t),n&&e!==!1&&this.queue(e||"fx",[]),this.each(function(){var t=!0,n=null!=e&&e+"queueHooks",o=b.timers,a=b._data(this);if(n)a[n]&&a[n].stop&&i(a[n]);else for(n in a)a[n]&&a[n].stop&&Jn.test(n)&&i(a[n]);for(n=o.length;n--;)o[n].elem!==this||null!=e&&o[n].queue!==e||(o[n].anim.stop(r),t=!1,o.splice(n,1));(t||!r)&&b.dequeue(this,e)})},finish:function(e){return e!==!1&&(e=e||"fx"),this.each(function(){var t,n=b._data(this),r=n[e+"queue"],i=n[e+"queueHooks"],o=b.timers,a=r?r.length:0;for(n.finish=!0,b.queue(this,e,[]),i&&i.cur&&i.cur.finish&&i.cur.finish.call(this),t=o.length;t--;)o[t].elem===this&&o[t].queue===e&&(o[t].anim.stop(!0),o.splice(t,1));for(t=0;a>t;t++)r[t]&&r[t].finish&&r[t].finish.call(this);delete n.finish})}});function ir(e,t){var n,r={height:e},i=0;for(t=t?1:0;4>i;i+=2-t)n=Zt[i],r["margin"+n]=r["padding"+n]=e;return t&&(r.opacity=r.width=e),r}b.each({slideDown:ir("show"),slideUp:ir("hide"),slideToggle:ir("toggle"),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(e,t){b.fn[e]=function(e,n,r){return this.animate(t,e,n,r)}}),b.speed=function(e,t,n){var r=e&&"object"==typeof e?b.extend({},e):{complete:n||!n&&t||b.isFunction(e)&&e,duration:e,easing:n&&t||t&&!b.isFunction(t)&&t};return r.duration=b.fx.off?0:"number"==typeof r.duration?r.duration:r.duration in b.fx.speeds?b.fx.speeds[r.duration]:b.fx.speeds._default,(null==r.queue||r.queue===!0)&&(r.queue="fx"),r.old=r.complete,r.complete=function(){b.isFunction(r.old)&&r.old.call(this),r.queue&&b.dequeue(this,r.queue)},r},b.easing={linear:function(e){return e},swing:function(e){return.5-Math.cos(e*Math.PI)/2}},b.timers=[],b.fx=rr.prototype.init,b.fx.tick=function(){var e,n=b.timers,r=0;for(Xn=b.now();n.length>r;r++)e=n[r],e()||n[r]!==e||n.splice(r--,1);n.length||b.fx.stop(),Xn=t},b.fx.timer=function(e){e()&&b.timers.push(e)&&b.fx.start()},b.fx.interval=13,b.fx.start=function(){Un||(Un=setInterval(b.fx.tick,b.fx.interval))},b.fx.stop=function(){clearInterval(Un),Un=null},b.fx.speeds={slow:600,fast:200,_default:400},b.fx.step={},b.expr&&b.expr.filters&&(b.expr.filters.animated=function(e){return b.grep(b.timers,function(t){return e===t.elem}).length}),b.fn.offset=function(e){if(arguments.length)return e===t?this:this.each(function(t){b.offset.setOffset(this,e,t)});var n,r,o={top:0,left:0},a=this[0],s=a&&a.ownerDocument;if(s)return n=s.documentElement,b.contains(n,a)?(typeof a.getBoundingClientRect!==i&&(o=a.getBoundingClientRect()),r=or(s),{top:o.top+(r.pageYOffset||n.scrollTop)-(n.clientTop||0),left:o.left+(r.pageXOffset||n.scrollLeft)-(n.clientLeft||0)}):o},b.offset={setOffset:function(e,t,n){var r=b.css(e,"position");"static"===r&&(e.style.position="relative");var i=b(e),o=i.offset(),a=b.css(e,"top"),s=b.css(e,"left"),u=("absolute"===r||"fixed"===r)&&b.inArray("auto",[a,s])>-1,l={},c={},p,f;u?(c=i.position(),p=c.top,f=c.left):(p=parseFloat(a)||0,f=parseFloat(s)||0),b.isFunction(t)&&(t=t.call(e,n,o)),null!=t.top&&(l.top=t.top-o.top+p),null!=t.left&&(l.left=t.left-o.left+f),"using"in t?t.using.call(e,l):i.css(l)}},b.fn.extend({position:function(){if(this[0]){var e,t,n={top:0,left:0},r=this[0];return"fixed"===b.css(r,"position")?t=r.getBoundingClientRect():(e=this.offsetParent(),t=this.offset(),b.nodeName(e[0],"html")||(n=e.offset()),n.top+=b.css(e[0],"borderTopWidth",!0),n.left+=b.css(e[0],"borderLeftWidth",!0)),{top:t.top-n.top-b.css(r,"marginTop",!0),left:t.left-n.left-b.css(r,"marginLeft",!0)}}},offsetParent:function(){return this.map(function(){var e=this.offsetParent||o.documentElement;while(e&&!b.nodeName(e,"html")&&"static"===b.css(e,"position"))e=e.offsetParent;return e||o.documentElement})}}),b.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(e,n){var r=/Y/.test(n);b.fn[e]=function(i){return b.access(this,function(e,i,o){var a=or(e);return o===t?a?n in a?a[n]:a.document.documentElement[i]:e[i]:(a?a.scrollTo(r?b(a).scrollLeft():o,r?o:b(a).scrollTop()):e[i]=o,t)},e,i,arguments.length,null)}});function or(e){return b.isWindow(e)?e:9===e.nodeType?e.defaultView||e.parentWindow:!1}b.each({Height:"height",Width:"width"},function(e,n){b.each({padding:"inner"+e,content:n,"":"outer"+e},function(r,i){b.fn[i]=function(i,o){var a=arguments.length&&(r||"boolean"!=typeof i),s=r||(i===!0||o===!0?"margin":"border");return b.access(this,function(n,r,i){var o;return b.isWindow(n)?n.document.documentElement["client"+e]:9===n.nodeType?(o=n.documentElement,Math.max(n.body["scroll"+e],o["scroll"+e],n.body["offset"+e],o["offset"+e],o["client"+e])):i===t?b.css(n,r,s):b.style(n,r,i,s)},n,a?i:t,a,null)}})}),e.jQuery=e.$=b,"function"==typeof define&&define.amd&&define.amd.jQuery&&define("jquery",[],function(){return b})})(window);;
//
// LESS - Leaner CSS v1.3.3
// http://lesscss.org
// 
// Copyright (c) 2009-2013, Alexis Sellier
// Licensed under the Apache 2.0 License.
//
(function(e,t){function n(t){return e.less[t.split("/")[1]]}function f(){r.env==="development"?(r.optimization=0,r.watchTimer=setInterval(function(){r.watchMode&&g(function(e,t,n,r,i){t&&S(t.toCSS(),r,i.lastModified)})},r.poll)):r.optimization=3}function m(){var e=document.getElementsByTagName("style");for(var t=0;t<e.length;t++)e[t].type.match(p)&&(new r.Parser({filename:document.location.href.replace(/#.*$/,""),dumpLineNumbers:r.dumpLineNumbers})).parse(e[t].innerHTML||"",function(n,r){var i=r.toCSS(),s=e[t];s.type="text/css",s.styleSheet?s.styleSheet.cssText=i:s.innerHTML=i})}function g(e,t){for(var n=0;n<r.sheets.length;n++)w(r.sheets[n],e,t,r.sheets.length-(n+1))}function y(e,t){var n=b(e),r=b(t),i,s,o,u,a="";if(n.hostPart!==r.hostPart)return"";s=Math.max(r.directories.length,n.directories.length);for(i=0;i<s;i++)if(r.directories[i]!==n.directories[i])break;u=r.directories.slice(i),o=n.directories.slice(i);for(i=0;i<u.length-1;i++)a+="../";for(i=0;i<o.length-1;i++)a+=o[i]+"/";return a}function b(e,t){var n=/^((?:[a-z-]+:)?\/\/(?:[^\/\?#]*\/)|([\/\\]))?((?:[^\/\\\?#]*[\/\\])*)([^\/\\\?#]*)([#\?].*)?$/,r=e.match(n),i={},s=[],o,u;if(!r)throw new Error("Could not parse sheet href - '"+e+"'");if(!r[1]||r[2]){u=t.match(n);if(!u)throw new Error("Could not parse page url - '"+t+"'");r[1]=u[1],r[2]||(r[3]=u[3]+r[3])}if(r[3]){s=r[3].replace("\\","/").split("/");for(o=0;o<s.length;o++)s[o]===".."&&o>0&&(s.splice(o-1,2),o-=2)}return i.hostPart=r[1],i.directories=s,i.path=r[1]+s.join("/"),i.fileUrl=i.path+(r[4]||""),i.url=i.fileUrl+(r[5]||""),i}function w(t,n,i,s){var o=t.contents||{},u=t.files||{},a=b(t.href,e.location.href),f=a.url,c=l&&l.getItem(f),h=l&&l.getItem(f+":timestamp"),p={css:c,timestamp:h},d;r.relativeUrls?r.rootpath?t.entryPath?d=b(r.rootpath+y(a.path,t.entryPath)).path:d=r.rootpath:d=a.path:r.rootpath?d=r.rootpath:t.entryPath?d=t.entryPath:d=a.path,x(f,t.type,function(e,l){v+=e.replace(/@import .+?;/ig,"");if(!i&&p&&l&&(new Date(l)).valueOf()===(new Date(p.timestamp)).valueOf())S(p.css,t),n(null,null,e,t,{local:!0,remaining:s},f);else try{o[f]=e,(new r.Parser({optimization:r.optimization,paths:[a.path],entryPath:t.entryPath||a.path,mime:t.type,filename:f,rootpath:d,relativeUrls:t.relativeUrls,contents:o,files:u,dumpLineNumbers:r.dumpLineNumbers})).parse(e,function(r,i){if(r)return k(r,f);try{n(r,i,e,t,{local:!1,lastModified:l,remaining:s},f),N(document.getElementById("less-error-message:"+E(f)))}catch(r){k(r,f)}})}catch(c){k(c,f)}},function(e,t){throw new Error("Couldn't load "+t+" ("+e+")")})}function E(e){return e.replace(/^[a-z]+:\/\/?[^\/]+/,"").replace(/^\//,"").replace(/\.[a-zA-Z]+$/,"").replace(/[^\.\w-]+/g,"-").replace(/\./g,":")}function S(e,t,n){var r,i=t.href||"",s="less:"+(t.title||E(i));if((r=document.getElementById(s))===null){r=document.createElement("style"),r.type="text/css",t.media&&(r.media=t.media),r.id=s;var o=t&&t.nextSibling||null;(o||document.getElementsByTagName("head")[0]).parentNode.insertBefore(r,o)}if(r.styleSheet)try{r.styleSheet.cssText=e}catch(u){throw new Error("Couldn't reassign styleSheet.cssText.")}else(function(e){r.childNodes.length>0?r.firstChild.nodeValue!==e.nodeValue&&r.replaceChild(e,r.firstChild):r.appendChild(e)})(document.createTextNode(e));if(n&&l){C("saving "+i+" to cache.");try{l.setItem(i,e),l.setItem(i+":timestamp",n)}catch(u){C("failed to save")}}}function x(e,t,n,i){function a(t,n,r){t.status>=200&&t.status<300?n(t.responseText,t.getResponseHeader("Last-Modified")):typeof r=="function"&&r(t.status,e)}var s=T(),u=o?r.fileAsync:r.async;typeof s.overrideMimeType=="function"&&s.overrideMimeType("text/css"),s.open("GET",e,u),s.setRequestHeader("Accept",t||"text/x-less, text/css; q=0.9, */*; q=0.5"),s.send(null),o&&!r.fileAsync?s.status===0||s.status>=200&&s.status<300?n(s.responseText):i(s.status,e):u?s.onreadystatechange=function(){s.readyState==4&&a(s,n,i)}:a(s,n,i)}function T(){if(e.XMLHttpRequest)return new XMLHttpRequest;try{return new ActiveXObject("MSXML2.XMLHTTP.3.0")}catch(t){return C("browser doesn't support AJAX."),null}}function N(e){return e&&e.parentNode.removeChild(e)}function C(e){r.env=="development"&&typeof console!="undefined"&&console.log("less: "+e)}function k(e,t){var n="less-error-message:"+E(t),i='<li><label>{line}</label><pre class="{class}">{content}</pre></li>',s=document.createElement("div"),o,u,a=[],f=e.filename||t,l=f.match(/([^\/]+(\?.*)?)$/)[1];s.id=n,s.className="less-error-message",u="<h3>"+(e.message||"There is an error in your .less file")+"</h3>"+'<p>in <a href="'+f+'">'+l+"</a> ";var c=function(e,t,n){e.extract[t]&&a.push(i.replace(/\{line\}/,parseInt(e.line)+(t-1)).replace(/\{class\}/,n).replace(/\{content\}/,e.extract[t]))};e.stack?u+="<br/>"+e.stack.split("\n").slice(1).join("<br/>"):e.extract&&(c(e,0,""),c(e,1,"line"),c(e,2,""),u+="on line "+e.line+", column "+(e.column+1)+":</p>"+"<ul>"+a.join("")+"</ul>"),s.innerHTML=u,S([".less-error-message ul, .less-error-message li {","list-style-type: none;","margin-right: 15px;","padding: 4px 0;","margin: 0;","}",".less-error-message label {","font-size: 12px;","margin-right: 15px;","padding: 4px 0;","color: #cc7777;","}",".less-error-message pre {","color: #dd6666;","padding: 4px 0;","margin: 0;","display: inline-block;","}",".less-error-message pre.line {","color: #ff0000;","}",".less-error-message h3 {","font-size: 20px;","font-weight: bold;","padding: 15px 0 5px 0;","margin: 0;","}",".less-error-message a {","color: #10a","}",".less-error-message .error {","color: red;","font-weight: bold;","padding-bottom: 2px;","border-bottom: 1px dashed red;","}"].join("\n"),{title:"error-message"}),s.style.cssText=["font-family: Arial, sans-serif","border: 1px solid #e00","background-color: #eee","border-radius: 5px","-webkit-border-radius: 5px","-moz-border-radius: 5px","color: #e00","padding: 15px","margin-bottom: 15px"].join(";"),r.env=="development"&&(o=setInterval(function(){document.body&&(document.getElementById(n)?document.body.replaceChild(s,document.getElementById(n)):document.body.insertBefore(s,document.body.firstChild),clearInterval(o))},10))}Array.isArray||(Array.isArray=function(e){return Object.prototype.toString.call(e)==="[object Array]"||e instanceof Array}),Array.prototype.forEach||(Array.prototype.forEach=function(e,t){var n=this.length>>>0;for(var r=0;r<n;r++)r in this&&e.call(t,this[r],r,this)}),Array.prototype.map||(Array.prototype.map=function(e){var t=this.length>>>0,n=new Array(t),r=arguments[1];for(var i=0;i<t;i++)i in this&&(n[i]=e.call(r,this[i],i,this));return n}),Array.prototype.filter||(Array.prototype.filter=function(e){var t=[],n=arguments[1];for(var r=0;r<this.length;r++)e.call(n,this[r])&&t.push(this[r]);return t}),Array.prototype.reduce||(Array.prototype.reduce=function(e){var t=this.length>>>0,n=0;if(t===0&&arguments.length===1)throw new TypeError;if(arguments.length>=2)var r=arguments[1];else do{if(n in this){r=this[n++];break}if(++n>=t)throw new TypeError}while(!0);for(;n<t;n++)n in this&&(r=e.call(null,r,this[n],n,this));return r}),Array.prototype.indexOf||(Array.prototype.indexOf=function(e){var t=this.length,n=arguments[1]||0;if(!t)return-1;if(n>=t)return-1;n<0&&(n+=t);for(;n<t;n++){if(!Object.prototype.hasOwnProperty.call(this,n))continue;if(e===this[n])return n}return-1}),Object.keys||(Object.keys=function(e){var t=[];for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&t.push(n);return t}),String.prototype.trim||(String.prototype.trim=function(){return String(this).replace(/^\s\s*/,"").replace(/\s\s*$/,"")});var r,i,s;typeof environment=="object"&&{}.toString.call(environment)==="[object Environment]"?(typeof e=="undefined"?r={}:r=e.less={},i=r.tree={},r.mode="rhino"):typeof e=="undefined"?(r=exports,i=n("./tree"),r.mode="node"):(typeof e.less=="undefined"&&(e.less={}),r=e.less,i=e.less.tree={},r.mode="browser"),r.Parser=function(t){function g(){a=c[u],f=o,h=o}function y(){c[u]=a,o=f,h=o}function b(){o>h&&(c[u]=c[u].slice(o-h),h=o)}function w(e){var t=e.charCodeAt(0);return t===32||t===10||t===9}function E(e){var t,n,r,i,a;if(e instanceof Function)return e.call(p.parsers);if(typeof e=="string")t=s.charAt(o)===e?e:null,r=1,b();else{b();if(!(t=e.exec(c[u])))return null;r=t[0].length}if(t)return S(r),typeof t=="string"?t:t.length===1?t[0]:t}function S(e){var t=o,n=u,r=o+c[u].length,i=o+=e;while(o<r){if(!w(s.charAt(o)))break;o++}return c[u]=c[u].slice(e+(o-i)),h=o,c[u].length===0&&u<c.length-1&&u++,t!==o||n!==u}function x(e,t){var n=E(e);if(!!n)return n;T(t||(typeof e=="string"?"expected '"+e+"' got '"+s.charAt(o)+"'":"unexpected token"))}function T(e,t){var n=new Error(e);throw n.index=o,n.type=t||"Syntax",n}function N(e){return typeof e=="string"?s.charAt(o)===e:e.test(c[u])?!0:!1}function C(e,t){return e.filename&&t.filename&&e.filename!==t.filename?p.imports.contents[e.filename]:s}function k(e,t){for(var n=e,r=-1;n>=0&&t.charAt(n)!=="\n";n--)r++;return{line:typeof e=="number"?(t.slice(0,e).match(/\n/g)||"").length:null,column:r}}function L(e){return r.mode==="browser"||r.mode==="rhino"?e.filename:n("path").resolve(e.filename)}function A(e,t,n){return{lineNumber:k(e,t).line+1,fileName:L(n)}}function O(e,t){var n=C(e,t),r=k(e.index,n),i=r.line,s=r.column,o=n.split("\n");this.type=e.type||"Syntax",this.message=e.message,this.filename=e.filename||t.filename,this.index=e.index,this.line=typeof i=="number"?i+1:null,this.callLine=e.call&&k(e.call,n).line+1,this.callExtract=o[k(e.call,n).line],this.stack=e.stack,this.column=s,this.extract=[o[i-1],o[i],o[i+1]]}var s,o,u,a,f,l,c,h,p,d=this,t=t||{};t.contents||(t.contents={}),t.rootpath=t.rootpath||"",t.files||(t.files={});var v=function(){},m=this.imports={paths:t.paths||[],queue:[],files:t.files,contents:t.contents,mime:t.mime,error:null,push:function(e,n){var i=this;this.queue.push(e),r.Parser.importer(e,this.paths,function(t,r,s){i.queue.splice(i.queue.indexOf(e),1);var o=s in i.files;i.files[s]=r,t&&!i.error&&(i.error=t),n(t,r,o),i.queue.length===0&&v(i.error)},t)}};return this.env=t=t||{},this.optimization="optimization"in this.env?this.env.optimization:1,this.env.filename=this.env.filename||null,p={imports:m,parse:function(e,a){var f,d,m,g,y,b,w=[],S,x=null;o=u=h=l=0,s=e.replace(/\r\n/g,"\n"),s=s.replace(/^\uFEFF/,""),c=function(e){var n=0,r=/(?:@\{[\w-]+\}|[^"'`\{\}\/\(\)\\])+/g,i=/\/\*(?:[^*]|\*+[^\/*])*\*+\/|\/\/.*/g,o=/"((?:[^"\\\r\n]|\\.)*)"|'((?:[^'\\\r\n]|\\.)*)'|`((?:[^`]|\\.)*)`/g,u=0,a,f=e[0],l;for(var c=0,h,p;c<s.length;){r.lastIndex=c,(a=r.exec(s))&&a.index===c&&(c+=a[0].length,f.push(a[0])),h=s.charAt(c),i.lastIndex=o.lastIndex=c;if(a=o.exec(s))if(a.index===c){c+=a[0].length,f.push(a[0]);continue}if(!l&&h==="/"){p=s.charAt(c+1);if(p==="/"||p==="*")if(a=i.exec(s))if(a.index===c){c+=a[0].length,f.push(a[0]);continue}}switch(h){case"{":if(!l){u++,f.push(h);break};case"}":if(!l){u--,f.push(h),e[++n]=f=[];break};case"(":if(!l){l=!0,f.push(h);break};case")":if(l){l=!1,f.push(h);break};default:f.push(h)}c++}return u!=0&&(x=new O({index:c-1,type:"Parse",message:u>0?"missing closing `}`":"missing opening `{`",filename:t.filename},t)),e.map(function(e){return e.join("")})}([[]]);if(x)return a(x,t);try{f=new i.Ruleset([],E(this.parsers.primary)),f.root=!0}catch(T){return a(new O(T,t))}f.toCSS=function(e){var s,o,u;return function(s,o){var u=[],a;s=s||{},typeof o=="object"&&!Array.isArray(o)&&(o=Object.keys(o).map(function(e){var t=o[e];return t instanceof i.Value||(t instanceof i.Expression||(t=new i.Expression([t])),t=new i.Value([t])),new i.Rule("@"+e,t,!1,0)}),u=[new i.Ruleset(null,o)]);try{var f=e.call(this,{frames:u}).toCSS([],{compress:s.compress||!1,dumpLineNumbers:t.dumpLineNumbers})}catch(l){throw new O(l,t)}if(a=p.imports.error)throw a instanceof O?a:new O(a,t);return s.yuicompress&&r.mode==="node"?n("ycssmin").cssmin(f):s.compress?f.replace(/(\s)+/g,"$1"):f}}(f.eval);if(o<s.length-1){o=l,b=s.split("\n"),y=(s.slice(0,o).match(/\n/g)||"").length+1;for(var N=o,C=-1;N>=0&&s.charAt(N)!=="\n";N--)C++;x={type:"Parse",message:"Syntax Error on line "+y,index:o,filename:t.filename,line:y,column:C,extract:[b[y-2],b[y-1],b[y]]}}this.imports.queue.length>0?v=function(e){e=x||e,e?a(e):a(null,f)}:a(x,f)},parsers:{primary:function(){var e,t=[];while((e=E(this.mixin.definition)||E(this.rule)||E(this.ruleset)||E(this.mixin.call)||E(this.comment)||E(this.directive))||E(/^[\s\n]+/)||E(/^;+/))e&&t.push(e);return t},comment:function(){var e;if(s.charAt(o)!=="/")return;if(s.charAt(o+1)==="/")return new i.Comment(E(/^\/\/.*/),!0);if(e=E(/^\/\*(?:[^*]|\*+[^\/*])*\*+\/\n?/))return new i.Comment(e)},entities:{quoted:function(){var e,t=o,n;s.charAt(t)==="~"&&(t++,n=!0);if(s.charAt(t)!=='"'&&s.charAt(t)!=="'")return;n&&E("~");if(e=E(/^"((?:[^"\\\r\n]|\\.)*)"|'((?:[^'\\\r\n]|\\.)*)'/))return new i.Quoted(e[0],e[1]||e[2],n)},keyword:function(){var e;if(e=E(/^[_A-Za-z-][_A-Za-z0-9-]*/))return i.colors.hasOwnProperty(e)?new i.Color(i.colors[e].slice(1)):new i.Keyword(e)},call:function(){var e,n,r,s,a=o;if(!(e=/^([\w-]+|%|progid:[\w\.]+)\(/.exec(c[u])))return;e=e[1],n=e.toLowerCase();if(n==="url")return null;o+=e.length;if(n==="alpha"){s=E(this.alpha);if(typeof s!="undefined")return s}E("("),r=E(this.entities.arguments);if(!E(")"))return;if(e)return new i.Call(e,r,a,t.filename)},arguments:function(){var e=[],t;while(t=E(this.entities.assignment)||E(this.expression)){e.push(t);if(!E(","))break}return e},literal:function(){return E(this.entities.ratio)||E(this.entities.dimension)||E(this.entities.color)||E(this.entities.quoted)||E(this.entities.unicodeDescriptor)},assignment:function(){var e,t;if((e=E(/^\w+(?=\s?=)/i))&&E("=")&&(t=E(this.entity)))return new i.Assignment(e,t)},url:function(){var e;if(s.charAt(o)!=="u"||!E(/^url\(/))return;return e=E(this.entities.quoted)||E(this.entities.variable)||E(/^(?:(?:\\[\(\)'"])|[^\(\)'"])+/)||"",x(")"),new i.URL(e.value!=null||e instanceof i.Variable?e:new i.Anonymous(e),t.rootpath)},variable:function(){var e,n=o;if(s.charAt(o)==="@"&&(e=E(/^@@?[\w-]+/)))return new i.Variable(e,n,t.filename)},variableCurly:function(){var e,n,r=o;if(s.charAt(o)==="@"&&(n=E(/^@\{([\w-]+)\}/)))return new i.Variable("@"+n[1],r,t.filename)},color:function(){var e;if(s.charAt(o)==="#"&&(e=E(/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})/)))return new i.Color(e[1])},dimension:function(){var e,t=s.charCodeAt(o);if(t>57||t<43||t===47||t==44)return;if(e=E(/^([+-]?\d*\.?\d+)(px|%|em|pc|ex|in|deg|s|ms|pt|cm|mm|rad|grad|turn|dpi|dpcm|dppx|rem|vw|vh|vmin|vm|ch)?/))return new i.Dimension(e[1],e[2])},ratio:function(){var e,t=s.charCodeAt(o);if(t>57||t<48)return;if(e=E(/^(\d+\/\d+)/))return new i.Ratio(e[1])},unicodeDescriptor:function(){var e;if(e=E(/^U\+[0-9a-fA-F?]+(\-[0-9a-fA-F?]+)?/))return new i.UnicodeDescriptor(e[0])},javascript:function(){var e,t=o,n;s.charAt(t)==="~"&&(t++,n=!0);if(s.charAt(t)!=="`")return;n&&E("~");if(e=E(/^`([^`]*)`/))return new i.JavaScript(e[1],o,n)}},variable:function(){var e;if(s.charAt(o)==="@"&&(e=E(/^(@[\w-]+)\s*:/)))return e[1]},shorthand:function(){var e,t;if(!N(/^[@\w.%-]+\/[@\w.-]+/))return;g();if((e=E(this.entity))&&E("/")&&(t=E(this.entity)))return new i.Shorthand(e,t);y()},mixin:{call:function(){var e=[],n,r,u=[],a=[],f,l,c,h,p,d,v,m=o,b=s.charAt(o),w,S,C=!1;if(b!=="."&&b!=="#")return;g();while(n=E(/^[#.](?:[\w-]|\\(?:[A-Fa-f0-9]{1,6} ?|[^A-Fa-f0-9]))+/))e.push(new i.Element(r,n,o)),r=E(">");if(E("(")){p=[];while(c=E(this.expression)){h=null,S=c;if(c.value.length==1){var k=c.value[0];k instanceof i.Variable&&E(":")&&(p.length>0&&(d&&T("Cannot mix ; and , as delimiter types"),v=!0),S=x(this.expression),h=w=k.name)}p.push(S),a.push({name:h,value:S});if(E(","))continue;if(E(";")||d)v&&T("Cannot mix ; and , as delimiter types"),d=!0,p.length>1&&(S=new i.Value(p)),u.push({name:w,value:S}),w=null,p=[],v=!1}x(")")}f=d?u:a,E(this.important)&&(C=!0);if(e.length>0&&(E(";")||N("}")))return new i.mixin.Call(e,f,m,t.filename,C);y()},definition:function(){var e,t=[],n,r,u,a,f,c=!1;if(s.charAt(o)!=="."&&s.charAt(o)!=="#"||N(/^[^{]*\}/))return;g();if(n=E(/^([#.](?:[\w-]|\\(?:[A-Fa-f0-9]{1,6} ?|[^A-Fa-f0-9]))+)\s*\(/)){e=n[1];do{E(this.comment);if(s.charAt(o)==="."&&E(/^\.{3}/)){c=!0,t.push({variadic:!0});break}if(!(u=E(this.entities.variable)||E(this.entities.literal)||E(this.entities.keyword)))break;if(u instanceof i.Variable)if(E(":"))a=x(this.expression,"expected expression"),t.push({name:u.name,value:a});else{if(E(/^\.{3}/)){t.push({name:u.name,variadic:!0}),c=!0;break}t.push({name:u.name})}else t.push({value:u})}while(E(",")||E(";"));E(")")||(l=o,y()),E(this.comment),E(/^when/)&&(f=x(this.conditions,"expected condition")),r=E(this.block);if(r)return new i.mixin.Definition(e,t,r,f,c);y()}}},entity:function(){return E(this.entities.literal)||E(this.entities.variable)||E(this.entities.url)||E(this.entities.call)||E(this.entities.keyword)||E(this.entities.javascript)||E(this.comment)},end:function(){return E(";")||N("}")},alpha:function(){var e;if(!E(/^\(opacity=/i))return;if(e=E(/^\d+/)||E(this.entities.variable))return x(")"),new i.Alpha(e)},element:function(){var e,t,n,r;n=E(this.combinator),e=E(/^(?:\d+\.\d+|\d+)%/)||E(/^(?:[.#]?|:*)(?:[\w-]|[^\x00-\x9f]|\\(?:[A-Fa-f0-9]{1,6} ?|[^A-Fa-f0-9]))+/)||E("*")||E("&")||E(this.attribute)||E(/^\([^()@]+\)/)||E(/^[\.#](?=@)/)||E(this.entities.variableCurly),e||E("(")&&(r=E(this.entities.variableCurly)||E(this.entities.variable)||E(this.selector))&&E(")")&&(e=new i.Paren(r));if(e)return new i.Element(n,e,o)},combinator:function(){var e,t=s.charAt(o);if(t===">"||t==="+"||t==="~"||t==="|"){o++;while(s.charAt(o).match(/\s/))o++;return new i.Combinator(t)}return s.charAt(o-1).match(/\s/)?new i.Combinator(" "):new i.Combinator(null)},selector:function(){var e,t,n=[],r,u;if(E("("))return e=E(this.entity),E(")")?new i.Selector([new i.Element("",e,o)]):null;while(t=E(this.element)){r=s.charAt(o),n.push(t);if(r==="{"||r==="}"||r===";"||r===","||r===")")break}if(n.length>0)return new i.Selector(n)},attribute:function(){var e="",t,n,r;if(!E("["))return;if(t=E(/^(?:[_A-Za-z0-9-]|\\.)+/)||E(this.entities.quoted))(r=E(/^[|~*$^]?=/))&&(n=E(this.entities.quoted)||E(/^[\w-]+/))?e=[t,r,n.toCSS?n.toCSS():n].join(""):e=t;if(!E("]"))return;if(e)return"["+e+"]"},block:function(){var e;if(E("{")&&(e=E(this.primary))&&E("}"))return e},ruleset:function(){var e=[],n,r,u,a;g(),t.dumpLineNumbers&&(a=A(o,s,t));while(n=E(this.selector)){e.push(n),E(this.comment);if(!E(","))break;E(this.comment)}if(e.length>0&&(r=E(this.block))){var f=new i.Ruleset(e,r,t.strictImports);return t.dumpLineNumbers&&(f.debugInfo=a),f}l=o,y()},rule:function(){var e,t,n=s.charAt(o),r,a;g();if(n==="."||n==="#"||n==="&")return;if(e=E(this.variable)||E(this.property)){e.charAt(0)!="@"&&(a=/^([^@+\/'"*`(;{}-]*);/.exec(c[u]))?(o+=a[0].length-1,t=new i.Anonymous(a[1])):e==="font"?t=E(this.font):t=E(this.value),r=E(this.important);if(t&&E(this.end))return new i.Rule(e,t,r,f);l=o,y()}},"import":function(){var e,n,r=o;g();var s=E(/^@import(?:-(once))?\s+/);if(s&&(e=E(this.entities.quoted)||E(this.entities.url))){n=E(this.mediaFeatures);if(E(";"))return new i.Import(e,m,n,s[1]==="once",r,t.rootpath)}y()},mediaFeature:function(){var e,t,n=[];do if(e=E(this.entities.keyword))n.push(e);else if(E("(")){t=E(this.property),e=E(this.entity);if(!E(")"))return null;if(t&&e)n.push(new i.Paren(new i.Rule(t,e,null,o,!0)));else{if(!e)return null;n.push(new i.Paren(e))}}while(e);if(n.length>0)return new i.Expression(n)},mediaFeatures:function(){var e,t=[];do if(e=E(this.mediaFeature)){t.push(e);if(!E(","))break}else if(e=E(this.entities.variable)){t.push(e);if(!E(","))break}while(e);return t.length>0?t:null},media:function(){var e,n,r,u;t.dumpLineNumbers&&(u=A(o,s,t));if(E(/^@media/)){e=E(this.mediaFeatures);if(n=E(this.block))return r=new i.Media(n,e),t.dumpLineNumbers&&(r.debugInfo=u),r}},directive:function(){var e,n,r,u,a,f,l,c,h,p;if(s.charAt(o)!=="@")return;if(n=E(this["import"])||E(this.media))return n;g(),e=E(/^@[a-z-]+/);if(!e)return;l=e,e.charAt(1)=="-"&&e.indexOf("-",2)>0&&(l="@"+e.slice(e.indexOf("-",2)+1));switch(l){case"@font-face":c=!0;break;case"@viewport":case"@top-left":case"@top-left-corner":case"@top-center":case"@top-right":case"@top-right-corner":case"@bottom-left":case"@bottom-left-corner":case"@bottom-center":case"@bottom-right":case"@bottom-right-corner":case"@left-top":case"@left-middle":case"@left-bottom":case"@right-top":case"@right-middle":case"@right-bottom":c=!0;break;case"@page":case"@document":case"@supports":case"@keyframes":c=!0,h=!0;break;case"@namespace":p=!0}h&&(e+=" "+(E(/^[^{]+/)||"").trim());if(c){if(r=E(this.block))return new i.Directive(e,r)}else if((n=p?E(this.expression):E(this.entity))&&E(";")){var d=new i.Directive(e,n);return t.dumpLineNumbers&&(d.debugInfo=A(o,s,t)),d}y()},font:function(){var e=[],t=[],n,r,s,o;while(o=E(this.shorthand)||E(this.entity))t.push(o);e.push(new i.Expression(t));if(E(","))while(o=E(this.expression)){e.push(o);if(!E(","))break}return new i.Value(e)},value:function(){var e,t=[],n;while(e=E(this.expression)){t.push(e);if(!E(","))break}if(t.length>0)return new i.Value(t)},important:function(){if(s.charAt(o)==="!")return E(/^! *important/)},sub:function(){var e;if(E("(")&&(e=E(this.expression))&&E(")"))return e},multiplication:function(){var e,t,n,r;if(e=E(this.operand)){while(!N(/^\/[*\/]/)&&(n=E("/")||E("*"))&&(t=E(this.operand)))r=new i.Operation(n,[r||e,t]);return r||e}},addition:function(){var e,t,n,r;if(e=E(this.multiplication)){while((n=E(/^[-+]\s+/)||!w(s.charAt(o-1))&&(E("+")||E("-")))&&(t=E(this.multiplication)))r=new i.Operation(n,[r||e,t]);return r||e}},conditions:function(){var e,t,n=o,r;if(e=E(this.condition)){while(E(",")&&(t=E(this.condition)))r=new i.Condition("or",r||e,t,n);return r||e}},condition:function(){var e,t,n,r,s=o,u=!1;E(/^not/)&&(u=!0),x("(");if(e=E(this.addition)||E(this.entities.keyword)||E(this.entities.quoted))return(r=E(/^(?:>=|=<|[<=>])/))?(t=E(this.addition)||E(this.entities.keyword)||E(this.entities.quoted))?n=new i.Condition(r,e,t,s,u):T("expected expression"):n=new i.Condition("=",e,new i.Keyword("true"),s,u),x(")"),E(/^and/)?new i.Condition("and",n,E(this.condition)):n},operand:function(){var e,t=s.charAt(o+1);s.charAt(o)==="-"&&(t==="@"||t==="(")&&(e=E("-"));var n=E(this.sub)||E(this.entities.dimension)||E(this.entities.color)||E(this.entities.variable)||E(this.entities.call);return e?new i.Operation("*",[new i.Dimension(-1),n]):n},expression:function(){var e,t,n=[],r;while(e=E(this.addition)||E(this.entity))n.push(e);if(n.length>0)return new i.Expression(n)},property:function(){var e;if(e=E(/^(\*?-?[_a-z0-9-]+)\s*:/))return e[1]}}}};if(r.mode==="browser"||r.mode==="rhino")r.Parser.importer=function(e,t,n,r){!/^([a-z-]+:)?\//.test(e)&&t.length>0&&(e=t[0]+e),w({href:e,title:e,type:r.mime,contents:r.contents,files:r.files,rootpath:r.rootpath,entryPath:r.entryPath,relativeUrls:r.relativeUrls},function(e,i,s,o,u,a){e&&typeof r.errback=="function"?r.errback.call(null,a,t,n,r):n.call(null,e,i,a)},!0)};(function(e){function t(t){return e.functions.hsla(t.h,t.s,t.l,t.a)}function n(t,n){return t instanceof e.Dimension&&t.unit=="%"?parseFloat(t.value*n/100):r(t)}function r(t){if(t instanceof e.Dimension)return parseFloat(t.unit=="%"?t.value/100:t.value);if(typeof t=="number")return t;throw{error:"RuntimeError",message:"color functions take numbers as parameters"}}function i(e){return Math.min(1,Math.max(0,e))}e.functions={rgb:function(e,t,n){return this.rgba(e,t,n,1)},rgba:function(t,i,s,o){var u=[t,i,s].map(function(e){return n(e,256)});return o=r(o),new e.Color(u,o)},hsl:function(e,t,n){return this.hsla(e,t,n,1)},hsla:function(e,t,n,i){function u(e){return e=e<0?e+1:e>1?e-1:e,e*6<1?o+(s-o)*e*6:e*2<1?s:e*3<2?o+(s-o)*(2/3-e)*6:o}e=r(e)%360/360,t=r(t),n=r(n),i=r(i);var s=n<=.5?n*(t+1):n+t-n*t,o=n*2-s;return this.rgba(u(e+1/3)*255,u(e)*255,u(e-1/3)*255,i)},hsv:function(e,t,n){return this.hsva(e,t,n,1)},hsva:function(e,t,n,i){e=r(e)%360/360*360,t=r(t),n=r(n),i=r(i);var s,o;s=Math.floor(e/60%6),o=e/60-s;var u=[n,n*(1-t),n*(1-o*t),n*(1-(1-o)*t)],a=[[0,3,1],[2,0,1],[1,0,3],[1,2,0],[3,1,0],[0,1,2]];return this.rgba(u[a[s][0]]*255,u[a[s][1]]*255,u[a[s][2]]*255,i)},hue:function(t){return new e.Dimension(Math.round(t.toHSL().h))},saturation:function(t){return new e.Dimension(Math.round(t.toHSL().s*100),"%")},lightness:function(t){return new e.Dimension(Math.round(t.toHSL().l*100),"%")},red:function(t){return new e.Dimension(t.rgb[0])},green:function(t){return new e.Dimension(t.rgb[1])},blue:function(t){return new e.Dimension(t.rgb[2])},alpha:function(t){return new e.Dimension(t.toHSL().a)},luma:function(t){return new e.Dimension(Math.round((.2126*(t.rgb[0]/255)+.7152*(t.rgb[1]/255)+.0722*(t.rgb[2]/255))*t.alpha*100),"%")},saturate:function(e,n){var r=e.toHSL();return r.s+=n.value/100,r.s=i(r.s),t(r)},desaturate:function(e,n){var r=e.toHSL();return r.s-=n.value/100,r.s=i(r.s),t(r)},lighten:function(e,n){var r=e.toHSL();return r.l+=n.value/100,r.l=i(r.l),t(r)},darken:function(e,n){var r=e.toHSL();return r.l-=n.value/100,r.l=i(r.l),t(r)},fadein:function(e,n){var r=e.toHSL();return r.a+=n.value/100,r.a=i(r.a),t(r)},fadeout:function(e,n){var r=e.toHSL();return r.a-=n.value/100,r.a=i(r.a),t(r)},fade:function(e,n){var r=e.toHSL();return r.a=n.value/100,r.a=i(r.a),t(r)},spin:function(e,n){var r=e.toHSL(),i=(r.h+n.value)%360;return r.h=i<0?360+i:i,t(r)},mix:function(t,n,r){r||(r=new e.Dimension(50));var i=r.value/100,s=i*2-1,o=t.toHSL().a-n.toHSL().a,u=((s*o==-1?s:(s+o)/(1+s*o))+1)/2,a=1-u,f=[t.rgb[0]*u+n.rgb[0]*a,t.rgb[1]*u+n.rgb[1]*a,t.rgb[2]*u+n.rgb[2]*a],l=t.alpha*i+n.alpha*(1-i);return new e.Color(f,l)},greyscale:function(t){return this.desaturate(t,new e.Dimension(100))},contrast:function(e,t,n,r){return e.rgb?(typeof n=="undefined"&&(n=this.rgba(255,255,255,1)),typeof t=="undefined"&&(t=this.rgba(0,0,0,1)),typeof r=="undefined"?r=.43:r=r.value,(.2126*(e.rgb[0]/255)+.7152*(e.rgb[1]/255)+.0722*(e.rgb[2]/255))*e.alpha<r?n:t):null},e:function(t){return new e.Anonymous(t instanceof e.JavaScript?t.evaluated:t)},escape:function(t){return new e.Anonymous(encodeURI(t.value).replace(/=/g,"%3D").replace(/:/g,"%3A").replace(/#/g,"%23").replace(/;/g,"%3B").replace(/\(/g,"%28").replace(/\)/g,"%29"))},"%":function(t){var n=Array.prototype.slice.call(arguments,1),r=t.value;for(var i=0;i<n.length;i++)r=r.replace(/%[sda]/i,function(e){var t=e.match(/s/i)?n[i].value:n[i].toCSS();return e.match(/[A-Z]$/)?encodeURIComponent(t):t});return r=r.replace(/%%/g,"%"),new e.Quoted('"'+r+'"',r)},unit:function(t,n){return new e.Dimension(t.value,n?n.toCSS():"")},round:function(e,t){var n=typeof t=="undefined"?0:t.value;return this._math(function(e){return e.toFixed(n)},e)},ceil:function(e){return this._math(Math.ceil,e)},floor:function(e){return this._math(Math.floor,e)},_math:function(t,n){if(n instanceof e.Dimension)return new e.Dimension(t(parseFloat(n.value)),n.unit);if(typeof n=="number")return t(n);throw{type:"Argument",message:"argument must be a number"}},argb:function(t){return new e.Anonymous(t.toARGB())},percentage:function(t){return new e.Dimension(t.value*100,"%")},color:function(t){if(t instanceof e.Quoted)return new e.Color(t.value.slice(1));throw{type:"Argument",message:"argument must be a string"}},iscolor:function(t){return this._isa(t,e.Color)},isnumber:function(t){return this._isa(t,e.Dimension)},isstring:function(t){return this._isa(t,e.Quoted)},iskeyword:function(t){return this._isa(t,e.Keyword)},isurl:function(t){return this._isa(t,e.URL)},ispixel:function(t){return t instanceof e.Dimension&&t.unit==="px"?e.True:e.False},ispercentage:function(t){return t instanceof e.Dimension&&t.unit==="%"?e.True:e.False},isem:function(t){return t instanceof e.Dimension&&t.unit==="em"?e.True:e.False},_isa:function(t,n){return t instanceof n?e.True:e.False},multiply:function(e,t){var n=e.rgb[0]*t.rgb[0]/255,r=e.rgb[1]*t.rgb[1]/255,i=e.rgb[2]*t.rgb[2]/255;return this.rgb(n,r,i)},screen:function(e,t){var n=255-(255-e.rgb[0])*(255-t.rgb[0])/255,r=255-(255-e.rgb[1])*(255-t.rgb[1])/255,i=255-(255-e.rgb[2])*(255-t.rgb[2])/255;return this.rgb(n,r,i)},overlay:function(e,t){var n=e.rgb[0]<128?2*e.rgb[0]*t.rgb[0]/255:255-2*(255-e.rgb[0])*(255-t.rgb[0])/255,r=e.rgb[1]<128?2*e.rgb[1]*t.rgb[1]/255:255-2*(255-e.rgb[1])*(255-t.rgb[1])/255,i=e.rgb[2]<128?2*e.rgb[2]*t.rgb[2]/255:255-2*(255-e.rgb[2])*(255-t.rgb[2])/255;return this.rgb(n,r,i)},softlight:function(e,t){var n=t.rgb[0]*e.rgb[0]/255,r=n+e.rgb[0]*(255-(255-e.rgb[0])*(255-t.rgb[0])/255-n)/255;n=t.rgb[1]*e.rgb[1]/255;var i=n+e.rgb[1]*(255-(255-e.rgb[1])*(255-t.rgb[1])/255-n)/255;n=t.rgb[2]*e.rgb[2]/255;var s=n+e.rgb[2]*(255-(255-e.rgb[2])*(255-t.rgb[2])/255-n)/255;return this.rgb(r,i,s)},hardlight:function(e,t){var n=t.rgb[0]<128?2*t.rgb[0]*e.rgb[0]/255:255-2*(255-t.rgb[0])*(255-e.rgb[0])/255,r=t.rgb[1]<128?2*t.rgb[1]*e.rgb[1]/255:255-2*(255-t.rgb[1])*(255-e.rgb[1])/255,i=t.rgb[2]<128?2*t.rgb[2]*e.rgb[2]/255:255-2*(255-t.rgb[2])*(255-e.rgb[2])/255;return this.rgb(n,r,i)},difference:function(e,t){var n=Math.abs(e.rgb[0]-t.rgb[0]),r=Math.abs(e.rgb[1]-t.rgb[1]),i=Math.abs(e.rgb[2]-t.rgb[2]);return this.rgb(n,r,i)},exclusion:function(e,t){var n=e.rgb[0]+t.rgb[0]*(255-e.rgb[0]-e.rgb[0])/255,r=e.rgb[1]+t.rgb[1]*(255-e.rgb[1]-e.rgb[1])/255,i=e.rgb[2]+t.rgb[2]*(255-e.rgb[2]-e.rgb[2])/255;return this.rgb(n,r,i)},average:function(e,t){var n=(e.rgb[0]+t.rgb[0])/2,r=(e.rgb[1]+t.rgb[1])/2,i=(e.rgb[2]+t.rgb[2])/2;return this.rgb(n,r,i)},negation:function(e,t){var n=255-Math.abs(255-t.rgb[0]-e.rgb[0]),r=255-Math.abs(255-t.rgb[1]-e.rgb[1]),i=255-Math.abs(255-t.rgb[2]-e.rgb[2]);return this.rgb(n,r,i)},tint:function(e,t){return this.mix(this.rgb(255,255,255),e,t)},shade:function(e,t){return this.mix(this.rgb(0,0,0),e,t)}}})(n("./tree")),function(e){e.colors={aliceblue:"#f0f8ff",antiquewhite:"#faebd7",aqua:"#00ffff",aquamarine:"#7fffd4",azure:"#f0ffff",beige:"#f5f5dc",bisque:"#ffe4c4",black:"#000000",blanchedalmond:"#ffebcd",blue:"#0000ff",blueviolet:"#8a2be2",brown:"#a52a2a",burlywood:"#deb887",cadetblue:"#5f9ea0",chartreuse:"#7fff00",chocolate:"#d2691e",coral:"#ff7f50",cornflowerblue:"#6495ed",cornsilk:"#fff8dc",crimson:"#dc143c",cyan:"#00ffff",darkblue:"#00008b",darkcyan:"#008b8b",darkgoldenrod:"#b8860b",darkgray:"#a9a9a9",darkgrey:"#a9a9a9",darkgreen:"#006400",darkkhaki:"#bdb76b",darkmagenta:"#8b008b",darkolivegreen:"#556b2f",darkorange:"#ff8c00",darkorchid:"#9932cc",darkred:"#8b0000",darksalmon:"#e9967a",darkseagreen:"#8fbc8f",darkslateblue:"#483d8b",darkslategray:"#2f4f4f",darkslategrey:"#2f4f4f",darkturquoise:"#00ced1",darkviolet:"#9400d3",deeppink:"#ff1493",deepskyblue:"#00bfff",dimgray:"#696969",dimgrey:"#696969",dodgerblue:"#1e90ff",firebrick:"#b22222",floralwhite:"#fffaf0",forestgreen:"#228b22",fuchsia:"#ff00ff",gainsboro:"#dcdcdc",ghostwhite:"#f8f8ff",gold:"#ffd700",goldenrod:"#daa520",gray:"#808080",grey:"#808080",green:"#008000",greenyellow:"#adff2f",honeydew:"#f0fff0",hotpink:"#ff69b4",indianred:"#cd5c5c",indigo:"#4b0082",ivory:"#fffff0",khaki:"#f0e68c",lavender:"#e6e6fa",lavenderblush:"#fff0f5",lawngreen:"#7cfc00",lemonchiffon:"#fffacd",lightblue:"#add8e6",lightcoral:"#f08080",lightcyan:"#e0ffff",lightgoldenrodyellow:"#fafad2",lightgray:"#d3d3d3",lightgrey:"#d3d3d3",lightgreen:"#90ee90",lightpink:"#ffb6c1",lightsalmon:"#ffa07a",lightseagreen:"#20b2aa",lightskyblue:"#87cefa",lightslategray:"#778899",lightslategrey:"#778899",lightsteelblue:"#b0c4de",lightyellow:"#ffffe0",lime:"#00ff00",limegreen:"#32cd32",linen:"#faf0e6",magenta:"#ff00ff",maroon:"#800000",mediumaquamarine:"#66cdaa",mediumblue:"#0000cd",mediumorchid:"#ba55d3",mediumpurple:"#9370d8",mediumseagreen:"#3cb371",mediumslateblue:"#7b68ee",mediumspringgreen:"#00fa9a",mediumturquoise:"#48d1cc",mediumvioletred:"#c71585",midnightblue:"#191970",mintcream:"#f5fffa",mistyrose:"#ffe4e1",moccasin:"#ffe4b5",navajowhite:"#ffdead",navy:"#000080",oldlace:"#fdf5e6",olive:"#808000",olivedrab:"#6b8e23",orange:"#ffa500",orangered:"#ff4500",orchid:"#da70d6",palegoldenrod:"#eee8aa",palegreen:"#98fb98",paleturquoise:"#afeeee",palevioletred:"#d87093",papayawhip:"#ffefd5",peachpuff:"#ffdab9",peru:"#cd853f",pink:"#ffc0cb",plum:"#dda0dd",powderblue:"#b0e0e6",purple:"#800080",red:"#ff0000",rosybrown:"#bc8f8f",royalblue:"#4169e1",saddlebrown:"#8b4513",salmon:"#fa8072",sandybrown:"#f4a460",seagreen:"#2e8b57",seashell:"#fff5ee",sienna:"#a0522d",silver:"#c0c0c0",skyblue:"#87ceeb",slateblue:"#6a5acd",slategray:"#708090",slategrey:"#708090",snow:"#fffafa",springgreen:"#00ff7f",steelblue:"#4682b4",tan:"#d2b48c",teal:"#008080",thistle:"#d8bfd8",tomato:"#ff6347",turquoise:"#40e0d0",violet:"#ee82ee",wheat:"#f5deb3",white:"#ffffff",whitesmoke:"#f5f5f5",yellow:"#ffff00",yellowgreen
:"#9acd32"}}(n("./tree")),function(e){e.Alpha=function(e){this.value=e},e.Alpha.prototype={toCSS:function(){return"alpha(opacity="+(this.value.toCSS?this.value.toCSS():this.value)+")"},eval:function(e){return this.value.eval&&(this.value=this.value.eval(e)),this}}}(n("../tree")),function(e){e.Anonymous=function(e){this.value=e.value||e},e.Anonymous.prototype={toCSS:function(){return this.value},eval:function(){return this},compare:function(e){if(!e.toCSS)return-1;var t=this.toCSS(),n=e.toCSS();return t===n?0:t<n?-1:1}}}(n("../tree")),function(e){e.Assignment=function(e,t){this.key=e,this.value=t},e.Assignment.prototype={toCSS:function(){return this.key+"="+(this.value.toCSS?this.value.toCSS():this.value)},eval:function(t){return this.value.eval?new e.Assignment(this.key,this.value.eval(t)):this}}}(n("../tree")),function(e){e.Call=function(e,t,n,r){this.name=e,this.args=t,this.index=n,this.filename=r},e.Call.prototype={eval:function(t){var n=this.args.map(function(e){return e.eval(t)}),r;if(this.name in e.functions)try{r=e.functions[this.name].apply(e.functions,n);if(r!=null)return r}catch(i){throw{type:i.type||"Runtime",message:"error evaluating function `"+this.name+"`"+(i.message?": "+i.message:""),index:this.index,filename:this.filename}}return new e.Anonymous(this.name+"("+n.map(function(e){return e.toCSS(t)}).join(", ")+")")},toCSS:function(e){return this.eval(e).toCSS()}}}(n("../tree")),function(e){e.Color=function(e,t){Array.isArray(e)?this.rgb=e:e.length==6?this.rgb=e.match(/.{2}/g).map(function(e){return parseInt(e,16)}):this.rgb=e.split("").map(function(e){return parseInt(e+e,16)}),this.alpha=typeof t=="number"?t:1},e.Color.prototype={eval:function(){return this},toCSS:function(){return this.alpha<1?"rgba("+this.rgb.map(function(e){return Math.round(e)}).concat(this.alpha).join(", ")+")":"#"+this.rgb.map(function(e){return e=Math.round(e),e=(e>255?255:e<0?0:e).toString(16),e.length===1?"0"+e:e}).join("")},operate:function(t,n){var r=[];n instanceof e.Color||(n=n.toColor());for(var i=0;i<3;i++)r[i]=e.operate(t,this.rgb[i],n.rgb[i]);return new e.Color(r,this.alpha+n.alpha)},toHSL:function(){var e=this.rgb[0]/255,t=this.rgb[1]/255,n=this.rgb[2]/255,r=this.alpha,i=Math.max(e,t,n),s=Math.min(e,t,n),o,u,a=(i+s)/2,f=i-s;if(i===s)o=u=0;else{u=a>.5?f/(2-i-s):f/(i+s);switch(i){case e:o=(t-n)/f+(t<n?6:0);break;case t:o=(n-e)/f+2;break;case n:o=(e-t)/f+4}o/=6}return{h:o*360,s:u,l:a,a:r}},toARGB:function(){var e=[Math.round(this.alpha*255)].concat(this.rgb);return"#"+e.map(function(e){return e=Math.round(e),e=(e>255?255:e<0?0:e).toString(16),e.length===1?"0"+e:e}).join("")},compare:function(e){return e.rgb?e.rgb[0]===this.rgb[0]&&e.rgb[1]===this.rgb[1]&&e.rgb[2]===this.rgb[2]&&e.alpha===this.alpha?0:-1:-1}}}(n("../tree")),function(e){e.Comment=function(e,t){this.value=e,this.silent=!!t},e.Comment.prototype={toCSS:function(e){return e.compress?"":this.value},eval:function(){return this}}}(n("../tree")),function(e){e.Condition=function(e,t,n,r,i){this.op=e.trim(),this.lvalue=t,this.rvalue=n,this.index=r,this.negate=i},e.Condition.prototype.eval=function(e){var t=this.lvalue.eval(e),n=this.rvalue.eval(e),r=this.index,i,i=function(e){switch(e){case"and":return t&&n;case"or":return t||n;default:if(t.compare)i=t.compare(n);else{if(!n.compare)throw{type:"Type",message:"Unable to perform comparison",index:r};i=n.compare(t)}switch(i){case-1:return e==="<"||e==="=<";case 0:return e==="="||e===">="||e==="=<";case 1:return e===">"||e===">="}}}(this.op);return this.negate?!i:i}}(n("../tree")),function(e){e.Dimension=function(e,t){this.value=parseFloat(e),this.unit=t||null},e.Dimension.prototype={eval:function(){return this},toColor:function(){return new e.Color([this.value,this.value,this.value])},toCSS:function(){var e=this.value+this.unit;return e},operate:function(t,n){return new e.Dimension(e.operate(t,this.value,n.value),this.unit||n.unit)},compare:function(t){return t instanceof e.Dimension?t.value>this.value?-1:t.value<this.value?1:t.unit&&this.unit!==t.unit?-1:0:-1}}}(n("../tree")),function(e){e.Directive=function(t,n){this.name=t,Array.isArray(n)?(this.ruleset=new e.Ruleset([],n),this.ruleset.allowImports=!0):this.value=n},e.Directive.prototype={toCSS:function(e,t){return this.ruleset?(this.ruleset.root=!0,this.name+(t.compress?"{":" {\n  ")+this.ruleset.toCSS(e,t).trim().replace(/\n/g,"\n  ")+(t.compress?"}":"\n}\n")):this.name+" "+this.value.toCSS()+";\n"},eval:function(t){var n=this;return this.ruleset&&(t.frames.unshift(this),n=new e.Directive(this.name),n.ruleset=this.ruleset.eval(t),t.frames.shift()),n},variable:function(t){return e.Ruleset.prototype.variable.call(this.ruleset,t)},find:function(){return e.Ruleset.prototype.find.apply(this.ruleset,arguments)},rulesets:function(){return e.Ruleset.prototype.rulesets.apply(this.ruleset)}}}(n("../tree")),function(e){e.Element=function(t,n,r){this.combinator=t instanceof e.Combinator?t:new e.Combinator(t),typeof n=="string"?this.value=n.trim():n?this.value=n:this.value="",this.index=r},e.Element.prototype.eval=function(t){return new e.Element(this.combinator,this.value.eval?this.value.eval(t):this.value,this.index)},e.Element.prototype.toCSS=function(e){var t=this.value.toCSS?this.value.toCSS(e):this.value;return t==""&&this.combinator.value.charAt(0)=="&"?"":this.combinator.toCSS(e||{})+t},e.Combinator=function(e){e===" "?this.value=" ":this.value=e?e.trim():""},e.Combinator.prototype.toCSS=function(e){return{"":""," ":" ",":":" :","+":e.compress?"+":" + ","~":e.compress?"~":" ~ ",">":e.compress?">":" > ","|":e.compress?"|":" | "}[this.value]}}(n("../tree")),function(e){e.Expression=function(e){this.value=e},e.Expression.prototype={eval:function(t){return this.value.length>1?new e.Expression(this.value.map(function(e){return e.eval(t)})):this.value.length===1?this.value[0].eval(t):this},toCSS:function(e){return this.value.map(function(t){return t.toCSS?t.toCSS(e):""}).join(" ")}}}(n("../tree")),function(e){e.Import=function(t,n,r,i,s,o){var u=this;this.once=i,this.index=s,this._path=t,this.features=r&&new e.Value(r),this.rootpath=o,t instanceof e.Quoted?this.path=/(\.[a-z]*$)|([\?;].*)$/.test(t.value)?t.value:t.value+".less":this.path=t.value.value||t.value,this.css=/css([\?;].*)?$/.test(this.path),this.css||n.push(this.path,function(t,n,r){t&&(t.index=s),r&&u.once&&(u.skip=r),u.root=n||new e.Ruleset([],[])})},e.Import.prototype={toCSS:function(e){var t=this.features?" "+this.features.toCSS(e):"";return this.css?(typeof this._path.value=="string"&&!/^(?:[a-z-]+:|\/)/.test(this._path.value)&&(this._path.value=this.rootpath+this._path.value),"@import "+this._path.toCSS()+t+";\n"):""},eval:function(t){var n,r=this.features&&this.features.eval(t);return this.skip?[]:this.css?this:(n=new e.Ruleset([],this.root.rules.slice(0)),n.evalImports(t),this.features?new e.Media(n.rules,this.features.value):n.rules)}}}(n("../tree")),function(e){e.JavaScript=function(e,t,n){this.escaped=n,this.expression=e,this.index=t},e.JavaScript.prototype={eval:function(t){var n,r=this,i={},s=this.expression.replace(/@\{([\w-]+)\}/g,function(n,i){return e.jsify((new e.Variable("@"+i,r.index)).eval(t))});try{s=new Function("return ("+s+")")}catch(o){throw{message:"JavaScript evaluation error: `"+s+"`",index:this.index}}for(var u in t.frames[0].variables())i[u.slice(1)]={value:t.frames[0].variables()[u].value,toJS:function(){return this.value.eval(t).toCSS()}};try{n=s.call(i)}catch(o){throw{message:"JavaScript evaluation error: '"+o.name+": "+o.message+"'",index:this.index}}return typeof n=="string"?new e.Quoted('"'+n+'"',n,this.escaped,this.index):Array.isArray(n)?new e.Anonymous(n.join(", ")):new e.Anonymous(n)}}}(n("../tree")),function(e){e.Keyword=function(e){this.value=e},e.Keyword.prototype={eval:function(){return this},toCSS:function(){return this.value},compare:function(t){return t instanceof e.Keyword?t.value===this.value?0:1:-1}},e.True=new e.Keyword("true"),e.False=new e.Keyword("false")}(n("../tree")),function(e){e.Media=function(t,n){var r=this.emptySelectors();this.features=new e.Value(n),this.ruleset=new e.Ruleset(r,t),this.ruleset.allowImports=!0},e.Media.prototype={toCSS:function(e,t){var n=this.features.toCSS(t);return this.ruleset.root=e.length===0||e[0].multiMedia,"@media "+n+(t.compress?"{":" {\n  ")+this.ruleset.toCSS(e,t).trim().replace(/\n/g,"\n  ")+(t.compress?"}":"\n}\n")},eval:function(t){t.mediaBlocks||(t.mediaBlocks=[],t.mediaPath=[]);var n=new e.Media([],[]);return this.debugInfo&&(this.ruleset.debugInfo=this.debugInfo,n.debugInfo=this.debugInfo),n.features=this.features.eval(t),t.mediaPath.push(n),t.mediaBlocks.push(n),t.frames.unshift(this.ruleset),n.ruleset=this.ruleset.eval(t),t.frames.shift(),t.mediaPath.pop(),t.mediaPath.length===0?n.evalTop(t):n.evalNested(t)},variable:function(t){return e.Ruleset.prototype.variable.call(this.ruleset,t)},find:function(){return e.Ruleset.prototype.find.apply(this.ruleset,arguments)},rulesets:function(){return e.Ruleset.prototype.rulesets.apply(this.ruleset)},emptySelectors:function(){var t=new e.Element("","&",0);return[new e.Selector([t])]},evalTop:function(t){var n=this;if(t.mediaBlocks.length>1){var r=this.emptySelectors();n=new e.Ruleset(r,t.mediaBlocks),n.multiMedia=!0}return delete t.mediaBlocks,delete t.mediaPath,n},evalNested:function(t){var n,r,i=t.mediaPath.concat([this]);for(n=0;n<i.length;n++)r=i[n].features instanceof e.Value?i[n].features.value:i[n].features,i[n]=Array.isArray(r)?r:[r];return this.features=new e.Value(this.permute(i).map(function(t){t=t.map(function(t){return t.toCSS?t:new e.Anonymous(t)});for(n=t.length-1;n>0;n--)t.splice(n,0,new e.Anonymous("and"));return new e.Expression(t)})),new e.Ruleset([],[])},permute:function(e){if(e.length===0)return[];if(e.length===1)return e[0];var t=[],n=this.permute(e.slice(1));for(var r=0;r<n.length;r++)for(var i=0;i<e[0].length;i++)t.push([e[0][i]].concat(n[r]));return t},bubbleSelectors:function(t){this.ruleset=new e.Ruleset(t.slice(0),[this.ruleset])}}}(n("../tree")),function(e){e.mixin={},e.mixin.Call=function(t,n,r,i,s){this.selector=new e.Selector(t),this.arguments=n,this.index=r,this.filename=i,this.important=s},e.mixin.Call.prototype={eval:function(t){var n,r,i,s=[],o=!1,u,a,f,l,c;i=this.arguments&&this.arguments.map(function(e){return{name:e.name,value:e.value.eval(t)}});for(u=0;u<t.frames.length;u++)if((n=t.frames[u].find(this.selector)).length>0){c=!0;for(a=0;a<n.length;a++){r=n[a],l=!1;for(f=0;f<t.frames.length;f++)if(!(r instanceof e.mixin.Definition)&&r===(t.frames[f].originalRuleset||t.frames[f])){l=!0;break}if(l)continue;if(r.matchArgs(i,t)){if(!r.matchCondition||r.matchCondition(i,t))try{Array.prototype.push.apply(s,r.eval(t,i,this.important).rules)}catch(h){throw{message:h.message,index:this.index,filename:this.filename,stack:h.stack}}o=!0}}if(o)return s}throw c?{type:"Runtime",message:"No matching definition was found for `"+this.selector.toCSS().trim()+"("+(i?i.map(function(e){var t="";return e.name&&(t+=e.name+":"),e.value.toCSS?t+=e.value.toCSS():t+="???",t}).join(", "):"")+")`",index:this.index,filename:this.filename}:{type:"Name",message:this.selector.toCSS().trim()+" is undefined",index:this.index,filename:this.filename}}},e.mixin.Definition=function(t,n,r,i,s){this.name=t,this.selectors=[new e.Selector([new e.Element(null,t)])],this.params=n,this.condition=i,this.variadic=s,this.arity=n.length,this.rules=r,this._lookups={},this.required=n.reduce(function(e,t){return!t.name||t.name&&!t.value?e+1:e},0),this.parent=e.Ruleset.prototype,this.frames=[]},e.mixin.Definition.prototype={toCSS:function(){return""},variable:function(e){return this.parent.variable.call(this,e)},variables:function(){return this.parent.variables.call(this)},find:function(){return this.parent.find.apply(this,arguments)},rulesets:function(){return this.parent.rulesets.apply(this)},evalParams:function(t,n,r,i){var s=new e.Ruleset(null,[]),o,u,a=this.params.slice(0),f,l,c,h,p,d;if(r){r=r.slice(0);for(f=0;f<r.length;f++){u=r[f];if(h=u&&u.name){p=!1;for(l=0;l<a.length;l++)if(!i[l]&&h===a[l].name){i[l]=u.value.eval(t),s.rules.unshift(new e.Rule(h,u.value.eval(t))),p=!0;break}if(p){r.splice(f,1),f--;continue}throw{type:"Runtime",message:"Named argument for "+this.name+" "+r[f].name+" not found"}}}}d=0;for(f=0;f<a.length;f++){if(i[f])continue;u=r&&r[d];if(h=a[f].name)if(a[f].variadic&&r){o=[];for(l=d;l<r.length;l++)o.push(r[l].value.eval(t));s.rules.unshift(new e.Rule(h,(new e.Expression(o)).eval(t)))}else{c=u&&u.value;if(c)c=c.eval(t);else{if(!a[f].value)throw{type:"Runtime",message:"wrong number of arguments for "+this.name+" ("+r.length+" for "+this.arity+")"};c=a[f].value.eval(n)}s.rules.unshift(new e.Rule(h,c)),i[f]=c}if(a[f].variadic&&r)for(l=d;l<r.length;l++)i[l]=r[l].value.eval(t);d++}return s},eval:function(t,n,r){var i=[],s=this.frames.concat(t.frames),o=this.evalParams(t,{frames:s},n,i),u,a,f,l;return o.rules.unshift(new e.Rule("@arguments",(new e.Expression(i)).eval(t))),a=r?this.parent.makeImportant.apply(this).rules:this.rules.slice(0),l=(new e.Ruleset(null,a)).eval({frames:[this,o].concat(s)}),l.originalRuleset=this,l},matchCondition:function(e,t){return this.condition&&!this.condition.eval({frames:[this.evalParams(t,{frames:this.frames.concat(t.frames)},e,[])].concat(t.frames)})?!1:!0},matchArgs:function(e,t){var n=e&&e.length||0,r,i;if(!this.variadic){if(n<this.required)return!1;if(n>this.params.length)return!1;if(this.required>0&&n>this.params.length)return!1}r=Math.min(n,this.arity);for(var s=0;s<r;s++)if(!this.params[s].name&&!this.params[s].variadic&&e[s].value.eval(t).toCSS()!=this.params[s].value.eval(t).toCSS())return!1;return!0}}}(n("../tree")),function(e){e.Operation=function(e,t){this.op=e.trim(),this.operands=t},e.Operation.prototype.eval=function(t){var n=this.operands[0].eval(t),r=this.operands[1].eval(t),i;if(n instanceof e.Dimension&&r instanceof e.Color){if(this.op!=="*"&&this.op!=="+")throw{name:"OperationError",message:"Can't substract or divide a color from a number"};i=r,r=n,n=i}if(!n.operate)throw{name:"OperationError",message:"Operation on an invalid type"};return n.operate(this.op,r)},e.operate=function(e,t,n){switch(e){case"+":return t+n;case"-":return t-n;case"*":return t*n;case"/":return t/n}}}(n("../tree")),function(e){e.Paren=function(e){this.value=e},e.Paren.prototype={toCSS:function(e){return"("+this.value.toCSS(e)+")"},eval:function(t){return new e.Paren(this.value.eval(t))}}}(n("../tree")),function(e){e.Quoted=function(e,t,n,r){this.escaped=n,this.value=t||"",this.quote=e.charAt(0),this.index=r},e.Quoted.prototype={toCSS:function(){return this.escaped?this.value:this.quote+this.value+this.quote},eval:function(t){var n=this,r=this.value.replace(/`([^`]+)`/g,function(r,i){return(new e.JavaScript(i,n.index,!0)).eval(t).value}).replace(/@\{([\w-]+)\}/g,function(r,i){var s=(new e.Variable("@"+i,n.index)).eval(t);return s instanceof e.Quoted?s.value:s.toCSS()});return new e.Quoted(this.quote+r+this.quote,r,this.escaped,this.index)},compare:function(e){if(!e.toCSS)return-1;var t=this.toCSS(),n=e.toCSS();return t===n?0:t<n?-1:1}}}(n("../tree")),function(e){e.Ratio=function(e){this.value=e},e.Ratio.prototype={toCSS:function(e){return this.value},eval:function(){return this}}}(n("../tree")),function(e){e.Rule=function(t,n,r,i,s){this.name=t,this.value=n instanceof e.Value?n:new e.Value([n]),this.important=r?" "+r.trim():"",this.index=i,this.inline=s||!1,t.charAt(0)==="@"?this.variable=!0:this.variable=!1},e.Rule.prototype.toCSS=function(e){return this.variable?"":this.name+(e.compress?":":": ")+this.value.toCSS(e)+this.important+(this.inline?"":";")},e.Rule.prototype.eval=function(t){return new e.Rule(this.name,this.value.eval(t),this.important,this.index,this.inline)},e.Rule.prototype.makeImportant=function(){return new e.Rule(this.name,this.value,"!important",this.index,this.inline)},e.Shorthand=function(e,t){this.a=e,this.b=t},e.Shorthand.prototype={toCSS:function(e){return this.a.toCSS(e)+"/"+this.b.toCSS(e)},eval:function(){return this}}}(n("../tree")),function(e){e.Ruleset=function(e,t,n){this.selectors=e,this.rules=t,this._lookups={},this.strictImports=n},e.Ruleset.prototype={eval:function(t){var n=this.selectors&&this.selectors.map(function(e){return e.eval(t)}),r=new e.Ruleset(n,this.rules.slice(0),this.strictImports),i;r.originalRuleset=this,r.root=this.root,r.allowImports=this.allowImports,this.debugInfo&&(r.debugInfo=this.debugInfo),t.frames.unshift(r),(r.root||r.allowImports||!r.strictImports)&&r.evalImports(t);for(var s=0;s<r.rules.length;s++)r.rules[s]instanceof e.mixin.Definition&&(r.rules[s].frames=t.frames.slice(0));var o=t.mediaBlocks&&t.mediaBlocks.length||0;for(var s=0;s<r.rules.length;s++)r.rules[s]instanceof e.mixin.Call&&(i=r.rules[s].eval(t),r.rules.splice.apply(r.rules,[s,1].concat(i)),s+=i.length-1,r.resetCache());for(var s=0,u;s<r.rules.length;s++)u=r.rules[s],u instanceof e.mixin.Definition||(r.rules[s]=u.eval?u.eval(t):u);t.frames.shift();if(t.mediaBlocks)for(var s=o;s<t.mediaBlocks.length;s++)t.mediaBlocks[s].bubbleSelectors(n);return r},evalImports:function(t){var n,r;for(n=0;n<this.rules.length;n++)this.rules[n]instanceof e.Import&&(r=this.rules[n].eval(t),typeof r.length=="number"?(this.rules.splice.apply(this.rules,[n,1].concat(r)),n+=r.length-1):this.rules.splice(n,1,r),this.resetCache())},makeImportant:function(){return new e.Ruleset(this.selectors,this.rules.map(function(e){return e.makeImportant?e.makeImportant():e}),this.strictImports)},matchArgs:function(e){return!e||e.length===0},resetCache:function(){this._rulesets=null,this._variables=null,this._lookups={}},variables:function(){return this._variables?this._variables:this._variables=this.rules.reduce(function(t,n){return n instanceof e.Rule&&n.variable===!0&&(t[n.name]=n),t},{})},variable:function(e){return this.variables()[e]},rulesets:function(){return this._rulesets?this._rulesets:this._rulesets=this.rules.filter(function(t){return t instanceof e.Ruleset||t instanceof e.mixin.Definition})},find:function(t,n){n=n||this;var r=[],i,s,o=t.toCSS();return o in this._lookups?this._lookups[o]:(this.rulesets().forEach(function(i){if(i!==n)for(var o=0;o<i.selectors.length;o++)if(s=t.match(i.selectors[o])){t.elements.length>i.selectors[o].elements.length?Array.prototype.push.apply(r,i.find(new e.Selector(t.elements.slice(1)),n)):r.push(i);break}}),this._lookups[o]=r)},toCSS:function(t,n){var r=[],i=[],s=[],o=[],u=[],a,f,l;this.root||this.joinSelectors(u,t,this.selectors);for(var c=0;c<this.rules.length;c++){l=this.rules[c];if(l.rules||l instanceof e.Media)o.push(l.toCSS(u,n));else if(l instanceof e.Directive){var h=l.toCSS(u,n);if(l.name==="@charset"){if(n.charset){l.debugInfo&&(o.push(e.debugInfo(n,l)),o.push((new e.Comment("/* "+h.replace(/\n/g,"")+" */\n")).toCSS(n)));continue}n.charset=!0}o.push(h)}else l instanceof e.Comment?l.silent||(this.root?o.push(l.toCSS(n)):i.push(l.toCSS(n))):l.toCSS&&!l.variable?i.push(l.toCSS(n)):l.value&&!l.variable&&i.push(l.value.toString())}o=o.join("");if(this.root)r.push(i.join(n.compress?"":"\n"));else if(i.length>0){f=e.debugInfo(n,this),a=u.map(function(e){return e.map(function(e){return e.toCSS(n)}).join("").trim()}).join(n.compress?",":",\n");for(var c=i.length-1;c>=0;c--)s.indexOf(i[c])===-1&&s.unshift(i[c]);i=s,r.push(f+a+(n.compress?"{":" {\n  ")+i.join(n.compress?"":"\n  ")+(n.compress?"}":"\n}\n"))}return r.push(o),r.join("")+(n.compress?"\n":"")},joinSelectors:function(e,t,n){for(var r=0;r<n.length;r++)this.joinSelector(e,t,n[r])},joinSelector:function(t,n,r){var i,s,o,u,a,f,l,c,h,p,d,v,m,g,y;for(i=0;i<r.elements.length;i++)f=r.elements[i],f.value==="&"&&(u=!0);if(!u){if(n.length>0)for(i=0;i<n.length;i++)t.push(n[i].concat(r));else t.push([r]);return}g=[],a=[[]];for(i=0;i<r.elements.length;i++){f=r.elements[i];if(f.value!=="&")g.push(f);else{y=[],g.length>0&&this.mergeElementsOnToSelectors(g,a);for(s=0;s<a.length;s++){l=a[s];if(n.length==0)l.length>0&&(l[0].elements=l[0].elements.slice(0),l[0].elements.push(new e.Element(f.combinator,"",0))),y.push(l);else for(o=0;o<n.length;o++)c=n[o],h=[],p=[],v=!0,l.length>0?(h=l.slice(0),m=h.pop(),d=new e.Selector(m.elements.slice(0)),v=!1):d=new e.Selector([]),c.length>1&&(p=p.concat(c.slice(1))),c.length>0&&(v=!1,d.elements.push(new e.Element(f.combinator,c[0].elements[0].value,0)),d.elements=d.elements.concat(c[0].elements.slice(1))),v||h.push(d),h=h.concat(p),y.push(h)}a=y,g=[]}}g.length>0&&this.mergeElementsOnToSelectors(g,a);for(i=0;i<a.length;i++)t.push(a[i])},mergeElementsOnToSelectors:function(t,n){var r,i;if(n.length==0){n.push([new e.Selector(t)]);return}for(r=0;r<n.length;r++)i=n[r],i.length>0?i[i.length-1]=new e.Selector(i[i.length-1].elements.concat(t)):i.push(new e.Selector(t))}}}(n("../tree")),function(e){e.Selector=function(e){this.elements=e},e.Selector.prototype.match=function(e){var t=this.elements,n=t.length,r,i,s,o;r=e.elements.slice(e.elements.length&&e.elements[0].value==="&"?1:0),i=r.length,s=Math.min(n,i);if(i===0||n<i)return!1;for(o=0;o<s;o++)if(t[o].value!==r[o].value)return!1;return!0},e.Selector.prototype.eval=function(t){return new e.Selector(this.elements.map(function(e){return e.eval(t)}))},e.Selector.prototype.toCSS=function(e){return this._css?this._css:(this.elements[0].combinator.value===""?this._css=" ":this._css="",this._css+=this.elements.map(function(t){return typeof t=="string"?" "+t.trim():t.toCSS(e)}).join(""),this._css)}}(n("../tree")),function(e){e.UnicodeDescriptor=function(e){this.value=e},e.UnicodeDescriptor.prototype={toCSS:function(e){return this.value},eval:function(){return this}}}(n("../tree")),function(e){e.URL=function(e,t){this.value=e,this.rootpath=t},e.URL.prototype={toCSS:function(){return"url("+this.value.toCSS()+")"},eval:function(t){var n=this.value.eval(t),r;return typeof n.value=="string"&&!/^(?:[a-z-]+:|\/)/.test(n.value)&&(r=this.rootpath,n.quote||(r=r.replace(/[\(\)'"\s]/g,function(e){return"\\"+e})),n.value=r+n.value),new e.URL(n,this.rootpath)}}}(n("../tree")),function(e){e.Value=function(e){this.value=e,this.is="value"},e.Value.prototype={eval:function(t){return this.value.length===1?this.value[0].eval(t):new e.Value(this.value.map(function(e){return e.eval(t)}))},toCSS:function(e){return this.value.map(function(t){return t.toCSS(e)}).join(e.compress?",":", ")}}}(n("../tree")),function(e){e.Variable=function(e,t,n){this.name=e,this.index=t,this.file=n},e.Variable.prototype={eval:function(t){var n,r,i=this.name;i.indexOf("@@")==0&&(i="@"+(new e.Variable(i.slice(1))).eval(t).value);if(this.evaluating)throw{type:"Name",message:"Recursive variable definition for "+i,filename:this.file,index:this.index};this.evaluating=!0;if(n=e.find(t.frames,function(e){if(r=e.variable(i))return r.value.eval(t)}))return this.evaluating=!1,n;throw{type:"Name",message:"variable "+i+" is undefined",filename:this.file,index:this.index}}}}(n("../tree")),function(e){e.debugInfo=function(t,n){var r="";if(t.dumpLineNumbers&&!t.compress)switch(t.dumpLineNumbers){case"comments":r=e.debugInfo.asComment(n);break;case"mediaquery":r=e.debugInfo.asMediaQuery(n);break;case"all":r=e.debugInfo.asComment(n)+e.debugInfo.asMediaQuery(n)}return r},e.debugInfo.asComment=function(e){return"/* line "+e.debugInfo.lineNumber+", "+e.debugInfo.fileName+" */\n"},e.debugInfo.asMediaQuery=function(e){return"@media -sass-debug-info{filename{font-family:"+("file://"+e.debugInfo.fileName).replace(/[\/:.]/g,"\\$&")+"}line{font-family:\\00003"+e.debugInfo.lineNumber+"}}\n"},e.find=function(e,t){for(var n=0,r;n<e.length;n++)if(r=t.call(e,e[n]))return r;return null},e.jsify=function(e){return Array.isArray(e.value)&&e.value.length>1?"["+e.value.map(function(e){return e.toCSS(!1)}).join(", ")+"]":e.toCSS(!1)}}(n("./tree"));var o=/^(file|chrome(-extension)?|resource|qrc|app):/.test(location.protocol);r.env=r.env||(location.hostname=="127.0.0.1"||location.hostname=="0.0.0.0"||location.hostname=="localhost"||location.port.length>0||o?"development":"production"),r.async=r.async||!1,r.fileAsync=r.fileAsync||!1,r.poll=r.poll||(o?1e3:1500);if(r.functions)for(var u in r.functions)r.tree.functions[u]=r.functions[u];var a=/!dumpLineNumbers:(comments|mediaquery|all)/.exec(location.hash);a&&(r.dumpLineNumbers=a[1]),r.watch=function(){return r.watchMode||(r.env="development",f()),this.watchMode=!0},r.unwatch=function(){return clearInterval(r.watchTimer),this.watchMode=!1},/!watch/.test(location.hash)&&r.watch();var l=null;if(r.env!="development")try{l=typeof e.localStorage=="undefined"?null:e.localStorage}catch(c){}var h=document.getElementsByTagName("link"),p=/^text\/(x-)?less$/;r.sheets=[];for(var d=0;d<h.length;d++)(h[d].rel==="stylesheet/less"||h[d].rel.match(/stylesheet/)&&h[d].type.match(p))&&r.sheets.push(h[d]);var v="";r.modifyVars=function(e){var t=v;for(name in e)t+=(name.slice(0,1)==="@"?"":"@")+name+": "+(e[name].slice(-1)===";"?e[name]:e[name]+";");(new r.Parser).parse(t,function(e,t){S(t.toCSS(),r.sheets[r.sheets.length-1])})},r.refresh=function(e){var t,n;t=n=new Date,g(function(e,r,i,s,o){o.local?C("loading "+s.href+" from cache."):(C("parsed "+s.href+" successfully."),S(r.toCSS(),s,o.lastModified)),C("css for "+s.href+" generated in "+(new Date-n)+"ms"),o.remaining===0&&C("css generated in "+(new Date-t)+"ms"),n=new Date},e),m()},r.refreshStyles=m,r.refresh(r.env==="development"),typeof define=="function"&&define.amd&&define("less",[],function(){return r})})(window);;
/*!
* Bootstrap.js by @fat & @mdo
* Copyright 2012 Twitter, Inc.
* http://www.apache.org/licenses/LICENSE-2.0.txt
*/
!function(e){"use strict";e(function(){e.support.transition=function(){var e=function(){var e=document.createElement("bootstrap"),t={WebkitTransition:"webkitTransitionEnd",MozTransition:"transitionend",OTransition:"oTransitionEnd otransitionend",transition:"transitionend"},n;for(n in t)if(e.style[n]!==undefined)return t[n]}();return e&&{end:e}}()})}(window.jQuery),!function(e){"use strict";var t='[data-dismiss="alert"]',n=function(n){e(n).on("click",t,this.close)};n.prototype.close=function(t){function s(){i.trigger("closed").remove()}var n=e(this),r=n.attr("data-target"),i;r||(r=n.attr("href"),r=r&&r.replace(/.*(?=#[^\s]*$)/,"")),i=e(r),t&&t.preventDefault(),i.length||(i=n.hasClass("alert")?n:n.parent()),i.trigger(t=e.Event("close"));if(t.isDefaultPrevented())return;i.removeClass("in"),e.support.transition&&i.hasClass("fade")?i.on(e.support.transition.end,s):s()};var r=e.fn.alert;e.fn.alert=function(t){return this.each(function(){var r=e(this),i=r.data("alert");i||r.data("alert",i=new n(this)),typeof t=="string"&&i[t].call(r)})},e.fn.alert.Constructor=n,e.fn.alert.noConflict=function(){return e.fn.alert=r,this},e(document).on("click.alert.data-api",t,n.prototype.close)}(window.jQuery),!function(e){"use strict";var t=function(t,n){this.$element=e(t),this.options=e.extend({},e.fn.button.defaults,n)};t.prototype.setState=function(e){var t="disabled",n=this.$element,r=n.data(),i=n.is("input")?"val":"html";e+="Text",r.resetText||n.data("resetText",n[i]()),n[i](r[e]||this.options[e]),setTimeout(function(){e=="loadingText"?n.addClass(t).attr(t,t):n.removeClass(t).removeAttr(t)},0)},t.prototype.toggle=function(){var e=this.$element.closest('[data-toggle="buttons-radio"]');e&&e.find(".active").removeClass("active"),this.$element.toggleClass("active")};var n=e.fn.button;e.fn.button=function(n){return this.each(function(){var r=e(this),i=r.data("button"),s=typeof n=="object"&&n;i||r.data("button",i=new t(this,s)),n=="toggle"?i.toggle():n&&i.setState(n)})},e.fn.button.defaults={loadingText:"loading..."},e.fn.button.Constructor=t,e.fn.button.noConflict=function(){return e.fn.button=n,this},e(document).on("click.button.data-api","[data-toggle^=button]",function(t){var n=e(t.target);n.hasClass("btn")||(n=n.closest(".btn")),n.button("toggle")})}(window.jQuery),!function(e){"use strict";var t=function(t,n){this.$element=e(t),this.$indicators=this.$element.find(".carousel-indicators"),this.options=n,this.options.pause=="hover"&&this.$element.on("mouseenter",e.proxy(this.pause,this)).on("mouseleave",e.proxy(this.cycle,this))};t.prototype={cycle:function(t){return t||(this.paused=!1),this.interval&&clearInterval(this.interval),this.options.interval&&!this.paused&&(this.interval=setInterval(e.proxy(this.next,this),this.options.interval)),this},getActiveIndex:function(){return this.$active=this.$element.find(".item.active"),this.$items=this.$active.parent().children(),this.$items.index(this.$active)},to:function(t){var n=this.getActiveIndex(),r=this;if(t>this.$items.length-1||t<0)return;return this.sliding?this.$element.one("slid",function(){r.to(t)}):n==t?this.pause().cycle():this.slide(t>n?"next":"prev",e(this.$items[t]))},pause:function(t){return t||(this.paused=!0),this.$element.find(".next, .prev").length&&e.support.transition.end&&(this.$element.trigger(e.support.transition.end),this.cycle(!0)),clearInterval(this.interval),this.interval=null,this},next:function(){if(this.sliding)return;return this.slide("next")},prev:function(){if(this.sliding)return;return this.slide("prev")},slide:function(t,n){var r=this.$element.find(".item.active"),i=n||r[t](),s=this.interval,o=t=="next"?"left":"right",u=t=="next"?"first":"last",a=this,f;this.sliding=!0,s&&this.pause(),i=i.length?i:this.$element.find(".item")[u](),f=e.Event("slide",{relatedTarget:i[0],direction:o});if(i.hasClass("active"))return;this.$indicators.length&&(this.$indicators.find(".active").removeClass("active"),this.$element.one("slid",function(){var t=e(a.$indicators.children()[a.getActiveIndex()]);t&&t.addClass("active")}));if(e.support.transition&&this.$element.hasClass("slide")){this.$element.trigger(f);if(f.isDefaultPrevented())return;i.addClass(t),i[0].offsetWidth,r.addClass(o),i.addClass(o),this.$element.one(e.support.transition.end,function(){i.removeClass([t,o].join(" ")).addClass("active"),r.removeClass(["active",o].join(" ")),a.sliding=!1,setTimeout(function(){a.$element.trigger("slid")},0)})}else{this.$element.trigger(f);if(f.isDefaultPrevented())return;r.removeClass("active"),i.addClass("active"),this.sliding=!1,this.$element.trigger("slid")}return s&&this.cycle(),this}};var n=e.fn.carousel;e.fn.carousel=function(n){return this.each(function(){var r=e(this),i=r.data("carousel"),s=e.extend({},e.fn.carousel.defaults,typeof n=="object"&&n),o=typeof n=="string"?n:s.slide;i||r.data("carousel",i=new t(this,s)),typeof n=="number"?i.to(n):o?i[o]():s.interval&&i.pause().cycle()})},e.fn.carousel.defaults={interval:5e3,pause:"hover"},e.fn.carousel.Constructor=t,e.fn.carousel.noConflict=function(){return e.fn.carousel=n,this},e(document).on("click.carousel.data-api","[data-slide], [data-slide-to]",function(t){var n=e(this),r,i=e(n.attr("data-target")||(r=n.attr("href"))&&r.replace(/.*(?=#[^\s]+$)/,"")),s=e.extend({},i.data(),n.data()),o;i.carousel(s),(o=n.attr("data-slide-to"))&&i.data("carousel").pause().to(o).cycle(),t.preventDefault()})}(window.jQuery),!function(e){"use strict";var t=function(t,n){this.$element=e(t),this.options=e.extend({},e.fn.collapse.defaults,n),this.options.parent&&(this.$parent=e(this.options.parent)),this.options.toggle&&this.toggle()};t.prototype={constructor:t,dimension:function(){var e=this.$element.hasClass("width");return e?"width":"height"},show:function(){var t,n,r,i;if(this.transitioning||this.$element.hasClass("in"))return;t=this.dimension(),n=e.camelCase(["scroll",t].join("-")),r=this.$parent&&this.$parent.find("> .accordion-group > .in");if(r&&r.length){i=r.data("collapse");if(i&&i.transitioning)return;r.collapse("hide"),i||r.data("collapse",null)}this.$element[t](0),this.transition("addClass",e.Event("show"),"shown"),e.support.transition&&this.$element[t](this.$element[0][n])},hide:function(){var t;if(this.transitioning||!this.$element.hasClass("in"))return;t=this.dimension(),this.reset(this.$element[t]()),this.transition("removeClass",e.Event("hide"),"hidden"),this.$element[t](0)},reset:function(e){var t=this.dimension();return this.$element.removeClass("collapse")[t](e||"auto")[0].offsetWidth,this.$element[e!==null?"addClass":"removeClass"]("collapse"),this},transition:function(t,n,r){var i=this,s=function(){n.type=="show"&&i.reset(),i.transitioning=0,i.$element.trigger(r)};this.$element.trigger(n);if(n.isDefaultPrevented())return;this.transitioning=1,this.$element[t]("in"),e.support.transition&&this.$element.hasClass("collapse")?this.$element.one(e.support.transition.end,s):s()},toggle:function(){this[this.$element.hasClass("in")?"hide":"show"]()}};var n=e.fn.collapse;e.fn.collapse=function(n){return this.each(function(){var r=e(this),i=r.data("collapse"),s=e.extend({},e.fn.collapse.defaults,r.data(),typeof n=="object"&&n);i||r.data("collapse",i=new t(this,s)),typeof n=="string"&&i[n]()})},e.fn.collapse.defaults={toggle:!0},e.fn.collapse.Constructor=t,e.fn.collapse.noConflict=function(){return e.fn.collapse=n,this},e(document).on("click.collapse.data-api","[data-toggle=collapse]",function(t){var n=e(this),r,i=n.attr("data-target")||t.preventDefault()||(r=n.attr("href"))&&r.replace(/.*(?=#[^\s]+$)/,""),s=e(i).data("collapse")?"toggle":n.data();n[e(i).hasClass("in")?"addClass":"removeClass"]("collapsed"),e(i).collapse(s)})}(window.jQuery),!function(e){"use strict";function r(){e(".dropdown-backdrop").remove(),e(t).each(function(){i(e(this)).removeClass("open")})}function i(t){var n=t.attr("data-target"),r;n||(n=t.attr("href"),n=n&&/#/.test(n)&&n.replace(/.*(?=#[^\s]*$)/,"")),r=n&&e(n);if(!r||!r.length)r=t.parent();return r}var t="[data-toggle=dropdown]",n=function(t){var n=e(t).on("click.dropdown.data-api",this.toggle);e("html").on("click.dropdown.data-api",function(){n.parent().removeClass("open")})};n.prototype={constructor:n,toggle:function(t){var n=e(this),s,o;if(n.is(".disabled, :disabled"))return;return s=i(n),o=s.hasClass("open"),r(),o||("ontouchstart"in document.documentElement&&e('<div class="dropdown-backdrop"/>').insertBefore(e(this)).on("click",r),s.toggleClass("open")),n.focus(),!1},keydown:function(n){var r,s,o,u,a,f;if(!/(38|40|27)/.test(n.keyCode))return;r=e(this),n.preventDefault(),n.stopPropagation();if(r.is(".disabled, :disabled"))return;u=i(r),a=u.hasClass("open");if(!a||a&&n.keyCode==27)return n.which==27&&u.find(t).focus(),r.click();s=e("[role=menu] li:not(.divider):visible a",u);if(!s.length)return;f=s.index(s.filter(":focus")),n.keyCode==38&&f>0&&f--,n.keyCode==40&&f<s.length-1&&f++,~f||(f=0),s.eq(f).focus()}};var s=e.fn.dropdown;e.fn.dropdown=function(t){return this.each(function(){var r=e(this),i=r.data("dropdown");i||r.data("dropdown",i=new n(this)),typeof t=="string"&&i[t].call(r)})},e.fn.dropdown.Constructor=n,e.fn.dropdown.noConflict=function(){return e.fn.dropdown=s,this},e(document).on("click.dropdown.data-api",r).on("click.dropdown.data-api",".dropdown form",function(e){e.stopPropagation()}).on("click.dropdown.data-api",t,n.prototype.toggle).on("keydown.dropdown.data-api",t+", [role=menu]",n.prototype.keydown)}(window.jQuery),!function(e){"use strict";var t=function(t,n){this.options=n,this.$element=e(t).delegate('[data-dismiss="modal"]',"click.dismiss.modal",e.proxy(this.hide,this)),this.options.remote&&this.$element.find(".modal-body").load(this.options.remote)};t.prototype={constructor:t,toggle:function(){return this[this.isShown?"hide":"show"]()},show:function(){var t=this,n=e.Event("show");this.$element.trigger(n);if(this.isShown||n.isDefaultPrevented())return;this.isShown=!0,this.escape(),this.backdrop(function(){var n=e.support.transition&&t.$element.hasClass("fade");t.$element.parent().length||t.$element.appendTo(document.body),t.$element.show(),n&&t.$element[0].offsetWidth,t.$element.addClass("in").attr("aria-hidden",!1),t.enforceFocus(),n?t.$element.one(e.support.transition.end,function(){t.$element.focus().trigger("shown")}):t.$element.focus().trigger("shown")})},hide:function(t){t&&t.preventDefault();var n=this;t=e.Event("hide"),this.$element.trigger(t);if(!this.isShown||t.isDefaultPrevented())return;this.isShown=!1,this.escape(),e(document).off("focusin.modal"),this.$element.removeClass("in").attr("aria-hidden",!0),e.support.transition&&this.$element.hasClass("fade")?this.hideWithTransition():this.hideModal()},enforceFocus:function(){var t=this;e(document).on("focusin.modal",function(e){t.$element[0]!==e.target&&!t.$element.has(e.target).length&&t.$element.focus()})},escape:function(){var e=this;this.isShown&&this.options.keyboard?this.$element.on("keyup.dismiss.modal",function(t){t.which==27&&e.hide()}):this.isShown||this.$element.off("keyup.dismiss.modal")},hideWithTransition:function(){var t=this,n=setTimeout(function(){t.$element.off(e.support.transition.end),t.hideModal()},500);this.$element.one(e.support.transition.end,function(){clearTimeout(n),t.hideModal()})},hideModal:function(){var e=this;this.$element.hide(),this.backdrop(function(){e.removeBackdrop(),e.$element.trigger("hidden")})},removeBackdrop:function(){this.$backdrop&&this.$backdrop.remove(),this.$backdrop=null},backdrop:function(t){var n=this,r=this.$element.hasClass("fade")?"fade":"";if(this.isShown&&this.options.backdrop){var i=e.support.transition&&r;this.$backdrop=e('<div class="modal-backdrop '+r+'" />').appendTo(document.body),this.$backdrop.click(this.options.backdrop=="static"?e.proxy(this.$element[0].focus,this.$element[0]):e.proxy(this.hide,this)),i&&this.$backdrop[0].offsetWidth,this.$backdrop.addClass("in");if(!t)return;i?this.$backdrop.one(e.support.transition.end,t):t()}else!this.isShown&&this.$backdrop?(this.$backdrop.removeClass("in"),e.support.transition&&this.$element.hasClass("fade")?this.$backdrop.one(e.support.transition.end,t):t()):t&&t()}};var n=e.fn.modal;e.fn.modal=function(n){return this.each(function(){var r=e(this),i=r.data("modal"),s=e.extend({},e.fn.modal.defaults,r.data(),typeof n=="object"&&n);i||r.data("modal",i=new t(this,s)),typeof n=="string"?i[n]():s.show&&i.show()})},e.fn.modal.defaults={backdrop:!0,keyboard:!0,show:!0},e.fn.modal.Constructor=t,e.fn.modal.noConflict=function(){return e.fn.modal=n,this},e(document).on("click.modal.data-api",'[data-toggle="modal"]',function(t){var n=e(this),r=n.attr("href"),i=e(n.attr("data-target")||r&&r.replace(/.*(?=#[^\s]+$)/,"")),s=i.data("modal")?"toggle":e.extend({remote:!/#/.test(r)&&r},i.data(),n.data());t.preventDefault(),i.modal(s).one("hide",function(){n.focus()})})}(window.jQuery),!function(e){"use strict";var t=function(e,t){this.init("tooltip",e,t)};t.prototype={constructor:t,init:function(t,n,r){var i,s,o,u,a;this.type=t,this.$element=e(n),this.options=this.getOptions(r),this.enabled=!0,o=this.options.trigger.split(" ");for(a=o.length;a--;)u=o[a],u=="click"?this.$element.on("click."+this.type,this.options.selector,e.proxy(this.toggle,this)):u!="manual"&&(i=u=="hover"?"mouseenter":"focus",s=u=="hover"?"mouseleave":"blur",this.$element.on(i+"."+this.type,this.options.selector,e.proxy(this.enter,this)),this.$element.on(s+"."+this.type,this.options.selector,e.proxy(this.leave,this)));this.options.selector?this._options=e.extend({},this.options,{trigger:"manual",selector:""}):this.fixTitle()},getOptions:function(t){return t=e.extend({},e.fn[this.type].defaults,this.$element.data(),t),t.delay&&typeof t.delay=="number"&&(t.delay={show:t.delay,hide:t.delay}),t},enter:function(t){var n=e.fn[this.type].defaults,r={},i;this._options&&e.each(this._options,function(e,t){n[e]!=t&&(r[e]=t)},this),i=e(t.currentTarget)[this.type](r).data(this.type);if(!i.options.delay||!i.options.delay.show)return i.show();clearTimeout(this.timeout),i.hoverState="in",this.timeout=setTimeout(function(){i.hoverState=="in"&&i.show()},i.options.delay.show)},leave:function(t){var n=e(t.currentTarget)[this.type](this._options).data(this.type);this.timeout&&clearTimeout(this.timeout);if(!n.options.delay||!n.options.delay.hide)return n.hide();n.hoverState="out",this.timeout=setTimeout(function(){n.hoverState=="out"&&n.hide()},n.options.delay.hide)},show:function(){var t,n,r,i,s,o,u=e.Event("show");if(this.hasContent()&&this.enabled){this.$element.trigger(u);if(u.isDefaultPrevented())return;t=this.tip(),this.setContent(),this.options.animation&&t.addClass("fade"),s=typeof this.options.placement=="function"?this.options.placement.call(this,t[0],this.$element[0]):this.options.placement,t.detach().css({top:0,left:0,display:"block"}),this.options.container?t.appendTo(this.options.container):t.insertAfter(this.$element),n=this.getPosition(),r=t[0].offsetWidth,i=t[0].offsetHeight;switch(s){case"bottom":o={top:n.top+n.height,left:n.left+n.width/2-r/2};break;case"top":o={top:n.top-i,left:n.left+n.width/2-r/2};break;case"left":o={top:n.top+n.height/2-i/2,left:n.left-r};break;case"right":o={top:n.top+n.height/2-i/2,left:n.left+n.width}}this.applyPlacement(o,s),this.$element.trigger("shown")}},applyPlacement:function(e,t){var n=this.tip(),r=n[0].offsetWidth,i=n[0].offsetHeight,s,o,u,a;n.offset(e).addClass(t).addClass("in"),s=n[0].offsetWidth,o=n[0].offsetHeight,t=="top"&&o!=i&&(e.top=e.top+i-o,a=!0),t=="bottom"||t=="top"?(u=0,e.left<0&&(u=e.left*-2,e.left=0,n.offset(e),s=n[0].offsetWidth,o=n[0].offsetHeight),this.replaceArrow(u-r+s,s,"left")):this.replaceArrow(o-i,o,"top"),a&&n.offset(e)},replaceArrow:function(e,t,n){this.arrow().css(n,e?50*(1-e/t)+"%":"")},setContent:function(){var e=this.tip(),t=this.getTitle();e.find(".tooltip-inner")[this.options.html?"html":"text"](t),e.removeClass("fade in top bottom left right")},hide:function(){function i(){var t=setTimeout(function(){n.off(e.support.transition.end).detach()},500);n.one(e.support.transition.end,function(){clearTimeout(t),n.detach()})}var t=this,n=this.tip(),r=e.Event("hide");this.$element.trigger(r);if(r.isDefaultPrevented())return;return n.removeClass("in"),e.support.transition&&this.$tip.hasClass("fade")?i():n.detach(),this.$element.trigger("hidden"),this},fixTitle:function(){var e=this.$element;(e.attr("title")||typeof e.attr("data-original-title")!="string")&&e.attr("data-original-title",e.attr("title")||"").attr("title","")},hasContent:function(){return this.getTitle()},getPosition:function(){var t=this.$element[0];return e.extend({},typeof t.getBoundingClientRect=="function"?t.getBoundingClientRect():{width:t.offsetWidth,height:t.offsetHeight},this.$element.offset())},getTitle:function(){var e,t=this.$element,n=this.options;return e=t.attr("data-original-title")||(typeof n.title=="function"?n.title.call(t[0]):n.title),e},tip:function(){return this.$tip=this.$tip||e(this.options.template)},arrow:function(){return this.$arrow=this.$arrow||this.tip().find(".tooltip-arrow")},validate:function(){this.$element[0].parentNode||(this.hide(),this.$element=null,this.options=null)},enable:function(){this.enabled=!0},disable:function(){this.enabled=!1},toggleEnabled:function(){this.enabled=!this.enabled},toggle:function(t){var n=t?e(t.currentTarget)[this.type](this._options).data(this.type):this;n.tip().hasClass("in")?n.hide():n.show()},destroy:function(){this.hide().$element.off("."+this.type).removeData(this.type)}};var n=e.fn.tooltip;e.fn.tooltip=function(n){return this.each(function(){var r=e(this),i=r.data("tooltip"),s=typeof n=="object"&&n;i||r.data("tooltip",i=new t(this,s)),typeof n=="string"&&i[n]()})},e.fn.tooltip.Constructor=t,e.fn.tooltip.defaults={animation:!0,placement:"top",selector:!1,template:'<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',trigger:"hover focus",title:"",delay:0,html:!1,container:!1},e.fn.tooltip.noConflict=function(){return e.fn.tooltip=n,this}}(window.jQuery),!function(e){"use strict";var t=function(e,t){this.init("popover",e,t)};t.prototype=e.extend({},e.fn.tooltip.Constructor.prototype,{constructor:t,setContent:function(){var e=this.tip(),t=this.getTitle(),n=this.getContent();e.find(".popover-title")[this.options.html?"html":"text"](t),e.find(".popover-content")[this.options.html?"html":"text"](n),e.removeClass("fade top bottom left right in")},hasContent:function(){return this.getTitle()||this.getContent()},getContent:function(){var e,t=this.$element,n=this.options;return e=(typeof n.content=="function"?n.content.call(t[0]):n.content)||t.attr("data-content"),e},tip:function(){return this.$tip||(this.$tip=e(this.options.template)),this.$tip},destroy:function(){this.hide().$element.off("."+this.type).removeData(this.type)}});var n=e.fn.popover;e.fn.popover=function(n){return this.each(function(){var r=e(this),i=r.data("popover"),s=typeof n=="object"&&n;i||r.data("popover",i=new t(this,s)),typeof n=="string"&&i[n]()})},e.fn.popover.Constructor=t,e.fn.popover.defaults=e.extend({},e.fn.tooltip.defaults,{placement:"right",trigger:"click",content:"",template:'<div class="popover"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'}),e.fn.popover.noConflict=function(){return e.fn.popover=n,this}}(window.jQuery),!function(e){"use strict";function t(t,n){var r=e.proxy(this.process,this),i=e(t).is("body")?e(window):e(t),s;this.options=e.extend({},e.fn.scrollspy.defaults,n),this.$scrollElement=i.on("scroll.scroll-spy.data-api",r),this.selector=(this.options.target||(s=e(t).attr("href"))&&s.replace(/.*(?=#[^\s]+$)/,"")||"")+" .nav li > a",this.$body=e("body"),this.refresh(),this.process()}t.prototype={constructor:t,refresh:function(){var t=this,n;this.offsets=e([]),this.targets=e([]),n=this.$body.find(this.selector).map(function(){var n=e(this),r=n.data("target")||n.attr("href"),i=/^#\w/.test(r)&&e(r);return i&&i.length&&[[i.position().top+(!e.isWindow(t.$scrollElement.get(0))&&t.$scrollElement.scrollTop()),r]]||null}).sort(function(e,t){return e[0]-t[0]}).each(function(){t.offsets.push(this[0]),t.targets.push(this[1])})},process:function(){var e=this.$scrollElement.scrollTop()+this.options.offset,t=this.$scrollElement[0].scrollHeight||this.$body[0].scrollHeight,n=t-this.$scrollElement.height(),r=this.offsets,i=this.targets,s=this.activeTarget,o;if(e>=n)return s!=(o=i.last()[0])&&this.activate(o);for(o=r.length;o--;)s!=i[o]&&e>=r[o]&&(!r[o+1]||e<=r[o+1])&&this.activate(i[o])},activate:function(t){var n,r;this.activeTarget=t,e(this.selector).parent(".active").removeClass("active"),r=this.selector+'[data-target="'+t+'"],'+this.selector+'[href="'+t+'"]',n=e(r).parent("li").addClass("active"),n.parent(".dropdown-menu").length&&(n=n.closest("li.dropdown").addClass("active")),n.trigger("activate")}};var n=e.fn.scrollspy;e.fn.scrollspy=function(n){return this.each(function(){var r=e(this),i=r.data("scrollspy"),s=typeof n=="object"&&n;i||r.data("scrollspy",i=new t(this,s)),typeof n=="string"&&i[n]()})},e.fn.scrollspy.Constructor=t,e.fn.scrollspy.defaults={offset:10},e.fn.scrollspy.noConflict=function(){return e.fn.scrollspy=n,this},e(window).on("load",function(){e('[data-spy="scroll"]').each(function(){var t=e(this);t.scrollspy(t.data())})})}(window.jQuery),!function(e){"use strict";var t=function(t){this.element=e(t)};t.prototype={constructor:t,show:function(){var t=this.element,n=t.closest("ul:not(.dropdown-menu)"),r=t.attr("data-target"),i,s,o;r||(r=t.attr("href"),r=r&&r.replace(/.*(?=#[^\s]*$)/,""));if(t.parent("li").hasClass("active"))return;i=n.find(".active:last a")[0],o=e.Event("show",{relatedTarget:i}),t.trigger(o);if(o.isDefaultPrevented())return;s=e(r),this.activate(t.parent("li"),n),this.activate(s,s.parent(),function(){t.trigger({type:"shown",relatedTarget:i})})},activate:function(t,n,r){function o(){i.removeClass("active").find("> .dropdown-menu > .active").removeClass("active"),t.addClass("active"),s?(t[0].offsetWidth,t.addClass("in")):t.removeClass("fade"),t.parent(".dropdown-menu")&&t.closest("li.dropdown").addClass("active"),r&&r()}var i=n.find("> .active"),s=r&&e.support.transition&&i.hasClass("fade");s?i.one(e.support.transition.end,o):o(),i.removeClass("in")}};var n=e.fn.tab;e.fn.tab=function(n){return this.each(function(){var r=e(this),i=r.data("tab");i||r.data("tab",i=new t(this)),typeof n=="string"&&i[n]()})},e.fn.tab.Constructor=t,e.fn.tab.noConflict=function(){return e.fn.tab=n,this},e(document).on("click.tab.data-api",'[data-toggle="tab"], [data-toggle="pill"]',function(t){t.preventDefault(),e(this).tab("show")})}(window.jQuery),!function(e){"use strict";var t=function(t,n){this.$element=e(t),this.options=e.extend({},e.fn.typeahead.defaults,n),this.matcher=this.options.matcher||this.matcher,this.sorter=this.options.sorter||this.sorter,this.highlighter=this.options.highlighter||this.highlighter,this.updater=this.options.updater||this.updater,this.source=this.options.source,this.$menu=e(this.options.menu),this.shown=!1,this.listen()};t.prototype={constructor:t,select:function(){var e=this.$menu.find(".active").attr("data-value");return this.$element.val(this.updater(e)).change(),this.hide()},updater:function(e){return e},show:function(){var t=e.extend({},this.$element.position(),{height:this.$element[0].offsetHeight});return this.$menu.insertAfter(this.$element).css({top:t.top+t.height,left:t.left}).show(),this.shown=!0,this},hide:function(){return this.$menu.hide(),this.shown=!1,this},lookup:function(t){var n;return this.query=this.$element.val(),!this.query||this.query.length<this.options.minLength?this.shown?this.hide():this:(n=e.isFunction(this.source)?this.source(this.query,e.proxy(this.process,this)):this.source,n?this.process(n):this)},process:function(t){var n=this;return t=e.grep(t,function(e){return n.matcher(e)}),t=this.sorter(t),t.length?this.render(t.slice(0,this.options.items)).show():this.shown?this.hide():this},matcher:function(e){return~e.toLowerCase().indexOf(this.query.toLowerCase())},sorter:function(e){var t=[],n=[],r=[],i;while(i=e.shift())i.toLowerCase().indexOf(this.query.toLowerCase())?~i.indexOf(this.query)?n.push(i):r.push(i):t.push(i);return t.concat(n,r)},highlighter:function(e){var t=this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g,"\\$&");return e.replace(new RegExp("("+t+")","ig"),function(e,t){return"<strong>"+t+"</strong>"})},render:function(t){var n=this;return t=e(t).map(function(t,r){return t=e(n.options.item).attr("data-value",r),t.find("a").html(n.highlighter(r)),t[0]}),t.first().addClass("active"),this.$menu.html(t),this},next:function(t){var n=this.$menu.find(".active").removeClass("active"),r=n.next();r.length||(r=e(this.$menu.find("li")[0])),r.addClass("active")},prev:function(e){var t=this.$menu.find(".active").removeClass("active"),n=t.prev();n.length||(n=this.$menu.find("li").last()),n.addClass("active")},listen:function(){this.$element.on("focus",e.proxy(this.focus,this)).on("blur",e.proxy(this.blur,this)).on("keypress",e.proxy(this.keypress,this)).on("keyup",e.proxy(this.keyup,this)),this.eventSupported("keydown")&&this.$element.on("keydown",e.proxy(this.keydown,this)),this.$menu.on("click",e.proxy(this.click,this)).on("mouseenter","li",e.proxy(this.mouseenter,this)).on("mouseleave","li",e.proxy(this.mouseleave,this))},eventSupported:function(e){var t=e in this.$element;return t||(this.$element.setAttribute(e,"return;"),t=typeof this.$element[e]=="function"),t},move:function(e){if(!this.shown)return;switch(e.keyCode){case 9:case 13:case 27:e.preventDefault();break;case 38:e.preventDefault(),this.prev();break;case 40:e.preventDefault(),this.next()}e.stopPropagation()},keydown:function(t){this.suppressKeyPressRepeat=~e.inArray(t.keyCode,[40,38,9,13,27]),this.move(t)},keypress:function(e){if(this.suppressKeyPressRepeat)return;this.move(e)},keyup:function(e){switch(e.keyCode){case 40:case 38:case 16:case 17:case 18:break;case 9:case 13:if(!this.shown)return;this.select();break;case 27:if(!this.shown)return;this.hide();break;default:this.lookup()}e.stopPropagation(),e.preventDefault()},focus:function(e){this.focused=!0},blur:function(e){this.focused=!1,!this.mousedover&&this.shown&&this.hide()},click:function(e){e.stopPropagation(),e.preventDefault(),this.select(),this.$element.focus()},mouseenter:function(t){this.mousedover=!0,this.$menu.find(".active").removeClass("active"),e(t.currentTarget).addClass("active")},mouseleave:function(e){this.mousedover=!1,!this.focused&&this.shown&&this.hide()}};var n=e.fn.typeahead;e.fn.typeahead=function(n){return this.each(function(){var r=e(this),i=r.data("typeahead"),s=typeof n=="object"&&n;i||r.data("typeahead",i=new t(this,s)),typeof n=="string"&&i[n]()})},e.fn.typeahead.defaults={source:[],items:8,menu:'<ul class="typeahead dropdown-menu"></ul>',item:'<li><a href="#"></a></li>',minLength:1},e.fn.typeahead.Constructor=t,e.fn.typeahead.noConflict=function(){return e.fn.typeahead=n,this},e(document).on("focus.typeahead.data-api",'[data-provide="typeahead"]',function(t){var n=e(this);if(n.data("typeahead"))return;n.typeahead(n.data())})}(window.jQuery),!function(e){"use strict";var t=function(t,n){this.options=e.extend({},e.fn.affix.defaults,n),this.$window=e(window).on("scroll.affix.data-api",e.proxy(this.checkPosition,this)).on("click.affix.data-api",e.proxy(function(){setTimeout(e.proxy(this.checkPosition,this),1)},this)),this.$element=e(t),this.checkPosition()};t.prototype.checkPosition=function(){if(!this.$element.is(":visible"))return;var t=e(document).height(),n=this.$window.scrollTop(),r=this.$element.offset(),i=this.options.offset,s=i.bottom,o=i.top,u="affix affix-top affix-bottom",a;typeof i!="object"&&(s=o=i),typeof o=="function"&&(o=i.top()),typeof s=="function"&&(s=i.bottom()),a=this.unpin!=null&&n+this.unpin<=r.top?!1:s!=null&&r.top+this.$element.height()>=t-s?"bottom":o!=null&&n<=o?"top":!1;if(this.affixed===a)return;this.affixed=a,this.unpin=a=="bottom"?r.top-n:null,this.$element.removeClass(u).addClass("affix"+(a?"-"+a:""))};var n=e.fn.affix;e.fn.affix=function(n){return this.each(function(){var r=e(this),i=r.data("affix"),s=typeof n=="object"&&n;i||r.data("affix",i=new t(this,s)),typeof n=="string"&&i[n]()})},e.fn.affix.Constructor=t,e.fn.affix.defaults={offset:0},e.fn.affix.noConflict=function(){return e.fn.affix=n,this},e(window).on("load",function(){e('[data-spy="affix"]').each(function(){var t=e(this),n=t.data();n.offset=n.offset||{},n.offsetBottom&&(n.offset.bottom=n.offsetBottom),n.offsetTop&&(n.offset.top=n.offsetTop),t.affix(n)})})}(window.jQuery);;
(function(){var n=this,t=n._,r={},e=Array.prototype,u=Object.prototype,i=Function.prototype,a=e.push,o=e.slice,c=e.concat,l=u.toString,f=u.hasOwnProperty,s=e.forEach,p=e.map,h=e.reduce,v=e.reduceRight,d=e.filter,g=e.every,m=e.some,y=e.indexOf,b=e.lastIndexOf,x=Array.isArray,_=Object.keys,j=i.bind,w=function(n){return n instanceof w?n:this instanceof w?(this._wrapped=n,void 0):new w(n)};"undefined"!=typeof exports?("undefined"!=typeof module&&module.exports&&(exports=module.exports=w),exports._=w):n._=w,w.VERSION="1.4.4";var A=w.each=w.forEach=function(n,t,e){if(null!=n)if(s&&n.forEach===s)n.forEach(t,e);else if(n.length===+n.length){for(var u=0,i=n.length;i>u;u++)if(t.call(e,n[u],u,n)===r)return}else for(var a in n)if(w.has(n,a)&&t.call(e,n[a],a,n)===r)return};w.map=w.collect=function(n,t,r){var e=[];return null==n?e:p&&n.map===p?n.map(t,r):(A(n,function(n,u,i){e[e.length]=t.call(r,n,u,i)}),e)};var O="Reduce of empty array with no initial value";w.reduce=w.foldl=w.inject=function(n,t,r,e){var u=arguments.length>2;if(null==n&&(n=[]),h&&n.reduce===h)return e&&(t=w.bind(t,e)),u?n.reduce(t,r):n.reduce(t);if(A(n,function(n,i,a){u?r=t.call(e,r,n,i,a):(r=n,u=!0)}),!u)throw new TypeError(O);return r},w.reduceRight=w.foldr=function(n,t,r,e){var u=arguments.length>2;if(null==n&&(n=[]),v&&n.reduceRight===v)return e&&(t=w.bind(t,e)),u?n.reduceRight(t,r):n.reduceRight(t);var i=n.length;if(i!==+i){var a=w.keys(n);i=a.length}if(A(n,function(o,c,l){c=a?a[--i]:--i,u?r=t.call(e,r,n[c],c,l):(r=n[c],u=!0)}),!u)throw new TypeError(O);return r},w.find=w.detect=function(n,t,r){var e;return E(n,function(n,u,i){return t.call(r,n,u,i)?(e=n,!0):void 0}),e},w.filter=w.select=function(n,t,r){var e=[];return null==n?e:d&&n.filter===d?n.filter(t,r):(A(n,function(n,u,i){t.call(r,n,u,i)&&(e[e.length]=n)}),e)},w.reject=function(n,t,r){return w.filter(n,function(n,e,u){return!t.call(r,n,e,u)},r)},w.every=w.all=function(n,t,e){t||(t=w.identity);var u=!0;return null==n?u:g&&n.every===g?n.every(t,e):(A(n,function(n,i,a){return(u=u&&t.call(e,n,i,a))?void 0:r}),!!u)};var E=w.some=w.any=function(n,t,e){t||(t=w.identity);var u=!1;return null==n?u:m&&n.some===m?n.some(t,e):(A(n,function(n,i,a){return u||(u=t.call(e,n,i,a))?r:void 0}),!!u)};w.contains=w.include=function(n,t){return null==n?!1:y&&n.indexOf===y?n.indexOf(t)!=-1:E(n,function(n){return n===t})},w.invoke=function(n,t){var r=o.call(arguments,2),e=w.isFunction(t);return w.map(n,function(n){return(e?t:n[t]).apply(n,r)})},w.pluck=function(n,t){return w.map(n,function(n){return n[t]})},w.where=function(n,t,r){return w.isEmpty(t)?r?null:[]:w[r?"find":"filter"](n,function(n){for(var r in t)if(t[r]!==n[r])return!1;return!0})},w.findWhere=function(n,t){return w.where(n,t,!0)},w.max=function(n,t,r){if(!t&&w.isArray(n)&&n[0]===+n[0]&&65535>n.length)return Math.max.apply(Math,n);if(!t&&w.isEmpty(n))return-1/0;var e={computed:-1/0,value:-1/0};return A(n,function(n,u,i){var a=t?t.call(r,n,u,i):n;a>=e.computed&&(e={value:n,computed:a})}),e.value},w.min=function(n,t,r){if(!t&&w.isArray(n)&&n[0]===+n[0]&&65535>n.length)return Math.min.apply(Math,n);if(!t&&w.isEmpty(n))return 1/0;var e={computed:1/0,value:1/0};return A(n,function(n,u,i){var a=t?t.call(r,n,u,i):n;e.computed>a&&(e={value:n,computed:a})}),e.value},w.shuffle=function(n){var t,r=0,e=[];return A(n,function(n){t=w.random(r++),e[r-1]=e[t],e[t]=n}),e};var k=function(n){return w.isFunction(n)?n:function(t){return t[n]}};w.sortBy=function(n,t,r){var e=k(t);return w.pluck(w.map(n,function(n,t,u){return{value:n,index:t,criteria:e.call(r,n,t,u)}}).sort(function(n,t){var r=n.criteria,e=t.criteria;if(r!==e){if(r>e||r===void 0)return 1;if(e>r||e===void 0)return-1}return n.index<t.index?-1:1}),"value")};var F=function(n,t,r,e){var u={},i=k(t||w.identity);return A(n,function(t,a){var o=i.call(r,t,a,n);e(u,o,t)}),u};w.groupBy=function(n,t,r){return F(n,t,r,function(n,t,r){(w.has(n,t)?n[t]:n[t]=[]).push(r)})},w.countBy=function(n,t,r){return F(n,t,r,function(n,t){w.has(n,t)||(n[t]=0),n[t]++})},w.sortedIndex=function(n,t,r,e){r=null==r?w.identity:k(r);for(var u=r.call(e,t),i=0,a=n.length;a>i;){var o=i+a>>>1;u>r.call(e,n[o])?i=o+1:a=o}return i},w.toArray=function(n){return n?w.isArray(n)?o.call(n):n.length===+n.length?w.map(n,w.identity):w.values(n):[]},w.size=function(n){return null==n?0:n.length===+n.length?n.length:w.keys(n).length},w.first=w.head=w.take=function(n,t,r){return null==n?void 0:null==t||r?n[0]:o.call(n,0,t)},w.initial=function(n,t,r){return o.call(n,0,n.length-(null==t||r?1:t))},w.last=function(n,t,r){return null==n?void 0:null==t||r?n[n.length-1]:o.call(n,Math.max(n.length-t,0))},w.rest=w.tail=w.drop=function(n,t,r){return o.call(n,null==t||r?1:t)},w.compact=function(n){return w.filter(n,w.identity)};var R=function(n,t,r){return A(n,function(n){w.isArray(n)?t?a.apply(r,n):R(n,t,r):r.push(n)}),r};w.flatten=function(n,t){return R(n,t,[])},w.without=function(n){return w.difference(n,o.call(arguments,1))},w.uniq=w.unique=function(n,t,r,e){w.isFunction(t)&&(e=r,r=t,t=!1);var u=r?w.map(n,r,e):n,i=[],a=[];return A(u,function(r,e){(t?e&&a[a.length-1]===r:w.contains(a,r))||(a.push(r),i.push(n[e]))}),i},w.union=function(){return w.uniq(c.apply(e,arguments))},w.intersection=function(n){var t=o.call(arguments,1);return w.filter(w.uniq(n),function(n){return w.every(t,function(t){return w.indexOf(t,n)>=0})})},w.difference=function(n){var t=c.apply(e,o.call(arguments,1));return w.filter(n,function(n){return!w.contains(t,n)})},w.zip=function(){for(var n=o.call(arguments),t=w.max(w.pluck(n,"length")),r=Array(t),e=0;t>e;e++)r[e]=w.pluck(n,""+e);return r},w.object=function(n,t){if(null==n)return{};for(var r={},e=0,u=n.length;u>e;e++)t?r[n[e]]=t[e]:r[n[e][0]]=n[e][1];return r},w.indexOf=function(n,t,r){if(null==n)return-1;var e=0,u=n.length;if(r){if("number"!=typeof r)return e=w.sortedIndex(n,t),n[e]===t?e:-1;e=0>r?Math.max(0,u+r):r}if(y&&n.indexOf===y)return n.indexOf(t,r);for(;u>e;e++)if(n[e]===t)return e;return-1},w.lastIndexOf=function(n,t,r){if(null==n)return-1;var e=null!=r;if(b&&n.lastIndexOf===b)return e?n.lastIndexOf(t,r):n.lastIndexOf(t);for(var u=e?r:n.length;u--;)if(n[u]===t)return u;return-1},w.range=function(n,t,r){1>=arguments.length&&(t=n||0,n=0),r=arguments[2]||1;for(var e=Math.max(Math.ceil((t-n)/r),0),u=0,i=Array(e);e>u;)i[u++]=n,n+=r;return i},w.bind=function(n,t){if(n.bind===j&&j)return j.apply(n,o.call(arguments,1));var r=o.call(arguments,2);return function(){return n.apply(t,r.concat(o.call(arguments)))}},w.partial=function(n){var t=o.call(arguments,1);return function(){return n.apply(this,t.concat(o.call(arguments)))}},w.bindAll=function(n){var t=o.call(arguments,1);return 0===t.length&&(t=w.functions(n)),A(t,function(t){n[t]=w.bind(n[t],n)}),n},w.memoize=function(n,t){var r={};return t||(t=w.identity),function(){var e=t.apply(this,arguments);return w.has(r,e)?r[e]:r[e]=n.apply(this,arguments)}},w.delay=function(n,t){var r=o.call(arguments,2);return setTimeout(function(){return n.apply(null,r)},t)},w.defer=function(n){return w.delay.apply(w,[n,1].concat(o.call(arguments,1)))},w.throttle=function(n,t){var r,e,u,i,a=0,o=function(){a=new Date,u=null,i=n.apply(r,e)};return function(){var c=new Date,l=t-(c-a);return r=this,e=arguments,0>=l?(clearTimeout(u),u=null,a=c,i=n.apply(r,e)):u||(u=setTimeout(o,l)),i}},w.debounce=function(n,t,r){var e,u;return function(){var i=this,a=arguments,o=function(){e=null,r||(u=n.apply(i,a))},c=r&&!e;return clearTimeout(e),e=setTimeout(o,t),c&&(u=n.apply(i,a)),u}},w.once=function(n){var t,r=!1;return function(){return r?t:(r=!0,t=n.apply(this,arguments),n=null,t)}},w.wrap=function(n,t){return function(){var r=[n];return a.apply(r,arguments),t.apply(this,r)}},w.compose=function(){var n=arguments;return function(){for(var t=arguments,r=n.length-1;r>=0;r--)t=[n[r].apply(this,t)];return t[0]}},w.after=function(n,t){return 0>=n?t():function(){return 1>--n?t.apply(this,arguments):void 0}},w.keys=_||function(n){if(n!==Object(n))throw new TypeError("Invalid object");var t=[];for(var r in n)w.has(n,r)&&(t[t.length]=r);return t},w.values=function(n){var t=[];for(var r in n)w.has(n,r)&&t.push(n[r]);return t},w.pairs=function(n){var t=[];for(var r in n)w.has(n,r)&&t.push([r,n[r]]);return t},w.invert=function(n){var t={};for(var r in n)w.has(n,r)&&(t[n[r]]=r);return t},w.functions=w.methods=function(n){var t=[];for(var r in n)w.isFunction(n[r])&&t.push(r);return t.sort()},w.extend=function(n){return A(o.call(arguments,1),function(t){if(t)for(var r in t)n[r]=t[r]}),n},w.pick=function(n){var t={},r=c.apply(e,o.call(arguments,1));return A(r,function(r){r in n&&(t[r]=n[r])}),t},w.omit=function(n){var t={},r=c.apply(e,o.call(arguments,1));for(var u in n)w.contains(r,u)||(t[u]=n[u]);return t},w.defaults=function(n){return A(o.call(arguments,1),function(t){if(t)for(var r in t)null==n[r]&&(n[r]=t[r])}),n},w.clone=function(n){return w.isObject(n)?w.isArray(n)?n.slice():w.extend({},n):n},w.tap=function(n,t){return t(n),n};var I=function(n,t,r,e){if(n===t)return 0!==n||1/n==1/t;if(null==n||null==t)return n===t;n instanceof w&&(n=n._wrapped),t instanceof w&&(t=t._wrapped);var u=l.call(n);if(u!=l.call(t))return!1;switch(u){case"[object String]":return n==t+"";case"[object Number]":return n!=+n?t!=+t:0==n?1/n==1/t:n==+t;case"[object Date]":case"[object Boolean]":return+n==+t;case"[object RegExp]":return n.source==t.source&&n.global==t.global&&n.multiline==t.multiline&&n.ignoreCase==t.ignoreCase}if("object"!=typeof n||"object"!=typeof t)return!1;for(var i=r.length;i--;)if(r[i]==n)return e[i]==t;r.push(n),e.push(t);var a=0,o=!0;if("[object Array]"==u){if(a=n.length,o=a==t.length)for(;a--&&(o=I(n[a],t[a],r,e)););}else{var c=n.constructor,f=t.constructor;if(c!==f&&!(w.isFunction(c)&&c instanceof c&&w.isFunction(f)&&f instanceof f))return!1;for(var s in n)if(w.has(n,s)&&(a++,!(o=w.has(t,s)&&I(n[s],t[s],r,e))))break;if(o){for(s in t)if(w.has(t,s)&&!a--)break;o=!a}}return r.pop(),e.pop(),o};w.isEqual=function(n,t){return I(n,t,[],[])},w.isEmpty=function(n){if(null==n)return!0;if(w.isArray(n)||w.isString(n))return 0===n.length;for(var t in n)if(w.has(n,t))return!1;return!0},w.isElement=function(n){return!(!n||1!==n.nodeType)},w.isArray=x||function(n){return"[object Array]"==l.call(n)},w.isObject=function(n){return n===Object(n)},A(["Arguments","Function","String","Number","Date","RegExp"],function(n){w["is"+n]=function(t){return l.call(t)=="[object "+n+"]"}}),w.isArguments(arguments)||(w.isArguments=function(n){return!(!n||!w.has(n,"callee"))}),"function"!=typeof/./&&(w.isFunction=function(n){return"function"==typeof n}),w.isFinite=function(n){return isFinite(n)&&!isNaN(parseFloat(n))},w.isNaN=function(n){return w.isNumber(n)&&n!=+n},w.isBoolean=function(n){return n===!0||n===!1||"[object Boolean]"==l.call(n)},w.isNull=function(n){return null===n},w.isUndefined=function(n){return n===void 0},w.has=function(n,t){return f.call(n,t)},w.noConflict=function(){return n._=t,this},w.identity=function(n){return n},w.times=function(n,t,r){for(var e=Array(n),u=0;n>u;u++)e[u]=t.call(r,u);return e},w.random=function(n,t){return null==t&&(t=n,n=0),n+Math.floor(Math.random()*(t-n+1))};var M={escape:{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;","/":"&#x2F;"}};M.unescape=w.invert(M.escape);var S={escape:RegExp("["+w.keys(M.escape).join("")+"]","g"),unescape:RegExp("("+w.keys(M.unescape).join("|")+")","g")};w.each(["escape","unescape"],function(n){w[n]=function(t){return null==t?"":(""+t).replace(S[n],function(t){return M[n][t]})}}),w.result=function(n,t){if(null==n)return null;var r=n[t];return w.isFunction(r)?r.call(n):r},w.mixin=function(n){A(w.functions(n),function(t){var r=w[t]=n[t];w.prototype[t]=function(){var n=[this._wrapped];return a.apply(n,arguments),D.call(this,r.apply(w,n))}})};var N=0;w.uniqueId=function(n){var t=++N+"";return n?n+t:t},w.templateSettings={evaluate:/<%([\s\S]+?)%>/g,interpolate:/<%=([\s\S]+?)%>/g,escape:/<%-([\s\S]+?)%>/g};var T=/(.)^/,q={"'":"'","\\":"\\","\r":"r","\n":"n","	":"t","\u2028":"u2028","\u2029":"u2029"},B=/\\|'|\r|\n|\t|\u2028|\u2029/g;w.template=function(n,t,r){var e;r=w.defaults({},r,w.templateSettings);var u=RegExp([(r.escape||T).source,(r.interpolate||T).source,(r.evaluate||T).source].join("|")+"|$","g"),i=0,a="__p+='";n.replace(u,function(t,r,e,u,o){return a+=n.slice(i,o).replace(B,function(n){return"\\"+q[n]}),r&&(a+="'+\n((__t=("+r+"))==null?'':_.escape(__t))+\n'"),e&&(a+="'+\n((__t=("+e+"))==null?'':__t)+\n'"),u&&(a+="';\n"+u+"\n__p+='"),i=o+t.length,t}),a+="';\n",r.variable||(a="with(obj||{}){\n"+a+"}\n"),a="var __t,__p='',__j=Array.prototype.join,"+"print=function(){__p+=__j.call(arguments,'');};\n"+a+"return __p;\n";try{e=Function(r.variable||"obj","_",a)}catch(o){throw o.source=a,o}if(t)return e(t,w);var c=function(n){return e.call(this,n,w)};return c.source="function("+(r.variable||"obj")+"){\n"+a+"}",c},w.chain=function(n){return w(n).chain()};var D=function(n){return this._chain?w(n).chain():n};w.mixin(w),A(["pop","push","reverse","shift","sort","splice","unshift"],function(n){var t=e[n];w.prototype[n]=function(){var r=this._wrapped;return t.apply(r,arguments),"shift"!=n&&"splice"!=n||0!==r.length||delete r[0],D.call(this,r)}}),A(["concat","join","slice"],function(n){var t=e[n];w.prototype[n]=function(){return D.call(this,t.apply(this._wrapped,arguments))}}),w.extend(w.prototype,{chain:function(){return this._chain=!0,this},value:function(){return this._wrapped}})}).call(this);;
(function(){var t=this;var e=t.Backbone;var i=[];var r=i.push;var s=i.slice;var n=i.splice;var a;if(typeof exports!=="undefined"){a=exports}else{a=t.Backbone={}}a.VERSION="1.0.0";var h=t._;if(!h&&typeof require!=="undefined")h=require("underscore");a.$=t.jQuery||t.Zepto||t.ender||t.$;a.noConflict=function(){t.Backbone=e;return this};a.emulateHTTP=false;a.emulateJSON=false;var o=a.Events={on:function(t,e,i){if(!l(this,"on",t,[e,i])||!e)return this;this._events||(this._events={});var r=this._events[t]||(this._events[t]=[]);r.push({callback:e,context:i,ctx:i||this});return this},once:function(t,e,i){if(!l(this,"once",t,[e,i])||!e)return this;var r=this;var s=h.once(function(){r.off(t,s);e.apply(this,arguments)});s._callback=e;return this.on(t,s,i)},off:function(t,e,i){var r,s,n,a,o,u,c,f;if(!this._events||!l(this,"off",t,[e,i]))return this;if(!t&&!e&&!i){this._events={};return this}a=t?[t]:h.keys(this._events);for(o=0,u=a.length;o<u;o++){t=a[o];if(n=this._events[t]){this._events[t]=r=[];if(e||i){for(c=0,f=n.length;c<f;c++){s=n[c];if(e&&e!==s.callback&&e!==s.callback._callback||i&&i!==s.context){r.push(s)}}}if(!r.length)delete this._events[t]}}return this},trigger:function(t){if(!this._events)return this;var e=s.call(arguments,1);if(!l(this,"trigger",t,e))return this;var i=this._events[t];var r=this._events.all;if(i)c(i,e);if(r)c(r,arguments);return this},stopListening:function(t,e,i){var r=this._listeners;if(!r)return this;var s=!e&&!i;if(typeof e==="object")i=this;if(t)(r={})[t._listenerId]=t;for(var n in r){r[n].off(e,i,this);if(s)delete this._listeners[n]}return this}};var u=/\s+/;var l=function(t,e,i,r){if(!i)return true;if(typeof i==="object"){for(var s in i){t[e].apply(t,[s,i[s]].concat(r))}return false}if(u.test(i)){var n=i.split(u);for(var a=0,h=n.length;a<h;a++){t[e].apply(t,[n[a]].concat(r))}return false}return true};var c=function(t,e){var i,r=-1,s=t.length,n=e[0],a=e[1],h=e[2];switch(e.length){case 0:while(++r<s)(i=t[r]).callback.call(i.ctx);return;case 1:while(++r<s)(i=t[r]).callback.call(i.ctx,n);return;case 2:while(++r<s)(i=t[r]).callback.call(i.ctx,n,a);return;case 3:while(++r<s)(i=t[r]).callback.call(i.ctx,n,a,h);return;default:while(++r<s)(i=t[r]).callback.apply(i.ctx,e)}};var f={listenTo:"on",listenToOnce:"once"};h.each(f,function(t,e){o[e]=function(e,i,r){var s=this._listeners||(this._listeners={});var n=e._listenerId||(e._listenerId=h.uniqueId("l"));s[n]=e;if(typeof i==="object")r=this;e[t](i,r,this);return this}});o.bind=o.on;o.unbind=o.off;h.extend(a,o);var d=a.Model=function(t,e){var i;var r=t||{};e||(e={});this.cid=h.uniqueId("c");this.attributes={};h.extend(this,h.pick(e,p));if(e.parse)r=this.parse(r,e)||{};if(i=h.result(this,"defaults")){r=h.defaults({},r,i)}this.set(r,e);this.changed={};this.initialize.apply(this,arguments)};var p=["url","urlRoot","collection"];h.extend(d.prototype,o,{changed:null,validationError:null,idAttribute:"id",initialize:function(){},toJSON:function(t){return h.clone(this.attributes)},sync:function(){return a.sync.apply(this,arguments)},get:function(t){return this.attributes[t]},escape:function(t){return h.escape(this.get(t))},has:function(t){return this.get(t)!=null},set:function(t,e,i){var r,s,n,a,o,u,l,c;if(t==null)return this;if(typeof t==="object"){s=t;i=e}else{(s={})[t]=e}i||(i={});if(!this._validate(s,i))return false;n=i.unset;o=i.silent;a=[];u=this._changing;this._changing=true;if(!u){this._previousAttributes=h.clone(this.attributes);this.changed={}}c=this.attributes,l=this._previousAttributes;if(this.idAttribute in s)this.id=s[this.idAttribute];for(r in s){e=s[r];if(!h.isEqual(c[r],e))a.push(r);if(!h.isEqual(l[r],e)){this.changed[r]=e}else{delete this.changed[r]}n?delete c[r]:c[r]=e}if(!o){if(a.length)this._pending=true;for(var f=0,d=a.length;f<d;f++){this.trigger("change:"+a[f],this,c[a[f]],i)}}if(u)return this;if(!o){while(this._pending){this._pending=false;this.trigger("change",this,i)}}this._pending=false;this._changing=false;return this},unset:function(t,e){return this.set(t,void 0,h.extend({},e,{unset:true}))},clear:function(t){var e={};for(var i in this.attributes)e[i]=void 0;return this.set(e,h.extend({},t,{unset:true}))},hasChanged:function(t){if(t==null)return!h.isEmpty(this.changed);return h.has(this.changed,t)},changedAttributes:function(t){if(!t)return this.hasChanged()?h.clone(this.changed):false;var e,i=false;var r=this._changing?this._previousAttributes:this.attributes;for(var s in t){if(h.isEqual(r[s],e=t[s]))continue;(i||(i={}))[s]=e}return i},previous:function(t){if(t==null||!this._previousAttributes)return null;return this._previousAttributes[t]},previousAttributes:function(){return h.clone(this._previousAttributes)},fetch:function(t){t=t?h.clone(t):{};if(t.parse===void 0)t.parse=true;var e=this;var i=t.success;t.success=function(r){if(!e.set(e.parse(r,t),t))return false;if(i)i(e,r,t);e.trigger("sync",e,r,t)};R(this,t);return this.sync("read",this,t)},save:function(t,e,i){var r,s,n,a=this.attributes;if(t==null||typeof t==="object"){r=t;i=e}else{(r={})[t]=e}if(r&&(!i||!i.wait)&&!this.set(r,i))return false;i=h.extend({validate:true},i);if(!this._validate(r,i))return false;if(r&&i.wait){this.attributes=h.extend({},a,r)}if(i.parse===void 0)i.parse=true;var o=this;var u=i.success;i.success=function(t){o.attributes=a;var e=o.parse(t,i);if(i.wait)e=h.extend(r||{},e);if(h.isObject(e)&&!o.set(e,i)){return false}if(u)u(o,t,i);o.trigger("sync",o,t,i)};R(this,i);s=this.isNew()?"create":i.patch?"patch":"update";if(s==="patch")i.attrs=r;n=this.sync(s,this,i);if(r&&i.wait)this.attributes=a;return n},destroy:function(t){t=t?h.clone(t):{};var e=this;var i=t.success;var r=function(){e.trigger("destroy",e,e.collection,t)};t.success=function(s){if(t.wait||e.isNew())r();if(i)i(e,s,t);if(!e.isNew())e.trigger("sync",e,s,t)};if(this.isNew()){t.success();return false}R(this,t);var s=this.sync("delete",this,t);if(!t.wait)r();return s},url:function(){var t=h.result(this,"urlRoot")||h.result(this.collection,"url")||U();if(this.isNew())return t;return t+(t.charAt(t.length-1)==="/"?"":"/")+encodeURIComponent(this.id)},parse:function(t,e){return t},clone:function(){return new this.constructor(this.attributes)},isNew:function(){return this.id==null},isValid:function(t){return this._validate({},h.extend(t||{},{validate:true}))},_validate:function(t,e){if(!e.validate||!this.validate)return true;t=h.extend({},this.attributes,t);var i=this.validationError=this.validate(t,e)||null;if(!i)return true;this.trigger("invalid",this,i,h.extend(e||{},{validationError:i}));return false}});var v=["keys","values","pairs","invert","pick","omit"];h.each(v,function(t){d.prototype[t]=function(){var e=s.call(arguments);e.unshift(this.attributes);return h[t].apply(h,e)}});var g=a.Collection=function(t,e){e||(e={});if(e.url)this.url=e.url;if(e.model)this.model=e.model;if(e.comparator!==void 0)this.comparator=e.comparator;this._reset();this.initialize.apply(this,arguments);if(t)this.reset(t,h.extend({silent:true},e))};var m={add:true,remove:true,merge:true};var y={add:true,merge:false,remove:false};h.extend(g.prototype,o,{model:d,initialize:function(){},toJSON:function(t){return this.map(function(e){return e.toJSON(t)})},sync:function(){return a.sync.apply(this,arguments)},add:function(t,e){return this.set(t,h.defaults(e||{},y))},remove:function(t,e){t=h.isArray(t)?t.slice():[t];e||(e={});var i,r,s,n;for(i=0,r=t.length;i<r;i++){n=this.get(t[i]);if(!n)continue;delete this._byId[n.id];delete this._byId[n.cid];s=this.indexOf(n);this.models.splice(s,1);this.length--;if(!e.silent){e.index=s;n.trigger("remove",n,this,e)}this._removeReference(n)}return this},set:function(t,e){e=h.defaults(e||{},m);if(e.parse)t=this.parse(t,e);if(!h.isArray(t))t=t?[t]:[];var i,s,a,o,u,l;var c=e.at;var f=this.comparator&&c==null&&e.sort!==false;var d=h.isString(this.comparator)?this.comparator:null;var p=[],v=[],g={};for(i=0,s=t.length;i<s;i++){if(!(a=this._prepareModel(t[i],e)))continue;if(u=this.get(a)){if(e.remove)g[u.cid]=true;if(e.merge){u.set(a.attributes,e);if(f&&!l&&u.hasChanged(d))l=true}}else if(e.add){p.push(a);a.on("all",this._onModelEvent,this);this._byId[a.cid]=a;if(a.id!=null)this._byId[a.id]=a}}if(e.remove){for(i=0,s=this.length;i<s;++i){if(!g[(a=this.models[i]).cid])v.push(a)}if(v.length)this.remove(v,e)}if(p.length){if(f)l=true;this.length+=p.length;if(c!=null){n.apply(this.models,[c,0].concat(p))}else{r.apply(this.models,p)}}if(l)this.sort({silent:true});if(e.silent)return this;for(i=0,s=p.length;i<s;i++){(a=p[i]).trigger("add",a,this,e)}if(l)this.trigger("sort",this,e);return this},reset:function(t,e){e||(e={});for(var i=0,r=this.models.length;i<r;i++){this._removeReference(this.models[i])}e.previousModels=this.models;this._reset();this.add(t,h.extend({silent:true},e));if(!e.silent)this.trigger("reset",this,e);return this},push:function(t,e){t=this._prepareModel(t,e);this.add(t,h.extend({at:this.length},e));return t},pop:function(t){var e=this.at(this.length-1);this.remove(e,t);return e},unshift:function(t,e){t=this._prepareModel(t,e);this.add(t,h.extend({at:0},e));return t},shift:function(t){var e=this.at(0);this.remove(e,t);return e},slice:function(t,e){return this.models.slice(t,e)},get:function(t){if(t==null)return void 0;return this._byId[t.id!=null?t.id:t.cid||t]},at:function(t){return this.models[t]},where:function(t,e){if(h.isEmpty(t))return e?void 0:[];return this[e?"find":"filter"](function(e){for(var i in t){if(t[i]!==e.get(i))return false}return true})},findWhere:function(t){return this.where(t,true)},sort:function(t){if(!this.comparator)throw new Error("Cannot sort a set without a comparator");t||(t={});if(h.isString(this.comparator)||this.comparator.length===1){this.models=this.sortBy(this.comparator,this)}else{this.models.sort(h.bind(this.comparator,this))}if(!t.silent)this.trigger("sort",this,t);return this},sortedIndex:function(t,e,i){e||(e=this.comparator);var r=h.isFunction(e)?e:function(t){return t.get(e)};return h.sortedIndex(this.models,t,r,i)},pluck:function(t){return h.invoke(this.models,"get",t)},fetch:function(t){t=t?h.clone(t):{};if(t.parse===void 0)t.parse=true;var e=t.success;var i=this;t.success=function(r){var s=t.reset?"reset":"set";i[s](r,t);if(e)e(i,r,t);i.trigger("sync",i,r,t)};R(this,t);return this.sync("read",this,t)},create:function(t,e){e=e?h.clone(e):{};if(!(t=this._prepareModel(t,e)))return false;if(!e.wait)this.add(t,e);var i=this;var r=e.success;e.success=function(s){if(e.wait)i.add(t,e);if(r)r(t,s,e)};t.save(null,e);return t},parse:function(t,e){return t},clone:function(){return new this.constructor(this.models)},_reset:function(){this.length=0;this.models=[];this._byId={}},_prepareModel:function(t,e){if(t instanceof d){if(!t.collection)t.collection=this;return t}e||(e={});e.collection=this;var i=new this.model(t,e);if(!i._validate(t,e)){this.trigger("invalid",this,t,e);return false}return i},_removeReference:function(t){if(this===t.collection)delete t.collection;t.off("all",this._onModelEvent,this)},_onModelEvent:function(t,e,i,r){if((t==="add"||t==="remove")&&i!==this)return;if(t==="destroy")this.remove(e,r);if(e&&t==="change:"+e.idAttribute){delete this._byId[e.previous(e.idAttribute)];if(e.id!=null)this._byId[e.id]=e}this.trigger.apply(this,arguments)}});var _=["forEach","each","map","collect","reduce","foldl","inject","reduceRight","foldr","find","detect","filter","select","reject","every","all","some","any","include","contains","invoke","max","min","toArray","size","first","head","take","initial","rest","tail","drop","last","without","indexOf","shuffle","lastIndexOf","isEmpty","chain"];h.each(_,function(t){g.prototype[t]=function(){var e=s.call(arguments);e.unshift(this.models);return h[t].apply(h,e)}});var w=["groupBy","countBy","sortBy"];h.each(w,function(t){g.prototype[t]=function(e,i){var r=h.isFunction(e)?e:function(t){return t.get(e)};return h[t](this.models,r,i)}});var b=a.View=function(t){this.cid=h.uniqueId("view");this._configure(t||{});this._ensureElement();this.initialize.apply(this,arguments);this.delegateEvents()};var x=/^(\S+)\s*(.*)$/;var E=["model","collection","el","id","attributes","className","tagName","events"];h.extend(b.prototype,o,{tagName:"div",$:function(t){return this.$el.find(t)},initialize:function(){},render:function(){return this},remove:function(){this.$el.remove();this.stopListening();return this},setElement:function(t,e){if(this.$el)this.undelegateEvents();this.$el=t instanceof a.$?t:a.$(t);this.el=this.$el[0];if(e!==false)this.delegateEvents();return this},delegateEvents:function(t){if(!(t||(t=h.result(this,"events"))))return this;this.undelegateEvents();for(var e in t){var i=t[e];if(!h.isFunction(i))i=this[t[e]];if(!i)continue;var r=e.match(x);var s=r[1],n=r[2];i=h.bind(i,this);s+=".delegateEvents"+this.cid;if(n===""){this.$el.on(s,i)}else{this.$el.on(s,n,i)}}return this},undelegateEvents:function(){this.$el.off(".delegateEvents"+this.cid);return this},_configure:function(t){if(this.options)t=h.extend({},h.result(this,"options"),t);h.extend(this,h.pick(t,E));this.options=t},_ensureElement:function(){if(!this.el){var t=h.extend({},h.result(this,"attributes"));if(this.id)t.id=h.result(this,"id");if(this.className)t["class"]=h.result(this,"className");var e=a.$("<"+h.result(this,"tagName")+">").attr(t);this.setElement(e,false)}else{this.setElement(h.result(this,"el"),false)}}});a.sync=function(t,e,i){var r=k[t];h.defaults(i||(i={}),{emulateHTTP:a.emulateHTTP,emulateJSON:a.emulateJSON});var s={type:r,dataType:"json"};if(!i.url){s.url=h.result(e,"url")||U()}if(i.data==null&&e&&(t==="create"||t==="update"||t==="patch")){s.contentType="application/json";s.data=JSON.stringify(i.attrs||e.toJSON(i))}if(i.emulateJSON){s.contentType="application/x-www-form-urlencoded";s.data=s.data?{model:s.data}:{}}if(i.emulateHTTP&&(r==="PUT"||r==="DELETE"||r==="PATCH")){s.type="POST";if(i.emulateJSON)s.data._method=r;var n=i.beforeSend;i.beforeSend=function(t){t.setRequestHeader("X-HTTP-Method-Override",r);if(n)return n.apply(this,arguments)}}if(s.type!=="GET"&&!i.emulateJSON){s.processData=false}if(s.type==="PATCH"&&window.ActiveXObject&&!(window.external&&window.external.msActiveXFilteringEnabled)){s.xhr=function(){return new ActiveXObject("Microsoft.XMLHTTP")}}var o=i.xhr=a.ajax(h.extend(s,i));e.trigger("request",e,o,i);return o};var k={create:"POST",update:"PUT",patch:"PATCH","delete":"DELETE",read:"GET"};a.ajax=function(){return a.$.ajax.apply(a.$,arguments)};var S=a.Router=function(t){t||(t={});if(t.routes)this.routes=t.routes;this._bindRoutes();this.initialize.apply(this,arguments)};var $=/\((.*?)\)/g;var T=/(\(\?)?:\w+/g;var H=/\*\w+/g;var A=/[\-{}\[\]+?.,\\\^$|#\s]/g;h.extend(S.prototype,o,{initialize:function(){},route:function(t,e,i){if(!h.isRegExp(t))t=this._routeToRegExp(t);if(h.isFunction(e)){i=e;e=""}if(!i)i=this[e];var r=this;a.history.route(t,function(s){var n=r._extractParameters(t,s);i&&i.apply(r,n);r.trigger.apply(r,["route:"+e].concat(n));r.trigger("route",e,n);a.history.trigger("route",r,e,n)});return this},navigate:function(t,e){a.history.navigate(t,e);return this},_bindRoutes:function(){if(!this.routes)return;this.routes=h.result(this,"routes");var t,e=h.keys(this.routes);while((t=e.pop())!=null){this.route(t,this.routes[t])}},_routeToRegExp:function(t){t=t.replace(A,"\\$&").replace($,"(?:$1)?").replace(T,function(t,e){return e?t:"([^/]+)"}).replace(H,"(.*?)");return new RegExp("^"+t+"$")},_extractParameters:function(t,e){var i=t.exec(e).slice(1);return h.map(i,function(t){return t?decodeURIComponent(t):null})}});var I=a.History=function(){this.handlers=[];h.bindAll(this,"checkUrl");if(typeof window!=="undefined"){this.location=window.location;this.history=window.history}};var N=/^[#\/]|\s+$/g;var P=/^\/+|\/+$/g;var O=/msie [\w.]+/;var C=/\/$/;I.started=false;h.extend(I.prototype,o,{interval:50,getHash:function(t){var e=(t||this).location.href.match(/#(.*)$/);return e?e[1]:""},getFragment:function(t,e){if(t==null){if(this._hasPushState||!this._wantsHashChange||e){t=this.location.pathname;var i=this.root.replace(C,"");if(!t.indexOf(i))t=t.substr(i.length)}else{t=this.getHash()}}return t.replace(N,"")},start:function(t){if(I.started)throw new Error("Backbone.history has already been started");I.started=true;this.options=h.extend({},{root:"/"},this.options,t);this.root=this.options.root;this._wantsHashChange=this.options.hashChange!==false;this._wantsPushState=!!this.options.pushState;this._hasPushState=!!(this.options.pushState&&this.history&&this.history.pushState);var e=this.getFragment();var i=document.documentMode;var r=O.exec(navigator.userAgent.toLowerCase())&&(!i||i<=7);this.root=("/"+this.root+"/").replace(P,"/");if(r&&this._wantsHashChange){this.iframe=a.$('<iframe src="javascript:0" tabindex="-1" />').hide().appendTo("body")[0].contentWindow;this.navigate(e)}if(this._hasPushState){a.$(window).on("popstate",this.checkUrl)}else if(this._wantsHashChange&&"onhashchange"in window&&!r){a.$(window).on("hashchange",this.checkUrl)}else if(this._wantsHashChange){this._checkUrlInterval=setInterval(this.checkUrl,this.interval)}this.fragment=e;var s=this.location;var n=s.pathname.replace(/[^\/]$/,"$&/")===this.root;if(this._wantsHashChange&&this._wantsPushState&&!this._hasPushState&&!n){this.fragment=this.getFragment(null,true);this.location.replace(this.root+this.location.search+"#"+this.fragment);return true}else if(this._wantsPushState&&this._hasPushState&&n&&s.hash){this.fragment=this.getHash().replace(N,"");this.history.replaceState({},document.title,this.root+this.fragment+s.search)}if(!this.options.silent)return this.loadUrl()},stop:function(){a.$(window).off("popstate",this.checkUrl).off("hashchange",this.checkUrl);clearInterval(this._checkUrlInterval);I.started=false},route:function(t,e){this.handlers.unshift({route:t,callback:e})},checkUrl:function(t){var e=this.getFragment();if(e===this.fragment&&this.iframe){e=this.getFragment(this.getHash(this.iframe))}if(e===this.fragment)return false;if(this.iframe)this.navigate(e);this.loadUrl()||this.loadUrl(this.getHash())},loadUrl:function(t){var e=this.fragment=this.getFragment(t);var i=h.any(this.handlers,function(t){if(t.route.test(e)){t.callback(e);return true}});return i},navigate:function(t,e){if(!I.started)return false;if(!e||e===true)e={trigger:e};t=this.getFragment(t||"");if(this.fragment===t)return;this.fragment=t;var i=this.root+t;if(this._hasPushState){this.history[e.replace?"replaceState":"pushState"]({},document.title,i)}else if(this._wantsHashChange){this._updateHash(this.location,t,e.replace);if(this.iframe&&t!==this.getFragment(this.getHash(this.iframe))){if(!e.replace)this.iframe.document.open().close();this._updateHash(this.iframe.location,t,e.replace)}}else{return this.location.assign(i)}if(e.trigger)this.loadUrl(t)},_updateHash:function(t,e,i){if(i){var r=t.href.replace(/(javascript:|#).*$/,"");t.replace(r+"#"+e)}else{t.hash="#"+e}}});a.history=new I;var j=function(t,e){var i=this;var r;if(t&&h.has(t,"constructor")){r=t.constructor}else{r=function(){return i.apply(this,arguments)}}h.extend(r,i,e);var s=function(){this.constructor=r};s.prototype=i.prototype;r.prototype=new s;if(t)h.extend(r.prototype,t);r.__super__=i.prototype;return r};d.extend=g.extend=S.extend=b.extend=I.extend=j;var U=function(){throw new Error('A "url" property or function must be specified')};var R=function(t,e){var i=e.error;e.error=function(r){if(i)i(t,r,e);t.trigger("error",t,r,e)}}}).call(this);
/*
//@ sourceMappingURL=backbone-min.map
*/;
/*
 * Copyright (c) 2010 Nick Galbreath
 * http://code.google.com/p/stringencoders/source/browse/#svn/trunk/javascript
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
*/

/* base64 encode/decode compatible with window.btoa/atob
 *
 * window.atob/btoa is a Firefox extension to convert binary data (the "b")
 * to base64 (ascii, the "a").
 *
 * It is also found in Safari and Chrome.  It is not available in IE.
 *
 * if (!window.btoa) window.btoa = base64.encode
 * if (!window.atob) window.atob = base64.decode
 *
 * The original spec's for atob/btoa are a bit lacking
 * https://developer.mozilla.org/en/DOM/window.atob
 * https://developer.mozilla.org/en/DOM/window.btoa
 *
 * window.btoa and base64.encode takes a string where charCodeAt is [0,255]
 * If any character is not [0,255], then an exception is thrown.
 *
 * window.atob and base64.decode take a base64-encoded string
 * If the input length is not a multiple of 4, or contains invalid characters
 *   then an exception is thrown.
 */
base64 = {};
base64.PADCHAR = '=';
base64.ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
base64.getbyte64 = function(s,i) {
    // This is oddly fast, except on Chrome/V8.
    //  Minimal or no improvement in performance by using a
    //   object with properties mapping chars to value (eg. 'A': 0)
    var idx = base64.ALPHA.indexOf(s.charAt(i));
    if (idx == -1) {
	throw "Cannot decode base64";
    }
    return idx;
}

base64.decode = function(s) {
    // convert to string
    s = "" + s;
    var getbyte64 = base64.getbyte64;
    var pads, i, b10;
    var imax = s.length
    if (imax == 0) {
        return s;
    }

    if (imax % 4 != 0) {
	throw "Cannot decode base64";
    }

    pads = 0
    if (s.charAt(imax -1) == base64.PADCHAR) {
        pads = 1;
        if (s.charAt(imax -2) == base64.PADCHAR) {
            pads = 2;
        }
        // either way, we want to ignore this last block
        imax -= 4;
    }

    var x = [];
    for (i = 0; i < imax; i += 4) {
        b10 = (getbyte64(s,i) << 18) | (getbyte64(s,i+1) << 12) |
            (getbyte64(s,i+2) << 6) | getbyte64(s,i+3);
        x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 0xff, b10 & 0xff));
    }

    switch (pads) {
    case 1:
        b10 = (getbyte64(s,i) << 18) | (getbyte64(s,i+1) << 12) | (getbyte64(s,i+2) << 6)
        x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 0xff));
        break;
    case 2:
        b10 = (getbyte64(s,i) << 18) | (getbyte64(s,i+1) << 12);
        x.push(String.fromCharCode(b10 >> 16));
        break;
    }
    return x.join('');
}

base64.getbyte = function(s,i) {
    var x = s.charCodeAt(i);
    if (x > 255) {
        throw "INVALID_CHARACTER_ERR: DOM Exception 5";
    }
    return x;
}


base64.encode = function(s) {
    if (arguments.length != 1) {
	throw "SyntaxError: Not enough arguments";
    }
    var padchar = base64.PADCHAR;
    var alpha   = base64.ALPHA;
    var getbyte = base64.getbyte;

    var i, b10;
    var x = [];

    // convert to string
    s = "" + s;

    var imax = s.length - s.length % 3;

    if (s.length == 0) {
        return s;
    }
    for (i = 0; i < imax; i += 3) {
        b10 = (getbyte(s,i) << 16) | (getbyte(s,i+1) << 8) | getbyte(s,i+2);
        x.push(alpha.charAt(b10 >> 18));
        x.push(alpha.charAt((b10 >> 12) & 0x3F));
        x.push(alpha.charAt((b10 >> 6) & 0x3f));
        x.push(alpha.charAt(b10 & 0x3f));
    }
    switch (s.length - imax) {
    case 1:
        b10 = getbyte(s,i) << 16;
        x.push(alpha.charAt(b10 >> 18) + alpha.charAt((b10 >> 12) & 0x3F) +
               padchar + padchar);
        break;
    case 2:
        b10 = (getbyte(s,i) << 16) | (getbyte(s,i+1) << 8);
        x.push(alpha.charAt(b10 >> 18) + alpha.charAt((b10 >> 12) & 0x3F) +
               alpha.charAt((b10 >> 6) & 0x3f) + padchar);
        break;
    }
    return x.join('');
}
;
/*!
 * jQuery Cookie Plugin v1.3.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function(a,b,c){function e(a){return a}function f(a){return g(decodeURIComponent(a.replace(d," ")))}function g(a){return 0===a.indexOf('"')&&(a=a.slice(1,-1).replace(/\\"/g,'"').replace(/\\\\/g,"\\")),a}function h(a){return i.json?JSON.parse(a):a}var d=/\+/g,i=a.cookie=function(d,g,j){if(g!==c){if(j=a.extend({},i.defaults,j),null===g&&(j.expires=-1),"number"==typeof j.expires){var k=j.expires,l=j.expires=new Date;l.setDate(l.getDate()+k)}return g=i.json?JSON.stringify(g):g+"",b.cookie=[encodeURIComponent(d),"=",i.raw?g:encodeURIComponent(g),j.expires?"; expires="+j.expires.toUTCString():"",j.path?"; path="+j.path:"",j.domain?"; domain="+j.domain:"",j.secure?"; secure":""].join("")}for(var m=i.raw?e:f,n=b.cookie.split("; "),o=d?null:{},p=0,q=n.length;q>p;p++){var r=n[p].split("="),s=m(r.shift()),t=m(r.join("="));if(d&&d===s){o=h(t);break}d||(o[s]=h(t))}return o};i.defaults={},a.removeCookie=function(b,c){return null!==a.cookie(b)?(a.cookie(b,null,c),!0):!1}})(jQuery,document);;
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */
/*  SHA-1 implementation in JavaScript | (c) Chris Veness 2002-2010 | www.movable-type.co.uk      */
/*   - see http://csrc.nist.gov/groups/ST/toolkit/secure_hashing.html                             */
/*         http://csrc.nist.gov/groups/ST/toolkit/examples.html                                   */
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

var Sha1 = {};  // Sha1 namespace

/**
 * Generates SHA-1 hash of string
 *
 * @param {String} msg                String to be hashed
 * @param {Boolean} [utf8encode=true] Encode msg as UTF-8 before generating hash
 * @returns {String}                  Hash of msg as hex character string
 */
Sha1.hash = function(msg, utf8encode) {
  utf8encode =  (typeof utf8encode == 'undefined') ? true : utf8encode;
  
  // convert string to UTF-8, as SHA only deals with byte-streams
  if (utf8encode) msg = Utf8.encode(msg);
  
  // constants [§4.2.1]
  var K = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6];
  
  // PREPROCESSING 
  
  msg += String.fromCharCode(0x80);  // add trailing '1' bit (+ 0's padding) to string [§5.1.1]
  
  // convert string msg into 512-bit/16-integer blocks arrays of ints [§5.2.1]
  var l = msg.length/4 + 2;  // length (in 32-bit integers) of msg + ‘1’ + appended length
  var N = Math.ceil(l/16);   // number of 16-integer-blocks required to hold 'l' ints
  var M = new Array(N);
  
  for (var i=0; i<N; i++) {
    M[i] = new Array(16);
    for (var j=0; j<16; j++) {  // encode 4 chars per integer, big-endian encoding
      M[i][j] = (msg.charCodeAt(i*64+j*4)<<24) | (msg.charCodeAt(i*64+j*4+1)<<16) | 
        (msg.charCodeAt(i*64+j*4+2)<<8) | (msg.charCodeAt(i*64+j*4+3));
    } // note running off the end of msg is ok 'cos bitwise ops on NaN return 0
  }
  // add length (in bits) into final pair of 32-bit integers (big-endian) [§5.1.1]
  // note: most significant word would be (len-1)*8 >>> 32, but since JS converts
  // bitwise-op args to 32 bits, we need to simulate this by arithmetic operators
  M[N-1][14] = ((msg.length-1)*8) / Math.pow(2, 32); M[N-1][14] = Math.floor(M[N-1][14])
  M[N-1][15] = ((msg.length-1)*8) & 0xffffffff;
  
  // set initial hash value [§5.3.1]
  var H0 = 0x67452301;
  var H1 = 0xefcdab89;
  var H2 = 0x98badcfe;
  var H3 = 0x10325476;
  var H4 = 0xc3d2e1f0;
  
  // HASH COMPUTATION [§6.1.2]
  
  var W = new Array(80); var a, b, c, d, e;
  for (var i=0; i<N; i++) {
  
    // 1 - prepare message schedule 'W'
    for (var t=0;  t<16; t++) W[t] = M[i][t];
    for (var t=16; t<80; t++) W[t] = Sha1.ROTL(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16], 1);
    
    // 2 - initialise five working variables a, b, c, d, e with previous hash value
    a = H0; b = H1; c = H2; d = H3; e = H4;
    
    // 3 - main loop
    for (var t=0; t<80; t++) {
      var s = Math.floor(t/20); // seq for blocks of 'f' functions and 'K' constants
      var T = (Sha1.ROTL(a,5) + Sha1.f(s,b,c,d) + e + K[s] + W[t]) & 0xffffffff;
      e = d;
      d = c;
      c = Sha1.ROTL(b, 30);
      b = a;
      a = T;
    }
    
    // 4 - compute the new intermediate hash value
    H0 = (H0+a) & 0xffffffff;  // note 'addition modulo 2^32'
    H1 = (H1+b) & 0xffffffff; 
    H2 = (H2+c) & 0xffffffff; 
    H3 = (H3+d) & 0xffffffff; 
    H4 = (H4+e) & 0xffffffff;
  }

  return Sha1.toHexStr(H0) + Sha1.toHexStr(H1) + 
    Sha1.toHexStr(H2) + Sha1.toHexStr(H3) + Sha1.toHexStr(H4);
}

//
// function 'f' [§4.1.1]
//
Sha1.f = function(s, x, y, z)  {
  switch (s) {
  case 0: return (x & y) ^ (~x & z);           // Ch()
  case 1: return x ^ y ^ z;                    // Parity()
  case 2: return (x & y) ^ (x & z) ^ (y & z);  // Maj()
  case 3: return x ^ y ^ z;                    // Parity()
  }
}

//
// rotate left (circular left shift) value x by n positions [§3.2.5]
//
Sha1.ROTL = function(x, n) {
  return (x<<n) | (x>>>(32-n));
}

//
// hexadecimal representation of a number 
//   (note toString(16) is implementation-dependant, and  
//   in IE returns signed numbers when used on full words)
//
Sha1.toHexStr = function(n) {
  var s="", v;
  for (var i=7; i>=0; i--) { v = (n>>>(i*4)) & 0xf; s += v.toString(16); }
  return s;
}

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */;
/*!
 * mustache.js - Logic-less {{mustache}} templates with JavaScript
 * http://github.com/janl/mustache.js
 */
var Mustache;(function(a){if(typeof module!=="undefined"&&module.exports){module.exports=a}else{if(typeof define==="function"){define(a)}else{Mustache=a}}}((function(){var u={};u.name="mustache.js";u.version="0.7.0";u.tags=["{{","}}"];u.Scanner=t;u.Context=r;u.Writer=p;var d=/\s*/;var l=/\s+/;var j=/\S/;var h=/\s*=/;var n=/\s*\}/;var s=/#|\^|\/|>|\{|&|=|!/;function o(x,w){return RegExp.prototype.test.call(x,w)}function g(w){return !o(j,w)}var k=Array.isArray||function(w){return Object.prototype.toString.call(w)==="[object Array]"};function f(w){return w.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g,"\\$&")}var c={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;","/":"&#x2F;"};function m(w){return String(w).replace(/[&<>"'\/]/g,function(x){return c[x]})}u.escape=m;function t(w){this.string=w;this.tail=w;this.pos=0}t.prototype.eos=function(){return this.tail===""};t.prototype.scan=function(x){var w=this.tail.match(x);if(w&&w.index===0){this.tail=this.tail.substring(w[0].length);this.pos+=w[0].length;return w[0]}return""};t.prototype.scanUntil=function(x){var w,y=this.tail.search(x);switch(y){case -1:w=this.tail;this.pos+=this.tail.length;this.tail="";break;case 0:w="";break;default:w=this.tail.substring(0,y);this.tail=this.tail.substring(y);this.pos+=y}return w};function r(w,x){this.view=w;this.parent=x;this.clearCache()}r.make=function(w){return(w instanceof r)?w:new r(w)};r.prototype.clearCache=function(){this._cache={}};r.prototype.push=function(w){return new r(w,this)};r.prototype.lookup=function(w){var z=this._cache[w];if(!z){if(w==="."){z=this.view}else{var y=this;while(y){if(w.indexOf(".")>0){var A=w.split("."),x=0;z=y.view;while(z&&x<A.length){z=z[A[x++]]}}else{z=y.view[w]}if(z!=null){break}y=y.parent}}this._cache[w]=z}if(typeof z==="function"){z=z.call(this.view)}return z};function p(){this.clearCache()}p.prototype.clearCache=function(){this._cache={};this._partialCache={}};p.prototype.compile=function(x,w){return this._compile(this._cache,x,x,w)};p.prototype.compilePartial=function(x,y,w){return this._compile(this._partialCache,x,y,w)};p.prototype.render=function(y,w,x){return this.compile(y)(w,x)};p.prototype._compile=function(x,z,B,y){if(!x[z]){var C=u.parse(B,y);var A=e(C);var w=this;x[z]=function(D,F){if(F){if(typeof F==="function"){w._loadPartial=F}else{for(var E in F){w.compilePartial(E,F[E])}}}return A(w,r.make(D),B)}}return x[z]};p.prototype._section=function(w,x,E,D){var C=x.lookup(w);switch(typeof C){case"object":if(k(C)){var y="";for(var z=0,B=C.length;z<B;++z){y+=D(this,x.push(C[z]))}return y}return C?D(this,x.push(C)):"";case"function":var F=this;var A=function(G){return F.render(G,x)};return C.call(x.view,E,A)||"";default:if(C){return D(this,x)}}return""};p.prototype._inverted=function(w,x,z){var y=x.lookup(w);if(!y||(k(y)&&y.length===0)){return z(this,x)}return""};p.prototype._partial=function(w,x){if(!(w in this._partialCache)&&this._loadPartial){this.compilePartial(w,this._loadPartial(w))}var y=this._partialCache[w];return y?y(x):""};p.prototype._name=function(w,x){var y=x.lookup(w);if(typeof y==="function"){y=y.call(x.view)}return(y==null)?"":String(y)};p.prototype._escaped=function(w,x){return u.escape(this._name(w,x))};function i(x){var z=x[3];var w=z;var y;while((y=x[4])&&y.length){x=y[y.length-1];w=x[3]}return[z,w]}function e(y){var w={};function x(A,D,C){if(!w[A]){var B=e(D);w[A]=function(F,E){return B(F,E,C)}}return w[A]}function z(G,E,F){var B="";var D,H;for(var C=0,A=y.length;C<A;++C){D=y[C];switch(D[0]){case"#":H=F.slice.apply(F,i(D));B+=G._section(D[1],E,H,x(C,D[4],F));break;case"^":B+=G._inverted(D[1],E,x(C,D[4],F));break;case">":B+=G._partial(D[1],E);break;case"&":B+=G._name(D[1],E);break;case"name":B+=G._escaped(D[1],E);break;case"text":B+=D[1];break}}return B}return z}function v(B){var w=[];var A=w;var C=[];var y,z;for(var x=0;x<B.length;++x){y=B[x];switch(y[0]){case"#":case"^":y[4]=[];C.push(y);A.push(y);A=y[4];break;case"/":if(C.length===0){throw new Error("Unopened section: "+y[1])}z=C.pop();if(z[1]!==y[1]){throw new Error("Unclosed section: "+z[1])}if(C.length>0){A=C[C.length-1][4]}else{A=w}break;default:A.push(y)}}z=C.pop();if(z){throw new Error("Unclosed section: "+z[1])}return w}function a(z){var y,w;for(var x=0;x<z.length;++x){y=z[x];if(w&&w[0]==="text"&&y[0]==="text"){w[1]+=y[1];w[3]=y[3];z.splice(x--,1)}else{w=y}}}function q(w){if(w.length!==2){throw new Error("Invalid tags: "+w.join(" "))}return[new RegExp(f(w[0])+"\\s*"),new RegExp("\\s*"+f(w[1]))]}u.parse=function(I,K){K=K||u.tags;var J=q(K);var z=new t(I);var G=[],E=[],C=false,L=false;function x(){if(C&&!L){while(E.length){G.splice(E.pop(),1)}}else{E=[]}C=false;L=false}var w,F,H,A;while(!z.eos()){w=z.pos;H=z.scanUntil(J[0]);if(H){for(var B=0,D=H.length;B<D;++B){A=H.charAt(B);if(g(A)){E.push(G.length)}else{L=true}G.push(["text",A,w,w+1]);w+=1;if(A==="\n"){x()}}}w=z.pos;if(!z.scan(J[0])){break}C=true;F=z.scan(s)||"name";z.scan(d);if(F==="="){H=z.scanUntil(h);z.scan(h);z.scanUntil(J[1])}else{if(F==="{"){var y=new RegExp("\\s*"+f("}"+K[1]));H=z.scanUntil(y);z.scan(n);z.scanUntil(J[1]);F="&"}else{H=z.scanUntil(J[1])}}if(!z.scan(J[1])){throw new Error("Unclosed tag at "+z.pos)}G.push([F,H,w,z.pos]);if(F==="name"||F==="{"||F==="&"){L=true}if(F==="="){K=H.split(l);J=q(K)}}a(G);return v(G)};var b=new p();u.clearCache=function(){return b.clearCache()};u.compile=function(x,w){return b.compile(x,w)};u.compilePartial=function(x,y,w){return b.compilePartial(x,y,w)};u.render=function(y,w,x){return b.render(y,w,x)};u.to_html=function(z,x,y,A){var w=u.render(z,x,y);if(typeof A==="function"){A(w)}else{return w}};return u}())));;
/*
Backbone.Table 0.1.0
(c) 2012 Jeremy Singer-Vine, The Wall Street Journal
Backbone.Table is freely distributable under the MIT license.
https://github.com/jsvine/Backbone.Table
*/
Backbone.Table = Backbone.View.extend({
  tagName: "table",
  initialize: function() {
    return this.$el = this.$el || $(this.el);
  },
  template: _.template("<% var rows = collection.models;  %>\n<thead>\n	<tr>\n		<% _.each(columns, function (col) { %>\n			<th class=\"<%= col.className || '' %>\">\n				<%= col.header || (_.isArray(col) && col[1]) || col %>\n			</th>\n		<% }) %>\n	</tr>\n</thead>\n<tbody>\n	<% _.each(rows, function (row, i) { %>\n	<tr class=\"<%= i % 2 ? 'even' : 'odd' %>\">\n		<% _.each(columns, function (col) { %>\n			<td class=\"<%= col.className || '' %>\"<% if (col.getValue) { %> value=\"<%= col.getValue.call(row) %>\"<% } %>>\n				<%= col.getFormatted ? col.getFormatted.call(row) : row.get((_.isArray(col) ? col[0] : col)) %>\n			</td>\n		<% }) %>\n	</tr>\n	<% }) %>\n</tbody>\n<tfoot>\n	<tr>\n		<% _.each(columns, function (col) { %>\n			<th class=\"<%= col.className || '' %>\"><%= col.footer || \"\" %></th>\n		<% }) %>\n	</tr>\n</tfoot>"),
  render: function() {
    this.$el.html(this.template({
      collection: this.collection,
      columns: this.options.columns
    }));
    return this;
  }
});
;
/*! http://mths.be/placeholder v2.0.7 by @mathias */
;(function(window, document, $) {

	var isInputSupported = 'placeholder' in document.createElement('input'),
	    isTextareaSupported = 'placeholder' in document.createElement('textarea'),
	    prototype = $.fn,
	    valHooks = $.valHooks,
	    hooks,
	    placeholder;

	if (isInputSupported && isTextareaSupported) {

		placeholder = prototype.placeholder = function() {
			return this;
		};

		placeholder.input = placeholder.textarea = true;

	} else {

		placeholder = prototype.placeholder = function() {
			var $this = this;
			$this
				.filter((isInputSupported ? 'textarea' : ':input') + '[placeholder]')
				.not('.placeholder')
				.bind({
					'focus.placeholder': clearPlaceholder,
					'blur.placeholder': setPlaceholder
				})
				.data('placeholder-enabled', true)
				.trigger('blur.placeholder');
			return $this;
		};

		placeholder.input = isInputSupported;
		placeholder.textarea = isTextareaSupported;

		hooks = {
			'get': function(element) {
				var $element = $(element);
				return $element.data('placeholder-enabled') && $element.hasClass('placeholder') ? '' : element.value;
			},
			'set': function(element, value) {
				var $element = $(element);
				if (!$element.data('placeholder-enabled')) {
					return element.value = value;
				}
				if (value == '') {
					element.value = value;
					// Issue #56: Setting the placeholder causes problems if the element continues to have focus.
					if (element != document.activeElement) {
						// We can't use `triggerHandler` here because of dummy text/password inputs :(
						setPlaceholder.call(element);
					}
				} else if ($element.hasClass('placeholder')) {
					clearPlaceholder.call(element, true, value) || (element.value = value);
				} else {
					element.value = value;
				}
				// `set` can not return `undefined`; see http://jsapi.info/jquery/1.7.1/val#L2363
				return $element;
			}
		};

		isInputSupported || (valHooks.input = hooks);
		isTextareaSupported || (valHooks.textarea = hooks);

		$(function() {
			// Look for forms
			$(document).delegate('form', 'submit.placeholder', function() {
				// Clear the placeholder values so they don't get submitted
				var $inputs = $('.placeholder', this).each(clearPlaceholder);
				setTimeout(function() {
					$inputs.each(setPlaceholder);
				}, 10);
			});
		});

		// Clear placeholder values upon page reload
		$(window).bind('beforeunload.placeholder', function() {
			$('.placeholder').each(function() {
				this.value = '';
			});
		});

	}

	function args(elem) {
		// Return an object of element attributes
		var newAttrs = {},
		    rinlinejQuery = /^jQuery\d+$/;
		$.each(elem.attributes, function(i, attr) {
			if (attr.specified && !rinlinejQuery.test(attr.name)) {
				newAttrs[attr.name] = attr.value;
			}
		});
		return newAttrs;
	}

	function clearPlaceholder(event, value) {
		var input = this,
		    $input = $(input);
		if (input.value == $input.attr('placeholder') && $input.hasClass('placeholder')) {
			if ($input.data('placeholder-password')) {
				$input = $input.hide().next().show().attr('id', $input.removeAttr('id').data('placeholder-id'));
				// If `clearPlaceholder` was called from `$.valHooks.input.set`
				if (event === true) {
					return $input[0].value = value;
				}
				$input.focus();
			} else {
				input.value = '';
				$input.removeClass('placeholder');
				input == document.activeElement && input.select();
			}
		}
	}

	function setPlaceholder() {
		var $replacement,
		    input = this,
		    $input = $(input),
		    $origInput = $input,
		    id = this.id;
		if (input.value == '') {
			if (input.type == 'password') {
				if (!$input.data('placeholder-textinput')) {
					try {
						$replacement = $input.clone().attr({ 'type': 'text' });
					} catch(e) {
						$replacement = $('<input>').attr($.extend(args(this), { 'type': 'text' }));
					}
					$replacement
						.removeAttr('name')
						.data({
							'placeholder-password': true,
							'placeholder-id': id
						})
						.bind('focus.placeholder', clearPlaceholder);
					$input
						.data({
							'placeholder-textinput': $replacement,
							'placeholder-id': id
						})
						.before($replacement);
				}
				$input = $input.removeAttr('id').hide().prev().attr('id', id).show();
				// Note: `$input[0] != input` now!
			}
			$input.addClass('placeholder');
			$input[0].value = $input.attr('placeholder');
		} else {
			$input.removeClass('placeholder');
		}
	}

}(this, document, jQuery));;
/*! jquery.infinitescroll.js | https://github.com/diy/jquery-infinitescroll | Apache License (v2) */
(function(b){b.fn.infiniteScroll=function(){var d=b(this),c=b(window),j=b("body"),e="init",f=!1,i=!0,a={threshold:80,onBottom:function(){},onEnd:null,iScroll:null};arguments.length&&("string"===typeof arguments[0]?(e=arguments[0],1<arguments.length&&"object"===typeof arguments[1]&&(a=b.extend(a,arguments[1]))):"object"===typeof arguments[0]&&(a=b.extend(a,arguments[0])));if("init"===e){var g=function(){if(!f&&i&&(a.iScroll?-a.iScroll.maxScrollY+a.iScroll.y:j.outerHeight()-c.height()-c.scrollTop())<
a.threshold){f=true;a.onBottom(function(b){if(b===false){i=false;if(typeof a.onEnd==="function")a.onEnd()}f=false})}};if(a.iScroll){var h=a.iScroll.options.onScrollMove||null;a.iScroll.options.onScrollMove=function(){h&&h();g()};a.iScroll_scrollMove=h}else c.on("scroll.infinite resize.infinite",g);d.data("infinite-scroll",a);b(g)}"reset"===e&&(a=d.data("infinite-scroll"),a.iScroll&&(a.iScroll_scrollMove&&(a.iScroll.options.onScrollMove=a.iScroll_scrollMove),a.iScroll.scrollTo(0,0,0,!1)),c.off("scroll.infinite resize.infinite"),
d.infiniteScroll(a));return this}})(jQuery);
;
function render_data_prefixes() {
    function prefixChange() {
        var row = $('#globalDataTableDrop option:selected').val();
        var prefix_drop = $('#prefixDrop option:selected').val();
        if (_.isUndefined(row) || _.isUndefined(prefix_drop)) {
            $('#permissions').html('');
            return;
        }
        var permissions = PREFIXES.get(row).get(decode_id(prefix_drop));
        ps = permissions;
        var perms = ['r'];
        if (permissions == 'rw')
            perms = ['rw', 'r'];
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#permissions').html(Mustache.render(select_template, {prefixes: _.map(perms, function (x) {return {text: x, value: encode_id(x)}})}));
    }
    function change() {
        var row = $('#globalDataTableDrop option:selected').val();
        if (_.isUndefined(row)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        var prefixes = [];
        var table_prefixes = PREFIXES.get(row);
        if (_.isUndefined(table_prefixes)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        _.each(table_prefixes.attributes, function (val, key) {
            if (key == 'row') {
                return;
            }
            prefixes.push(key);
        });
        prefixes.sort();
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#prefixDrop').html(Mustache.render(select_template, {prefixes: _.map(prefixes, function (x) {return {text: x, value: encode_id(x)}})}));
        $('#prefixDrop').change(prefixChange); // TODO: Redo this in backbone
        prefixChange();
    }
    $('#globalDataTableDrop').change(change);
    $('#createButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        if (_.isUndefined(row)) {
            return;
        }
        var data = {};
        data[decode_id($('#prefixDrop option:selected').val()) + unescape($('#suffix').val())] = decode_id($('#permissions option:selected').val());
        PREFIXES.get(row).save(data, {patch: true});
    });
    new RowsView({collection: PREFIXES, el: $('#prefixes'), deleteValues: true, postRender: change});
}
function render_data_projects() {
    prefixes_selector();
    $('#modifyProjectButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        var data = {};
        var value = slices_selector_get(true).join(',');
        var project = $('#projectName').val();
        if (project === '')
            return;
        data[project] = value;
        PROJECTS.get(row).save(data, {patch: true});
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return this.escape('row');
    }};
    new RowsView({collection: PROJECTS, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
}
function render_data_usage() {
    new RowsView({collection: USAGE, el: $('#usage')});
}
function render_models_list() {
    var columns = ['meta:name', 'meta:input_type', 'meta:output_type', 'row', 'meta:creation_time', 'meta:input',
                   'meta:model_link_size', 'meta:model_chain_size', 'meta:factory_info'];

    var takeoutColumn = {header: "Takeout", getFormatted: function() {
        return Mustache.render("<a class='takeout_link' row='{{row}}'>Link</a>/<a class='takeout_chain' row='{{row}}'>Chain</a>", {row: encode_id(this.get('row'))});
    }};
    var tagsColumn = {header: "Tags", className: "models-tags", getFormatted: function() { return this.escape('meta:tags') + '<span style="font-size:5px"><a class="modal_link_tags" row="' + encode_id(this.get('row')) + '">edit</a></span>'}};
    var notesColumn = {header: "Notes", className: "models-notes", getFormatted: function() { return this.escape('meta:notes') + '<span style="font-size:5px"><a class="modal_link_notes" row="' + encode_id(this.get('row')) + '">edit</a></span>'}};
    var rowB64Column = {header: "RowB64", getFormatted: function() { return base64.encode(this.get('row'))}};
    function postRender() {
        function process_takeout(row, model_chunks_column, model_column, model_type) {
            function takeoutSuccess(response) {
                 chunks = _.map(response, function (v, k) {
                    return [Number(k.split('-')[1]), v];
                }).sort();
                 model = _.map(chunks, function (v, k) {
                    return v[1];
                }).join('');
                var curSha1 = Sha1.hash(model, false);
                var trueSha1 = MODELS.get(row).escape('meta:model_' + model_type + '_sha1');
                if (curSha1 === trueSha1) {
                    var modelByteArray = new Uint8Array(model.length);
                    for (var i = 0; i < model.length; i++) {
                        modelByteArray[i] = model.charCodeAt(i) & 0xff;
                    }
                    var blob = new Blob([modelByteArray]);
                    saveAs(blob, 'picarus-model-' + encode_id(row) + '.sha1-' +  trueSha1 + '.' + model_type + '.msgpack');
                } else {
                    alert("Model SHA1 doesn't match!");
                }
            }
            var num_chunks = Number(MODELS.get(row).escape(model_chunks_column));
            var columns =  _.map(_.range(num_chunks), function (x) {
                return model_column + '-' + x;
            });
            console.log(row)
            PICARUS.getRow('models', row, {columns: columns, success: takeoutSuccess})
        }
        $('.takeout_link').click(function (data) {
            process_takeout(decode_id($(data.target).attr('row')), 'meta:model_link_chunks', 'data:model_link', 'link');
        });
        $('.takeout_chain').click(function (data) {
            process_takeout(decode_id($(data.target).attr('row')), 'meta:model_chain_chunks', 'data:model_chain', 'chain');
        });

        function setup_modal(links, col) {
            links.click(function (data) {
                var row = decode_id(data.target.getAttribute('row'));
                var model = MODELS.get(row);
                $('#modal_content').val(model.escape(col));
                $('#save_button').unbind();
                $('#save_button').click(function () {
                    var attributes = {};
                    attributes[col] = $('#modal_content').val();
                    model.save(attributes, {patch: true});
                    $('#myModal').modal('hide');
                });
                $('#myModal').modal('show')
            })
        }
        setup_modal($('.modal_link_notes'), 'meta:notes');
        setup_modal($('.modal_link_tags'), 'meta:tags');
    }
    new RowsView({collection: MODELS, el: $('#results'), extraColumns: [takeoutColumn, notesColumn, tagsColumn, rowB64Column], postRender: postRender, deleteRows: true, columns: columns});
}
function render_models_create() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'renderKind');
            _.bindAll(this, 'renderName');
            this.collection.bind('reset', this.renderKind);
            this.collection.bind('change', this.renderKind);
            this.collection.bind('add', this.renderKind);
            this.renderKind();
        },
        events: {'change #kind_select': 'renderName',
                 'change #name_select': 'renderParam'},
        renderParam: function () {
            $('#params').html('');
            $('#slices_select').html('');
            var model_kind = $('#kind_select option:selected').val();
            var name = $('#name_select option:selected').val();
            model_create_selector($('#slices_select'), $('#params'), model_kind, name);
        },
        renderKind: function() {
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.uniq(_.map(this.collection.models, function (data) {return data.escape('kind')}));
            if (!models_filt.length)
                return;
            $('#kind_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderName();
        },
        renderName: function () {
            var model_kind = $('#kind_select option:selected').val();
            var cur_models = this.collection.filter(function (x) { return x.escape('kind') == model_kind});
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.map(cur_models, function (data) {return data.escape('name')});
            $('#name_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderParam();
        }
    });
    av = new AppView({collection: PARAMETERS, el: $('#selects')});
    $('#runButton').click(function () {
        var params = model_create_selector_get($('#params'))
        function success(response) {
            var row = response.row;
            if (_.isUndefined(row))
                row = response.modelRow;
            var model = new PicarusRow({row: row}, {table: 'models', columns: ['meta:']});
            MODELS.add(model);
            model.fetch();
            $('#results').html(response.row);
            button_reset();
        }
        var model_kind = $('#kind_select option:selected').val();
        var name = $('#name_select option:selected').val();
        var model = PARAMETERS.filter(function (x) {
            if (x.escape('kind') == model_kind && x.escape('name') == name)
                return true;
        })[0];
        var path = model.get('row');
        params.path = path;
        if (model.escape('type') === 'factory') {
            params.table = 'images';
            params.slices = slices_selector_get().join(';');
            p = params;
            PICARUS.postTable('models', {success: _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: success}), data: params});
        } else {
            PICARUS.postTable('models', {success: success, data: params});
        }
    });
}
function render_models_single() {
    function render_image(image_data, div, success) {
        var image_id = _.uniqueId('image_');
        var canvas_id = _.uniqueId('canvas_');
        var image_tag = $('<img>').css('visibility', 'hidden').css('display', 'none').attr('id', image_id);
        image_tag.load(function () {
            success(image_id, canvas_id);
        });
        div.append(image_tag.attr('src', image_data));
    }
    function render_image_boxes(image_data, boxes, num_boxes, div) {
        render_image(image_data, div, function (image_id, canvas_id) {
            var h = $('#' + image_id).height();
            var w = $('#' + image_id).width();
            div.append($('<canvas>').attr('id', canvas_id).attr('height', h + 'px').attr('width', w + 'px'));
            var c = document.getElementById(canvas_id);
            var ctx = c.getContext("2d");
            ctx.strokeStyle = 'blue';
            var img = document.getElementById(image_id);
            ctx.drawImage(img, 0, 0);
            _.each(_.range(num_boxes), function (x) {
                var x0 = boxes[x * 4 + 2] * w;
                var x1 = boxes[x * 4 + 3] * w;
                var y0 = boxes[x * 4] * h;
                var y1 = boxes[x * 4 + 1] * h;
                ctx.moveTo(x0, y0);ctx.lineTo(x0, y1);ctx.stroke(); // TL->BL
                ctx.moveTo(x0, y1);ctx.lineTo(x1, y1);ctx.stroke(); // BL->BR
                ctx.moveTo(x1, y1);ctx.lineTo(x1, y0);ctx.stroke(); // BR->TR
                ctx.moveTo(x1, y0);ctx.lineTo(x0, y0);ctx.stroke(); // TR->TL
            });
        });
    }
    function render_image_points(image_data, points, num_points, div) {
        render_image(image_data, div, function (image_id, canvas_id) {
            var h = $('#' + image_id).height();
            var w = $('#' + image_id).width();
            div.append($('<canvas>').attr('id', canvas_id).attr('height', h + 'px').attr('width', w + 'px'));
            var c = document.getElementById(canvas_id);
            var ctx = c.getContext("2d");
            ctx.strokeStyle = 'blue';
            var img = document.getElementById(image_id);
            ctx.drawImage(img, 0, 0);
            _.each(_.range(num_points), function (x) {
                var sz = Math.max(h, w) * points[x * 6 + 5] / 2;
                var y = points[x * 6 + 0] * h;
                var x = points[x * 6 + 1] * w;
                ctx.beginPath();
                ctx.arc(x, y,sz,0,2*Math.PI);
                ctx.stroke();
            })
                });
    }
    var models = model_dropdown({modelFilter: function (x) {return true},
                                 change: function() {},
                                 el: $('#model_select')});
    function handleFileSelect(func, evt) {
        var files = evt.target.files;
        for (var i = 0, f; f = files[i]; i++) {
            if (!f.type.match('image.*'))
                continue;
            var reader = new FileReader();
            reader.onload = (function(theFile) {
                return function(e) {
                    func(e.target.result);
                };
            })(f);
            reader.readAsDataURL(f);
        }
    }
    function fileChange(evt) {
        imageData = undefined;
        handleFileSelect(function (x) {imageData = x}, evt);
        $('#imagefile').wrap('<div />');
        if ($('#imagefile')[0].files.length != 1) {
            display_alert('You must specify an image!');
            return;
        }
        var modelKey = decode_id($('#model_select').find(":selected").val());
        function success_func(result) {
            $('#imagefile').parent().html($('#imagefile').parent().html());
            $('#imagefile').change(fileChange);
            var outputType = models.get(modelKey).escape('meta:output_type');
            if (outputType == 'binary_class_confidence') {
                $('#results').html($('<h3>').text('Classifier Confidence'));
                $('#results').append(msgpack.unpack(result[modelKey]));
            } else if (outputType == 'binary_prediction') {
                $('#results').html($('<h3>').text('Binary Prediction'));
                $('#results').append(String(msgpack.unpack(result[modelKey])));
            } else if (outputType == 'processed_image') {
                $('#results').html($('<h3>').text('Processed Image'));
                $('#results').append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(result[modelKey])));
            } else if (outputType == 'image_detections') {
                $('#results').html($('<h3>').text('Detections'));
                v = msgpack.unpack(result[modelKey]);
                render_image_boxes(imageData, v[0], v[1][0], $('#results'));
            } else if (outputType == 'feature') {
                $('#results').html($('<h3>').text('Feature'));
                $('#results').append(_.escape(JSON.stringify(msgpack.unpack(result[modelKey])[0])));
            } else if (outputType == 'multi_class_distance') {
                $('#results').html($('<h3>').text('Multi Class Distance'));
                var data = msgpack.unpack(result[modelKey]);
                _.each(data, function (x) {
                    $('#results').append(x[1] + ' ' + x[0] + '<br>');
                });
            } else if (outputType == 'distance_image_rows') {
                $('#results').html($('<h3>').text('Image Search Results'));
                var data = msgpack.unpack(result[modelKey]);
                debug_data = msgpack.unpack(result[modelKey]);
                _.each(data, function (x) {
                    var image_id = _.uniqueId('image_');
                    $('#results').append('<img id="' + image_id + '">' + ' ' + x[0] + '<br>');
                    imageThumbnail(x[1], image_id);
                });
            } else if (outputType == 'feature2d_binary') {
                var data = msgpack.unpack(result[modelKey]);
                debug_data = data;
                render_image_points(imageData, data[1], data[2][0], $('#results'));
            } else {
                debug_result = result[modelKey];
                alert('Unrecognized output type');
            }
        }
        function upload_func(response) {
            PICARUS.postRow(table, response.row, {success: success_func, data: {model: modelKey, action: 'i/chain'}});
        }
        var table = 'images';
        var data = {};
        data['data:image'] = $('#imagefile')[0].files[0];
        PICARUS.postTable(table, {success: upload_func, data: data})
        $('#results').html('');
    }
    $('#imagefile').change(fileChange);
}
function render_models_slice() {
    model_dropdown({modelFilter: function (x) {return true},
                    el: $('#model_select')});
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var action = 'io/link';
        if ($('#chainCheck').is(':checked'))
            action = 'io/chain';
        var model = decode_id($('#model_select').find(":selected").val());
        PICARUS.postSlice('images', startRow, stopRow, {success:  _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: button_reset}), fail: button_error, data: {action: action, model: model}});
    });
}
function render_process_thumbnail() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.postSlice('images', startRow, stopRow, {data: {action: 'io/thumbnail'},
                                                        success: _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: button_reset}), fail: button_error})
    });
}
function render_process_delete() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.deleteSlice('images', startRow, stopRow, {success: button_reset, fail: button_error})
    });
}
function render_process_exif() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.postSlice('images', startRow, stopRow, {data: {action: 'io/exif'}, success:  _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: button_reset}), fail: button_error})
    });
}
function render_process_modify() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var columnName = $('#columnName').val();
        var columnValue = $('#columnValue').val();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var data = {};
        data[columnName] = columnValue;
        PICARUS.patchSlice('images', startRow, stopRow, {success: button_reset, fail: button_error, data: data})
    });
}
function render_process_copy() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    row_selector($('#rowPrefixDrop2'));
    $('#runButton').click(function () {
        button_running();
        var imageColumn = 'data:image';
        var columnName = $('#columnName').val();
        var columnValue = $('#columnValue').val();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var prefix = $('#rowPrefixDrop2 option:selected').val();
        var maxRows = Number($('#maxRows').val());
        function success(row, columns) {
            // Generate row key
            var cur_row = prefix + random_bytes(10);
            cur_data = {};
            cur_data[imageColumn] = columns[imageColumn];
            if (columnName.length)
                cur_data[columnName] = columnValue;
            PICARUS.patchRow("images", cur_row, {data: cur_data});
        }
        // Scan through rows, each one write back to the prefix
        PICARUS.scanner("images", startRow, stopRow, {success: success, done: button_reset, fail: button_error, maxRows: maxRows, maxRowsIter: 5, columns: [imageColumn]});
    });
}
function render_jobs_list() {
    var workerColumn = {header: "Worker", getFormatted: function() {
        if (JOBS.get(this.get('row')).get('type') != 'annotation')
            return '';
        return Mustache.render("<a href='/v0/annotation/{{task}}/index.html' target='_blank'>Worker</a>", {task: this.escape('row')});
    }};
    var syncColumn = {header: "Sync", getFormatted: function() {
        if (JOBS.get(this.get('row')).get('type') != 'annotation')
            return '';
        return '<span style="font-size:5px"><a class="tasks-sync" row="' + encode_id(this.get('row')) + '">sync</a></span>';
    }};

    function postRender() {
        $('.tasks-sync').click(function (data) {
            var row = decode_id(data.target.getAttribute('row'));
            var model = JOBS.get(row);
            PICARUS.postRow('jobs', row, {data: {'action': 'io/annotation/sync'}});
        });
    }
    // TODO: Filter based on type == annotation
    new RowsView({collection: JOBS, el: $('#annotations'), extraColumns: [workerColumn, syncColumn], postRender: postRender, deleteRows: true});
}
function render_jobs_flickr() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var demo_class = $('#democlass').val();
        var demo_query = $('#demoquery').val();
        var row_prefix = $('#rowPrefixDrop').val();
        if (demo_query.length == 0 && row_prefix.length == 0) {
            display_alert('Must specify query and prefix');
            return;
        }
        queries = _.shuffle(demo_query.split(';'));
        var iters = parseInt($('#demoiters').val())
        var simul = 10;
        if (isNaN(iters) || iters < 1 || iters > 20) {
            display_alert('Iters must be 0 < x <= 20');
            return;
        }
        $('#results').html('');
        /* Check input */
        //reset_state();
        var min_time = 1232170610;
        var latitude = Number($('#demolat').val());
        var longitude = Number($('#demolon').val());
        var done = 0;

        states = [];
        _.each(queries, function (query) {
            var state = {query: query, className: demo_class};
            _.each(_.range(iters), function () {states.push(state)});
        });
        states = _.shuffle(states);
        simul = Math.min(simul, states.length);
        function call_api(state) {
            var timeRadius = 60 * 60 * 24 * 30 * 6; // 6 months
            var minUploadDate = parseInt((new Date().getTime() / 1000 - min_time) * Math.random() + min_time - timeRadius);
            var maxUploadDate = parseInt(timeRadius * 2 + minUploadDate);
            var p = {action: 'o/crawl/flickr', hasGeo: Number($('#demogeo').is(':checked')), query: state.query, minUploadDate: minUploadDate, maxUploadDate: maxUploadDate};
            var apiKey = $('#demoapikey').val();
            var apiSecret = $('#demoapisecret').val();
            if (apiKey && apiSecret) {
                p.apiKey = apiKey;
                p.apiSecret = apiSecret;
            }
            if (state.className.length)
                p.className = state.className;
            if (latitude && longitude) {
                p.lat = String(latitude);
                p.lon = String(longitude);
            }
            function success() {          
                function etod(e) {
                    var d = new Date(0);
                    d.setUTCSeconds(e);
                    return d.toString();
                }
                var data = {minUploadDate: etod(minUploadDate), maxUploadDate: etod(maxUploadDate)};
                $('#results').append('Crawl Finished : ' + state.query + ' '+ JSON.stringify(data) + '<br>');
                if (!states.length) {
                    simul -= 1;
                    if (!simul)
                        button_reset();
                    return;
                }
                call_api(states.pop());
            }
            var graphDiv = $('<div>');
            $('#results').append(graphDiv);
            $('#results').append($('<br>'));
            PICARUS.postSlice('images', row_prefix, prefix_to_stop_row(row_prefix), {success: _.partial(watchJob, {success: _.partial(updateJobStatus, graphDiv), done: success}), data: p});
        }
        _.each(_.range(simul), function () {call_api(states.pop())});
    });
}
function render_jobs_class() {
    slices_selector();
    $('#runButton').click(function () {
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var imageColumn = 'thum:image_150sq';
        var numTasks = Number($('#num_tasks').val());
        var classColumn = $('#class').val();
        var mode = $('#modeSelect').val();
        function success(response) {
            JOBS.fetch();
            $('#results').append($('<a>').attr('href', '/v0/annotation/' + response.row + '/index.html').text('Worker').attr('target', '_blank'));
        }
        PICARUS.postTable('jobs', {success: success, data: {path: 'annotation/images/class', slices: slices_selector_get().join(';'), imageColumn: imageColumn, classColumn: classColumn, instructions: $('#instructions').val(), numTasks: numTasks, mode: mode}});
    });
}
function render_visualize_thumbnails() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        function uninstallScroll() {
            $(window).unbind("scroll");
            $(window).off('scroll.infinite resize.infinite');
        }
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var imageColumn = 'thum:image_150sq';
        var getMoreData = undefined;
        var hasMoreData = true;
        var gimmeMoreData = false; // 
        uninstallScroll();
        $('#results').html('');
        var $el = $('<div>');
        $('#results').append($el);
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        function success(row, columns) {
            c = columns;
            console.log(row);
            if (!_.has(columns, imageColumn))
                return;
            console.log(row);
            $el.append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', row));
        }
        function done() {
            hasMoreData = false;
        }
        function resume(callback) {
            console.log('Got resume');
            if (gimmeMoreData) {
                gimmeMoreData = false;
                callback();
            } else
                getMoreData = callback;
        }
        var params = {success: success, columns: [imageColumn], resume: resume};
        $el.infiniteScroll({threshold: 1024, onEnd: function () {
            console.log('No more results');
        }, onBottom: function (callback) {
            if (!jQuery.contains(document.documentElement, $el[0])) {
                uninstallScroll();
                return;
            }
            console.log('More data!');
            if (hasMoreData)
                if (!_.isUndefined(getMoreData)) {
                    var more = getMoreData;
                    getMoreData = undefined;
                    more();
                } else {
                    gimmeMoreData = true;
                }
            callback(hasMoreData);
        }});
        PICARUS.scanner("images", startRow, stopRow, params);
    });
}
function render_visualize_metadata() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var max_size = Number($('#maxSize').val());
        var metaCF = 'meta:';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        button_confirm_click_reset($('#removeButton'));
        // Setup table
        images = new PicarusRows([], {'table': 'images'});
        function remove_rows() {
            // TODO: Since there is a maxRows setting, this won't remove all rows, just the ones we have available
            var rows = _.map(images.models, function (x) {return x.id});
            picarus_api_delete_rows(rows, progressModal());
        }
        function done() {
            $('#results').html('');
            if (!images.length)
                return;
            // TODO: Change to use RowsView
            var AppView = Backbone.View.extend({
                initialize: function() {
                    _.bindAll(this, 'render');
                    this.collection.bind('reset', this.render);
                    this.collection.bind('change', this.render);
                    this.collection.bind('add', this.render);
                    this.collection.bind('sync', this.render);
                },
                render: function() {
                    var columns = _.uniq(_.flatten(_.map(this.collection.models, function (x) {
                        return _.keys(x.attributes);
                    })));
                    picarus_table = new Backbone.Table({
                        collection: this.collection,
                        columns: _.map(columns, function (v) {
                            if (v === "row")
                                return [v, v];
                            return {header: v, getFormatted: function() {
                                var out = this.get(v);
                                if (typeof out !== 'undefined') {
                                    if (out.length <= max_size)
                                        return out;
                                    else
                                        return '<span style="color:red">' + out.slice(0, max_size) + '</span>'
                                }
                            }};
                        })
                    });
                    this.$el.html(picarus_table.render().el);
                }
            });
            av = new AppView({collection: images, el: $('#results')});
            av.render();
            $('#removeButton').removeAttr('disabled');
            button_confirm_click($('#removeButton'), remove_rows);
        }
        function success(row, columns) {
            columns.row = row;
            images.add(columns);
        }
        var params = {success: success, maxRows: 1000, done: done, columns: [metaCF]};
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}
function render_visualize_exif() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var max_size = Number($('#maxSize').val());
        var exif_column = 'meta:exif';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        images = new PicarusRows([], {'table': 'images'});
        function done() {
            $('#results').html('');
            if (!images.length)
                return;
            // TODO: Change to use RowsView
            var AppView = Backbone.View.extend({
                initialize: function() {
                    _.bindAll(this, 'render');
                    this.collection.bind('reset', this.render);
                    this.collection.bind('change', this.render);
                    this.collection.bind('add', this.render);
                },
                render: function() {
                    var cur_images = this.collection.filter(function (x) {return x.get(exif_column) != '{}' && !_.isUndefined(x.get(exif_column))});
                    columns = _.uniq(_.flatten(_.map(cur_images, function (x) {
                        return _.keys(JSON.parse(x.get(exif_column)));
                    }))).concat(['row']);
                    picarus_table = new Backbone.Table({
                        collection: this.collection,
                        columns: _.map(columns, function (v) {
                            if (v === "row")
                                return [v, v];
                            return {header: v, getFormatted: function() {
                                var cur_exif = JSON.parse(this.get(exif_column));
                                var out = cur_exif[v];
                                if (typeof out !== 'undefined') {
                                    if (!_.isString(out))
                                        return _.escape(JSON.stringify(out));
                                    out = base64.decode(out);
                                    if (typeof out.length <= max_size)
                                        return _.escape(out);
                                    else
                                        return '<span style="color:red">' + _.escape(out.slice(0, max_size)) + '</span>'
                                }
                            }};
                        })
                    });
                    this.$el.html(picarus_table.render().el);
                }
            });
            av = new AppView({collection: images, el: $('#results')});
            av.render();
        }
        function success(row, columns) {
            columns.row = row;
            if (columns[exif_column] != '{}')
                images.add(columns);
        }
        var params = {success: success, maxRows: 1000, done: done, columns: [exif_column]};
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}
function render_visualize_locations() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBBsKtzgLTIsaoxAFUvSNoJ8n3j4w9VZs0&sensor=false&callback=render_visualize_locations_loaded";
    document.body.appendChild(script);
}
function render_visualize_locations_loaded() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    function deg2rad(deg) {
        return deg * (Math.PI/180)
    }
    function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
        // From: http://stackoverflow.com/questions/27928/how-do-i-calculate-distance-between-two-latitude-longitude-points
        var R = 6371; // Radius of the earth in km
        var dLat = deg2rad(lat2-lat1);
        var dLon = deg2rad(lon2-lon1); 
        var a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon/2) * Math.sin(dLon/2); 
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
        var d = R * c; // Distance in km
        return d;
    }
    function filter_lat_long(lat, lon) {
        var targetLat = Number($('#demolat').val());
        var targetLong = Number($('#demolong').val());
        var targetDist = Number($('#demodist').val());
        var checked = $('#filterInvert').is(':checked');
        if (!targetLat || !targetLong)
            return checked;
        if (getDistanceFromLatLonInKm(targetLat, targetLong, lat, lon) > targetDist)
            return !checked;
        return checked;
    }
    $('#runButton').click(function () {
        var latitude = 'meta:latitude';
        var longitude = 'meta:longitude';
        button_confirm_click_reset($('#removeButton'));
        images = new PicarusRows([], {'table': 'images'});
        function maps_success(row, columns) {
            columns.row = row;
            var curLat = columns[latitude];
            var curLong = columns[longitude];
            if (filter_lat_long(Number(curLat), Number(curLong))) {
                return;
            }
            images.add(new PicarusRow(columns));
        }
        function maps_done() {
            var centerLat = Number($('#demolat').val());
            var centerLong = Number($('#demolong').val());
            button_confirm_click($('#removeButton'), function () {
                var rows = _.map(images.models, function (x) {return x.get('row')});
                picarus_api_delete_rows(rows, progressModal());
            });
            $('#removeButton').removeAttr('disabled');
            if (!centerLat || !centerLat) {
                centerLat = Number(images.at(0).get(latitude));
                centerLong = Number(images.at(0).get(longitude));
            }
            var mapOptions = {
                zoom: 14,
                center: new google.maps.LatLng(centerLat, centerLong),
                mapTypeId: google.maps.MapTypeId.HYBRID
            };
            map = new google.maps.Map(document.getElementById("map_canvas"),
                                      mapOptions);
            google.maps.event.addListener(map, 'rightclick', function(event){
                $('#demolat').val(event.latLng.lat());
                $('#demolong').val(event.latLng.lng());
            });
            images.each(function (x) {
                var lat = Number(x.get(latitude));
                var lon = Number(x.get(longitude));
                new google.maps.Marker({position: new google.maps.LatLng(lat, lon), map: map});
            });
        }
        PICARUS.scanner("images", unescape($('#startRow').val()), unescape($('#stopRow').val()), {success: maps_success, done: maps_done, columns: [latitude, longitude]});
    })
}
function render_visualize_times() {
    google_visualization_load(render_visualize_times_loaded);
}

function render_visualize_times_loaded() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    function drawYears(hist) {
        var data = google.visualization.arrayToDataTable([['Year', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histYear')).draw(data, {title:"Histogram (Year)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Year"}});
    }
    function drawMonths(hist) {
        var data = google.visualization.arrayToDataTable([['Month', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histMonth')).draw(data, {title:"Histogram (Month)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Month"}});
    }
    function drawHours(hist) {
        var data = google.visualization.arrayToDataTable([['Hour', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histHour')).draw(data, {title:"Histogram (Hour)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Hour"}});
    }
    function drawDays(hist) {
        var data = google.visualization.arrayToDataTable([['Day', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histDay')).draw(data, {title:"Histogram (Day)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Day"}});
    }
    function dataToHist(data) {
        var hist = {};
        _.each(data, function (x) {
            var y = 0;
            if (_.has(hist, x)) {
                y = hist[x];
            }
            hist[x] = y + 1;
        });
        return hist;
    }
    function dataToListHist(data) {
        return _.map(_.pairs(dataToHist(data)), function (x) {return [Number(x[0]), x[1]]}).sort();
    }
    $('#runButton').click(function () {
        var timeColumn = 'meta:dateupload';
        images = new PicarusRows([], {'table': 'images'});
        function time_success(row, columns) {
            columns.row = row;
            images.add(new PicarusRow(columns));
        }
        function time_done() {
            years = [];
            months = [];
            hours = [];
            days = [];
            // TODO: FInish visual
            images.each(function (x) {
                var curTime = Number(x.get(timeColumn));
                var curDate = new Date(0);
                curDate.setUTCSeconds(curTime);
                years.push(curDate.getFullYear());
                months.push(curDate.getMonth());
                hours.push(curDate.getHours());
                days.push(curDate.getDay());
            });
            drawYears(dataToListHist(years));
            drawMonths(dataToListHist(months));
            drawHours(dataToListHist(hours));
            drawDays(dataToListHist(days));
        }
        PICARUS.scanner("images", unescape($('#startRow').val()), unescape($('#stopRow').val()), {success: time_success, done: time_done, columns: [timeColumn]});
    })
}
function render_visualize_annotations() {
    google_visualization_load(render_visualize_annotations_loaded);
}

function render_visualize_annotations_loaded() {
    function collect_users(users, results, onlyWorkers, onlyAnnotated) {
        var users_filtered = {};
        users.each(function(x) {
            if (x.escape('workerId') || !onlyWorkers)
                users_filtered[x.get('row')] = [];
        });
        results.each(function (x) {
            var i = x.escape('userId');
            if (_.has(users_filtered, i) && (!onlyAnnotated || x.escape('endTime'))) {
                users_filtered[i].push(x);
            }
        });
        _.each(users_filtered, function (x) {
            x.sort(function (a, b) {
                a = Number(a.escape('startTime'));
                b = Number(b.escape('startTime'));
                if (a < b)
                    return -1;
                if (a > b)
                    return 1;
                return 0;
            });
        });
        return users_filtered;
    }
    function image_class_score(results) {
        // Only count explicit marks
        var scores = {};

        _.each(results, function (x) {
            var annotation = x.get('userData');
            if (_.isUndefined(annotation))
                return;
            annotation = JSON.parse(annotation);
            var image = x.get('image');
            var cls = x.escape('class');
            if (!_.has(scores, cls)) {
                scores[cls] = {scoresPos: {}, scoresNeg: {}, scoresTotal: {}};
            }
            var scoresPos = scores[cls].scoresPos;
            var scoresNeg = scores[cls].scoresNeg;
            var scoresTotal = scores[cls].scoresTotal;
            if (_.has(scoresTotal, image))
                scoresTotal[image] += 1;
            else
                scoresTotal[image] = 1;
            if (annotation == 'true') {
                if (_.has(scoresPos, image))
                    scoresPos[image] += 1;
                else
                    scoresPos[image] = 1;
            }
            if (annotation == 'false') {
                if (_.has(scoresNeg, image))
                    scoresNeg[image] += 1;
                else
                    scoresNeg[image] = 1;
            }
        });
        return scores;
    }
    function display_annotation_task(task, get_classes, get_scores) {
        results = new PicarusRows([], {'table': 'annotation-results-' + task});
        users = new PicarusRows([], {'table': 'annotation-users-' + task});
        var imageColumn = 'thum:image_150sq';
        $('#negPct').change(data_change);
        $('#posPct').change(data_change);
        $('#posCnt').change(data_change);
        $('#negCnt').change(data_change);
        function data_change() {
            user_annotations = collect_users(users, results, true, true);
            clean_results = _.flatten(_.values(user_annotations), true);
            var classes = get_classes(clean_results);
            var select_template = "{{#classes}}<option value='{{.}}'>{{.}}</option>{{/classes}};"
            $('#class_select').html(Mustache.render(select_template, {classes: classes}));
            $('#class_select').unbind();
            $('#class_select').change(class_select_change);
            class_scores = get_scores(clean_results);
            class_select_change();
            var scores = _.map(class_scores, function (s, class_name) {
                var out = {pos: 0, neg: 0, total: 0, unique: _.size(s.scoresTotal)};
                _.each(s.scoresPos, function (x) {
                    out.pos += x;
                });
                _.each(s.scoresNeg, function (x) {
                    out.neg += x;
                });
                _.each(s.scoresTotal, function (x) {
                    out.total += x;
                });
                out.quality = (out.pos - out.neg) / (out.total + .0000001);
                out.class_name = class_name;
                return out;
            });
            // Update class annotations table
            scores.sort(function (x, y) {return y.quality - x.quality})
            var scores_template = "<table><tr><td>Name</td><td>Pos Annot.</td><td>Neg Annot.</td><td>Tot Annot.</td><td>Unique</td></tr>{{#scores}}<tr><td>{{class_name}}</td><td>{{pos}}</td><td>{{neg}}</td><td>{{total}}</td><td>{{unique}}</td></tr>{{/scores}}</table>";
            $('#annotation-stats').html(Mustache.render(scores_template, {scores: scores}));
            // Update user annotation time vs iteration
            annotation_times = {};
            _.each(user_annotations, function (z) {
                _.each(z, function(x, y) {
                    var t = Number(x.escape('endTime')) - Number(x.escape('startTime'));
                    if (_.has(annotation_times, y))
                        annotation_times[y].push(t)
                    else
                        annotation_times[y] = [t];
                });
            });
            var mean = function (x) { return _.reduce(x, function(memo, num){ return memo + num; }, 0) / x.length};
            median_rows = _.map(annotation_times, function (x, y) {
                x.sort(function (x, y) {return x - y});
                return [Number(y), _.min(x), x[Math.round(x.length / 2)], mean(x)]
            });
            var data0 = to_google_data(median_rows, ['Iteration', 'Min', 'Median', 'Mean']);
            var options = {title: 'Annotation Time vs Iteration #',
                           hAxis: {title: 'Iteration'}};
            var chart0 = new google.visualization.LineChart(document.getElementById('annotator_time_graph'));
            chart0.draw(data0, options);
        }
        function class_select_change() {
            var class_name = $('#class_select').find(":selected").val();
            negPct = Number($('#negPct').val());
            posPct = Number($('#posPct').val());
            negCnt = Math.max(1, Number($('#negCnt').val()));
            posCnt = Math.max(1, Number($('#posCnt').val()));
            scores = class_scores[class_name];
            if (_.isUndefined(scores))
                return;
            ts = scores.scoresTotal;
            posScores = _.sortBy(_.filter(_.pairs(scores.scoresPos), function (x) {return x[1] >= posCnt && (x[1] / ts[x[0]]) >= posPct}), function (x) { return -x[1] });
            negScores = _.sortBy(_.filter(_.pairs(scores.scoresNeg), function (x) {return x[1] >= negCnt && (x[1] / ts[x[0]]) >= negPct}), function (x) { return x[1] });
            os = _.omit(_.omit(ts, _.keys(scores.scoresPos)), _.keys(scores.scoresNeg));
            otherScores = _.shuffle(_.pairs(os));
            function display_samples(div, scores, title) {
                div.html('');
                div.append($('<h3>').text(title + ' ' + scores.length + ' / ' + _.size(ts)));
                
                _.each(scores.slice(0, 24), function (x) {
                    var id = _.uniqueId('image_');
                    div.append($('<img>').attr('id', id).attr('title', 'Row: ' + base64.encode(x[0]) + ' Score: ' + x[1]).addClass('hide'));
                    function success(response) {
                        if (_.isUndefined(response[imageColumn]))
                            return;
                        $('#' + id).attr('src', 'data:image/jpeg;base64,' + base64.encode(response[imageColumn])).attr('width', '150px').removeClass('hide');
                    }
                    PICARUS.getRow("images", x[0], {success: success, columns: [imageColumn]});
                });
            }
            display_samples($('#positive_samples'), posScores, 'Positive Samples');
            display_samples($('#negative_samples'), negScores, 'Negative Samples');
            display_samples($('#other_samples'), otherScores, 'Other Samples (not pos/neg)');
            
            // Hookup delete
            function delete_row() {
                action = $('#actionSplit').find(":selected").val();
                delKeys = _.keys(_.object({'positive': posScores, 'negative': negScores, 'other': otherScores}[action]));
                picarus_api_delete_rows(delKeys, progressModal());
                button_confirm_click_reset($('#removeButton'));
                button_confirm_click($('#removeButton'), delete_row);
            }
            button_confirm_click($('#removeButton'), delete_row);
            // Hookup modify
            function modify_row() {
                var action = $('#actionSplit').find(":selected").val();
                var modifyKeys = _.keys(_.object({'positive': posScores, 'negative': negScores, 'other': otherScores}[action]));
                picarus_api_modify_rows(modifyKeys, $('#colName').val(), $('#colValue').val(), progressModal());
                button_confirm_click_reset($('#modifyButton'));
                button_confirm_click($('#modifyButton'), modify_row);
            }
            button_confirm_click($('#modifyButton'), modify_row);
            $('#actionSplit').change(change_actions);
            function change_actions () {
                button_confirm_click_reset($('#removeButton'));
                button_confirm_click($('#removeButton'), delete_row);
                button_confirm_click_reset($('#modifyButton'));
                button_confirm_click($('#modifyButton'), modify_row);
            }
        }
        new RowsView({collection: results, el: $('#annotation-results'), postRender: _.debounce(data_change, 100)});
        results.fetch();
        
        new RowsView({collection: users, el: $('#annotation-users'), postRender: _.debounce(data_change, 100)});
        users.fetch();
        debug_dc = data_change;
    }
    function change() {
        var task = decode_id($('#annotator_select').find(":selected").val());
        if (_.isUndefined(task)) {
            return;
        }
        function success_annotation(annotation) {
            annotation_type = JSON.parse(annotation['params']).type;
            if (annotation_type == 'image_class') {
                get_classes = function (results) {
                    return _.unique(results.map(function (x, y) {return x.escape('class')})).sort()
                }
                get_scores = image_class_score;
            }
            display_annotation_task(task, get_classes, get_scores);
        }
        PICARUS.getRow("jobs", task, {success: success_annotation});
    }
    // TODO: Need to filter based on type == annotation
    rows_dropdown(JOBS, {el: $('#annotator_select'), text: function (x) {
        var p = JSON.parse(x.get('params'));
        if (p.type == "image_class")
            return p.type + ' ' + p.num_tasks;
        return p.type;
    }, change: change});
}
function render_evaluate_classifier() {
    google_visualization_load(render_evaluate_classifier_loaded);
}

function render_evaluate_classifier_loaded() {
    model_dropdown({modelFilter: function (x) {return x.escape('meta:output_type') === 'binary_class_confidence'},
                    change: function() {
                        var row = decode_id(this.$el.find(":selected").val());
                        m = this.collection.get(row);
                        $('#gtColumn').val(JSON.parse(m.get('meta:factory_info')).inputs.meta);
                        $('#posClass').val(JSON.parse(m.get('meta:factory_info')).params.class_positive);
                        $('#modelKey').val(encode_id(row));
                    },
                    el: $('#model_select')});
    slices_selector();
    $('#runButton').click(function () {
        button_running();
        confs = {pos_confs: [], neg_confs: []};
        var gt_column = decode_id($('#gtColumn').val());
        var conf_column = decode_id($('#modelKey').val());
        var posClass = $('#posClass').val();
        
        sliceStats = {}; // [startRow/stopRow] = {# pos, # neg, # noconf, #nometa, #noconfmeta}
        var slices = slices_selector_get(true);
        _.each(slices, function (start_stop_row, index) {
            var curSlice = start_stop_row.join('/');
            sliceStats[curSlice] = {'numPos': 0, 'numNeg': 0, 'noConf': 0, 'noGT': 0, 'noConfGT': 0};
            function success(row, columns) {
                $('#progress').css('width', (100 * (confs.pos_confs.length + confs.neg_confs.length) / 19850.) + '%')
                c = columns;
                if (_.has(columns, conf_column) && _.has(columns, gt_column)) {
                    if (columns[gt_column] == posClass) {
                        sliceStats[curSlice].numPos += 1;
                        confs.pos_confs.push(msgpack.unpack(columns[conf_column]));
                    } else {
                        sliceStats[curSlice].numNeg += 1;
                        confs.neg_confs.push(msgpack.unpack(columns[conf_column]));
                    }
                } else {
                    if (!_.has(columns, conf_column))
                        sliceStats[curSlice].noConf += 1;
                    if (!_.has(columns, gt_column))
                        sliceStats[curSlice].noConfGT += 1;
                    if (!_.has(columns, gt_column))
                        sliceStats[curSlice].noGT += 1;
                }
            }
            var success_confs;
            if (index == (slices.length - 1))
                success_confs = function () {
                    confs.neg_confs.sort(function(a, b) {return a - b});
                    confs.pos_confs.sort(function(a, b) {return a - b});
                    plot_confs(confs);
                    render_slice_stats_table($('#slicesTable'), sliceStats);
                    button_reset();
                }
            else
                success_confs = function () {}
            PICARUS.scanner("images", decode_id(start_stop_row[0]), decode_id(start_stop_row[1]), {success: success, done: success_confs, columns: [gt_column, conf_column]});
        });
    })
}
function render_slice_stats_table(table, sliceStats) {
    //sliceStats[curSlice] = {'numPos': 0, 'numNeg': 0, 'noConf': 0, 'noGT': 0, 'noConfGT': 0};
    var select_template = "<table>{{#slices}}<tr><td>{{name}}</td><td>{{numPos}}</td><td>{{numNeg}}</td><td>{{noConf}}</td><td>{{noGT}}</td><td>{{noConfGT}}</td></tr>{{/slices}}</table>"
    function convert_name(k) {
        return _.map(k.split('/'), function (x) {
            return decode_id(x);
        }).join('/');
    }
    var slices = [{name: 'Slice', numPos: 'Pos', numNeg: 'Neg', noConf: 'No Conf', noGT: 'No GT', noConfGT: 'No ConfGT'}];
    slices = slices.concat(_.map(sliceStats, function (v, k) {v.name = convert_name(k); return v}));
    table.html(Mustache.render(select_template, {slices: slices}));
}
function confs_to_conf_hist(pos_confs, neg_confs, bins, normalize) {
    /* Takes in confs, produces a histogram capturing both pos/neg confs in each bin
       TODO: Check that each bin gets get an equal portion of the range
    */
    var min_conf = Math.min(pos_confs[0], neg_confs[0]);
    var max_conf = Math.min(pos_confs[pos_confs.length - 1], neg_confs[neg_confs.length - 1]);
    var shift = min_conf;
    var scale = bins / (max_conf - min_conf);
    var pos_buckets = [];
    var neg_buckets = [];
    var coords = [];
    var i, cur_bucket;
    for (i = 0; i < bins; i++) {
        pos_buckets[i] = 0;
        neg_buckets[i] = 0;
    }
    for (i = 0; i < pos_confs.length; i++) {
        pos_buckets[Math.min(bins - 1, Math.max(0, Math.floor((pos_confs[i] - shift) * scale)))] += 1;
    }
    for (i = 0; i < neg_confs.length; i++) {
        neg_buckets[Math.min(bins - 1, Math.max(0, Math.floor((neg_confs[i] - shift) * scale)))] += 1;
    }
    for (i = 0; i < bins; i++) {
        coords[i] = [(i + .5) / scale + shift, pos_buckets[i], neg_buckets[i]];
        if (normalize) {
            coords[i][1] /= pos_confs.length;
            coords[i][2] /= neg_confs.length;
        }
    }
    return coords;
}
function test_confs_to_confusion_matrix() {
    //var cms;
    cms = confs_to_confusion_matrix([], []);
    if (!_.isEqual(cms, []))
        return 1;
    
    cms = confs_to_confusion_matrix([0], []);
    if (!_.isEqual(cms, [[1, 0, 0, 0, 0]]))
        return 2;
    
    cms = confs_to_confusion_matrix([], [0]);
    if (!_.isEqual(cms, [[0, 0, 1, 0, Infinity]]))
        return 3;
    
    cms = confs_to_confusion_matrix([0], [0]);
    if (!_.isEqual(cms, [[1, 1, 0, 0, 0], [0, 0, 1, 1, Infinity]]))
        return 4;
    
    cms = confs_to_confusion_matrix([1], [0]);
    if (!_.isEqual(cms, [[1, 0, 1, 0, 1]]))
        return 5;
    
    cms = confs_to_confusion_matrix([0], [1]);
    if (!_.isEqual(cms, [[1, 1, 0, 0, 0], [0, 0, 1, 1, Infinity]]))
        return 6;
    
    cms = confs_to_confusion_matrix([0, 0], [0]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [0, 0, 1, 2, Infinity]]))
        return 7;
    
    cms = confs_to_confusion_matrix([0, 1], [0]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [1, 0, 1, 1, 1]]))
        return 8;
    
    cms = confs_to_confusion_matrix([0, 0], [1]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [0, 0, 1, 2, Infinity]]))
        return 9;
    
    cms = confs_to_confusion_matrix([1, 2], [0]);
    if (!_.isEqual(cms, [[2, 0, 1, 0, 1]]))
        return 10;
    
    cms = confs_to_confusion_matrix([0, 2], [1]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [1, 0, 1, 1, 2]]))
        return 11;
    
    cms = confs_to_confusion_matrix([0, 1], [2]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [0, 0, 1, 2, Infinity]]))
        return 12;
    
    cms = confs_to_confusion_matrix([1, 2], [0, 3]);
    if (!_.isEqual(cms, [[2, 1, 1, 0, 1], [0, 0, 2, 2, Infinity]]))
        return 13;
    
    cms = confs_to_confusion_matrix([1, 2, 3], [0, 3]);
    if (!_.isEqual(cms, [[3, 1, 1, 0, 1], [0, 0, 2, 3, Infinity]]))
        return 14;
    
    cms = confs_to_confusion_matrix([1, 2, 3, 3], [0, 3]);
    if (!_.isEqual(cms, [[4, 1, 1, 0, 1], [0, 0, 2, 4, Infinity]]))
        return 15;
    return 0;
}
function confs_to_confusion_matrix(pos_confs, neg_confs) {
    /* Takes in confs, produces list of [tp, fp, tn, fn, thresh] */
    var cm_threshs = [];
    var fn = 0;
    var tn = 0;
    var i;
    var cur_thresh;
    while (pos_confs.length || neg_confs.length) {
        // Skip Negatives
        for (i = 0; i < neg_confs.length; i++) {
            if (neg_confs[i] >= pos_confs[0]) {
                break;
            }
        }
        neg_confs = neg_confs.slice(i, neg_confs.length);
        tn += i;
        // Add PR point (cur_thresh = pos_confs[0])
        if (pos_confs.length) {
            cur_thresh = pos_confs[0];
        } else {
            cur_thresh = Infinity;
        }
        cm_threshs.push([pos_confs.length, neg_confs.length, tn, fn, cur_thresh]);
        // Skip Positives
        for (i = 0; i < pos_confs.length; i++) {
            if (pos_confs[i] > neg_confs[0]) {
                break;
            }
        }
        pos_confs = pos_confs.slice(i, pos_confs.length);
        fn += i;
    }
    return cm_threshs;
}
function cms_to_rps(cms) {
    var rps = [];
    var i;
    for (i = 0; i < cms.length; i++) {
        rps.push([cms[i][0] / (cms[i][0] + cms[i][3]), cms[i][0] / (cms[i][0] + cms[i][1]), cms[i][4]])
    }
    return rps;
}
function cms_to_conf_accs(cms) {
    var conf_accs = [];
    var i;
    for (i = 0; i < cms.length; i++) {
        conf_accs.push([cms[i][4], (cms[i][0] + cms[i][2]) / (cms[i][0] + cms[i][1] + cms[i][2] + cms[i][3])])
    }
    return conf_accs;
}
function cms_to_fpr_tprs(cms) {
    var fpr_tprs = [];
    var i, fpr, tpr;
    var p = confs.pos_confs.length;
    var n = confs.neg_confs.length;
    for (i = 0; i < cms.length; i++) {
        fpr = cms[i][1] / n; // FP / N
        tpr = cms[i][0] / p; // TP / P
        fpr_tprs.push([fpr, tpr, cms[i][4]]);
    }
    return fpr_tprs;
}
function to_google_data(pts, labels, tooltip) {
    var i;
    var data = new google.visualization.DataTable();
    for (i = 0; i < labels.length; i++) {
        data.addColumn('number', labels[i]);
    }
    if (tooltip) {
        data.addColumn({type: 'number', role: 'tooltip'});
    }
    d = pts;
    data.addRows(pts);
    return data;
}
function plot_confs(confs) {
    var test_out = test_confs_to_confusion_matrix();
    if (test_out)
        alert(test_out);
    var data0 = to_google_data(confs_to_conf_hist(confs.pos_confs, confs.neg_confs, 100), ['Confidence', '+', '-']);
    var options = {title: 'Classifier Confidence',
                   hAxis: {title: 'Confidence'}};
    var chart0 = new google.visualization.LineChart(document.getElementById('graph_confidence_scatter'));
    chart0.draw(data0, options);
    
    var data1 = to_google_data(confs_to_conf_hist(confs.pos_confs, confs.neg_confs, 100, true), ['Confidence', '+', '-']);
    options = {title: 'Classifier Confidence (normalized)',
               hAxis: {title: 'Confidence'}};
    var chart1 = new google.visualization.LineChart(document.getElementById('graph_confidence_scatter_norm'));
    chart1.draw(data1, options);
    
    // PR Curve
    var cms = confs_to_confusion_matrix(confs.pos_confs, confs.neg_confs);
    // Confidence accuracy
    var data4 = to_google_data(cms_to_conf_accs(cms), ['Confidence', 'Accuracy']);
    options = {title: 'Classifier Confidence vs Accuracy',
               hAxis: {title: 'Confidence'}};
    var chart4 = new google.visualization.LineChart(document.getElementById('graph_confidence_accuracy'));
    chart4.draw(data4, options);
    var data2 = to_google_data(cms_to_rps(cms), ['recall', 'precision'], true);
    options = {title: 'PR Curve',
               hAxis: {title: 'Recall', minValue: 0, maxValue: 1},
               vAxis: {title: 'Precision', minValue: 0, maxValue: 1},
               chartArea: {width: 200, height: 200},
               legend: {position: 'none'}};
    var chart2 = new google.visualization.LineChart(document.getElementById('graph_rps'));
    chart2.draw(data2, options);
    
    var data3 = to_google_data(cms_to_fpr_tprs(cms), ['fpr', 'tpr'], true);
    options = {title: 'ROC Curve',
               hAxis: {title: 'FPR', minValue: 0, maxValue: 1},
               vAxis: {title: 'TPR', minValue: 0, maxValue: 1},
               chartArea: {width: 200, height: 200},
               legend: {position: 'none'}};
    var chart3 = new google.visualization.LineChart(document.getElementById('graph_roc'));
    chart3.draw(data3, options);
    
    
    // This connects all the charts together
    function setNearest(chart, data, column, select_columns, val) {
        var i, minVal = Infinity, minIndex, curVal;
        for (i = 0; i < data.getNumberOfRows(); i++) {
            curVal = Math.abs(val - data.getValue(i, column));
            if (curVal < minVal) {
                minVal = curVal;
                minIndex = i;
            }
        }
        
        chart.setSelection(_.map(select_columns, function (col) {return {row: minIndex, column: col}}));
    }
    function setSelections(thresh) {
        setNearest(chart0, data0, 0, [1, 2], thresh);
        setNearest(chart1, data1, 0, [1, 2], thresh);
        setNearest(chart2, data2, 2, [1], thresh);
        setNearest(chart3, data3, 2, [1], thresh);
        setNearest(chart4, data4, 0, [1], thresh);
    }
    var al = google.visualization.events.addListener;
    al(chart0, 'select', function () {var sel = chart0.getSelection(); if (sel[0] !== undefined) setSelections(data0.getValue(sel[0].row, 0))});
    al(chart1, 'select', function () {var sel = chart1.getSelection(); if (sel[0] !== undefined) setSelections(data1.getValue(sel[0].row, 0))});
    al(chart2, 'select', function () {var sel = chart2.getSelection(); if (sel[0] !== undefined) setSelections(data2.getValue(sel[0].row, 2))});
    al(chart3, 'select', function () {var sel = chart3.getSelection(); if (sel[0] !== undefined) setSelections(data3.getValue(sel[0].row, 2))});
    al(chart4, 'select', function () {var sel = chart4.getSelection(); if (sel[0] !== undefined) setSelections(data4.getValue(sel[0].row, 0))});
};
/*!{id:msgpack.js,ver:1.05,license:"MIT",author:"uupaa.js@gmail.com"}*/

// === msgpack ===
// MessagePack -> http://msgpack.sourceforge.net/

this.msgpack || (function(globalScope) {

globalScope.msgpack = {
    pack:       msgpackpack,    // msgpack.pack(data:Mix,
                                //              toString:Boolean = false):ByteArray/ByteString/false
                                //  [1][mix to String]    msgpack.pack({}, true) -> "..."
                                //  [2][mix to ByteArray] msgpack.pack({})       -> [...]
    unpack:     msgpackunpack,  // msgpack.unpack(data:BinaryString/ByteArray):Mix
                                //  [1][String to mix]    msgpack.unpack("...") -> {}
                                //  [2][ByteArray to mix] msgpack.unpack([...]) -> {}
    worker:     "msgpack.js",   // msgpack.worker - WebWorkers script filename
    upload:     msgpackupload,  // msgpack.upload(url:String, option:Hash, callback:Function)
    download:   msgpackdownload // msgpack.download(url:String, option:Hash, callback:Function)
};

var _ie         = /MSIE/.test(navigator.userAgent),
    _bin2num    = {}, // BinaryStringToNumber   { "\00": 0, ... "\ff": 255 }
    _num2bin    = {}, // NumberToBinaryString   { 0: "\00", ... 255: "\ff" }
    _num2b64    = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                   "abcdefghijklmnopqrstuvwxyz0123456789+/").split(""),
    _buf        = [], // decode buffer
    _idx        = 0,  // decode buffer[index]
    _error      = 0,  // msgpack.pack() error code. 1 = CYCLIC_REFERENCE_ERROR
    _isArray    = Array.isArray || (function(mix) {
                    return Object.prototype.toString.call(mix) === "[object Array]";
                  }),
    _toString   = String.fromCharCode, // CharCode/ByteArray to String
    _MAX_DEPTH  = 512;

// for WebWorkers Code Block
self.importScripts && (onmessage = function(event) {
    if (event.data.method === "pack") {
        postMessage(base64encode(msgpackpack(event.data.data)));
    } else {
        postMessage(msgpackunpack(event.data.data));
    }
});

// msgpack.pack
function msgpackpack(data,       // @param Mix:
                     toString) { // @param Boolean(= false):
                                 // @return ByteArray/BinaryString/false:
                                 //     false is error return
    //  [1][mix to String]    msgpack.pack({}, true) -> "..."
    //  [2][mix to ByteArray] msgpack.pack({})       -> [...]

    _error = 0;

    var byteArray = encode([], data, 0);

    return _error ? false
                  : toString ? byteArrayToByteString(byteArray)
                             : byteArray;
}

// msgpack.unpack
function msgpackunpack(data) { // @param BinaryString/ByteArray:
                               // @return Mix/undefined:
                               //       undefined is error return
    //  [1][String to mix]    msgpack.unpack("...") -> {}
    //  [2][ByteArray to mix] msgpack.unpack([...]) -> {}

    _buf = typeof data === "string" ? toByteArray(data) : data;
    _idx = -1;
    return decode(); // mix or undefined
}

// inner - encoder
function encode(rv,      // @param ByteArray: result
                mix,     // @param Mix: source data
                depth) { // @param Number: depth
    var size, i, iz, c, pos,        // for UTF8.encode, Array.encode, Hash.encode
        high, low, sign, exp, frac; // for IEEE754

    if (mix == null) { // null or undefined -> 0xc0 ( null )
        rv.push(0xc0);
    } else if (mix === false) { // false -> 0xc2 ( false )
        rv.push(0xc2);
    } else if (mix === true) {  // true  -> 0xc3 ( true  )
        rv.push(0xc3);
    } else {
        switch (typeof mix) {
        case "number":
            if (mix !== mix) { // isNaN
                rv.push(0xcb, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff); // quiet NaN
            } else if (mix === Infinity) {
                rv.push(0xcb, 0x7f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00); // positive infinity
            } else if (Math.floor(mix) === mix) { // int or uint
                if (mix < 0) {
                    // int
                    if (mix >= -32) { // negative fixnum
                        rv.push(0xe0 + mix + 32);
                    } else if (mix > -0x80) {
                        rv.push(0xd0, mix + 0x100);
                    } else if (mix > -0x8000) {
                        mix += 0x10000;
                        rv.push(0xd1, mix >> 8, mix & 0xff);
                    } else if (mix > -0x80000000) {
                        mix += 0x100000000;
                        rv.push(0xd2, mix >>> 24, (mix >> 16) & 0xff,
                                                  (mix >>  8) & 0xff, mix & 0xff);
                    } else {
                        high = Math.floor(mix / 0x100000000);
                        low  = mix & 0xffffffff;
                        rv.push(0xd3, (high >> 24) & 0xff, (high >> 16) & 0xff,
                                      (high >>  8) & 0xff,         high & 0xff,
                                      (low  >> 24) & 0xff, (low  >> 16) & 0xff,
                                      (low  >>  8) & 0xff,          low & 0xff);
                    }
                } else {
                    // uint
                    if (mix < 0x80) {
                        rv.push(mix); // positive fixnum
                    } else if (mix < 0x100) { // uint 8
                        rv.push(0xcc, mix);
                    } else if (mix < 0x10000) { // uint 16
                        rv.push(0xcd, mix >> 8, mix & 0xff);
                    } else if (mix < 0x100000000) { // uint 32
                        rv.push(0xce, mix >>> 24, (mix >> 16) & 0xff,
                                                  (mix >>  8) & 0xff, mix & 0xff);
                    } else {
                        high = Math.floor(mix / 0x100000000);
                        low  = mix & 0xffffffff;
                        rv.push(0xcf, (high >> 24) & 0xff, (high >> 16) & 0xff,
                                      (high >>  8) & 0xff,         high & 0xff,
                                      (low  >> 24) & 0xff, (low  >> 16) & 0xff,
                                      (low  >>  8) & 0xff,          low & 0xff);
                    }
                }
            } else { // double
                // THX!! @edvakf
                // http://javascript.g.hatena.ne.jp/edvakf/20101128/1291000731
                sign = mix < 0;
                sign && (mix *= -1);

                // add offset 1023 to ensure positive
                // 0.6931471805599453 = Math.LN2;
                exp  = ((Math.log(mix) / 0.6931471805599453) + 1023) | 0;

                // shift 52 - (exp - 1023) bits to make integer part exactly 53 bits,
                // then throw away trash less than decimal point
                frac = mix * Math.pow(2, 52 + 1023 - exp);

                //  S+-Exp(11)--++-----------------Fraction(52bits)-----------------------+
                //  ||          ||                                                        |
                //  v+----------++--------------------------------------------------------+
                //  00000000|00000000|00000000|00000000|00000000|00000000|00000000|00000000
                //  6      5    55  4        4        3        2        1        8        0
                //  3      6    21  8        0        2        4        6
                //
                //  +----------high(32bits)-----------+ +----------low(32bits)------------+
                //  |                                 | |                                 |
                //  +---------------------------------+ +---------------------------------+
                //  3      2    21  1        8        0
                //  1      4    09  6
                low  = frac & 0xffffffff;
                sign && (exp |= 0x800);
                high = ((frac / 0x100000000) & 0xfffff) | (exp << 20);

                rv.push(0xcb, (high >> 24) & 0xff, (high >> 16) & 0xff,
                              (high >>  8) & 0xff,  high        & 0xff,
                              (low  >> 24) & 0xff, (low  >> 16) & 0xff,
                              (low  >>  8) & 0xff,  low         & 0xff);
            }
            break;
        case "string":
            // http://d.hatena.ne.jp/uupaa/20101128
            iz = mix.length;
            pos = rv.length; // keep rewrite position

            rv.push(0); // placeholder

            // utf8.encode
            for (i = 0; i < iz; ++i) {
                c = mix.charCodeAt(i);
                if (c < 0x80) { // ASCII(0x00 ~ 0x7f)
                    rv.push(c & 0x7f);
                } else if (c < 0x0800) {
                    rv.push(((c >>>  6) & 0x1f) | 0xc0, (c & 0x3f) | 0x80);
                } else if (c < 0x10000) {
                    rv.push(((c >>> 12) & 0x0f) | 0xe0,
                            ((c >>>  6) & 0x3f) | 0x80, (c & 0x3f) | 0x80);
                }
            }
            size = rv.length - pos - 1;

            if (size < 32) {
                rv[pos] = 0xa0 + size; // rewrite
            } else if (size < 0x10000) { // 16
                rv.splice(pos, 1, 0xda, size >> 8, size & 0xff);
            } else if (size < 0x100000000) { // 32
                rv.splice(pos, 1, 0xdb,
                          size >>> 24, (size >> 16) & 0xff,
                                       (size >>  8) & 0xff, size & 0xff);
            }
            break;
        default: // array or hash
            if (++depth >= _MAX_DEPTH) {
                _error = 1; // CYCLIC_REFERENCE_ERROR
                return rv = []; // clear
            }
            if (_isArray(mix)) {
                size = mix.length;
                if (size < 16) {
                    rv.push(0x90 + size);
                } else if (size < 0x10000) { // 16
                    rv.push(0xdc, size >> 8, size & 0xff);
                } else if (size < 0x100000000) { // 32
                    rv.push(0xdd, size >>> 24, (size >> 16) & 0xff,
                                               (size >>  8) & 0xff, size & 0xff);
                }
                for (i = 0; i < size; ++i) {
                    encode(rv, mix[i], depth);
                }
            } else { // hash
                // http://d.hatena.ne.jp/uupaa/20101129
                pos = rv.length; // keep rewrite position
                rv.push(0); // placeholder
                size = 0;
                for (i in mix) {
                    ++size;
                    encode(rv, i,      depth);
                    encode(rv, mix[i], depth);
                }
                if (size < 16) {
                    rv[pos] = 0x80 + size; // rewrite
                } else if (size < 0x10000) { // 16
                    rv.splice(pos, 1, 0xde, size >> 8, size & 0xff);
                } else if (size < 0x100000000) { // 32
                    rv.splice(pos, 1, 0xdf,
                              size >>> 24, (size >> 16) & 0xff,
                                           (size >>  8) & 0xff, size & 0xff);
                }
            }
        }
    }
    return rv;
}

// inner - decoder
function decode() { // @return Mix:
    var size, i, iz, c, num = 0,
        sign, exp, frac, ary, hash,
        buf = _buf, type = buf[++_idx];

    if (type >= 0xe0) {             // Negative FixNum (111x xxxx) (-32 ~ -1)
        return type - 0x100;
    }
    if (type < 0xc0) {
        if (type < 0x80) {          // Positive FixNum (0xxx xxxx) (0 ~ 127)
            return type;
        }
        if (type < 0x90) {          // FixMap (1000 xxxx)
            num  = type - 0x80;
            type = 0x80;
        } else if (type < 0xa0) {   // FixArray (1001 xxxx)
            num  = type - 0x90;
            type = 0x90;
        } else { // if (type < 0xc0) {   // FixRaw (101x xxxx)
            num  = type - 0xa0;
            type = 0xa0;
        }
    }
    switch (type) {
    case 0xc0:  return null;
    case 0xc2:  return false;
    case 0xc3:  return true;
    case 0xca:  // float
                num = buf[++_idx] * 0x1000000 + (buf[++_idx] << 16) +
                                                (buf[++_idx] <<  8) + buf[++_idx];
                sign =  num & 0x80000000;    //  1bit
                exp  = (num >> 23) & 0xff;   //  8bits
                frac =  num & 0x7fffff;      // 23bits
                if (!num || num === 0x80000000) { // 0.0 or -0.0
                    return 0;
                }
                if (exp === 0xff) { // NaN or Infinity
                    return frac ? NaN : Infinity;
                }
                return (sign ? -1 : 1) *
                            (frac | 0x800000) * Math.pow(2, exp - 127 - 23); // 127: bias
    case 0xcb:  // double
                num = buf[++_idx] * 0x1000000 + (buf[++_idx] << 16) +
                                                (buf[++_idx] <<  8) + buf[++_idx];
                sign =  num & 0x80000000;    //  1bit
                exp  = (num >> 20) & 0x7ff;  // 11bits
                frac =  num & 0xfffff;       // 52bits - 32bits (high word)
                if (!num || num === 0x80000000) { // 0.0 or -0.0
                    _idx += 4;
                    return 0;
                }
                if (exp === 0x7ff) { // NaN or Infinity
                    _idx += 4;
                    return frac ? NaN : Infinity;
                }
                num = buf[++_idx] * 0x1000000 + (buf[++_idx] << 16) +
                                                (buf[++_idx] <<  8) + buf[++_idx];
                return (sign ? -1 : 1) *
                            ((frac | 0x100000) * Math.pow(2, exp - 1023 - 20) // 1023: bias
                             + num * Math.pow(2, exp - 1023 - 52));
    // 0xcf: uint64, 0xce: uint32, 0xcd: uint16
    case 0xcf:  num =  buf[++_idx] * 0x1000000 + (buf[++_idx] << 16) +
                                                 (buf[++_idx] <<  8) + buf[++_idx];
                return num * 0x100000000 +
                       buf[++_idx] * 0x1000000 + (buf[++_idx] << 16) +
                                                 (buf[++_idx] <<  8) + buf[++_idx];
    case 0xce:  num += buf[++_idx] * 0x1000000 + (buf[++_idx] << 16);
    case 0xcd:  num += buf[++_idx] << 8;
    case 0xcc:  return num + buf[++_idx];
    // 0xd3: int64, 0xd2: int32, 0xd1: int16, 0xd0: int8
    case 0xd3:  num = buf[++_idx];
                if (num & 0x80) { // sign -> avoid overflow
                    return ((num         ^ 0xff) * 0x100000000000000 +
                            (buf[++_idx] ^ 0xff) *   0x1000000000000 +
                            (buf[++_idx] ^ 0xff) *     0x10000000000 +
                            (buf[++_idx] ^ 0xff) *       0x100000000 +
                            (buf[++_idx] ^ 0xff) *         0x1000000 +
                            (buf[++_idx] ^ 0xff) *           0x10000 +
                            (buf[++_idx] ^ 0xff) *             0x100 +
                            (buf[++_idx] ^ 0xff) + 1) * -1;
                }
                return num         * 0x100000000000000 +
                       buf[++_idx] *   0x1000000000000 +
                       buf[++_idx] *     0x10000000000 +
                       buf[++_idx] *       0x100000000 +
                       buf[++_idx] *         0x1000000 +
                       buf[++_idx] *           0x10000 +
                       buf[++_idx] *             0x100 +
                       buf[++_idx];
    case 0xd2:  num  =  buf[++_idx] * 0x1000000 + (buf[++_idx] << 16) +
                       (buf[++_idx] << 8) + buf[++_idx];
                return num < 0x80000000 ? num : num - 0x100000000; // 0x80000000 * 2
    case 0xd1:  num  = (buf[++_idx] << 8) + buf[++_idx];
                return num < 0x8000 ? num : num - 0x10000; // 0x8000 * 2
    case 0xd0:  num  =  buf[++_idx];
                return num < 0x80 ? num : num - 0x100; // 0x80 * 2
    // 0xdb: raw32, 0xda: raw16, 0xa0: raw ( string )
    case 0xdb:  num +=  buf[++_idx] * 0x1000000 + (buf[++_idx] << 16);
    case 0xda:  num += (buf[++_idx] << 8)       +  buf[++_idx];
    case 0xa0:  // utf8.decode
                for (ary = [], i = _idx, iz = i + num; i < iz; ) {
                    c = buf[++i]; // lead byte
                    ary.push(c); // NOTE(Brandyn): Changed this
                    /*ary.push(c < 0x80 ? c : // ASCII(0x00 ~ 0x7f)
                             c < 0xe0 ? ((c & 0x1f) <<  6 | (buf[++i] & 0x3f)) :
                                        ((c & 0x0f) << 12 | (buf[++i] & 0x3f) << 6
                                                          | (buf[++i] & 0x3f))); */
                }
                _idx = i;
                return ary.length < 10240 ? _toString.apply(null, ary)
                                          : byteArrayToByteString(ary);
    // 0xdf: map32, 0xde: map16, 0x80: map
    case 0xdf:  num +=  buf[++_idx] * 0x1000000 + (buf[++_idx] << 16);
    case 0xde:  num += (buf[++_idx] << 8)       +  buf[++_idx];
    case 0x80:  hash = {};
                while (num--) {
                    // make key/value pair
                    size = buf[++_idx] - 0xa0;

                    for (ary = [], i = _idx, iz = i + size; i < iz; ) {
                        c = buf[++i]; // lead byte
                        ary.push(c < 0x80 ? c : // ASCII(0x00 ~ 0x7f)
                                 c < 0xe0 ? ((c & 0x1f) <<  6 | (buf[++i] & 0x3f)) :
                                            ((c & 0x0f) << 12 | (buf[++i] & 0x3f) << 6
                                                              | (buf[++i] & 0x3f)));
                    }
                    _idx = i;
                    hash[_toString.apply(null, ary)] = decode();
                }
                return hash;
    // 0xdd: array32, 0xdc: array16, 0x90: array
    case 0xdd:  num +=  buf[++_idx] * 0x1000000 + (buf[++_idx] << 16);
    case 0xdc:  num += (buf[++_idx] << 8)       +  buf[++_idx];
    case 0x90:  ary = [];
                while (num--) {
                    ary.push(decode());
                }
                return ary;
    }
    return;
}

// inner - byteArray To ByteString
function byteArrayToByteString(byteArray) { // @param ByteArray
                                            // @return String
    // http://d.hatena.ne.jp/uupaa/20101128
    try {
        return _toString.apply(this, byteArray); // toString
    } catch(err) {
        ; // avoid "Maximum call stack size exceeded"
    }
    var rv = [], i = 0, iz = byteArray.length, num2bin = _num2bin;

    for (; i < iz; ++i) {
        rv[i] = num2bin[byteArray[i]];
    }
    return rv.join("");
}

// msgpack.download - load from server
function msgpackdownload(url,        // @param String:
                         option,     // @param Hash: { worker, timeout, before, after }
                                     //    option.worker - Boolean(= false): true is use WebWorkers
                                     //    option.timeout - Number(= 10): timeout sec
                                     //    option.before  - Function: before(xhr, option)
                                     //    option.after   - Function: after(xhr, option, { status, ok })
                         callback) { // @param Function: callback(data, option, { status, ok })
                                     //    data   - Mix/null:
                                     //    option - Hash:
                                     //    status - Number: HTTP status code
                                     //    ok     - Boolean:
    option.method = "GET";
    option.binary = true;
    ajax(url, option, callback);
}

// msgpack.upload - save to server
function msgpackupload(url,        // @param String:
                       option,     // @param Hash: { data, worker, timeout, before, after }
                                   //    option.data - Mix:
                                   //    option.worker - Boolean(= false): true is use WebWorkers
                                   //    option.timeout - Number(= 10): timeout sec
                                   //    option.before  - Function: before(xhr, option)
                                   //    option.after   - Function: after(xhr, option, { status, ok })
                       callback) { // @param Function: callback(data, option, { status, ok })
                                   //    data   - String: responseText
                                   //    option - Hash:
                                   //    status - Number: HTTP status code
                                   //    ok     - Boolean:
    option.method = "PUT";
    option.binary = true;

    if (option.worker && globalScope.Worker) {
        var worker = new Worker(msgpack.worker);

        worker.onmessage = function(event) {
            option.data = event.data;
            ajax(url, option, callback);
        };
        worker.postMessage({ method: "pack", data: option.data });
    } else {
        // pack and base64 encode
        option.data = base64encode(msgpackpack(option.data));
        ajax(url, option, callback);
    }
}

// inner -
function ajax(url,        // @param String:
              option,     // @param Hash: { data, ifmod, method, timeout,
                          //                header, binary, before, after, worker }
                          //    option.data    - Mix: upload data
                          //    option.ifmod   - Boolean: true is "If-Modified-Since" header
                          //    option.method  - String: "GET", "POST", "PUT"
                          //    option.timeout - Number(= 10): timeout sec
                          //    option.header  - Hash(= {}): { key: "value", ... }
                          //    option.binary  - Boolean(= false): true is binary data
                          //    option.before  - Function: before(xhr, option)
                          //    option.after   - Function: after(xhr, option, { status, ok })
                          //    option.worker  - Boolean(= false): true is use WebWorkers
              callback) { // @param Function: callback(data, option, { status, ok })
                          //    data   - String/Mix/null:
                          //    option - Hash:
                          //    status - Number: HTTP status code
                          //    ok     - Boolean:
    function readyStateChange() {
        if (xhr.readyState === 4) {
            var data, status = xhr.status, worker, byteArray,
                rv = { status: status, ok: status >= 200 && status < 300 };

            if (!run++) {
                if (method === "PUT") {
                    data = rv.ok ? xhr.responseText : "";
                } else {
                    if (rv.ok) {
                        if (option.worker && globalScope.Worker) {
                            worker = new Worker(msgpack.worker);
                            worker.onmessage = function(event) {
                                callback(event.data, option, rv);
                            };
                            worker.postMessage({ method: "unpack",
                                                 data: xhr.responseText });
                            gc();
                            return;
                        } else {
                            byteArray = _ie ? toByteArrayIE(xhr)
                                            : toByteArray(xhr.responseText);
                            data = msgpackunpack(byteArray);
                        }
                    }
                }
                after && after(xhr, option, rv);
                callback(data, option, rv);
                gc();
            }
        }
    }

    function ng(abort, status) {
        if (!run++) {
            var rv = { status: status || 400, ok: false };

            after && after(xhr, option, rv);
            callback(null, option, rv);
            gc(abort);
        }
    }

    function gc(abort) {
        abort && xhr && xhr.abort && xhr.abort();
        watchdog && (clearTimeout(watchdog), watchdog = 0);
        xhr = null;
        globalScope.addEventListener &&
            globalScope.removeEventListener("beforeunload", ng, false);
    }

    var watchdog = 0,
        method = option.method || "GET",
        header = option.header || {},
        before = option.before,
        after = option.after,
        data = option.data || null,
        xhr = globalScope.XMLHttpRequest ? new XMLHttpRequest() :
              globalScope.ActiveXObject  ? new ActiveXObject("Microsoft.XMLHTTP") :
              null,
        run = 0, i,
        overrideMimeType = "overrideMimeType",
        setRequestHeader = "setRequestHeader",
        getbinary = method === "GET" && option.binary;

    try {
        xhr.onreadystatechange = readyStateChange;
        xhr.open(method, url, true); // ASync

        before && before(xhr, option);

        getbinary && xhr[overrideMimeType] &&
            xhr[overrideMimeType]("text/plain; charset=x-user-defined");
        data &&
            xhr[setRequestHeader]("Content-Type",
                                  "application/x-www-form-urlencoded");

        for (i in header) {
            xhr[setRequestHeader](i, header[i]);
        }

        globalScope.addEventListener &&
            globalScope.addEventListener("beforeunload", ng, false); // 400: Bad Request

        xhr.send(data);
        watchdog = setTimeout(function() {
            ng(1, 408); // 408: Request Time-out
        }, (option.timeout || 10) * 1000);
    } catch (err) {
        ng(0, 400); // 400: Bad Request
    }
}

// inner - BinaryString To ByteArray
function toByteArray(data) { // @param BinaryString: "\00\01"
                             // @return ByteArray: [0x00, 0x01]
    var rv = [], bin2num = _bin2num, remain,
        ary = data.split(""),
        i = -1, iz;

    iz = ary.length;
    remain = iz % 8;

    while (remain--) {
        ++i;
        rv[i] = bin2num[ary[i]];
    }
    remain = iz >> 3;
    while (remain--) {
        rv.push(bin2num[ary[++i]], bin2num[ary[++i]],
                bin2num[ary[++i]], bin2num[ary[++i]],
                bin2num[ary[++i]], bin2num[ary[++i]],
                bin2num[ary[++i]], bin2num[ary[++i]]);
    }
    return rv;
}

// inner - BinaryString to ByteArray
function toByteArrayIE(xhr) {
    var rv = [], data, remain,
        charCodeAt = "charCodeAt",
        loop, v0, v1, v2, v3, v4, v5, v6, v7,
        i = -1, iz;

    iz = vblen(xhr);
    data = vbstr(xhr);
    loop = Math.ceil(iz / 2);
    remain = loop % 8;

    while (remain--) {
        v0 = data[charCodeAt](++i); // 0x00,0x01 -> 0x0100
        rv.push(v0 & 0xff, v0 >> 8);
    }
    remain = loop >> 3;
    while (remain--) {
        v0 = data[charCodeAt](++i);
        v1 = data[charCodeAt](++i);
        v2 = data[charCodeAt](++i);
        v3 = data[charCodeAt](++i);
        v4 = data[charCodeAt](++i);
        v5 = data[charCodeAt](++i);
        v6 = data[charCodeAt](++i);
        v7 = data[charCodeAt](++i);
        rv.push(v0 & 0xff, v0 >> 8, v1 & 0xff, v1 >> 8,
                v2 & 0xff, v2 >> 8, v3 & 0xff, v3 >> 8,
                v4 & 0xff, v4 >> 8, v5 & 0xff, v5 >> 8,
                v6 & 0xff, v6 >> 8, v7 & 0xff, v7 >> 8);
    }
    iz % 2 && rv.pop();

    return rv;
}

// inner - base64.encode
function base64encode(data) { // @param ByteArray:
                              // @return Base64String:
    var rv = [],
        c = 0, i = -1, iz = data.length,
        pad = [0, 2, 1][data.length % 3],
        num2bin = _num2bin,
        num2b64 = _num2b64;

    if (globalScope.btoa) {
        while (i < iz) {
            rv.push(num2bin[data[++i]]);
        }
        return btoa(rv.join(""));
    }
    --iz;
    while (i < iz) {
        c = (data[++i] << 16) | (data[++i] << 8) | (data[++i]); // 24bit
        rv.push(num2b64[(c >> 18) & 0x3f],
                num2b64[(c >> 12) & 0x3f],
                num2b64[(c >>  6) & 0x3f],
                num2b64[ c        & 0x3f]);
    }
    pad > 1 && (rv[rv.length - 2] = "=");
    pad > 0 && (rv[rv.length - 1] = "=");
    return rv.join("");
}

// --- init ---
(function() {
    var i = 0, v;

    for (; i < 0x100; ++i) {
        v = _toString(i);
        _bin2num[v] = i; // "\00" -> 0x00
        _num2bin[i] = v; //     0 -> "\00"
    }
    // http://twitter.com/edvakf/statuses/15576483807
    for (i = 0x80; i < 0x100; ++i) { // [Webkit][Gecko]
        _bin2num[_toString(0xf700 + i)] = i; // "\f780" -> 0x80
    }
})();

_ie && document.write('<script type="text/vbscript">\
Function vblen(b)vblen=LenB(b.responseBody)End Function\n\
Function vbstr(b)vbstr=CStr(b.responseBody)+chr(0)End Function</'+'script>');

})(this);
;
/**
*
*  Secure Hash Algorithm (SHA1)
*  http://www.webtoolkit.info/
*
**/
 
function SHA1 (msg) {
 
    function rotate_left(n,s) {
        var t4 = ( n<<s ) | (n>>>(32-s));
        return t4;
    };
 
    function lsb_hex(val) {
        var str="";
        var i;
        var vh;
        var vl;
 
        for( i=0; i<=6; i+=2 ) {
            vh = (val>>>(i*4+4))&0x0f;
            vl = (val>>>(i*4))&0x0f;
            str += vh.toString(16) + vl.toString(16);
        }
        return str;
    };
 
    function cvt_hex(val) {
        var str="";
        var i;
        var v;
 
        for( i=7; i>=0; i-- ) {
            v = (val>>>(i*4))&0x0f;
            str += v.toString(16);
        }
        return str;
    };
 
 
    function Utf8Encode(string) {
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";
 
        for (var n = 0; n < string.length; n++) {
 
            var c = string.charCodeAt(n);
 
            if (c < 128) {
                utftext += String.fromCharCode(c);
            }
            else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
 
        }
 
        return utftext;
    };
 
    var blockstart;
    var i, j;
    var W = new Array(80);
    var H0 = 0x67452301;
    var H1 = 0xEFCDAB89;
    var H2 = 0x98BADCFE;
    var H3 = 0x10325476;
    var H4 = 0xC3D2E1F0;
    var A, B, C, D, E;
    var temp;
 
    msg = Utf8Encode(msg);
 
    var msg_len = msg.length;
 
    var word_array = new Array();
    for( i=0; i<msg_len-3; i+=4 ) {
        j = msg.charCodeAt(i)<<24 | msg.charCodeAt(i+1)<<16 |
            msg.charCodeAt(i+2)<<8 | msg.charCodeAt(i+3);
        word_array.push( j );
    }
 
    switch( msg_len % 4 ) {
    case 0:
        i = 0x080000000;
        break;
    case 1:
        i = msg.charCodeAt(msg_len-1)<<24 | 0x0800000;
        break;
 
    case 2:
        i = msg.charCodeAt(msg_len-2)<<24 | msg.charCodeAt(msg_len-1)<<16 | 0x08000;
        break;
 
    case 3:
        i = msg.charCodeAt(msg_len-3)<<24 | msg.charCodeAt(msg_len-2)<<16 | msg.charCodeAt(msg_len-1)<<8| 0x80;
        break;
    }
 
    word_array.push( i );
 
    while( (word_array.length % 16) != 14 ) word_array.push( 0 );
 
    word_array.push( msg_len>>>29 );
    word_array.push( (msg_len<<3)&0x0ffffffff );
 
 
    for ( blockstart=0; blockstart<word_array.length; blockstart+=16 ) {
 
        for( i=0; i<16; i++ ) W[i] = word_array[blockstart+i];
        for( i=16; i<=79; i++ ) W[i] = rotate_left(W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16], 1);
 
        A = H0;
        B = H1;
        C = H2;
        D = H3;
        E = H4;
 
        for( i= 0; i<=19; i++ ) {
            temp = (rotate_left(A,5) + ((B&C) | (~B&D)) + E + W[i] + 0x5A827999) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
 
        for( i=20; i<=39; i++ ) {
            temp = (rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0x6ED9EBA1) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
 
        for( i=40; i<=59; i++ ) {
            temp = (rotate_left(A,5) + ((B&C) | (B&D) | (C&D)) + E + W[i] + 0x8F1BBCDC) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
 
        for( i=60; i<=79; i++ ) {
            temp = (rotate_left(A,5) + (B ^ C ^ D) + E + W[i] + 0xCA62C1D6) & 0x0ffffffff;
            E = D;
            D = C;
            C = rotate_left(B,30);
            B = A;
            A = temp;
        }
 
        H0 = (H0 + A) & 0x0ffffffff;
        H1 = (H1 + B) & 0x0ffffffff;
        H2 = (H2 + C) & 0x0ffffffff;
        H3 = (H3 + D) & 0x0ffffffff;
        H4 = (H4 + E) & 0x0ffffffff;
 
    }
 
    var temp = cvt_hex(H0) + cvt_hex(H1) + cvt_hex(H2) + cvt_hex(H3) + cvt_hex(H4);
 
    return temp.toLowerCase();
 
}

// b64
b64_enc = base64.encode
b64_dec = base64.decode
 
// ub64
function ub64_enc(x) {
    return base64.encode(x).replace(/\+/g , '-').replace(/\//g , '_');
}
function ub64_dec(x) {
    return base64.decode(x.replace(/\-/g , '+').replace(/\_/g , '/'));
}

function object_ub64_b64_enc(x) {
    return _.object(_.map(_.pairs(x), function (i) {
        return [ub64_enc(i[0]), b64_enc(i[1])];
    }));
}

function object_ub64_b64_dec(x) {
    return _.object(_.map(_.pairs(x), function (i) {
        return [ub64_dec(i[0]), b64_dec(i[1])];
    }));
}

// json_ub64_b64
function json_ub64_b64_enc(x) {
    return JSON.stringify(object_ub64_b64_enc(x));
}

function json_ub64_b64_dec(x) {
    return object_ub64_b64_dec(JSON.parse(x));
};
if(!window['googleLT_']){window['googleLT_']=(new Date()).getTime();}if (!window['google']) {
window['google'] = {};
}
if (!window['google']['loader']) {
window['google']['loader'] = {};
google.loader.ServiceBase = 'https://www.google.com/uds';
google.loader.GoogleApisBase = 'https://ajax.googleapis.com/ajax';
google.loader.ApiKey = 'notsupplied';
google.loader.KeyVerified = true;
google.loader.LoadFailure = false;
google.loader.Secure = true;
google.loader.GoogleLocale = 'www.google.com';
google.loader.ClientLocation = null;
google.loader.AdditionalParams = '';
(function() {var d=void 0,g=!0,h=null,l=!1,m=encodeURIComponent,n=window,p=document;function q(a,b){return a.load=b}var s="push",t="replace",u="charAt",w="indexOf",x="ServiceBase",y="name",z="getTime",A="length",B="prototype",C="setTimeout",D="loader",E="substring",F="join",G="toLowerCase";function H(a){return a in I?I[a]:I[a]=-1!=navigator.userAgent[G]()[w](a)}var I={};function J(a,b){var c=function(){};c.prototype=b[B];a.U=b[B];a.prototype=new c}
function aa(a,b,c){var e=Array[B].slice.call(arguments,2)||[];return function(){var c=e.concat(Array[B].slice.call(arguments));return a.apply(b,c)}}function K(a){a=Error(a);a.toString=function(){return this.message};return a}function L(a,b){for(var c=a.split(/\./),e=n,f=0;f<c[A]-1;f++)e[c[f]]||(e[c[f]]={}),e=e[c[f]];e[c[c[A]-1]]=b}function ba(a,b,c){a[b]=c}if(!M)var M=L;if(!N)var N=ba;google[D].v={};M("google.loader.callbacks",google[D].v);var O={},P={};google[D].eval={};M("google.loader.eval",google[D].eval);
q(google,function(a,b,c){function e(a){var b=a.split(".");if(2<b[A])throw K("Module: '"+a+"' not found!");"undefined"!=typeof b[1]&&(f=b[0],c.packages=c.packages||[],c.packages[s](b[1]))}var f=a;c=c||{};if(a instanceof Array||a&&"object"==typeof a&&"function"==typeof a[F]&&"function"==typeof a.reverse)for(var k=0;k<a[A];k++)e(a[k]);else e(a);if(a=O[":"+f]){c&&(!c.language&&c.locale)&&(c.language=c.locale);c&&"string"==typeof c.callback&&(k=c.callback,k.match(/^[[\]A-Za-z0-9._]+$/)&&(k=n.eval(k),c.callback=
k));if((k=c&&c.callback!=h)&&!a.s(b))throw K("Module: '"+f+"' must be loaded before DOM onLoad!");k?a.m(b,c)?n[C](c.callback,0):a.load(b,c):a.m(b,c)||a.load(b,c)}else throw K("Module: '"+f+"' not found!");});M("google.load",google.load);
google.T=function(a,b){b?(0==Q[A]&&(R(n,"load",S),!H("msie")&&!H("safari")&&!H("konqueror")&&H("mozilla")||n.opera?n.addEventListener("DOMContentLoaded",S,l):H("msie")?p.write("<script defer onreadystatechange='google.loader.domReady()' src=//:>\x3c/script>"):(H("safari")||H("konqueror"))&&n[C](ca,10)),Q[s](a)):R(n,"load",a)};M("google.setOnLoadCallback",google.T);
function R(a,b,c){if(a.addEventListener)a.addEventListener(b,c,l);else if(a.attachEvent)a.attachEvent("on"+b,c);else{var e=a["on"+b];a["on"+b]=e!=h?da([c,e]):c}}function da(a){return function(){for(var b=0;b<a[A];b++)a[b]()}}var Q=[];google[D].P=function(){var a=n.event.srcElement;"complete"==a.readyState&&(a.onreadystatechange=h,a.parentNode.removeChild(a),S())};M("google.loader.domReady",google[D].P);var ea={loaded:g,complete:g};function ca(){ea[p.readyState]?S():0<Q[A]&&n[C](ca,10)}
function S(){for(var a=0;a<Q[A];a++)Q[a]();Q.length=0}google[D].d=function(a,b,c){if(c){var e;"script"==a?(e=p.createElement("script"),e.type="text/javascript",e.src=b):"css"==a&&(e=p.createElement("link"),e.type="text/css",e.href=b,e.rel="stylesheet");(a=p.getElementsByTagName("head")[0])||(a=p.body.parentNode.appendChild(p.createElement("head")));a.appendChild(e)}else"script"==a?p.write('<script src="'+b+'" type="text/javascript">\x3c/script>'):"css"==a&&p.write('<link href="'+b+'" type="text/css" rel="stylesheet"></link>')};
M("google.loader.writeLoadTag",google[D].d);google[D].Q=function(a){P=a};M("google.loader.rfm",google[D].Q);google[D].S=function(a){for(var b in a)"string"==typeof b&&(b&&":"==b[u](0)&&!O[b])&&(O[b]=new T(b[E](1),a[b]))};M("google.loader.rpl",google[D].S);google[D].R=function(a){if((a=a.specs)&&a[A])for(var b=0;b<a[A];++b){var c=a[b];"string"==typeof c?O[":"+c]=new U(c):(c=new W(c[y],c.baseSpec,c.customSpecs),O[":"+c[y]]=c)}};M("google.loader.rm",google[D].R);google[D].loaded=function(a){O[":"+a.module].l(a)};
M("google.loader.loaded",google[D].loaded);google[D].O=function(){return"qid="+((new Date)[z]().toString(16)+Math.floor(1E7*Math.random()).toString(16))};M("google.loader.createGuidArg_",google[D].O);L("google_exportSymbol",L);L("google_exportProperty",ba);google[D].a={};M("google.loader.themes",google[D].a);google[D].a.I="//www.google.com/cse/style/look/bubblegum.css";N(google[D].a,"BUBBLEGUM",google[D].a.I);google[D].a.K="//www.google.com/cse/style/look/greensky.css";N(google[D].a,"GREENSKY",google[D].a.K);
google[D].a.J="//www.google.com/cse/style/look/espresso.css";N(google[D].a,"ESPRESSO",google[D].a.J);google[D].a.M="//www.google.com/cse/style/look/shiny.css";N(google[D].a,"SHINY",google[D].a.M);google[D].a.L="//www.google.com/cse/style/look/minimalist.css";N(google[D].a,"MINIMALIST",google[D].a.L);google[D].a.N="//www.google.com/cse/style/look/v2/default.css";N(google[D].a,"V2_DEFAULT",google[D].a.N);function U(a){this.b=a;this.o=[];this.n={};this.e={};this.f={};this.j=g;this.c=-1}
U[B].g=function(a,b){var c="";b!=d&&(b.language!=d&&(c+="&hl="+m(b.language)),b.nocss!=d&&(c+="&output="+m("nocss="+b.nocss)),b.nooldnames!=d&&(c+="&nooldnames="+m(b.nooldnames)),b.packages!=d&&(c+="&packages="+m(b.packages)),b.callback!=h&&(c+="&async=2"),b.style!=d&&(c+="&style="+m(b.style)),b.noexp!=d&&(c+="&noexp=true"),b.other_params!=d&&(c+="&"+b.other_params));if(!this.j){google[this.b]&&google[this.b].JSHash&&(c+="&sig="+m(google[this.b].JSHash));var e=[],f;for(f in this.n)":"==f[u](0)&&e[s](f[E](1));
for(f in this.e)":"==f[u](0)&&this.e[f]&&e[s](f[E](1));c+="&have="+m(e[F](","))}return google[D][x]+"/?file="+this.b+"&v="+a+google[D].AdditionalParams+c};U[B].t=function(a){var b=h;a&&(b=a.packages);var c=h;if(b)if("string"==typeof b)c=[a.packages];else if(b[A]){c=[];for(a=0;a<b[A];a++)"string"==typeof b[a]&&c[s](b[a][t](/^\s*|\s*$/,"")[G]())}c||(c=["default"]);b=[];for(a=0;a<c[A];a++)this.n[":"+c[a]]||b[s](c[a]);return b};
q(U[B],function(a,b){var c=this.t(b),e=b&&b.callback!=h;if(e)var f=new X(b.callback);for(var k=[],r=c[A]-1;0<=r;r--){var v=c[r];e&&f.B(v);if(this.e[":"+v])c.splice(r,1),e&&this.f[":"+v][s](f);else k[s](v)}if(c[A]){b&&b.packages&&(b.packages=c.sort()[F](","));for(r=0;r<k[A];r++)v=k[r],this.f[":"+v]=[],e&&this.f[":"+v][s](f);if(!b&&P[":"+this.b]!=h&&P[":"+this.b].versions[":"+a]!=h&&!google[D].AdditionalParams&&this.j){c=P[":"+this.b];google[this.b]=google[this.b]||{};for(var V in c.properties)V&&":"==
V[u](0)&&(google[this.b][V[E](1)]=c.properties[V]);google[D].d("script",google[D][x]+c.path+c.js,e);c.css&&google[D].d("css",google[D][x]+c.path+c.css,e)}else(!b||!b.autoloaded)&&google[D].d("script",this.g(a,b),e);this.j&&(this.j=l,this.c=(new Date)[z](),1!=this.c%100&&(this.c=-1));for(r=0;r<k[A];r++)v=k[r],this.e[":"+v]=g}});
U[B].l=function(a){-1!=this.c&&(fa("al_"+this.b,"jl."+((new Date)[z]()-this.c),g),this.c=-1);this.o=this.o.concat(a.components);google[D][this.b]||(google[D][this.b]={});google[D][this.b].packages=this.o.slice(0);for(var b=0;b<a.components[A];b++){this.n[":"+a.components[b]]=g;this.e[":"+a.components[b]]=l;var c=this.f[":"+a.components[b]];if(c){for(var e=0;e<c[A];e++)c[e].C(a.components[b]);delete this.f[":"+a.components[b]]}}};U[B].m=function(a,b){return 0==this.t(b)[A]};U[B].s=function(){return g};
function X(a){this.F=a;this.q={};this.r=0}X[B].B=function(a){this.r++;this.q[":"+a]=g};X[B].C=function(a){this.q[":"+a]&&(this.q[":"+a]=l,this.r--,0==this.r&&n[C](this.F,0))};function W(a,b,c){this.name=a;this.D=b;this.p=c;this.u=this.h=l;this.k=[];google[D].v[this[y]]=aa(this.l,this)}J(W,U);q(W[B],function(a,b){var c=b&&b.callback!=h;c?(this.k[s](b.callback),b.callback="google.loader.callbacks."+this[y]):this.h=g;(!b||!b.autoloaded)&&google[D].d("script",this.g(a,b),c)});W[B].m=function(a,b){return b&&b.callback!=h?this.u:this.h};W[B].l=function(){this.u=g;for(var a=0;a<this.k[A];a++)n[C](this.k[a],0);this.k=[]};
var Y=function(a,b){return a.string?m(a.string)+"="+m(b):a.regex?b[t](/(^.*$)/,a.regex):""};W[B].g=function(a,b){return this.G(this.w(a),a,b)};
W[B].G=function(a,b,c){var e="";a.key&&(e+="&"+Y(a.key,google[D].ApiKey));a.version&&(e+="&"+Y(a.version,b));b=google[D].Secure&&a.ssl?a.ssl:a.uri;if(c!=h)for(var f in c)a.params[f]?e+="&"+Y(a.params[f],c[f]):"other_params"==f?e+="&"+c[f]:"base_domain"==f&&(b="http://"+c[f]+a.uri[E](a.uri[w]("/",7)));google[this[y]]={};-1==b[w]("?")&&e&&(e="?"+e[E](1));return b+e};W[B].s=function(a){return this.w(a).deferred};W[B].w=function(a){if(this.p)for(var b=0;b<this.p[A];++b){var c=this.p[b];if(RegExp(c.pattern).test(a))return c}return this.D};function T(a,b){this.b=a;this.i=b;this.h=l}J(T,U);q(T[B],function(a,b){this.h=g;google[D].d("script",this.g(a,b),l)});T[B].m=function(){return this.h};T[B].l=function(){};T[B].g=function(a,b){if(!this.i.versions[":"+a]){if(this.i.aliases){var c=this.i.aliases[":"+a];c&&(a=c)}if(!this.i.versions[":"+a])throw K("Module: '"+this.b+"' with version '"+a+"' not found!");}return google[D].GoogleApisBase+"/libs/"+this.b+"/"+a+"/"+this.i.versions[":"+a][b&&b.uncompressed?"uncompressed":"compressed"]};
T[B].s=function(){return l};var ga=l,Z=[],ha=(new Date)[z](),ja=function(){ga||(R(n,"unload",ia),ga=g)},ka=function(a,b){ja();if(!google[D].Secure&&(!google[D].Options||google[D].Options.csi===l)){for(var c=0;c<a[A];c++)a[c]=m(a[c][G]()[t](/[^a-z0-9_.]+/g,"_"));for(c=0;c<b[A];c++)b[c]=m(b[c][G]()[t](/[^a-z0-9_.]+/g,"_"));n[C](aa($,h,"//gg.google.com/csi?s=uds&v=2&action="+a[F](",")+"&it="+b[F](",")),1E4)}},fa=function(a,b,c){c?ka([a],[b]):(ja(),Z[s]("r"+Z[A]+"="+m(a+(b?"|"+b:""))),n[C](ia,5<Z[A]?0:15E3))},ia=function(){if(Z[A]){var a=
google[D][x];0==a[w]("http:")&&(a=a[t](/^http:/,"https:"));$(a+"/stats?"+Z[F]("&")+"&nc="+(new Date)[z]()+"_"+((new Date)[z]()-ha));Z.length=0}},$=function(a){var b=new Image,c=$.H++;$.A[c]=b;b.onload=b.onerror=function(){delete $.A[c]};b.src=a;b=h};$.A={};$.H=0;L("google.loader.recordCsiStat",ka);L("google.loader.recordStat",fa);L("google.loader.createImageForLogging",$);

}) ();google.loader.rm({"specs":["feeds","spreadsheets","gdata","visualization",{"name":"sharing","baseSpec":{"uri":"http://www.google.com/s2/sharing/js","ssl":null,"key":{"string":"key"},"version":{"string":"v"},"deferred":false,"params":{"language":{"string":"hl"}}}},"search","orkut","ads","elements",{"name":"books","baseSpec":{"uri":"http://books.google.com/books/api.js","ssl":"https://encrypted.google.com/books/api.js","key":{"string":"key"},"version":{"string":"v"},"deferred":true,"params":{"callback":{"string":"callback"},"language":{"string":"hl"}}}},{"name":"friendconnect","baseSpec":{"uri":"http://www.google.com/friendconnect/script/friendconnect.js","ssl":null,"key":{"string":"key"},"version":{"string":"v"},"deferred":false,"params":{}}},"identitytoolkit","ima",{"name":"maps","baseSpec":{"uri":"http://maps.google.com/maps?file\u003dgoogleapi","ssl":"https://maps-api-ssl.google.com/maps?file\u003dgoogleapi","key":{"string":"key"},"version":{"string":"v"},"deferred":true,"params":{"callback":{"regex":"callback\u003d$1\u0026async\u003d2"},"language":{"string":"hl"}}},"customSpecs":[{"uri":"http://maps.googleapis.com/maps/api/js","ssl":"https://maps.googleapis.com/maps/api/js","version":{"string":"v"},"deferred":true,"params":{"callback":{"string":"callback"},"language":{"string":"hl"}},"pattern":"^(3|3..*)$"}]},"payments","wave","annotations_v2","earth","language",{"name":"annotations","baseSpec":{"uri":"http://www.google.com/reviews/scripts/annotations_bootstrap.js","ssl":null,"key":{"string":"key"},"version":{"string":"v"},"deferred":true,"params":{"callback":{"string":"callback"},"language":{"string":"hl"},"country":{"string":"gl"}}}},"picker"]});
google.loader.rfm({":search":{"versions":{":1":"1",":1.0":"1"},"path":"/api/search/1.0/dafe20cc2afc0dcfa10b802f251c72d0/","js":"default+en.I.js","css":"default+en.css","properties":{":JSHash":"dafe20cc2afc0dcfa10b802f251c72d0",":NoOldNames":false,":Version":"1.0"}},":language":{"versions":{":1":"1",":1.0":"1"},"path":"/api/language/1.0/f7a156df16b25154ba5d46841b009d9d/","js":"default+en.I.js","properties":{":JSHash":"f7a156df16b25154ba5d46841b009d9d",":Version":"1.0"}},":feeds":{"versions":{":1":"1",":1.0":"1"},"path":"/api/feeds/1.0/77f89919ef841f93359ce886504e4e3f/","js":"default+en.I.js","css":"default+en.css","properties":{":JSHash":"77f89919ef841f93359ce886504e4e3f",":Version":"1.0"}},":spreadsheets":{"versions":{":0":"1",":0.4":"1"},"path":"/api/spreadsheets/0.4/87ff7219e9f8a8164006cbf28d5e911a/","js":"default.I.js","properties":{":JSHash":"87ff7219e9f8a8164006cbf28d5e911a",":Version":"0.4"}},":ima":{"versions":{":3":"1",":3.0":"1"},"path":"/api/ima/3.0/28a914332232c9a8ac0ae8da68b1006e/","js":"default.I.js","properties":{":JSHash":"28a914332232c9a8ac0ae8da68b1006e",":Version":"3.0"}},":wave":{"versions":{":1":"1",":1.0":"1"},"path":"/api/wave/1.0/3b6f7573ff78da6602dda5e09c9025bf/","js":"default.I.js","properties":{":JSHash":"3b6f7573ff78da6602dda5e09c9025bf",":Version":"1.0"}},":earth":{"versions":{":1":"1",":1.0":"1"},"path":"/api/earth/1.0/109c7b2bae7fe6cc34ea875176165d81/","js":"default.I.js","properties":{":JSHash":"109c7b2bae7fe6cc34ea875176165d81",":Version":"1.0"}},":annotations":{"versions":{":1":"1",":1.0":"1"},"path":"/api/annotations/1.0/632d801f04d14d064b3a2e4290697a29/","js":"default+en.I.js","properties":{":JSHash":"632d801f04d14d064b3a2e4290697a29",":Version":"1.0"}},":picker":{"versions":{":1":"1",":1.0":"1"},"path":"/api/picker/1.0/8b07f3bbcff2f7432e52154f72066e3e/","js":"default.I.js","css":"default.css","properties":{":JSHash":"8b07f3bbcff2f7432e52154f72066e3e",":Version":"1.0"}}});
google.loader.rpl({":scriptaculous":{"versions":{":1.8.3":{"uncompressed":"scriptaculous.js","compressed":"scriptaculous.js"},":1.9.0":{"uncompressed":"scriptaculous.js","compressed":"scriptaculous.js"},":1.8.2":{"uncompressed":"scriptaculous.js","compressed":"scriptaculous.js"},":1.8.1":{"uncompressed":"scriptaculous.js","compressed":"scriptaculous.js"}},"aliases":{":1.8":"1.8.3",":1":"1.9.0",":1.9":"1.9.0"}},":yui":{"versions":{":2.6.0":{"uncompressed":"build/yuiloader/yuiloader.js","compressed":"build/yuiloader/yuiloader-min.js"},":2.9.0":{"uncompressed":"build/yuiloader/yuiloader.js","compressed":"build/yuiloader/yuiloader-min.js"},":2.7.0":{"uncompressed":"build/yuiloader/yuiloader.js","compressed":"build/yuiloader/yuiloader-min.js"},":2.8.0r4":{"uncompressed":"build/yuiloader/yuiloader.js","compressed":"build/yuiloader/yuiloader-min.js"},":2.8.2r1":{"uncompressed":"build/yuiloader/yuiloader.js","compressed":"build/yuiloader/yuiloader-min.js"},":2.8.1":{"uncompressed":"build/yuiloader/yuiloader.js","compressed":"build/yuiloader/yuiloader-min.js"},":3.3.0":{"uncompressed":"build/yui/yui.js","compressed":"build/yui/yui-min.js"}},"aliases":{":3":"3.3.0",":2":"2.9.0",":2.7":"2.7.0",":2.8.2":"2.8.2r1",":2.6":"2.6.0",":2.9":"2.9.0",":2.8":"2.8.2r1",":2.8.0":"2.8.0r4",":3.3":"3.3.0"}},":swfobject":{"versions":{":2.1":{"uncompressed":"swfobject_src.js","compressed":"swfobject.js"},":2.2":{"uncompressed":"swfobject_src.js","compressed":"swfobject.js"}},"aliases":{":2":"2.2"}},":ext-core":{"versions":{":3.1.0":{"uncompressed":"ext-core-debug.js","compressed":"ext-core.js"},":3.0.0":{"uncompressed":"ext-core-debug.js","compressed":"ext-core.js"}},"aliases":{":3":"3.1.0",":3.0":"3.0.0",":3.1":"3.1.0"}},":webfont":{"versions":{":1.0.28":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.27":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.29":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.12":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.13":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.14":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.15":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.10":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.11":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.2":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.1":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.0":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.6":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.19":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.5":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.18":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.4":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.17":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.3":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.16":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.9":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.21":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.22":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.25":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.26":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.23":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"},":1.0.24":{"uncompressed":"webfont_debug.js","compressed":"webfont.js"}},"aliases":{":1":"1.0.29",":1.0":"1.0.29"}},":mootools":{"versions":{":1.3.1":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.1.1":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.3.0":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.3.2":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.1.2":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.2.3":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.2.4":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.2.1":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.2.2":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.2.5":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.4.0":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.4.1":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"},":1.4.2":{"uncompressed":"mootools.js","compressed":"mootools-yui-compressed.js"}},"aliases":{":1":"1.1.2",":1.11":"1.1.1",":1.4":"1.4.2",":1.3":"1.3.2",":1.2":"1.2.5",":1.1":"1.1.2"}},":jqueryui":{"versions":{":1.8.0":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.2":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.1":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.15":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.14":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.13":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.12":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.11":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.10":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.17":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.16":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.6.0":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.9":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.7":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.8":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.7.2":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.5":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.7.3":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.6":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.7.0":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.7.1":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.8.4":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.5.3":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"},":1.5.2":{"uncompressed":"jquery-ui.js","compressed":"jquery-ui.min.js"}},"aliases":{":1.8":"1.8.17",":1.7":"1.7.3",":1.6":"1.6.0",":1":"1.8.17",":1.5":"1.5.3",":1.8.3":"1.8.4"}},":chrome-frame":{"versions":{":1.0.2":{"uncompressed":"CFInstall.js","compressed":"CFInstall.min.js"},":1.0.1":{"uncompressed":"CFInstall.js","compressed":"CFInstall.min.js"},":1.0.0":{"uncompressed":"CFInstall.js","compressed":"CFInstall.min.js"}},"aliases":{":1":"1.0.2",":1.0":"1.0.2"}},":prototype":{"versions":{":1.7.0.0":{"uncompressed":"prototype.js","compressed":"prototype.js"},":1.6.0.2":{"uncompressed":"prototype.js","compressed":"prototype.js"},":1.6.1.0":{"uncompressed":"prototype.js","compressed":"prototype.js"},":1.6.0.3":{"uncompressed":"prototype.js","compressed":"prototype.js"}},"aliases":{":1.7":"1.7.0.0",":1.6.1":"1.6.1.0",":1":"1.7.0.0",":1.6":"1.6.1.0",":1.7.0":"1.7.0.0",":1.6.0":"1.6.0.3"}},":dojo":{"versions":{":1.3.1":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.3.0":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.6.1":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.1.1":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.3.2":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.6.0":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.2.3":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.7.2":{"uncompressed":"dojo/dojo.js.uncompressed.js","compressed":"dojo/dojo.js"},":1.7.0":{"uncompressed":"dojo/dojo.js.uncompressed.js","compressed":"dojo/dojo.js"},":1.7.1":{"uncompressed":"dojo/dojo.js.uncompressed.js","compressed":"dojo/dojo.js"},":1.4.3":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.5.1":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.5.0":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.2.0":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.4.0":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"},":1.4.1":{"uncompressed":"dojo/dojo.xd.js.uncompressed.js","compressed":"dojo/dojo.xd.js"}},"aliases":{":1.7":"1.7.2",":1":"1.6.1",":1.6":"1.6.1",":1.5":"1.5.1",":1.4":"1.4.3",":1.3":"1.3.2",":1.2":"1.2.3",":1.1":"1.1.1"}},":jquery":{"versions":{":1.6.2":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.3.1":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.6.1":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.3.0":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.6.4":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.6.3":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.3.2":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.6.0":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.2.3":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.7.0":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.7.1":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.2.6":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.4.3":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.4.4":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.5.1":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.5.0":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.4.0":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.5.2":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.4.1":{"uncompressed":"jquery.js","compressed":"jquery.min.js"},":1.4.2":{"uncompressed":"jquery.js","compressed":"jquery.min.js"}},"aliases":{":1.7":"1.7.1",":1.6":"1.6.4",":1":"1.7.1",":1.5":"1.5.2",":1.4":"1.4.4",":1.3":"1.3.2",":1.2":"1.2.6"}}});
}
;
/*! @source http://purl.eligrey.com/github/FileSaver.js/blob/master/FileSaver.js */
var saveAs=saveAs||navigator.msSaveBlob&&navigator.msSaveBlob.bind(navigator)||function(a){"use strict";var b=a.document,c=function(){return a.URL||a.webkitURL||a},d=a.URL||a.webkitURL||a,e=b.createElementNS("http://www.w3.org/1999/xhtml","a"),f="download"in e,g=function(c){var d=b.createEvent("MouseEvents");return d.initMouseEvent("click",!0,!1,a,0,0,0,0,0,!1,!1,!1,!1,0,null),c.dispatchEvent(d)},h=a.webkitRequestFileSystem,i=a.requestFileSystem||h||a.mozRequestFileSystem,j=function(b){(a.setImmediate||a.setTimeout)(function(){throw b},0)},k="application/octet-stream",l=0,m=[],n=function(){for(var a=m.length;a--;){var b=m[a];"string"==typeof b?d.revokeObjectURL(b):b.remove()}m.length=0},o=function(a,b,c){b=[].concat(b);for(var d=b.length;d--;){var e=a["on"+b[d]];if("function"==typeof e)try{e.call(a,c||a)}catch(f){j(f)}}},p=function(b,d){var q,r,x,j=this,n=b.type,p=!1,s=function(){var a=c().createObjectURL(b);return m.push(a),a},t=function(){o(j,"writestart progress write writeend".split(" "))},u=function(){(p||!q)&&(q=s(b)),r&&(r.location.href=q),j.readyState=j.DONE,t()},v=function(a){return function(){return j.readyState!==j.DONE?a.apply(this,arguments):void 0}},w={create:!0,exclusive:!1};return j.readyState=j.INIT,d||(d="download"),f&&(q=s(b),e.href=q,e.download=d,g(e))?(j.readyState=j.DONE,t(),void 0):(a.chrome&&n&&n!==k&&(x=b.slice||b.webkitSlice,b=x.call(b,0,b.size,k),p=!0),h&&"download"!==d&&(d+=".download"),r=n===k||h?a:a.open(),i?(l+=b.size,i(a.TEMPORARY,l,v(function(a){a.root.getDirectory("saved",w,v(function(a){var c=function(){a.getFile(d,w,v(function(a){a.createWriter(v(function(c){c.onwriteend=function(b){r.location.href=a.toURL(),m.push(a),j.readyState=j.DONE,o(j,"writeend",b)},c.onerror=function(){var a=c.error;a.code!==a.ABORT_ERR&&u()},"writestart progress write abort".split(" ").forEach(function(a){c["on"+a]=j["on"+a]}),c.write(b),j.abort=function(){c.abort(),j.readyState=j.DONE},j.readyState=j.WRITING}),u)}),u)};a.getFile(d,{create:!1},v(function(a){a.remove(),c()}),v(function(a){a.code===a.NOT_FOUND_ERR?c():u()}))}),u)}),u),void 0):(u(),void 0))},q=p.prototype,r=function(a,b){return new p(a,b)};return q.abort=function(){var a=this;a.readyState=a.DONE,o(a,"abort")},q.readyState=q.INIT=0,q.WRITING=1,q.DONE=2,q.error=q.onwritestart=q.onprogress=q.onwrite=q.onabort=q.onerror=q.onwriteend=null,a.addEventListener("unload",n,!1),r}(self);
;
// Peity jQuery plugin version 1.2.0
// (c) 2013 Ben Pickles
//
// http://benpickles.github.com/peity
//
// Released under MIT license.
(function(h,j,k,m){var r=j.createElement("canvas").getContext,i=h.fn.peity=function(a,b){r&&this.each(function(){var d=h(this),c=d.data("peity");if(c)a&&(c.type=a),h.extend(c.opts,b),c.draw();else{var f=i.defaults[a],e={};h.each(d.data(),function(a,b){a in f&&(e[a]=b)});var l=h.extend({},f,e,b),c=new q(d,a,l);c.draw();d.change(function(){c.draw()}).data("peity",c)}});return this},q=function(a,b,d){this.$el=a;this.type=b;this.opts=d},j=q.prototype;j.colours=function(){var a=this.opts.colours,b=a;h.isFunction(b)||
(b=function(b,c){return a[c%a.length]});return b};j.draw=function(){i.graphers[this.type].call(this,this.opts)};j.prepareCanvas=function(a,b){var d=this.canvas,c;d?(this.context.clearRect(0,0,d.width,d.height),c=h(d)):(c=h("<canvas>").css({height:b,width:a}).addClass("peity").data("peity",this),this.canvas=d=c[0],this.context=d.getContext("2d"),this.$el.hide().after(d));d.height=c.height()*m;d.width=c.width()*m;return d};j.values=function(){return h.map(this.$el.text().split(this.opts.delimiter),
function(a){return parseFloat(a)})};i.defaults={};i.graphers={};i.register=function(a,b,d){this.defaults[a]=b;this.graphers[a]=d};i.register("pie",{colours:["#ff9900","#fff4dd","#ffc66e"],delimiter:null,diameter:16},function(a){if(!a.delimiter){var b=this.$el.text().match(/[^0-9\.]/);a.delimiter=b?b[0]:","}b=this.values();if("/"==a.delimiter)var d=b[0],b=[d,b[1]-d];for(var c=0,d=b.length,f=0;c<d;c++)f+=b[c];var e=this.prepareCanvas(a.width||a.diameter,a.height||a.diameter),a=this.context,c=e.width,
l=e.height,e=k.min(c,l)/2,h=k.PI,n=this.colours();a.save();a.translate(c/2,l/2);a.rotate(-h/2);for(c=0;c<d;c++){var l=b[c],g=2*l/f*h;a.beginPath();a.moveTo(0,0);a.arc(0,0,e,0,g,!1);a.fillStyle=n.call(this,l,c,b);a.fill();a.rotate(g)}a.restore()});i.register("line",{colour:"#c6d9fd",strokeColour:"#4d89f9",strokeWidth:1,delimiter:",",height:16,max:null,min:0,width:32},function(a){var b=this.values();1==b.length&&b.push(b[0]);var d=k.max.apply(k,b.concat([a.max])),c=k.min.apply(k,b.concat([a.min])),
f=this.prepareCanvas(a.width,a.height),e=this.context,l=f.width,f=f.height,h=l/(b.length-1),d=f/(d-c),n=[],g;e.beginPath();e.moveTo(0,f+c*d);for(g=0;g<b.length;g++){var i=g*h,j=f-d*(b[g]-c);n.push({x:i,y:j});e.lineTo(i,j)}e.lineTo(l,f+c*d);e.fillStyle=a.colour;e.fill();if(a.strokeWidth){e.beginPath();e.moveTo(0,n[0].y);for(g=0;g<n.length;g++)e.lineTo(n[g].x,n[g].y);e.lineWidth=a.strokeWidth*m;e.strokeStyle=a.strokeColour;e.stroke()}});i.register("bar",{colours:["#4D89F9"],delimiter:",",height:16,
max:null,min:0,spacing:m,width:32},function(a){for(var b=this.values(),d=k.max.apply(k,b.concat([a.max])),c=k.min.apply(k,b.concat([a.min])),f=this.prepareCanvas(a.width,a.height),e=this.context,h=f.height,i=h/(d-c),a=a.spacing,f=(f.width+a)/b.length,j=this.colours(),g=0;g<b.length;g++){var m=b[g],o=h-i*(m-c),p;if(0==m){if(0<=c||0<d)o-=1;p=1}else p=i*b[g];e.fillStyle=j.call(this,m,g,b);e.fillRect(g*f,o,f-a,p)}})})(jQuery,document,Math,window.devicePixelRatio||1);
;
function encode_id(data) {
    return base64.encode(data).replace(/\+/g , '-').replace(/\//g , '_');
}

function decode_id(data) {
    return base64.decode(data.replace(/\-/g , '+').replace(/\_/g , '/'));
}

function PicarusClient(args) {
    this.version = 'v0';

    this.setAuth = function (email, key) {
        $.ajaxSetup({'beforeSend': function (xhr) {
            xhr.setRequestHeader("Authorization", "Basic " + base64.encode(email + ":" + key));
        }});
    };

    if (_.isUndefined(args) || _.isUndefined(args.server))
        this.server = '';
    else
        this.server = args.server;

    if (!(_.isUndefined(args) || _.isUndefined(args.email) || _.isUndefined(args.apiKey)))
        this.setAuth(args.email, args.apiKey);

    this.get = function (path, data, success, fail) {
        path = [this.server, this.version].concat(_.map(path, encodeURIComponent)).join('/');
        return $.ajax(path, {data: data, success: success}).fail(fail);
    };

    this._ajax = function (path, data, success, fail, type) {
        path = [this.server, this.version].concat(_.map(path, encodeURIComponent)).join('/');
        var formData = new FormData();
        _.each(data, function (v, k) {
            formData.append(k, v);
        });
        return $.ajax(path, {type: type, data: formData, success: success, contentType: false, processData: false}).fail(fail);
    };
    
    this.post = function (path, data, success, fail) {
        return this._ajax(path, data, success, fail, 'POST');
    };

    this.patch = function (path, data, success, fail) {
        return this._ajax(path, data, success, fail, 'PATCH');
    };

    this.del = function (path, data, success, fail) {
        return this._ajax(path, data, success, fail, 'DELETE');
    };

    this.authEmailAPIKey = function (args) {
        args = this._argsDefaults(args);
        return this.post(["auth", "email"], {}, this._wrapNull(args.success), args.fail);
    };

    this.authYubikey = function (otp, args) {
        args = this._argsDefaults(args);
        return this.post(["auth", "yubikey"], {otp: otp}, this._wrapParseJSON(args.success), args.fail);
    };

    this.getTable = function (table, args) {
        //args: success, fail, columns
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        return this.get(['data', table], args.data, this._wrapDecodeLod(args.success), args.fail);
    };
    this.postTable = function (table, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.post(['data', table], this.encdict(args.data), this._wrapDecodeValues(args.success), args.fail);
    };
    this.postRow = function (table, row, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.post(['data', table, encode_id(row)], this.encvalues(args.data), this._wrapDecodeDict(args.success), args.fail);
    };
    this.deleteRow = function (table, row, args) {
        //args: success, fail
        args = this._argsDefaults(args);
        return this.del(['data', table, encode_id(row)], args.data, this._wrapNull(args.success), args.fail);
    };
    this.deleteColumn = function (table, row, column, args) {
        //args: success, fail
        args = this._argsDefaults(args);
        return this.del(['data', table, encode_id(row), encode_id(column)], args.data, this._wrapNull(args.success), args.fail);
    };
    this.postSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.post(['slice', table, encode_id(startRow), encode_id(stopRow)], this.encvalues(args.data), this._wrapDecodeDict(args.success), args.fail);
    };

    this.patchRow = function (table, row, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.patch(['data', table, encode_id(row)], this.encdict(args.data), this._wrapDecodeValues(args.success), args.fail);
    };
    this.encdict = function (d) {
        // TODO: Add same logic as the python library for upgrading to file blobs
        return _.object(_.map(d, function (v, k) {
            if (!_.isObject(v)) // NOTE(brandyn): The reason is that files are "object" type
                v = base64.encode(v);
            return [base64.encode(k), v];
        }));
    };
    this.encvalues = function (d) {
        // TODO: Add same logic as the python library for upgrading to file blobs
        return _.object(_.map(d, function (v, k) {
            if (!_.isObject(v)) // NOTE(brandyn): The reason is that files are "object" type
                v = base64.encode(v);
            return [k, v];
        }));
    };
    this.getRow = function (table, row, args) {
        //args: success, fail, columns
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        return this.get(['data', table, encode_id(row)], args.data, this._wrapDecodeDict(args.success), args.fail);
    };
    this.getSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        return this.get(['slice', table, encode_id(startRow), encode_id(stopRow)], args.data, this._wrapDecodeLod(args.success), args.fail);
    };
    this.patchSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        return this.patch(['slice', table, encode_id(startRow), encode_id(stopRow)], this.encdict(args.data), this._wrapNull(args.success), args.fail);
    };
    this.deleteSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        return this.del(['slice', table, encode_id(startRow), encode_id(stopRow)], {}, this._wrapNull(args.success), args.fail);
    };
    this.scanner = function (table, startRow, stopRow, args) {
        // args: success, fail, done, maxRows, maxRowsIter, filter, resume
        args = this._argsDefaults(args);
        if (_.isUndefined(args.maxRows)) {
            args.maxRows = Infinity;
        }
        if (_.isUndefined(args.maxRowsIter)) {
            args.maxRowsIter = Math.min(10000, args.maxRows);
        }
        if (_.isUndefined(args.maxBytes)) {
            args.maxBytes = 1048576;
        }
        var lastRow = undefined;
        var numRows = 0;
        function innerSuccess(data) {
            debug_data = data;
            var isdone = true;
            args.maxRows -= data.length;
            if (args.maxRows < 0) {
                // Truncates any excess rows we may have gotten
                data = data.slice(0, args.maxRows);
            }
            if (numRows == 0 && data.length && !_.isUndefined(args.first)) {
                var firstRow = _.first(data);
                args.first(firstRow[0], firstRow[1]);
            }
            _.each(data, function (v) {
                lastRow = v[0];
                args.success(v[0], v[1]);
            });
            numRows += data.length;
            console.log(numRows);
            // If there is more data left to get, and we want more data
            // It's possible that this will make 1 extra call at the end that returns nothing,
            // but there are several trade-offs and that is the simplest implementation that doesn't
            // encode extra parameters, modify status codes (nonstandard), output fixed rows only, etc.
            if (data.length && args.maxRows > 0) {
                isdone = false;
                console.log('Not Done');
                function nextCall() {
                    iterArgs.data.excludeStart = 1;
                    this.getSlice(table, _.last(data)[0], stopRow, iterArgs);
                }
                nextCall = _.bind(nextCall, this);
                // This allows for pagination instead of immediately requesting the next chunk
                if (_.isUndefined(args.resume))
                    nextCall();
                else
                    args.resume(nextCall);
            }
            if (isdone && !_.isUndefined(args.done))
                args.done({lastRow: lastRow, numRows: numRows});
        }
        var iterArgs = {data: {maxRows: args.maxRowsIter}, success: _.bind(innerSuccess, this), fail: args.fail};
        if (_.has(args, 'filter'))
            iterArgs.data.filter = args.filter;
        if (_.has(args, 'columns'))
            iterArgs.columns = args.columns;
        this.getSlice(table, startRow, stopRow, iterArgs);
    };
    this._argsDefaults = function (args) {
        if (_.isUndefined(args))
            args = {};
        args = _.clone(args);
        if (!_.has(args, 'success'))
            args.success = function () {};
        if (!_.has(args, 'fail'))
            args.fail = function () {};
        if (!_.has(args, 'data'))
            args.data = {};
        return args;
    };
    this._wrapDecodeLod = function(f) {
        return function(msg, text_status, xhr) {
            f(_.map(JSON.parse(xhr.responseText), function (x) {
                var row = base64.decode(x.row);
                var columns = _.object(_.map(_.omit(x, 'row'), function (v, k) {
                    return [base64.decode(k), base64.decode(v)];
                }));
                return [row, columns];
            }));
        };
    };
    this._wrapNull = function(f) {
        return function(msg, text_status, xhr) {
            f();
        };
    };
    this._wrapDecodeDict = function(f) {
        return function(msg, text_status, xhr) {
            f(_.object(_.map(JSON.parse(xhr.responseText), function (v, k) {
                    return [base64.decode(k), base64.decode(v)];
            })));
        };
    };
    this._wrapParseJSON = function(f) {
        return function(msg, text_status, xhr) {
            f(JSON.parse(xhr.responseText));
        };
    };
    this._wrapDecodeValues = function(f) {
        return function(msg, text_status, xhr) {
            f(_.object(_.map(JSON.parse(xhr.responseText), function (v, k) {
                    return [k, base64.decode(v)];
            })));
        };
    };
    this.test = function () {
        this.getTable('parameters', {success: function (x) {console.log('Set debug_a'); debug_a=x}});
        this.getTable('models', {success: function (x) {console.log('Set debug_b'); debug_b=x}, columns: ['meta:']});
        this.getSlice('images', 'sun397:', 'sun397;', {success: function (x) {console.log('Set debug_c'); debug_c=x}, columns: ['meta:']});
        this.scanner('images', 'sun397:', 'sun397;', {columns: ['meta:'], maxRows: 10, success: function (x) {console.log('Set debug_i'); debug_i=x}})
        this.postSlice('images', 'automated_tests:', 'automated_tests;', {data: {action: 'io/thumbnail'}, success: function (x) {console.log('Set debug_g'); debug_g=x}});
        function test_patchRow(row) {
            this.patchRow('images', row, {success: function (x) {console.log('Set debug_f'); debug_f=x;test_getRow(row)}, data: {'meta:class_0': 'test_data2'}});
        }
        function test_deleteRow(row) {
            this.deleteRow('images', row, {success: function (x) {console.log('Set debug_h'); debug_h=x}});
        }
        function test_getRow(row) {
            this.getRow('images', row, {success: function (x) {console.log('Set debug_d'); debug_d=x;test_deleteRow(row)}, columns: ['meta:']});
        }
        test_getRow = _.bind(test_getRow, this);
        test_deleteRow = _.bind(test_deleteRow, this);
        test_patchRow = _.bind(test_patchRow, this);
        this.postTable('images', {success: function (x) {console.log('Set debug_e');debug_e=x;test_patchRow(x.row);}, data: {'meta:class': 'test_data'}});
        this.postRow('images', base64.decode('c3VuMzk3OnRlc3QAC2nfc3VuX2F4dndzZHd5cW1waG5hcGIuanBn'), {data: {action: 'i/chain', model: base64.decode('ZmVhdDpRhhxwtznn3dTyAfPRMSdO')}, success: function (x) {console.log('Set debug_g'); debug_g=x}});
    };
}

function prefix_to_stop_row(prefix) {
    // TODO: need to fix wrap around if last char is "255"
    return prefix.slice(0, -1) + String.fromCharCode(prefix.slice(-1).charCodeAt(0) + 1);
}

function picarus_api_delete_rows(rows, params) {
    function action(row, s) {
        PICARUS.deleteRow('images', row, {success: s})
    }
    picarus_api_row_action(rows, action, params);
}

function picarus_api_modify_rows(rows, column, value, params) {
    var data = {};
    data[column] = value;
    function action(row, s) {
        PICARUS.patchRow('images', row, {success: s, data: data})
    }
    picarus_api_row_action(rows, action, params);
}

function picarus_api_row_action(rows, action, params) {
    var maxRowsIter = 20;
    var rowsLeft = rows.length;
    var origRows = rows.length;
    if (_.isUndefined(params))
        params = {};
    if (!_.isUndefined(params.maxRowsIter))
        maxRowsIter = params.maxRowsIter;
    if (_.isUndefined(params.update))
        params.update = function () {};
    if (_.isUndefined(params.done))
        params.done = function () {};
    if (!rowsLeft)
        params.done();
    function success() {
        rowsLeft -= 1;
        params.update(1 - rowsLeft / origRows);
        if (!rowsLeft)
            params.done();
    }
    function work(s) {
        var row = rows.pop();
        if (_.isUndefined(row))
            return;
        action(row, s);
    }
    _.each(_.range(maxRowsIter), function () {
        work(function () { 
                 success();
                 while (rows.length)
                     work(success);
             });
    });
}
;
function login_get(func) {
    var otp = $('#otp');
    var apiKey = $('#apiKey');
    var modal = $('#authModal');
    var emailKeys = $('#emailKeys');
    emailKeys.click(function () {
        var email = $('#email').val();
        var loginKey = $('#loginKey').val();
        PICARUS.setAuth(email, loginKey);
        PICARUS.authEmailAPIKey();
    });
    if (typeof EMAIL_AUTH === 'undefined') {
        function get_auth() {
            function success(response) {
                PICARUS.setAuth(email, response.apiKey);
                use_api(response.apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            var otp_val = otp.val();
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            PICARUS.setAuth(email, loginKey);
            PICARUS.authYubikey(otp_val, {success: success, fail: fail});
        }
        function get_api() {
            var email = $('#email').val();
            var apiKey = $('#apiKey').val();
            function success() {
                use_api(apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            $('#secondFactorAuth').addClass('info');
            $('#secondFactorAuth').removeClass('error');
            PICARUS.setAuth(email, apiKey);
            PICARUS.getTable('prefixes', {success: success, fail: fail});
        }
        function use_api(apiKey) {
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            $('#secondFactorAuth').removeClass('error');
            // NOTE: Removed secure attribute since this
            // information isn't strictly secret (can only be used to send you an email an hour)
            // This makes using a demo http version much nicer, to add back use {secure: true} below
            $.cookie('email', email);
            $.cookie('loginKey', loginKey);
            EMAIL_AUTH = {auth: apiKey, email: email};
            $('#otp').unbind();
            $('#apiKey').unbind('keypress');
            func(EMAIL_AUTH);
            modal.modal('hide');
        }
        function enable_inputs() {
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            if (email.length && loginKey.length) {
                otp.removeAttr("disabled");
                apiKey.removeAttr("disabled");
                emailKeys.removeAttr("disabled");
            }
        }
        $('#email').val($.cookie('email'));
        $('#loginKey').val($.cookie('loginKey'));
        enable_inputs();
        $('#email').keypress(enable_inputs);
        $('#email').on('paste', function () {_.defer(enable_inputs)});
        $('#loginKey').keypress(enable_inputs);
        $('#loginKey').on('paste', function () {_.defer(enable_inputs)});
        otp.keypress(_.debounce(get_auth, 100));
        otp.on('paste', function () {_.defer(get_auth)});
        apiKey.keypress(_.debounce(get_api, 100));
        apiKey.on('paste', function () {_.defer(get_api)});
        modal.modal('show');
        modal.off('shown');
        modal.on('shown', function () {otp.focus()});
    } else {
        func(EMAIL_AUTH);
    }
}

function google_visualization_load(callback) {
    google.load("visualization", "1", {packages:["corechart"], callback: callback});
}

function add_hint(el, text) {
    el.wrap($('<span>').attr('class', 'hint hint--bottom').attr('data-hint', text));
}
function random_bytes(num) {
    return _.map(_.range(10), function () {
        return String.fromCharCode(_.random(255));
    }).join('');
}

function imageThumbnail(row, id) {
    var imageColumn = 'thum:image_150sq';
    function success(columns) {
        $('#' + id).attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', row)
    }
    PICARUS.getRow('images', row, {success: success, data: {columns: [imageColumn]}});
}

function button_confirm_click(button, fun) {
    button.unbind();
    button.click(function (data) {
        var button = $(data.target);
        button.unbind();
        button.addClass('btn-danger');
        button.click(fun);
    });
}
function button_confirm_click_reset(button) {
    button.removeClass('btn-danger');
    button.unbind();
}

function progressModal() {
    $('#progressModal').modal('show');
    function update(pct) {
        $('#progress').css('width', (100 * pct + '%'));
    }
    function done() {
        $('#progressModal').modal('hide');
    }
    return {done: done, update: update};
}

function alert_running() {
    $('#results').html('<div class="alert alert-info"><strong>Running!</strong> Job is running, please wait...</div>');
}

function alert_done() {
    $('#results').html('<div class="alert alert-success"><strong>Done!</strong> Job is done.</div>');
}

function alert_running_wrap(el) {
    return function () {
        el.html('<div class="alert alert-info"><strong>Running!</strong> Job is running, please wait...</div>');
    }
}

function alert_success_wrap(el) {
    return function () {
        el.html('<div class="alert alert-success"><strong>Done!</strong> Job is done.</div>');
    }
}

function alert_fail_wrap(el) {
    return function () {
        el.html('<div class="alert alert-error"><strong>Error!</strong> Job failed!</div>');
    }
}

function wrap_hints() {
    $('[hint]').each(function (x) {
        $(this).wrap($('<span>').attr('class', 'hint hint--bottom').attr('data-hint', $(this).attr('hint')));
    });
}

function button_running() {
    $('#runButton').button('loading');
}

function updateJobStatus($el, data, pollData) {
    if (!$.contains(document.documentElement, $el[0]))
        return;
    var goodRows = 0;
    var badRows = 0;
    var status = '';
    if (_.has(pollData, 'goodRows'))
        goodRows = Number(pollData.goodRows);
    if (_.has(pollData, 'badRows'))
        badRows = Number(pollData.badRows);
    if (_.has(pollData, 'status'))
        status = pollData.status;
    $el.html('');
    if (goodRows + badRows) {
        var pie = $('<span>', {'data-diameter': '60', 'class': 'pie', 'data-colours': '["green", "red"]'}).text(goodRows + ',' + badRows);
        $el.append(pie);
        pie.peity("pie");
        $el.append('Good[' + goodRows + '] Bad[' + badRows + '] Status[' + _.escape(status) + '] Row[' + _.escape(data.row) + ']');
    }
    if (pollData.status == 'completed' || pollData.status == 'failed')
        return;
}

function watchJob(options, data) {
    function pollJobsStatus() {
        PICARUS.getRow(data.table, data.row, {success: function (pollData) {
            JOBS.add(_.extend(pollData, {row: data.row}), {merge: true});
            if (!_.isUndefined(options.success))
                options.success(data, pollData);
            if (pollData.status != 'completed' && pollData.status != 'failed')
                _.delay(pollJobsStatus, 1000);
            if (pollData.status == 'completed' && !_.isUndefined(options.done))
                options.done();
        }, fail: function () {
            console.log('Poll Failed');
        }});
    }
    pollJobsStatus();
}

function button_reset() {
    $('#runButton').button('reset');
}

function button_error() {
    $('#runButton').button('error');
}

function model_dropdown(args) {
    var columns_model = ['meta:'];
    if (typeof args.change === 'undefined') {
        args.change = function () {};
    }
    var AppView = Backbone.View.extend({
        el: $('#container'),
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        renderDrop: args.change,
        modelFilter: args.modelFilter,
        events: {'change': 'renderDrop'},
        render: function() {
            n = this.$el;
            this.$el.empty();
            var select_template = "{{#models}}<option value='{{row}}'>{{{text}}}</option>{{/models}};" // text is escaped already
            var models_filt = _.map(MODELS.filter(this.modelFilter), function (data) {return {row: encode_id(data.get('row')), text: data.escape('meta:tags') + ' ' + data.escape('meta:name')}});
            models_filt.sort(function (x, y) {return Number(x.text > y.text) - Number(x.text < y.text)});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: MODELS, el: args.el});
    return MODELS;
}

function rows_dropdown(rows, args) {
    if (_.isUndefined(args.change)) {
        args.change = function () {};
    }
    if (_.isUndefined(args.filter)) {
        args.filter = function () {return true};
    }
    if (_.isUndefined(args.text)) {
        args.text = function (x) {return x.escape('row')};
    }
    var AppView = Backbone.View.extend({
        el: $('#container'),
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change': 'renderDrop'},
        renderDrop: args.change,
        render: function() {
            n = this.$el;
            this.$el.empty();
            var select_template = "{{#models}}<option value='{{row}}'>{{text}}</option>{{/models}};"
            var models_filt = _.map(rows.filter(args.filter), function (data) {return {row: encode_id(data.get('row')), text: args.text(data)}});
            models_filt.sort(function (x, y) {return Number(x.text > y.text) - Number(x.text < y.text)});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: rows, el: args.el});
}

function project_selector() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.$projects = $('#globalProjectDrop');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change': 'renderDrop'},
        renderDrop: function() {
            this.$projects.empty();
            var projects = this.collection.get(this.$el.val());
            if (_.isUndefined(projects))
                return;
            projects = [''].concat(_.keys(_.omit(projects.attributes, 'row')));
            var select_template = "{{#projects}}<option value='{{.}}'>{{.}}</option>{{/projects}};";
            this.$projects.append(Mustache.render(select_template, {projects: projects}));
            this.$projects.trigger('change');
        },
        render: function() {
            this.$el.empty();
            var tables = this.collection.pluck('row');
            if (!tables.length)
                return;
            var select_template = "{{#tables}}<option value='{{.}}'>{{.}}</option>{{/tables}};"
            this.$el.append(Mustache.render(select_template, {tables: tables}));
            this.$el.trigger('change');
            this.renderDrop();
        }
    });
    new AppView({collection: PROJECTS, el: $('#globalDataTableDrop')});
}

function row_selector(prefixDrop, args) {
    if (_.isUndefined(args))
        args = {};
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.$tables = $('#globalDataTableDrop');
            this.$projects = $('#globalProjectDrop');
            this.$tables.change(this.render);  // TODO: Hack
            this.$projects.change(this.render);
            this.postRender = function () {};
            if (!_.isUndefined(args.postRender))
                this.postRender = args.postRender;
            this.render();
        },
        events: {'change': 'renderDrop'},
        renderDrop: function () {
            var prefix = prefixDrop.children().filter('option:selected').val();
            if (typeof args.startRow !== 'undefined')
                args.startRow.val(prefix);
            // TODO: Assumes that prefix is not empty and that the last character is not 0xff (it would overflow)
            if (typeof args.stopRow !== 'undefined')
                args.stopRow.val(prefix_to_stop_row(prefix));
        },
        render: function() {
            this.$el.empty();
            // TODO: Check permissions and accept perissions as argument
            var project = this.$projects.val();
            prefixes = this.collection.get(this.$tables.val());
            projects = PROJECTS.get(this.$tables.val());
            if (_.isUndefined(prefixes))
                return;
            var prefixes = _.keys(_.omit(prefixes.attributes, 'row'));
            if (!_.isUndefined(project) && project !== '') {
                var table_project = PROJECTS.get(this.$tables.val()).get(project);
                var table_prefixes = _.map(table_project.split(','), function (x) {
                    return base64.decode(x);
                });
                prefixes = _.intersection(prefixes, table_prefixes);
            }
            prefixes.sort(function (x, y) {return Number(x > y) - Number(x < y)});
            var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
            this.$el.append(Mustache.render(select_template, {prefixes: prefixes}));
            this.postRender();
            this.renderDrop();
        }
    });
    new AppView({collection: PREFIXES, el: prefixDrop});
}

function slices_selector() {
    var prefixDrop = $('#slicesSelectorPrefixDrop'), startRow = $('#slicesSelectorStartRow'), stopRow = $('#slicesSelectorStopRow');
    var addButton = $('#slicesSelectorAddButton'), clearButton = $('#slicesSelectorClearButton'), slicesText = $('#slicesSelectorSlices');
    function clear() {
        slicesText.html('');
    }
    if (!prefixDrop.size())  // Skip if not visible
        return;
    row_selector(prefixDrop, {startRow: startRow, stopRow: stopRow, postRender: clear});
    addButton.click(function () {
        slicesText.append($('<option>').text(_.escape(startRow.val()) + '/' + _.escape(stopRow.val())).attr('value', base64.encode(unescape(startRow.val())) + ',' + base64.encode(unescape(stopRow.val()))));
    });
    clearButton.click(clear);
}

function model_create_selector($slicesSelect, $params, modelKind, name, hideInputs) {
    model = PARAMETERS.filter(function (x) {
        if (x.escape('kind') == modelKind && x.escape('name') == name)
            return true;
    })[0];
    if (_.isUndefined(model))
        return;
    function add_param_selections(params, param_prefix) {
        _.each(params, function (value, key) {
            var cur_el;
            if (value.type == 'enum') {
                var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
                cur_el = $('<select>').attr('name', param_prefix + key).html(Mustache.render(select_template, {models: value.values}));
            } else if (value.type == 'int') {
                // TODO: Client-side data validation
                cur_el = $('<input>').attr('name', param_prefix + key).attr('type', 'text').addClass('input-medium');
            } else if (value.type == 'float') {
                // TODO: Client-side data validation
                cur_el = $('<input>').attr('name', param_prefix + key).attr('type', 'text').addClass('input-medium');
            } else if (value.type == 'int_list') {
                // Create as many input boxes as the min # of boxes
                cur_el = $('<input>').attr('type', 'text').addClass('input-medium').val(value.min_size);
                var box_func = function () {
                    $("[name^=" + param_prefix + key +  "]").remove();
                    _.each(_.range(Number(cur_el.val())), function (x) {
                        var cur_el_num = $('<input>').attr('name', param_prefix + key + ':' + x).attr('type', 'text').addClass('input-mini');
                        $params.append(cur_el_num);
                        add_hint(cur_el_num, key + ':' + x);
                    });
                }
                box_func();
                cur_el.change(box_func);
            } else if (value.type == 'str') {
                // TODO: Client-side data validation
                cur_el = $('<input>').attr('name', param_prefix + key).attr('type', 'text').addClass('input-medium');
            }
            if (typeof cur_el !== 'undefined') {
                $params.append(cur_el);
                add_hint(cur_el, key);
            }
        });
    }
    add_param_selections(JSON.parse(model.get('params')), 'param-');
    if (model.escape('data') === 'slices') {
        if (!hideInputs) {
            $slicesSelect.append(document.getElementById('bpl_slices_select').innerHTML);
            slices_selector();
        }
    }
    if (!hideInputs) {
        var inputs;
        if (model.escape('type') == 'model')
            inputs = [model.escape('input_type')];
        else
            inputs = JSON.parse(model.get('input_types'));
        _.each(inputs, function (value) {
            var cur_el;
            var cur_id = _.uniqueId('model_select_');          
            if (value === 'raw_image') {
                $params.append($('<input>').attr('name', 'input-' + value).attr('type', 'hidden').val('data:image'));
            } else if (value === 'meta') {
                var cur_id = _.uniqueId('model_select_');
                var el = $('<input>').attr('id', cur_id).attr('name', 'input-' +  value).attr('type', 'text').addClass('input-medium');
                $params.append(el);
                add_hint(el, 'Metadata column (e.g., meta:class)');
            } else {
                $params.append($('<select>').attr('id', cur_id).attr('name', 'input-' + value).addClass('input-medium'));
                model_dropdown({modelFilter: function (x) {return x.escape('meta:output_type') === value},
                                change: function() {},
                                el: $('#' + cur_id)});
            }
        });
    }
}

function model_create_selector_get($params) {
    return _.object($params.find(':input[name]').map(function () {
        var k = $(this).attr('name');
        var v = $(this).val();
        if (_.isUndefined(k))
            return;
        if (k.slice(0, 5) === 'input' && k != 'input-meta' && k != 'input-raw_image')
            return [[k, decode_id(v)]];
        return [[k, v]];
    }));
}

function prefixes_selector() {
    var prefixDrop = $('#slicesSelectorPrefixDrop');
    var addButton = $('#slicesSelectorAddButton'), clearButton = $('#slicesSelectorClearButton'), slicesText = $('#slicesSelectorSlices');
    function clear() {
        slicesText.html('');
    }
    if (!prefixDrop.size())  // Skip if not visible
        return;
    row_selector(prefixDrop, {postRender: clear});
    addButton.click(function () {
        slicesText.append($('<option>').text(prefixDrop.children().filter('option:selected').val()).attr('value', base64.encode(prefixDrop.children().filter('option:selected').val())));
    });
    clearButton.click(clear);
}

function slices_selector_get(split) {
    var out = _.map($('#slicesSelectorSlices').children(), function (x) {return $(x).attr('value')});
    if (split)
        return _.map(out, function (x) {
            return x.split(',');
        });
    return out;
}

function prefixes_selector_get() {
    var out = _.map($('#slicesSelectorSlices').children(), function (x) {return $(x).attr('value')});
    return out;
}

function app_main() {
    PICARUS = new PicarusClient();
    // Setup models
    function param_encode(dd) {
        return _.map(dd, function (v) {
            return v.join('=');
        }).join('&');
    }
    PicarusRow = Backbone.Model.extend({
        idAttribute: "row",
        initialize: function(attributes, options) {
            if (!_.isUndefined(options)) {
                if (_.has(options, 'table'))
                    this.table = options.table;
                if (_.isArray(options.columns))
                    this.columns = options.columns;
            }
        },
        sync: function (method, model, options) {
            opt = options;
            console.log('row:' + method);
            mod = model;
            var table = model.get_table();
            var out;
            var success = options.success;
            var params = {success: success};
            params.data = model.attributes;
            if (_.has(options, 'attrs')) {
                params.data = options.attrs;
            }
            if (method == 'read') {
                if (_.has(this, 'columns'))
                    params.columns = this.columns;
                out = PICARUS.getRow(table, model.id, params);
            } else if (method == 'delete') {
                out = PICARUS.deleteRow(table, model.id, params);
            } else if (method == 'patch') {
                out = PICARUS.patchRow(table, model.id, params);
            } else if (method == 'create') {
                out = PICARUS.postTable(table, params);
            }
            debug_out = out;
            model.trigger('request', model, out, options);
            return out;
        },
        get_table: function () {
            var table = this.table;
            if (_.isUndefined(table))
                table = this.collection.table;
            return table;
        },
        unset: function (attr, options) {
            function s() {
                return this.set(attr, void 0, _.extend({}, options, {unset: true}));
            }
            s = _.bind(s, this);
            return PICARUS.deleteColumn(this.get_table(), this.id, attr, {success: s});
        }
    });
    PicarusRows = Backbone.Collection.extend({
        model : PicarusRow,
        initialize: function(models, options) {
            this.table = options.table;
            if (_.isArray(options.columns))
                this.columns = options.columns;
        },
        sync: function (method, model, options) {
            opt = options;
            console.log('rows:' + method);
            mod = model;
            var out;
            var params = {};
            var table = this.table;
            if (_.has(options, 'attrs'))
                params.data = options.attrs;
            if (method == 'read') {
                if (_.has(this, 'columns'))
                    params.columns = this.columns;
                params.success = function (lod) {
                    options.success(_.map(lod, function (v) {v[1].row = v[0]; return v[1]}));
                };
                out = PICARUS.getTable(this.table, params);
            }
            model.trigger('request', model, out, options);
            return out;
        }
    });


    function deleteValueFunc(row, column) {
        if (column == 'row')
            return '';
        return Mustache.render('<a class="value_delete" style="padding-left: 5px" row="{{row}}" column="{{column}}">Delete</a>', {row: encode_id(row), column: encode_id(column)});
    }
    function deleteRowFunc(row) {
        return Mustache.render('<button class="btn row_delete" type="submit" row="{{row}}"">Delete</button>', {row: encode_id(row)});
    }

    RowsView = Backbone.View.extend({
        initialize: function(options) {
            _.bindAll(this, 'render', 'renderWait');
            this.collection.bind('add', this.renderWait);
            this.collection.bind('sync', this.render);
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.renderWait);
            this.collection.bind('remove', this.renderWait);
            this.collection.bind('destroy', this.renderWait);
            this.extraColumns = [];
            this.postRender = function () {};
            this.deleteValues = false;
            this.deleteRows = false;
            if (!_.isUndefined(options.postRender))
                this.postRender = options.postRender;
            if (!_.isUndefined(options.extraColumns))
                this.extraColumns = options.extraColumns;
            if (options.deleteRows) {
                this.deleteRows = true;
                function delete_row(data) {
                    var row = decode_id(data.target.getAttribute('row'));
                    this.collection.get(row).destroy({wait: true});
                }
                delete_row = _.bind(delete_row, this);
                this.postRender = _.compose(this.postRender, function () {
                    button_confirm_click($('.row_delete'), delete_row);
                });
                this.extraColumns.push({header: "Delete", getFormatted: function() { return deleteRowFunc(this.get('row'))}});
            }
            if (options.deleteValues) {
                this.deleteValues = true;
                function delete_value(data) {
                    var row = decode_id(data.target.getAttribute('row'));
                    var column = decode_id(data.target.getAttribute('column'));
                    this.collection.get(row).unset(column);
                }
                delete_value = _.bind(delete_value, this);
                this.postRender = _.compose(this.postRender, function () {
                    button_confirm_click($('.value_delete'), delete_value);
                });
            }
            if (options.columns)
                this.columns = options.columns;
            this.renderWait();
        },
        renderWait: _.debounce(function () {this.render()}, 5),
        render: function() {
            console.log('Rendering!');
            var columns = this.columns;
            if (_.isUndefined(columns))
                columns = _.uniq(_.flatten(_.map(this.collection.models, function (x) {
                    return _.keys(x.attributes);
                })));
            var deleteValueFuncLocal = function () {return ''};
            if (this.deleteValues)
                deleteValueFuncLocal = deleteValueFunc;
            var table_columns = _.map(columns, function (x) {
                if (x === 'row')
                    return {header: 'row', getFormatted: function() { return _.escape(this.get(x))}};
                outExtra = '';
                return {header: x, getFormatted: function() {
                    var val = this.get(x);
                    if (_.isUndefined(val))
                        return '';
                    return _.escape(val) + deleteValueFuncLocal(this.get('row'), x);
                }
                };
            }).concat(this.extraColumns);
            picarus_table = new Backbone.Table({
                collection: this.collection,
                columns: table_columns
            });
            if (this.collection.length) {
                this.$el.html(picarus_table.render().el);
                this.postRender();
            } else {
                this.$el.html('<div class="alert alert-info">Table Empty</div>');
            }
        }
    });

    // Based on: https://gist.github.com/2711454
    var all_view = _.map($('#tpls [id*=tpl]'), function (v) {
        return v.id.slice(4).split('_').join('/')
    });

    function capFirst(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    //This is the Backbone controller that manages the content of the app
    var Content = Backbone.View.extend({
        initialize:function(options){
            Backbone.history.on('route',function(source, path){
                this.render(path);
            }, this);
        },
        //This object defines the content for each of the routes in the application
        content: _.object(_.map(all_view, function (val) {
            var selector_id;
            var prefix = 'tpl_';
            if (val === "") {
                selector_id = "data_user"
            } else {
                selector_id = val.split('/').join('_');
            }
            return [val, _.template(document.getElementById(prefix + selector_id).innerHTML, {baseLogin: document.getElementById('bpl_login').innerHTML,
                                                                                              rowSelect: document.getElementById('bpl_row_select').innerHTML,
                                                                                              slicesSelect: document.getElementById('bpl_slices_select').innerHTML,
                                                                                              prefixesSelect: document.getElementById('bpl_prefixes_select').innerHTML,
                                                                                              filter: document.getElementById('bpl_filter').innerHTML,
                                                                                              prefixSelect: document.getElementById('bpl_prefix_select').innerHTML,
                                                                                              runButton: document.getElementById('bpl_run_button').innerHTML})];
        })),
        render:function(route){
            //Simply sets the content as appropriate
            this.$el.html(this.content[route]);
            // Post-process the DOM for Picarus specific helpers
            wrap_hints();
            // Handles post render javascript calls if available
            if (route === "")
                route = 'models/list';
            var func_name = 'render_' + route.split('/').join('_');
            if (window.hasOwnProperty(func_name))
                login_get(window[func_name]);
        }
    });
    
    //This is the Backbone controller that manages the Nav Bar
    var NavBar = Backbone.View.extend({
        initialize:function(options){
            Backbone.history.on('route',function(source, path){
                this.render(path);
            }, this);
        },
        //This is a collection of possible routes and their accompanying
        //user-friendly titles
        titles: _.object(_.map(all_view, function (val) {
            var name;
            if (val === "") {
                name = "user";
            } else {
                name = _.last(val.split('/', 2));
            }
            return [val, capFirst(name)];
        })),
        events:{
            'click a':function(source) {
                var hrefRslt = source.target.getAttribute('href');
                Backbone.history.navigate(hrefRslt, {trigger:true});
                //Cancel the regular event handling so that we won't actual change URLs
                //We are letting Backbone handle routing
                return false;
            }
        },
        //Each time the routes change, we refresh the navigation (dropdown magic by Brandyn)
        render:function(route){
            this.$el.empty();
            var template = _.template("<li class='<%=active%>'><a href='<%=url%>'><%=visible%></a></li>");
            var drop_template = _.template("<li class='dropdown' <%=active%>><a href='#' class='dropdown-toggle' data-toggle='dropdown'><%=prev_key%></a><ul class='dropdown-menu'><% _.each(vals, function(data) { %> <li class='<%=data[2]%>'><a href='#<%=data[0]%>'><%=data[1]%></a></li> <% }); %></ul></li>");
            var prev_els = [];
            var prev_key = undefined;
            var route_key = route.split('/', 2)[0]
            function flush_dropdown(el) {
                el.append(drop_template({prev_key: capFirst(prev_key), vals: prev_els, active: route_key === prev_key ? "class='active'" : ''}));
            }
            for (var key in this.titles) {
                var active = route === key ? 'active' : '';
                var key_splits = key.split('/', 2);
                var name = this.titles[key];
                if (typeof prev_key != 'undefined' && (prev_key != key_splits[0] || key_splits.length < 2)) {
                    flush_dropdown(this.$el);
                    prev_key = undefined;
                    prev_els = [];
                }
                // If a part of a dropdown, add to list, else add directly
                if (key_splits.length >= 2) {
                    prev_key = key_splits[0];
                    prev_els.push([key, name, active]);
                } else {
                    this.$el.append(template({url:'#' + key,visible:this.titles[key],active:active}));
                }
            }
            if (typeof prev_key != 'undefined') {
                flush_dropdown(this.$el);
            }
            $('.dropdown-toggle').dropdown()
        }
    });
    
    //Every time a Router is instantiated, the route is added
    //to a global Backbone.history object. Thus, this is just a
    //nice way of defining possible application states
    new (Backbone.Router.extend({
        routes: _.object(_.map(all_view, function (val) {
            return [val, val];
        }).concat([['*path', 'models/list']]))
    }));
    
    //Attach Backbone Views to existing HTML elements
    new NavBar({el:document.getElementById('nav-item-container')});
    new Content({el:document.getElementById('container')});
    
    login_get(app_main_postauth);
}

function refresh_models() {
    _.each([PROJECTS, PREFIXES, JOBS, PARAMETERS, MODELS, USAGE], function (x) {x.fetch()});
}

function app_main_postauth(email_auth) {
    PROJECTS = new PicarusRows([], {'table': 'projects'});
    PREFIXES = new PicarusRows([], {'table': 'prefixes'});
    JOBS = new PicarusRows([], {'table': 'jobs'});
    PARAMETERS = new PicarusRows([], {'table': 'parameters'});
    USAGE = new PicarusRows([], {'table': 'usage'});
    MODELS = new PicarusRows([], {'table': 'models', columns: ['meta:']});
    refresh_models();
    project_selector();
    //Start the app by setting kicking off the history behaviour.
    //We will get a routing event with the initial URL fragment
    Backbone.history.start();
    window.onbeforeunload = function() {return "Leaving Picarus..."};
}