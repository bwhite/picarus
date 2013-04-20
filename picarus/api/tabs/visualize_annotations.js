function render_visualize_annotations() {
    google_visualization_load(render_visualize_annotations_loaded);
}

function render_visualize_annotations_loaded() {
    var rows = new Picarus2Rows([], {'table': 'annotations'});
    function collect_users(users, results, onlyWorkers, onlyAnnotated) {
        var users_filtered = {};
        users.each(function(x) {
            if (x.escape('workerId') || !onlyWorkers)
                users_filtered[x.get('row')] = [];
        });
        results.each(function (x) {
            // TODO: Fix this encoding mismatch
            var i = encode_id(x.escape('user_id'));
            if (_.has(users_filtered, i) && (!onlyAnnotated || x.escape('end_time'))) {
                users_filtered[i].push(x);
            }
        });
        _.each(users_filtered, function (x) {
            x.sort(function (a, b) {
                a = Number(a.escape('start_time'));
                b = Number(b.escape('start_time'));
                if (a < b)
                    return -1;
                if (a > b)
                    return 1;
                return 0;
            });
        });
        return users_filtered;
    }
    function accumulate(hist, vals, inc) {
        _.each(vals, function (x) {
            if (_.has(hist, x))
                hist[x] += inc;
            else
                hist[x] = inc;
        });
    }
    function score_total(scoresPos, scoresNeg, scoresTotal) {
        if (_.isUndefined(scoresTotal))
            scoresTotal = {};
        _.each(scoresPos, function (y, x) {
            if (_.has(scoresTotal, x))
                scoresTotal[x] += y;
            else
                scoresTotal[x] = y;
        });
        _.each(scoresNeg, function (y, x) {
            if (_.has(scoresTotal, x))
                scoresTotal[x] += y;
            else
                scoresTotal[x] = y;
        });
        return scoresTotal;
    }
    function image_batch_score(users, results, unused_class_name, scoreUnselected) {
        // Only count explicit marks
        scoresPos = {};
        scoresNeg = {};
        scoresTotal = {};

        pick = function (s, l) { return _.map(s, function (x) {return l[x]});}

        results.each(function (x) {
            d = x.get('user_data');
            if (_.isUndefined(d))
                return;
            d = JSON.parse(d);
            images = JSON.parse(x.get('images'));
            accumulate(scoresTotal, images, 0);  // Makes each image show up, even if not annotated
            if (d.polarity)
                accumulate(scoresPos, pick(d.selected, images), 1);
            if (scoreUnselected)
                accumulate(scoresNeg, pick(d.notSelected, images), 1);
            else
                accumulate(scoresNeg, pick(d.selected, images), 1);
            if (scoreUnselected)
                accumulate(scoresPos, pick(d.notSelected, images), 1);
        });
        _.each(scoresPos, function (y, x) {
            if (_.has(scoresTotal, x))
                scoresTotal[x] += y;
            else
                scoresTotal[x] = y;
        });
        _.each(scoresNeg, function (y, x) {
            if (_.has(scoresTotal, x))
                scoresTotal[x] += y;
            else
                scoresTotal[x] = y;
        });
        return {scoresPos: scoresPos, scoresNeg: scoresNeg, scoresTotal: score_total(scoresPos, scoresNeg, scoresTotal)};
    }
    function image_entity_score(users, results) {
        // Only count explicit marks
        var scores = {};

        results.each(function (x) {
            var annotation = JSON.parse(x.get('user_data'));
            var image = x.escape('image');
            var entity = x.escape('entity');
            if (!_.has(scores, entity)) {
                scores[entity] = {scoresPos: {}, scoresNeg: {}, scoresTotal: {}};
            }
            var scoresPos = scores[entity].scoresPos;
            var scoresNeg = scores[entity].scoresNeg;
            var scoresTotal = scores[entity].scoresTotal;
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
        /* TODO: Compute a dropdown list of available classes (new view for results model) */
        results = new Picarus2Rows([], {'table': 'annotations-results-' + task});
        users = new Picarus2Rows([], {'table': 'annotations-users-' + task});
        var imageColumn = 'thum:image_150sq';
        $('#negPct').change(data_change);
        $('#posPct').change(data_change);
        $('#posCnt').change(data_change);
        $('#negCnt').change(data_change);
        $('#unclicked').change(data_change);
        function data_change() {
            var unclicked = $('#unclicked').is(':checked')
            var classes = get_classes(results);
            var select_template = "{{#classes}}<option value='{{.}}'>{{.}}</option>{{/classes}};"
            $('#class_select').html(Mustache.render(select_template, {classes: classes}));
            $('#class_select').unbind();
            $('#class_select').change(class_select_change);
            class_scores = get_scores(users, results, unclicked);
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
            user_annotations = collect_users(users, results, true, true);
            annotation_times = {};
            _.each(user_annotations, function (z) {
                _.each(z, function(x, y) {
                    var t = Number(x.escape('end_time')) - Number(x.escape('start_time'));
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
            unclicked = $('#unclicked').is(':checked');
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
                    div.append($('<img>').attr('id', id).attr('title', 'Row: ' + x[0] + ' Score: ' + x[1]).addClass('hide'));
                    function success(response) {
                        if (_.isUndefined(response[imageColumn]))
                            return;
                        $('#' + id).attr('src', 'data:image/jpeg;base64,' + base64.encode(response[imageColumn])).attr('width', '150px').removeClass('hide');
                    }
                    PICARUS.getRow("images", decode_id(x[0]), {success: success, columns: [imageColumn]});
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
    }
    function change() {
        var task = decode_id($('#annotator_select').find(":selected").val());
        if (_.isUndefined(task)) {
            return;
        }
        function success_annotation(annotation) {
            annotation_type = JSON.parse(annotation['params']).type;
            // Code is over nested, use partial application to flatten it
            if (annotation_type == 'image_entity') {
                get_classes = function (results) {
                    return _.unique(results.map(function (x, y) {return x.escape('entity')})).sort()
                }
                get_scores = image_entity_score;
                // TODO: Add function to get scores from results given a class
            } else if (annotation_type == 'image_query_batch') {
                
            } else {
                
            }
            display_annotation_task(task, get_classes, get_scores);
        }
        // TODO: Add dropdown to select annotator to query
        // TODO: Histogram of annotation times, annotation time vs annotation iteration (scatter and median), histogram of image annotations
        // TODO: Abstract functions for getting image annotations based on annotation type
        // TODO: Filter rows and/or modify column based on annotation
        // TODO: Add voting rules for neg/pos/unsure
        // TODO: Add other annotation types
        PICARUS.getRow("annotations", task, {success: success_annotation});
    }
    rows_dropdown(rows, {el: $('#annotator_select'), text: function (x) {
        var p = JSON.parse(x.get('params'));
        if (p.type == "image_entity")
            return p.type + ' ' + p.num_tasks;
        if (p.type == "image_query_batch")
            return p.type + ' ' +  p.query + ' '+ p.num_tasks;
        return p.type;
    }, change: change});
    rows.fetch();
}