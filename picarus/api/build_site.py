import glob
import subprocess
import argparse

def render_app():
    template_names = 'data_prefixes data_projects data_user data_uploads crawl_flickr models_list models_create models_single models_slice process_thumbnail process_garbage process_exif process_modify process_copy annotate_list annotate_batch annotate_entity visualize_thumbnails visualize_metadata visualize_exif visualize_locations visualize_times visualize_annotations evaluate_classifier'.split()

    app_template = open('app_template.html').read()
    templates = []
    scripts = []
    for template_name in template_names:
        fn = 'tabs/%s.html' % template_name
        templates.append(open(fn).read())
        fn = 'tabs/%s.js' % template_name
        scripts.append(open(fn).read())
    open('static/app.html', 'w').write(app_template.replace('{{ TEMPLATES }}', '\n'.join(templates)))
    open('js/tabs.js', 'w').write('\n'.join(scripts))
    preinclude_css = ['bootstrap_flat.css', 'flat-ui.css', 'hint.min.css', 'custom.css']
    open('static/style.css', 'w').write('\n'.join([open('css/' + x).read() for x in preinclude_css]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help="Don't minify the source")
    args = parser.parse_args()
    render_app()
    preinclude = ['jquery.min.js', 'underscore-min.js']
    preinclude = ['js/' + x for x in preinclude]
    a = preinclude + list(set(glob.glob('js/*.js')) - set(preinclude))
    if args.debug:
        open('static/compressed.js', 'w').write('\n'.join([open(x).read() for x in a]))
    else:
        a= ' '.join(['--js %s' % x for x in a])
        cmd = 'java -jar compiler.jar %s --js_output_file static/compressed.js' % a
        subprocess.call(cmd.split(' '))


if __name__ == '__main__':
    main()
