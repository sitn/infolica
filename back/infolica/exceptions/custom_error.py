class CustomError(Exception):
    # General constants
    GENERAL_EXCEPTION = 'An error occured while executing the query'
    ID_NOT_FOUND_EXCEPTION = 'Id not found'
    USER_NOT_FOUND_EXCEPTION = 'User not found'
    NOT_AUTHORIZED_EXCEPTION = 'Not authorized'
    INCOMPLETE_REQUEST = "Requête incomplète (paramètres manquants)"
    RECORD_WITH_ID_NOT_FOUND = '{} with id {} not found'
    UPDATE_NO_CHANGE_RECORDED = "No change recorded for id {} in table {}"
    NOT_FOUND_ERROR = "Route {} with method {} not found"
    RESERVATION_NUMBER_WITHOUT_BASE_NUMBER = "Manque le numéro de base lors de la réservation de numéros de DDP, PPE ou PCOP"
    FILE_NOT_FOUND = "Le fichier '{}' n'a pas été trouvé"
    DIRECTORY_WRONG_BASE = "Le dossier '{}' n'a pas la bonne base ({})" 
    DIRECTORY_NOT_FOUND = "Le dossier '{}' n'existe pas"
    NUMBER_REGISTRATION_FAILED = "Le numéro {} du cadastre {} dépasse le max + 1 autorisé (dernier numéro: {})"
