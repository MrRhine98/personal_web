$(function (){
$('#btnLogin').click(function () {
    username = $('#username').val();
    password = $('#password').val();
    $('.login').addClass('test');
    setTimeout(function () {
        $('.login').addClass('testtwo');
    }, 300);
    setTimeout(function () {
        $('.authent').show().animate({ right: -150 }, {
            easing: 'easeOutQuint',
            duration: 600,
            queue: false
        });
        $('.authent').animate({ opacity: 1 }, {
            duration: 200,
            queue: false
        }).addClass('visible');
    }, 500);
    $.ajax({
        'url': '/login_check',
        'type': 'post',
        'data': {'username': username, 'password': password},
        'dataType': 'json',
    }).success(function (data) {
        //alert(1);
        if (data.res == 0){
            alert("Wrong password or username!")
            window.location.href = "/login";
        }
        else{
            setTimeout(function () {
                $('.authent').show().animate({ right: 90 }, {
                    easing: 'easeOutQuint',
                    duration: 600,
                    queue: false
                });
                $('.authent').animate({ opacity: 0 }, {
                    duration: 200,
                    queue: false
                }).addClass('visible');
            }, 2500);
            setTimeout(function () {
                $('.login').removeClass('test');
                $('.login').removeClass('testtwo');
                $('.login div').fadeOut(123);
            }, 2800);
            setTimeout(function () {
                $('.success').fadeIn();
            }, 3200);
            setTimeout(function () {
                window.location.href = "/";
            }, 4000);
        }
    })

});
})
