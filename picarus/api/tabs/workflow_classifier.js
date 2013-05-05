function render_workflow_classifier() {
    model_create_selector($('#slices_select'), $('#params_preprocessor'), 'preprocessor', 'preprocessor');
    model_create_selector($('#slices_select'), $('#params_feature'), 'feature', 'bovw');
    model_create_selector($('#slices_select'), $('#params_classifier'), 'classifier', 'svmkernel');
}