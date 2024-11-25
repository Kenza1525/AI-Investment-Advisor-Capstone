window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        redirect_to_home: function(pathname) {
            if (pathname === '/home') {
                setTimeout(function() {
                    window.location.reload(true);
                }, 100);  // Adjust timing as necessary
            }
            return '';
        }
    }
});