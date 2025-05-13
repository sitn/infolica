
/**
 * Handle exception
 */
export const handleException = function (error, component) {
    //Error code
    let code = error && error.response && error.response.status || 500;

    //No error but no content response
    if(error && error.status === 204){
        component.$root.$emit("ShowError", "Aucune donnée trouvée");
    }
    //Not authorized
    else if(code === 403){
        const currentRoute = component.$router.currentRoute;
        if (currentRoute.name !== 'Login') {
            const a = component.$router.push({name: "Login", query: { redirect: currentRoute.path }});
            a.then(() => {
                localStorage.removeItem('infolica_user');
                component.$root.$emit("ShowError", "Veuillez vous connecter pour continuer") ;
            });
        }
    }
    //Custom error
    else if(error && error.msg){
        component.$root.$emit("ShowError", `Une erreur est survenue, contacter l'administrateur.\n${error.msg}`);
    }
    //Custom error
    else if(error){
        component.$root.$emit("ShowError", `Une erreur est survenue, contacter l'administrateur.\n${error}`);
    }
    //All other error codes
    else
    {
       component.$root.$emit("ShowError", "Une erreur est survenue, contacter l'administrateur.");
    }
};
