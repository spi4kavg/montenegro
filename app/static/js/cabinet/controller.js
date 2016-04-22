$(document).ready(function () {
    function Controller() {
        this.params = {
            'page': 1
        };

        this.elements = {
            "userList": $("#user-list"),
            "pagination": $("#pagination"),
            "createUserButton": $("#create-user-button")
        };

        this.templates = {
            "userList": $("#user-list-template").html(),
            "pagination": $("#pagination-template").html(),
            "createUser": $("#create-user-template").html(),
            "updateUser": $("#update-user-template").html(),
            "newPassword": $("#new-password-template").html()
        };

        this.errorHandler = function (error) {
            if (_.isObject(error)) {
                if (error.status) {
                    switch(error.status) {
                        case 401: this.errorHandler("Вы не авторизованны"); break;
                        case 404: this.errorHandler("Пользователь не найден"); break;
                        default: alert('Произошла ошибка, попробуйте позже');
                    }
                } else {
                    var that = this;
                    _.each(error.messages, function (v, k) {
                        that.find("." + k + "-error").html(v.join("<br />"));
                    });
                }
            } else if (_.isString(error)) {
                this.find('.text-danger').first().html(error);
            }
        };

        this.refreshUserList = function () {
            var that = this,
                def = api.fetch(this.params);

            // creates list
            def.then(function (data) {
                var template = _.template(that.templates.userList),
                    compiledTemplate = template({'data': data.data});
                that.elements.userList.html(compiledTemplate);

                $(".delete-button", that.elements.userList).click(_.bind(that.dropUser, that));
                $(".update-button", that.elements.userList).click(_.bind(that.updateUser, that));
                $(".new-password-button", that.elements.userList).click(_.bind(that.newPassword, that));
            });

            def.fail(function (data) {
                this.elements.userList.html("Ошибка");
            });

            // creates pagination
            def.then(function (data) {
                var template = _.template(that.templates.pagination),
                    compiledTemplate = template({'data': data.meta});

                that.elements.pagination.html(compiledTemplate);
                $(".prev-page", that.elements.pagination).click(_.bind(that.prevPage, that));
                $(".next-page", that.elements.pagination).click(_.bind(that.nextPage, that));
            });

            def.fail(function (data) {
                this.elements.pagination.html("Ошибка");
            });
        };

        this.prevPage = function () {
            this.params.page--;
            this.refreshUserList();
        };

        this.nextPage = function () {
            this.params.page++;
            this.refreshUserList();
        };

        this.createUserButtonClick = function () {
            var that = this;
            $.fancybox({
                'helpers': {
                    'title': "Создание нового пользователя"
                },
                'content': this.templates.createUser,
                'afterShow': function () {
                    this.inner.find('form').submit(function () {
                        var form = $(this),
                            params = {
                                'login': form.find('[name="login"]').val(),
                                'password': form.find('[name="password"]').val(),
                                'repassword': form.find('[name="repassword"]').val(),
                                'grant': form.find('[name="grant"]').is(":checked")
                            };
                        if (params.password === params.repassword) {
                            var def = api.insert(params);

                            def.then(function (data) {
                                if (data.status_code === 400) {
                                    return that.errorHandler.call(form, data);
                                }
                                $.fancybox.close();
                                that.refreshUserList();
                            });

                            def.fail(function (data) {
                                that.errorHandler.call(form, data);
                            });
                        } else {
                            that.errorHandler.call(form, "Введенные пароли не идентичны");
                        }
                        return false;
                    });
                }
            });
        };

        this.dropUser = function (e) {
            var answer = confirm("Вы уверены?"),
                pk = $(e.target).data("pk") || $(e.target).parent().data("pk"),
                def = answer? api.del(pk): false,
                that = this;
            if (def) {
                def.then(function () {
                    if ($("#user-list table tbody tr").length == 1) {
                        that.prevPage();
                    }
                    that.refreshUserList();
                });

                def.fail(function () {
                    alert('произошла ошибка');
                });
            }
        };

        this.updateUser = function (e) {
            var pk = $(e.target).data("pk") || $(e.target).parent().data("pk"),
                def = api.fetchOne(pk),
                that = this;

            def.then(function (data) {
                $.fancybox({
                    'helpers': {
                        'title': "Рекдактирование пользователя"
                    },
                    'content': that.templates.updateUser,
                    'afterShow': function () {
                        var form = this.inner.find('form');

                        form.find("[name='pk']").val(data.pk);
                        form.find("[name='login']").val(data.login);
                        form.find("[name='grant']").prop('checked', data.grant);

                        form.submit(function () {
                            var form = $(this),
                                params = {
                                    'pk': form.find('[name="pk"]').val(),
                                    'login': form.find('[name="login"]').val(),
                                    'grant': form.find('[name="grant"]').is(":checked")
                                },
                                def = api.update(params);

                            def.then(function (data) {
                                if (data.status_code === 400) {
                                    return that.errorHandler.call(form, data);
                                }
                                $.fancybox.close();
                                that.refreshUserList();
                            });

                            def.fail(function (data) {
                                that.errorHandler.call(form, data);
                            });
                            return false;
                        });
                    }
                });
            });

            def.fail(function () {
                alert("Произошла ошибка");
            });
            return false;
        };

        this.newPassword = function (e) {
            var that = this,
                pk = $(e.target).data("pk") || $(e.target).parent().data("pk");
            $.fancybox({
                'helpers': {
                    'title': "Изменение пароля пользователя"
                },
                'content': this.templates.newPassword,
                'afterShow': function (e) {
                    var form = this.inner.find('form');
                    form.find('[name="pk"]').val(pk);

                    form.submit(function () {
                        var password = $("[name='password']", form).val(),
                            repassword = $("[name='repassword']", form).val();

                        if (password === repassword) {
                            var def = api.updatePassword({
                                'pk': pk,
                                'password': password,
                                'repassword': repassword
                            });

                            def.then(function (data) {
                                if (data.status_code === 400) {
                                    return that.errorHandler.call(form, data);
                                }
                                $.fancybox.close();
                                that.refreshUserList();
                            });

                            def.fail(function (data) {
                                that.errorHandler.call(form, data);
                            });
                        } else {
                            that.errorHandler.call(that, "Введенные пароли не идентичны");
                        }

                        return false;
                    });
                }
            });

            return false;
        };

        this.refreshUserList();

        this.elements.createUserButton.click(_.bind(this.createUserButtonClick, this));
    }

    new Controller();
});