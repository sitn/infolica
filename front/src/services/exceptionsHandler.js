
/**
 * Handle exception
 */
export const handleException = function (error, component) {
    //Error code
    var code = error && error.response && error.response.status || 500;
    
    //Not authorized
    if(code === 403){
        component.$root.$emit("ShowError", "Veuillez vous connecter pour continuer"); 
        if(component.$router && component.$router.currentRoute && component.$router.currentRoute.path != '/login')
            component.$router.push('/login');
    }
    //All other error codes
    else
    {
       component.$root.$emit("ShowError", "Une erreur est survenue");   
    }                      
};

