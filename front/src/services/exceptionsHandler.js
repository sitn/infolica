
/**
 * Handle exception
 */
export const handleException = function (error, component) {
    //Error code
    var code = error && error.response && error.response.status || 500;

    switch(code){
        //Not authorized
        case 403:
            if(window.location.href.indexOf("/login") === -1)
                window.location.href = "/login";
            break;

        //All other error codes
        default:
            component.$root.$emit("ShowError", "Une erreur est survenue");
    }
};

