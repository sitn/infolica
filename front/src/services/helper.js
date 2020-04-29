
import axios from 'axios';

/**
 * Check if the user is logged in
 */
export const checkLogged = function () {
    var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
    
    /*if(!session_user && component.$router && component.$router.currentRoute && component.$router.currentRoute.path != '/login')
        component.$router.push('/login');
    */

    //Set current user functions
    if(session_user)
        setCurrentUserFunctions();
    
    return session_user !== null;
};


/**
 * Check permission
 */
export const checkPermission = function (fonction) {
    var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;

    if(session_user && session_user.fonctions && session_user.fonctions.indexOf(fonction) > -1){
        return true;
    }

    return false;
};

/*
 * Set current user functions
 */
export const setCurrentUserFunctions = async function () {    
    axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CURRENT_USERS_FUNCTIONS_ENDPOINT,
        {
            withCredentials: true,
            headers: {'Accept': 'application/json'}
        })
        .then(response =>{
            if(response && response.data){
                var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
    
                if(session_user){
                    session_user.fonctions = response.data.fonctions;
                    localStorage.setItem('infolica_user', JSON.stringify(session_user));
                }
            }
            })
        .catch(() => {
            //To do message
        })
};

/*
 * Get Cadastres
 */
export const getCadastres = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CADASTRES_ENDPOINT,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            })
            .then(response => resolve(response))
            .catch(() => reject)
    });
};

/*
 * Get Types Numeros
 */
export const getTypesNumeros = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_NUMEROS_ENDPOINT,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            })
            .then(response => resolve(response))
            .catch(() => reject)
    });
};

/*
 * Get Types Affaires
 */
export const getTypesAffaires = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            })
            .then(response => resolve(response))
            .catch(() => reject)
    });
};

/*
 * Get Etats Numeros
 */
export const getEtatsNumeros = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_ETATS_NUMEROS_ENDPOINT,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            })
            .then(response => resolve(response))
            .catch(() => reject)
    });
};

/*
 * Get clients
 */
export const getClients = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
            {
              withCredentials: true,
              headers: {'Accept': 'application/json'}
            })
            .then(response => resolve(response))
            .catch(() => reject)
    });
};

/**
 * Get date of the day in good format for BD
 */
export const getCurrentDate = function () {
    var today = new Date();
    var date =
        ("0" + today.getDate()).slice(-2) + "." + ("0" + (today.getMonth() + 1)).slice(-2) + "." + today.getFullYear();
    return date
};