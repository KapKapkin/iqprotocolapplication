hide_page = true;
fieldset_repr = [".field-repr_name", ".field-repr_org_name", '.field-repr_position', '.field-repr_phone_number', '.field-repr_email'];

django.jQuery(document).ready(function () {
    if (django.jQuery('#id_resp_is_repr').is(':checked')) {
        for (field in fieldset_repr) {
            django.jQuery(fieldset_repr[field]).hide();
        }
        hide_page = true;
    } else {
        for (field in fieldset_repr) {
            django.jQuery(fieldset_repr[field]).show();
        }
        hide_page = false;
    }
    django.jQuery("#id_resp_is_repr").click(function () {
        console.log("check!")
        hide_page = !hide_page;
        if (hide_page) {
            for (field in fieldset_repr) {
                django.jQuery(fieldset_repr[field]).hide();
            }
        } else {
            for (field in fieldset_repr) {
                django.jQuery(fieldset_repr[field]).show();
            }

        }
    })
})