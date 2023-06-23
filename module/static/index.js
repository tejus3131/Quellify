$(document).ready(function () {
    $('#registerForm').submit(function (e) {
        e.preventDefault();
        $('#registerLoading').show();
        $('#registerButton').hide();
        $.ajax({
            type: 'POST',
            url: '/auth/register',
            data: $(this).serialize(),
            success: function (response) {
                if (response.message === 'success') {
                    window.location.href = '/';
                } else {
                    alert(response.message);
                }
            },
            complete: function () {
                $('#registerLoading').hide();
                $('#registerButton').show();
            }
        });
    });
});

$(document).ready(function () {
    $('#loginForm').submit(function (e) {
        e.preventDefault();
        $('#loginLoading').show();
        $('#loginButton').hide();
        $.ajax({
            type: 'POST',
            url: '/auth/login',
            data: $(this).serialize(),
            success: function (response) {
                if (response.message === 'success') {
                    window.location.href = '/';
                } else {
                    alert(response.message);
                }
            },
            complete: function () {
                $('#loginLoading').hide();
                $('#loginButton').show();
            }
        });
    });
});

$(document).ready(function () {
    $('#courseForm').submit(function (e) {
        e.preventDefault();
        $('#courseLoading').show();
        $('#courseButton').hide();
        $.ajax({
            type: 'POST',
            url: '/admin/add_course/1',
            data: $(this).serialize(),
            success: function (response) {
                if (response.message === 'success') {
                    window.location.href = '/admin/add_course/' + response.code;
                } else {
                    alert(response.message);
                }
            },
            complete: function () {
                $('#courseLoading').hide();
                $('#courseButton').show();
            }
        });
    });
});

$('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') 
        || location.hostname == this.hostname) {

        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
           if (target.length) {
             $('html,body').animate({
                 scrollTop: target.offset().top
            }, 1000);
            return false;
        }
    }
});