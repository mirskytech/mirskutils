heartbeat = (function() {

  var my = {};

  my.autologout = function() {

    $.idleTimeout('.modal.auto-logout', '.modal.auto-logout a.continue', {
        idleAfter: 60*30,
        warningLength:30,
        pollingInterval:60*5,
        keepAliveURL:'/heartbeat/', //TODO : DRY
        serverResponseEquals:"heartbeat",
        onTimeout: function(){
                $(this).slideUp();
                window.location = "/timeout/"; //TODO : DRY
        },
        onIdle: function(){
          $('.modal.auto-logout').modal('show');
        },
        onCountdown: function( counter ){
          $('.countdown', '.modal.auto-logout').html(counter);
        },
        onResume: function(){
          $('.modal.auto-logout').modal('hide');
        }
    });
  }

  return my;

});