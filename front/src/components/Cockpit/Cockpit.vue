<style src="./cockpit.css" scoped></style>
<template src="./cockpit.html"></template>


<script>
import Matdiff from "@/components/Cockpit/Matdiff/Matdiff.vue";

import { handleException } from '@/services/exceptionsHandler';
import { checkPermission, getOperateurs, stringifyAutocomplete, stringifyAutocomplete2, getCurrentUserRoleId } from '@/services/helper';

export default {
  name: "Cockpit",
  components: {
      Matdiff,
  },
  data: () => {
    return {
        affaires: [{}],
        affaireEtapes: [],
        affaireTypes: [],
        loadingAffaires: false,
        newAffaireAllowed: false,
        operateurs: [],
        plural: '',
        refreshAffaire: null,
        showMatdiff_secr: false,
        showMatdiff_mo: false,
        showMatdiff_ctrl: false,
        showPPE: false,
        role: {
            secretaire: Number(process.env.VUE_APP_SECRETAIRE_ROLE_ID),
            mo: Number(process.env.VUE_APP_MO_ROLE_ID),
            ppe: Number(process.env.VUE_APP_PPE_ROLE_ID),
            responsable: Number(process.env.VUE_APP_RESPONSABLE_ROLE_ID)
        },
        search: {
            operateur_id: -1,
            type_id: -1,
            showFinProcessus: false,
            showOnlyAffairesUrgentes: false,
            current_sort: "id",
            current_sort_order: "desc",
        },
        searchTerm: null,
        current_sort: "id",
        current_sort_order: "desc",
    };
  },

  methods: {
    /**
     * Get permissions
     */
    getPermissions() {
        // set time out of 0.5 seconds. If not, local storage has not time to memorize user allowed functions
        setTimeout(() => {
            
            this.newAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_PPE_EDITION) ||
                                     checkPermission(process.env.VUE_APP_AFFAIRE_REVISION_ABORNEMENT_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_CADASTRATION_EDITION) ||
                                     checkPermission(process.env.VUE_APP_AFFAIRE_RETABLISSEMENT_PFP3_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_PCOP_EDITION) ||
                                     checkPermission(process.env.VUE_APP_AFFAIRE_AUTRE_EDITION);
            
            //Check if role secretaire
            let role_id = getCurrentUserRoleId();
            if ( role_id && !isNaN(role_id) && Number(role_id) === this.role.secretaire  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                this.showMatdiff_secr = true;
            } 
            
            //Check if role MO
            if ( role_id && !isNaN(role_id) && Number(role_id) === this.role.mo  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                this.showMatdiff_mo = true;
            }

            //Check if role responsable
            if ( role_id && !isNaN(role_id) && Number(role_id) === this.role.responsable  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                // this.showMatdiff_secr = true;
                this.showMatdiff_mo = true;
                this.showMatdiff_ctrl = true;
            } 
            
        }, 500);
    },

    /**
     * get Affaires
     */
    async getAffaire() {
        // show progress bar
        this.loadingAffaires = true;

        // set query for get request
        const query = this.setSearchParamsQuery();

        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_COCKPIT_ENDPOINT + query,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = response.data;

                tmp = this.customSort(tmp);

                this.affaires = tmp;

                this.plural = '';
                if (tmp.length > 1) {
                    this.plural = 's';
                }

                // hide progress bar
                this.loadingAffaires = false;
            }
        }).catch(err => {
            handleException(err, this);
            this.loadingAffaires = false;
        });
    },

    /**
     * Get affaire etapes
     */
    async getAffaireEtapes() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPES_INDEX_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.affaireEtapes = response.data;
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * Get affaire types
     */
    async getAffaireTypes() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = response.data;
                
                this.affaireTypes = stringifyAutocomplete(tmp);
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * Update table and content to show or not FinProcessus step
     */
    setSearchParamsQuery() {
        let query = [];
        if (this.searchTerm) {
            query.push("searchTerm=" + this.searchTerm);
        }
        if (this.search.operateur_id > 0) {
            query.push("operateur_id=" + this.search.operateur_id);
        }
        if (this.search.type_id > 0) {
            query.push("type_id=" + this.search.type_id);
        }
        query.push("showFinProcessus=" + this.search.showFinProcessus);
        query.push("showOnlyAffairesUrgentes=" + this.search.showOnlyAffairesUrgentes);
        // query.push("sort_by=" + this.current_sort);
        // query.push("sort_order=" + this.current_sort_order);
        
        query = "?" + query.join('&');

        return query;
    },

    /**
     * Get operateurs
     */
    async getOperateursList() {
        return new Promise ((resolve, reject) => {
            getOperateurs()
            .then(response => {
                if (response && response.data) {
                    let tmp = response.data;
                    tmp = tmp.filter(x => x.chef_equipe);
    
                    // set operateur by default if he is chef_equipe
                    let currentUserID = JSON.parse(localStorage.getItem("infolica_user")).id;
                    let currentUserRoleID = getCurrentUserRoleId();
                    if (tmp.some(x => (x.id === currentUserID) && x.chef_equipe) && (currentUserRoleID && [this.role.mo, this.role.ppe].includes(currentUserRoleID))) {
                        this.search.operateur_id = Number(currentUserID);
                    }
    
                    tmp = stringifyAutocomplete2(tmp, "prenom_nom", null, "prenom_nom");
    
                    this.operateurs = tmp;
                    resolve(tmp);
                }
            }).catch(err => {
                handleException(err, this);
                reject(err);
            });
        });
    },

    /**
     * custom sort
     */
    customSort (value) {
        return value.sort((a, b) => {
            const sortBy = this.current_sort;

            let c = a[sortBy];
            let d = b[sortBy];

            if (!c) {
                return 1;
            }

            if (!d) {
                return -1;
            }

            if (this.current_sort_order === 'asc') {
                if (isNaN(c) || isNaN(d)) {
                    return String(c).localeCompare(String(d));
                } else {
                    return (c > d)? 1: -1;
                }
            } else {
                if (isNaN(c) || isNaN(d)) {
                    return String(d).localeCompare(String(c));
                } else {
                    return (c > d)? -1: 1;
                }
            }
        });
    },

    /**
     * get search params from localstorage
     */
    getSearchParams() {
        return new Promise((resolve) => {
            const searchParams = localStorage.getItem('infolica_cockpit_searchParams');
            if (searchParams) {
                this.search = JSON.parse(searchParams);
                this.current_sort = this.search.current_sort;
                this.current_sort_order = this.search.current_sort_order;
                this.customSort(this.affaires);
            }
            resolve();
        });
    },

    setSearchParams() {
        this.search.current_sort = this.current_sort;
        this.search.current_sort_order = this.current_sort_order;
        localStorage.setItem("infolica_cockpit_searchParams", JSON.stringify(this.search));
    }

  },

  mounted: function() {
    this.getAffaireEtapes()
    this.getAffaireTypes()
    this.getOperateursList().then(() => {
        this.getAffaire();
    });
    this.getPermissions();
  },
  
  created() {
    this.getSearchParams().then(() => {
        this.refreshAffaire = setInterval(this.getAffaire, 60000); // Recharge le tableau toutes les minutes
    });
  },

  beforeDestroy() {
    this.setSearchParams();
    clearInterval(this.refreshAffaire);
  }
};
</script>

