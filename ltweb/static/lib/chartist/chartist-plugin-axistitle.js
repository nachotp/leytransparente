/* chartist-plugin-axistitle 0.0.7
 * Copyright © 2019 Alex Stanbury
 * Free to use under the WTFPL license.
 * http://www.wtfpl.net/
 */

!function(a,b){"function"==typeof define&&define.amd?define(["chartist"],function(c){return a.returnExportsGlobal=b(c)}):"object"==typeof exports?module.exports=b(require("chartist")):a["Chartist.plugins.ctAxisTitle"]=b(Chartist)}(this,function(a){return function(a){"use strict";var b={axisTitle:"",axisClass:"ct-axis-title",offset:{x:0,y:0},textAnchor:"middle",flipTitle:!1},c={axisX:b,axisY:b},d=function(a){return a instanceof Function?a():a},e=function(a){return a instanceof Function?a():a};a.plugins=a.plugins||{},a.plugins.ctAxisTitle=function(b){return b=a.extend({},c,b),function(c){c.on("created",function(c){if(!b.axisX.axisTitle&&!b.axisY.axisTitle)throw new Error("ctAxisTitle plugin - You must provide at least one axis title");if(!c.axisX&&!c.axisY)throw new Error("ctAxisTitle plugin can only be used on charts that have at least one axis");var f,g,h,i=a.normalizePadding(c.options.chartPadding);if(b.axisX.axisTitle&&c.axisX&&(f=c.axisX.axisLength/2+c.options.axisY.offset+i.left,g=i.top,"end"===c.options.axisY.position&&(f-=c.options.axisY.offset),"end"===c.options.axisX.position&&(g+=c.axisY.axisLength),h=new a.Svg("text"),h.addClass(e(b.axisX.axisClass)),h.text(d(b.axisX.axisTitle)),h.attr({x:f+b.axisX.offset.x,y:g+b.axisX.offset.y,"text-anchor":b.axisX.textAnchor}),c.svg.append(h,!0)),b.axisY.axisTitle&&c.axisY){f=0,g=c.axisY.axisLength/2+i.top,"start"===c.options.axisX.position&&(g+=c.options.axisX.offset),"end"===c.options.axisY.position&&(f=c.axisX.axisLength);var j="rotate("+(b.axisY.flipTitle?-90:90)+", "+f+", "+g+")";h=new a.Svg("text"),h.addClass(e(b.axisY.axisClass)),h.text(d(b.axisY.axisTitle)),h.attr({x:f+b.axisY.offset.x,y:g+b.axisY.offset.y,transform:j,"text-anchor":b.axisY.textAnchor}),c.svg.append(h,!0)}})}}}(a),a.plugins.ctAxisTitle});
//# sourceMappingURL=chartist-plugin-axistitle.min.js.map