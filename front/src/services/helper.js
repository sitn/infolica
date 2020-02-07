

/**
 * Check if the user is logged in
 */
export const checkLogged = function() {
  var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;

  if(!session_user){
    window.location.href = "/login"
  }
  
}