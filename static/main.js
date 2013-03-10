function checkCommons() {
    $.get( '/user/' + fbUserID ).done( function( data ) {
        userdata = data;
        setState( 'authenticated' );
    }).fail( function( xhr ) {
        setState( 'no-commons' );
    });
}
var stateEnter = {
    "starting": function() {
        FB.getLoginStatus( function( resp ) {
            if( resp.status === 'connected' ) {
                fbUserID = resp.authResponse.userID;
                checkCommons();
            } else {
                setState( "no-facebook" );
            }
        });
    },
    "no-commons": function() {
        checkCommons();
    },
    "authenticated": function() {
        $( 'span#commons-display-name' ).text( userdata.commons_username );
        $( 'span#commons-last-sync' ).text( userdata.last_sync || 'unsynced' );
    }
};


function setState( state ) {
    if( $( "body" ).hasClass( state ) ) {
        return;
    }
    $( "body" ).removeClass( "no-facebook starting no-commons" ).addClass( state );
    if( stateEnter[ state ] ) {
        stateEnter[ state ]();
    }
}

var fbUserID = null;
var userdata = null;

window.fbAsyncInit = function() {
    FB.init({
        appId      : '545467088820536', // App ID
        channelUrl : '//commonsfeed.us/channel.html', // Channel File
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        xfbml      : true  // parse XFBML
    });

    $( "#facebook-login" ).click( function() {
        FB.login( function( resp ) {
            if( resp.authResponse ) {
                fbUserID = resp.authResponse.userID;
                setState( "no-commons" );
            }
        }, { scope: "publish_actions" } );
        $( this ).text( "Logging in..." );
        return false;
    } );

    $( "#commons-login" ).click( function() {
        var commonsUserName = $( "#commons-username" ).val();
        $.post( '/user', { commons_username: commonsUserName, facebook_userid: fbUserID } ).done( function( data ) {
            userdata = data;
            setState( 'authenticated' );
        } );
        return false;
    } );

    setState( 'starting' );

};

// Load the SDK Asynchronously
(function(d){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement('script'); js.id = id; js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));
