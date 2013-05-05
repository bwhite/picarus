function render_workflow_classifier() {
    model_create_selector($('#slices_select'), $('#params_preprocessor'), 'image_preprocessor', 'picarus.ImagePreprocessor');
    model_create_selector($('#slices_select'), $('#params_feature'), 'feature', 'bovw');
    model_create_selector($('#slices_select'), $('#params_classifier'), 'classifier', 'svmkernel');
}