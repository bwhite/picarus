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
