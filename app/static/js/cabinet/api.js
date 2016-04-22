var api = {
    fetch: function (params) {
        return $.ajax({
            "url": window.script_settings.fetch_url,
            "method": "GET",
            "dataType": "json",
            "data": params
        });
    },

    fetchOne: function (pk) {
        return $.ajax({
            "url": window.script_settings.fetch_one_url,
            "method": "GET",
            "dataType": "json",
            "data": {'pk': pk}
        });
    },

    updatePassword: function (params) {
        return $.ajax({
            "url": window.script_settings.update_password_url,
            "method": "POST",
            "dataType": "json",
            "data": params
        });
    },

    update: function (params) {
        return $.ajax({
            "url": window.script_settings.update_url,
            "method": "POST",
            "dataType": "json",
            "data": params
        });
    },

    insert: function (params) {
        return $.ajax({
            "url": window.script_settings.insert_url,
            "method": "PUT",
            "dataType": "json",
            "data": params
        });
    },

    del: function (pk) {
        return $.ajax({
            "url": window.script_settings.delete_url,
            "method": "DELETE",
            "dataType": "json",
            "data": {"pk": pk}
        });
    }
};