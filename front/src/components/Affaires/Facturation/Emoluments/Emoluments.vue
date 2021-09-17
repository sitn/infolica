<style src="./emoluments.css" scoped></style>
<template src="./emoluments.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler';
const numeral = require("numeral");

export default {
  name: 'Emoluments',
  props: {
    affaire: {type: Object},
    affaire_factures: {type: Array},
    configFactureTypeID: {type: Object},
    factureTypes: {type: Array},
    numeros_references: {type: Array},
    permission: {type: Object},
    typesAffaires_conf: {type: Object},
  },
  data: function () {
      return {
        // clientsFacture_list: [],
        confirmationRemoveDialog: {
          title: "Demande de confirmation",
          msg: "Confirmez-vous la suppression de l'émolument?",
          confirmBtn: "Confirmer",
          cancelBtn: "Annuler",
          show: false,
          onConfirm: () => {},
          onCancel: () => {},
        },
        disabled: false,
        divers: [],
        emolument_facture_repartition_ctrl: false,
        emolumentsGeneral_list: [],
        emolumentsUnits: [],
        factures_repartition: [],
        form_general: {}, //général
        form_detail: {}, //emoluments sans bâtiment
        form_detail_batiment: [], //emoluments avec bâtiments
        n_divers: 8,
        pointsMatDiff_nombre: 0,

        // ####################################################################################
        // SI LE TABLEAU DES EMOLUMENTS EST MODIFIE, APPORTER LES MODIFICATIONS ICI !     START
        // ####################################################################################
        indexFromDB: {
          mandat: [1,2,3,4,5,6],
          travauxTerrain: [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
          travauxMaterialisation: [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48],
          deplacementDebours: [49],
          travauxBureau: [50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95],
          registreFoncier: [96,97,98,99,100],
          divers: 101,
          relations_autres_services: 102,
          forfait_rf: 103
        },
        // ####################################################################################
        // SI LE TABLEAU DES EMOLUMENTS EST MODIFIE, APPORTER LES MODIFICATIONS ICI !      STOP
        // ####################################################################################

        showEmolumentsDialog: false,
        showProgressBar: false,
        showSendValuesToFacture: false,
        total: {}
      }
  },

  methods:{
    /**
     * Get emoluments units from DB
     */
    async getEmolumentsUnit() {
      return new Promise((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_TABLEAU_EMOLUMENTS_ENDPOINT,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            let tmp = response.data;
            tmp.forEach(x => x.montant = Number(x.montant));
  
            // Mandat
            let i = 1;
            this.indexFromDB.mandat.forEach(x => {
              this.form_detail["mandat" + String(i)] = {
                tableau_emolument_id: x,
                nom: tmp[x-1].nom,
                unite: tmp[x-1].unite,
                prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
              i = i+1;
            });
  
            // Travaux terrain
            i = 1;
            this.indexFromDB.travauxTerrain.forEach(x => {
              this.form_detail["travauxTerrain" + String(i)] = {
                tableau_emolument_id: x,
                nom: tmp[x-1].nom,
                unite: tmp[x-1].unite,
                prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
              i = i+1;
            });
  
            // Travaux matérialisation
            i = 1;
            this.indexFromDB.travauxMaterialisation.forEach(x => {
              this.form_detail["travauxMaterialisation" + String(i)] = {
                tableau_emolument_id: x,
                nom: tmp[x-1].nom,
                unite: tmp[x-1].unite,
                prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
              i = i+1;
            });
  
            // Déplacements et débours
            i = 1;
            this.indexFromDB.deplacementDebours.forEach(x => {
              this.form_detail["deplacementDebours" + String(i)] = {
                tableau_emolument_id: x,
                nom: tmp[x-1].nom,
                unite: tmp[x-1].unite,
                prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
              i = i+1;
            });
  
            // Travaux bureau
            i = 1;
            this.indexFromDB.travauxBureau.forEach(x => {
              this.form_detail["travauxBureau" + String(i)] = {
                tableau_emolument_id: x,
                nom: tmp[x-1].nom,
                unite: tmp[x-1].unite,
                prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
              i = i+1;
            });
  
            // RF
            i = 1;
            this.indexFromDB.registreFoncier.forEach(x => {
              this.form_detail["registreFoncier" + String(i)] = {
                tableau_emolument_id: x,
                nom: tmp[x-1].nom,
                unite: tmp[x-1].unite,
                prix_unitaire: numeral(tmp[x-1].montant).format("0.00"),
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
              i = i+1;
            });
  
            // Divers
            for (let i=0; i<this.n_divers; i++) {
              this.form_detail["divers" + String(i+1)] = {
                tableau_emolument_id: this.indexFromDB.divers,
                nom: null,
                unite: "Heure",
                prix_unitaire: null,
                nombre: 0,
                batiment: 0,
                batiment_f: 1,
                montant: numeral(0).format("0.00"),
              }
            }
  
            //relations avec autres services
            this.form_detail["relations_autres_services1"] = {
              tableau_emolument_id: this.indexFromDB.relations_autres_services,
              nom: "Relations avec d'autres services (de 50.00 à 200.00 CHF)",
              unite: "-",
              prix_unitaire: numeral(0).format("0.00"),
              nombre: 1,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
  
            //forfait RF
            this.form_detail["forfait_rf1"] = {
              tableau_emolument_id: this.indexFromDB.forfait_rf,
              nom: "Forfait RF",
              unite: "-",
              prix_unitaire: numeral(0).format("0.00"),
              nombre: 1,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
  
            this.emolumentsUnits = tmp;
            resolve(tmp);
  
            this.initForm();
  
          }
        }).catch(err => {
          handleException(err, this);
          reject(err);
        });
      });
    },


    initForm(form_general=true) {
      
      if (form_general) {
        this.form_general = {
          id: null,
          affaire_id: this.affaire.id,
          pente_pc: 0,
          diff_visibilite_pc: 0,
          trafic_pc: 0,
          zi: 1,
          nb_batiments: 0,
          indice_application: 1.22,
          tva_pc: 7.7, // %
          remarque: "",
          facture_type_id: 1,
          numeros: [],
          numeros_id: [],
          utilise: false,
  
          // Bâtiments
          batiment_f: [],
        };


        for (const emol in this.form_detail) {
          this.form_detail[emol].nombre = 0;
          this.form_detail[emol].montant = numeral(0).format("0.00");
        }

        //relations avec autres services
        this.form_detail["relations_autres_services1"].prix_unitaire = numeral(0).format("0.00"),
        this.form_detail["relations_autres_services1"].nombre = 1,
        this.form_detail["relations_autres_services1"].montant = numeral(0).format("0.00"),

        //forfait RF
        this.form_detail["forfait_rf1"].prix_unitaire = numeral(0).format("0.00");
        this.form_detail["forfait_rf1"].nombre = 1;
        this.form_detail["forfait_rf1"].montant = numeral(0).format("0.00");

        //init form-detail to 0
        for (let i=0; i<this.n_divers; i++) {
          this.form_detail["divers" + String(i+1)] = {
            tableau_emolument_id: this.indexFromDB.divers,
            nom: null,
            unite: "Heure",
            prix_unitaire: null,
            nombre: 0,
            batiment: 0,
            batiment_f: 1,
            montant: numeral(0).format("0.00"),
          }
        }
        
        // empty form_detail_batiment
        this.form_detail_batiment= [];
      }


      this.total = {
        montant_mandat_total: 0,
        montant_mandat_batiment_total: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_mandat_batiment_total_f: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_21pfp: 0,
        montant_23sit: 0,
        montant_22pl: 0,
        montant_travauxTerrain_total: 0,
        montant_travauxTerrain_total_zi: 0,
        montant_travauxTerrain_batiment_total: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxTerrain_batiment_total_f: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxTerrain_batiment_total_f_somme: 0,
        montant_travauxTerrain_batiment_total_f_somme_zi: 0,
        montant_31_32_std_compl: 0,
        montant_31_32_std_compl_zi: 0,
        montant_33_materiel: 0,
        montant_34_matdiff: 0,
        montant_5_depl_debours: 0,
        montant_travauxMaterialisation_total: 0,
        montant_41pfp: 0,
        montant_43sit: 0,
        montant_44surf: 0,
        montant_42pl: 0,
        montant_travauxBureau_total: 0,
        montant_travauxBureau_batiment_total: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxBureau_batiment_total_f: this.form_general.nb_batiments>0? new Array(Number(this.form_general.nb_batiments)).fill(0): [],
        montant_travauxBureau_batiment_total_f_somme: 0,
        montant_divers_total: 0,
        montant_rf_total: 0,
        montant_recapitulatif_mandat: 0,
        montant_recapitulatif_somme1: 0,
        montant_recapitulatif_terrain_materialisation_deplacements: 0,
        montant_recapitulatif_somme2: 0,
        montant_recapitulatif_bureau: 0,
        montant_recapitulatif_somme3: 0,
        montant_recapitulatif_indice_application: 0,
        montant_recapitulatif_somme4: 0,
        montant_recapitulatif_materiel_divers: 0,
        montant_recapitulatif_somme5: 0,
        montant_recapitulatif_matdiff: 0,
        montant_recapitulatif_somme6: 0,
        montant_recapitulatif_tva: 0,
        montant_recapitulatif_somme7: 0,
        montant_recapitulatif_registre_foncier: 0,
        montant_recapitulatif_total: 0,
        montant_divers_total_with_5_depl_debours: 0,
      };

      this.disabled = false;
      this.computeZi();
      this.updateMontants()
    },

    /**
     * set form for nb of batiment
     */
    setFormDetail() {
      this.form_detail_batiment = [];
      for (let i=0; i<Number(this.form_general.nb_batiments); i++)  {
        this.form_detail_batiment.push( JSON.parse( JSON.stringify(this.form_detail)) );
        for (let key in this.form_detail_batiment[i]) {
          this.form_detail_batiment[i][key].batiment = i+1;
          this.form_detail_batiment[i][key].montant = numeral(0).format("0.00");
          this.form_detail_batiment[i][key].nombre = 0;
          this.form_detail_batiment[i][key].batiment_f = this.form_general.batiment_f[i];
        }
      }
    },

    /**
     * Add batiment
     */
    addBatiment() {
      this.form_general.nb_batiments += 1;

      let tmp = JSON.parse( JSON.stringify(this.form_detail));
      for (const key in tmp) {
        tmp[key].batiment = this.form_general.nb_batiments;
        tmp[key].montant = numeral(0).format("0.00");
        tmp[key].nombre = 0;
        tmp[key].batiment_f = this.form_general.batiment_f[this.form_general.nb_batiments];
      }
      this.form_detail_batiment.push(tmp);
    },

    /**
     * Remove batiment
     */
    removeBatiment(batiment_i) {
      let tmp = [];
      let c = 1; // renumérotation bâtiment
      for (let i=0; i<this.form_general.nb_batiments; i++) {
        if (this.form_detail_batiment[i]['mandat1'].batiment !== batiment_i) {
          for (let key in this.form_detail_batiment[i]) {
            this.form_detail_batiment[i][key].batiment = c;
          }
          tmp.push(this.form_detail_batiment[i]);
          c += 1;
        }
      }
      this.form_detail_batiment = JSON.parse(JSON.stringify(tmp));
      this.form_general.batiment_f.splice(batiment_i-1,1);
      this.form_general.nb_batiments -= 1;
      this.initForm(false);
      this.updateMontants();
    },


    /**
     * Update batimentCorrectionFactor
     */
    updateBatimentCorrectionFactor() {
      for (let i=0; i<Number(this.form_general.nb_batiments); i++) {
        for (let key in this.form_detail_batiment[i]) {
          this.form_detail_batiment[i][key].batiment_f = Number(this.form_general.batiment_f[i]);
        }
      }

      this.updateMontants();
    },


    /**
     * Update value of zi
     */
    computeZi() {
      this.form_general.zi = numeral(
        1 + 
        Number(this.form_general.pente_pc) / 100 +
        Number(this.form_general.diff_visibilite_pc) / 100 + 
        Number(this.form_general.trafic_pc) / 100
      ).format("0.00");
    },

    /**
     * Update montants
     */
    updateMontants() {
      //update form_detail.relations_autres_services1
      if (this.form_detail.relations_autres_services1 && this.form_detail.relations_autres_services1.prix_unitaire) {
        if (Number(this.form_detail.relations_autres_services1.prix_unitaire) > 0) {
          this.form_detail.relations_autres_services1.nombre = 1;
        } else {
          this.form_detail.relations_autres_services1.nombre = 0;
        }
      } else {
        this.form_detail.relations_autres_services1.nombre = 0;
        this.form_detail.relations_autres_services1.prix_unitaire = numeral(0).format("0.00");
      }
      
      //update form_detail.forfait_rf1.prix_unitaire
      if (this.form_detail.forfait_rf1.prix_unitaire) {
        if (Number(this.form_detail.forfait_rf1.prix_unitaire) > 0) {
          this.form_detail.forfait_rf1.nombre = 1;
        } else {
          this.form_detail.forfait_rf1.nombre = 0;
        }
      } else {
        this.form_detail.forfait_rf1.nombre = 0;
      }

      // set number of pces matdiff
      this.pointsMatDiff_nombre = 
        this.form_detail.travauxMaterialisation14.nombre +
        this.form_detail.travauxMaterialisation15.nombre +
        this.form_detail.travauxMaterialisation16.nombre +
        this.form_detail.travauxMaterialisation17.nombre;

      //form_detail
      for (let key in this.form_detail) {
        this.form_detail[key].montant = numeral(this.round(Number(this.form_detail[key].nombre) * Number(this.form_detail[key].prix_unitaire))).format("0.00");
      }
      //form_detail_batiment
      for (let i=0; i<Number(this.form_general.nb_batiments); i++) {
        for (let key in this.form_detail_batiment[i]) {
          this.form_detail_batiment[i][key].montant = numeral(this.round(Number(this.form_detail_batiment[i][key].nombre) * Number(this.form_detail_batiment[i][key].prix_unitaire))).format("0.00");
        }
      }
      
      // cas particuliers relations_autres_services et forfait_rf
      this.form_detail.relations_autres_services1.prix_unitaire = numeral(this.round(this.form_detail.relations_autres_services1.prix_unitaire)).format("0.00");
      this.form_detail.forfait_rf1.prix_unitaire = numeral(this.form_detail.forfait_rf1.prix_unitaire).format("0.00");
      
      // update montant_total par categorie
      //Montants totaux Mandat
      this.total.montant_mandat_total = 
        Number(this.form_detail.mandat1.montant) +
        Number(this.form_detail.mandat2.montant) +
        Number(this.form_detail.mandat3.montant) +
        Number(this.form_detail.mandat4.montant) +
        Number(this.form_detail.mandat5.montant) +
        Number(this.form_detail.mandat6.montant);

      for (let j=0; j<Number(this.form_general.nb_batiments); j++) {
        // Mandat
        this.total.montant_mandat_batiment_total[j] = 
          Number(this.form_detail_batiment[j].mandat1.montant) +
          Number(this.form_detail_batiment[j].mandat2.montant) +
          Number(this.form_detail_batiment[j].mandat3.montant) +
          Number(this.form_detail_batiment[j].mandat4.montant) +
          Number(this.form_detail_batiment[j].mandat5.montant) +
          Number(this.form_detail_batiment[j].mandat6.montant);

        this.total.montant_mandat_batiment_total_f[j] =
          this.round(Number(this.total.montant_mandat_batiment_total[j]) * Number(this.form_general.batiment_f[j]));
      
        // Travaux terrain
        this.total.montant_travauxTerrain_batiment_total[j] =
          Number(this.form_detail_batiment[j].travauxTerrain1.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain2.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain3.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain4.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain5.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain6.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain7.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain8.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain9.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain10.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain11.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain12.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain13.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain14.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain15.montant) +
          Number(this.form_detail_batiment[j].travauxTerrain16.montant);

        this.total.montant_travauxTerrain_batiment_total_f[j] =
          this.round(Number(this.total.montant_travauxTerrain_batiment_total[j]) * Number(this.form_general.batiment_f[j]));

        // Travaux bureau
        this.total.montant_travauxBureau_batiment_total[j] =
          Number(this.form_detail_batiment[j].travauxBureau1.montant) +
          Number(this.form_detail_batiment[j].travauxBureau2.montant) +
          Number(this.form_detail_batiment[j].travauxBureau3.montant) +
          Number(this.form_detail_batiment[j].travauxBureau4.montant) +
          Number(this.form_detail_batiment[j].travauxBureau5.montant) +
          Number(this.form_detail_batiment[j].travauxBureau6.montant) +
          Number(this.form_detail_batiment[j].travauxBureau7.montant) +
          Number(this.form_detail_batiment[j].travauxBureau8.montant) +
          Number(this.form_detail_batiment[j].travauxBureau9.montant) +
          Number(this.form_detail_batiment[j].travauxBureau10.montant) +
          Number(this.form_detail_batiment[j].travauxBureau11.montant) +
          Number(this.form_detail_batiment[j].travauxBureau12.montant) +
          Number(this.form_detail_batiment[j].travauxBureau13.montant) +
          Number(this.form_detail_batiment[j].travauxBureau14.montant) +
          Number(this.form_detail_batiment[j].travauxBureau15.montant) +
          Number(this.form_detail_batiment[j].travauxBureau16.montant) +
          Number(this.form_detail_batiment[j].travauxBureau17.montant) +
          Number(this.form_detail_batiment[j].travauxBureau18.montant) +
          Number(this.form_detail_batiment[j].travauxBureau19.montant) +
          Number(this.form_detail_batiment[j].travauxBureau20.montant) +
          Number(this.form_detail_batiment[j].travauxBureau21.montant) +
          Number(this.form_detail_batiment[j].travauxBureau22.montant) +
          Number(this.form_detail_batiment[j].travauxBureau23.montant) +
          Number(this.form_detail_batiment[j].travauxBureau24.montant) +
          Number(this.form_detail_batiment[j].travauxBureau25.montant) +
          Number(this.form_detail_batiment[j].travauxBureau26.montant) +
          Number(this.form_detail_batiment[j].travauxBureau27.montant);

        this.total.montant_travauxBureau_batiment_total_f[j] =
          this.round(Number(this.total.montant_travauxBureau_batiment_total[j]) * Number(this.form_general.batiment_f[j]));
      }

      //Montants totaux TravauxTerrain
      this.total.montant_21pfp = 
        Number(this.form_detail.travauxTerrain1.montant) +
        Number(this.form_detail.travauxTerrain2.montant) +
        Number(this.form_detail.travauxTerrain3.montant) +
        Number(this.form_detail.travauxTerrain4.montant) +
        Number(this.form_detail.travauxTerrain5.montant) +
        Number(this.form_detail.travauxTerrain6.montant) +
        Number(this.form_detail.travauxTerrain7.montant) +
        Number(this.form_detail.travauxTerrain8.montant) +
        Number(this.form_detail.travauxTerrain9.montant) +
        Number(this.form_detail.travauxTerrain10.montant) +
        Number(this.form_detail.travauxTerrain11.montant) +
        Number(this.form_detail.travauxTerrain12.montant) +
        Number(this.form_detail.travauxTerrain13.montant) +
        Number(this.form_detail.travauxTerrain14.montant);
      
      this.total.montant_23sit = 
        Number(this.form_detail.travauxTerrain15.montant) +
        Number(this.form_detail.travauxTerrain16.montant);
      
      this.total.montant_22pl = 
        Number(this.form_detail.travauxTerrain17.montant) +
        Number(this.form_detail.travauxTerrain18.montant) +
        Number(this.form_detail.travauxTerrain19.montant) +
        Number(this.form_detail.travauxTerrain20.montant) +
        Number(this.form_detail.travauxTerrain21.montant) +
        Number(this.form_detail.travauxTerrain22.montant) +
        Number(this.form_detail.travauxTerrain23.montant) +
        Number(this.form_detail.travauxTerrain24.montant) +
        Number(this.form_detail.travauxTerrain25.montant);
      
      this.total.montant_travauxTerrain_total = 
        Number(this.total.montant_21pfp) +
        Number(this.total.montant_23sit) +
        Number(this.total.montant_22pl);

      this.total.montant_travauxTerrain_total_zi =
        Number(this.total.montant_travauxTerrain_total) * Number(this.form_general.zi);

      this.total.montant_travauxTerrain_batiment_total_f_somme =
        this.form_general.nb_batiments>0? this.round(Number(this.total.montant_travauxTerrain_batiment_total_f.reduce((a, b) => Number(a) + Number(b)))): 0;

      this.total.montant_travauxTerrain_batiment_total_f_somme_zi =
        this.round(Number(this.total.montant_travauxTerrain_batiment_total_f_somme) * Number(this.form_general.zi));

      //Montants totaux TravauxMatérialisation
      this.total.montant_31_32_std_compl = 
        Number(this.form_detail.travauxMaterialisation1.montant) +
        Number(this.form_detail.travauxMaterialisation2.montant) +
        Number(this.form_detail.travauxMaterialisation3.montant) +
        Number(this.form_detail.travauxMaterialisation4.montant) +
        Number(this.form_detail.travauxMaterialisation5.montant) +
        Number(this.form_detail.travauxMaterialisation6.montant) +
        Number(this.form_detail.travauxMaterialisation7.montant);
      
      this.total.montant_31_32_std_compl_zi = 
        this.total.montant_31_32_std_compl * Number(this.form_general.zi);

      this.total.montant_33_materiel = 
        Number(this.form_detail.travauxMaterialisation8.montant) +
        Number(this.form_detail.travauxMaterialisation9.montant) +
        Number(this.form_detail.travauxMaterialisation10.montant) +
        Number(this.form_detail.travauxMaterialisation11.montant) +
        Number(this.form_detail.travauxMaterialisation12.montant) +
        Number(this.form_detail.travauxMaterialisation13.montant);
      
      this.total.montant_5_depl_debours = 
        Number(this.form_detail.deplacementDebours1.montant);

      this.total.montant_34_matdiff = 
        Number(this.form_detail.travauxMaterialisation14.montant) +
        Number(this.form_detail.travauxMaterialisation15.montant) +
        Number(this.form_detail.travauxMaterialisation16.montant) +
        Number(this.form_detail.travauxMaterialisation17.montant);
      
      this.total.montant_travauxMaterialisation_total = 
        Number(this.total.montant_31_32_std_compl_zi) +
        Number(this.total.montant_33_materiel) +
        Number(this.total.montant_34_matdiff);

      //Montants totaux TravauxBureau
      this.total.montant_41pfp = 
        Number(this.form_detail.travauxBureau1.montant) +
        Number(this.form_detail.travauxBureau2.montant) +
        Number(this.form_detail.travauxBureau3.montant) +
        Number(this.form_detail.travauxBureau4.montant) +
        Number(this.form_detail.travauxBureau5.montant) +
        Number(this.form_detail.travauxBureau6.montant) +
        Number(this.form_detail.travauxBureau7.montant) +
        Number(this.form_detail.travauxBureau8.montant) +
        Number(this.form_detail.travauxBureau9.montant) +
        Number(this.form_detail.travauxBureau10.montant) +
        Number(this.form_detail.travauxBureau11.montant) +
        Number(this.form_detail.travauxBureau12.montant);
      
      this.total.montant_43sit = 
        Number(this.form_detail.travauxBureau13.montant) +
        Number(this.form_detail.travauxBureau14.montant) +
        Number(this.form_detail.travauxBureau15.montant) +
        Number(this.form_detail.travauxBureau16.montant) +
        Number(this.form_detail.travauxBureau17.montant) +
        Number(this.form_detail.travauxBureau18.montant) +
        Number(this.form_detail.travauxBureau19.montant) +
        Number(this.form_detail.travauxBureau20.montant) +
        Number(this.form_detail.travauxBureau21.montant) +
        Number(this.form_detail.travauxBureau22.montant);
      
      this.total.montant_44surf = 
        Number(this.form_detail.travauxBureau23.montant) +
        Number(this.form_detail.travauxBureau24.montant) +
        Number(this.form_detail.travauxBureau25.montant) +
        Number(this.form_detail.travauxBureau26.montant) +
        Number(this.form_detail.travauxBureau27.montant);
      
      this.total.montant_42pl = 
        Number(this.form_detail.travauxBureau28.montant) +
        Number(this.form_detail.travauxBureau29.montant) +
        Number(this.form_detail.travauxBureau30.montant) +
        Number(this.form_detail.travauxBureau31.montant) +
        Number(this.form_detail.travauxBureau32.montant) +
        Number(this.form_detail.travauxBureau33.montant) +
        Number(this.form_detail.travauxBureau34.montant) +
        Number(this.form_detail.travauxBureau35.montant) +
        Number(this.form_detail.travauxBureau36.montant) +
        Number(this.form_detail.travauxBureau37.montant) +
        Number(this.form_detail.travauxBureau38.montant) +
        Number(this.form_detail.travauxBureau39.montant) +
        Number(this.form_detail.travauxBureau40.montant) +
        Number(this.form_detail.travauxBureau41.montant) +
        Number(this.form_detail.travauxBureau42.montant) +
        Number(this.form_detail.travauxBureau43.montant) +
        Number(this.form_detail.travauxBureau44.montant) +
        Number(this.form_detail.travauxBureau45.montant) +
        Number(this.form_detail.travauxBureau46.montant);

      this.total.montant_travauxBureau_total = 
        Number(this.total.montant_41pfp) +
        Number(this.total.montant_43sit) +
        Number(this.total.montant_44surf) +
        Number(this.total.montant_42pl);

      this.total.montant_travauxBureau_batiment_total_f_somme = 
        this.form_general.nb_batiments>0? this.round(Number(this.total.montant_travauxBureau_batiment_total_f.reduce((a, b) => Number(a) + Number(b)))): 0;

      //Divers
      this.total.montant_divers_total = 0;
      for (let i=0; i<this.n_divers; i++) {
        this.total.montant_divers_total += Number(this.form_detail["divers" + String(i+1)].montant);
      }
      this.total.montant_divers_total += Number(this.form_detail.relations_autres_services1.montant);

      //Registre foncier
      this.total.montant_rf_total =
        Number(this.form_detail.registreFoncier1.montant) +
        Number(this.form_detail.registreFoncier2.montant) +
        Number(this.form_detail.registreFoncier3.montant) +
        Number(this.form_detail.registreFoncier4.montant) +
        Number(this.form_detail.registreFoncier5.montant) +
        Number(this.form_detail.forfait_rf1.montant);


      this.updateRecapitulatif();
    },


    updateRecapitulatif() {
      let mandat_batiment = (this.form_general.nb_batiments > 0)? Number(this.total.montant_mandat_batiment_total_f.reduce((a, b) => Number(a) + Number(b))): 0
      this.total.montant_recapitulatif_mandat = Number(this.total.montant_mandat_total) + mandat_batiment;
      this.total.montant_recapitulatif_somme1 = Number(this.total.montant_recapitulatif_mandat)

      this.total.montant_recapitulatif_terrain_materialisation_deplacements = Number(this.total.montant_travauxTerrain_total_zi) + Number(this.total.montant_31_32_std_compl) + Number(this.total.montant_5_depl_debours) + Number(this.total.montant_travauxTerrain_batiment_total_f_somme_zi);
      this.total.montant_recapitulatif_somme2 = Number(this.total.montant_recapitulatif_somme1) + Number(this.total.montant_recapitulatif_terrain_materialisation_deplacements);

      this.total.montant_recapitulatif_bureau = Number(this.total.montant_travauxBureau_total) + Number(this.total.montant_travauxBureau_batiment_total_f_somme);
      this.total.montant_recapitulatif_somme3 = Number(this.total.montant_recapitulatif_somme2) + Number(this.total.montant_recapitulatif_bureau);

      this.total.montant_recapitulatif_indice_application = this.round( Number(this.total.montant_recapitulatif_somme3) * (Number(this.form_general.indice_application) - 1));
      this.total.montant_recapitulatif_somme4 = Number(this.total.montant_recapitulatif_somme3) + Number(this.total.montant_recapitulatif_indice_application);

      this.total.montant_recapitulatif_materiel_divers = Number(this.total.montant_33_materiel) + Number(this.total.montant_divers_total);
      this.total.montant_recapitulatif_somme5 = Number(this.total.montant_recapitulatif_somme4) + Number(this.total.montant_recapitulatif_materiel_divers);

      this.total.montant_recapitulatif_matdiff = this.round( Number(this.total.montant_34_matdiff) * Number(this.form_general.indice_application));
      this.total.montant_recapitulatif_somme6 = Number(this.total.montant_recapitulatif_somme5) + Number(this.total.montant_recapitulatif_matdiff);

      this.total.montant_recapitulatif_tva = this.round(Number(this.total.montant_recapitulatif_somme5) * Number(this.form_general.tva_pc) / 100, 0.05) + this.round(Number(this.total.montant_recapitulatif_matdiff) * Number(this.form_general.tva_pc) / 100, 0.05);
      this.total.montant_recapitulatif_somme7 = this.total.montant_recapitulatif_somme6 + Number(this.total.montant_recapitulatif_tva);

      this.total.montant_recapitulatif_registre_foncier = Number(this.total.montant_rf_total);

      this.total.montant_recapitulatif_total = Number(this.total.montant_recapitulatif_somme7) + Number(this.total.montant_recapitulatif_registre_foncier);

      this.setComptabiliteFormat();
    },


    /** Set nombre points mat_diff */
    updateMatDiff() {
      // répartir les points dans les bons émoluments
      this.form_detail.travauxMaterialisation14.nombre = 0;
      this.form_detail.travauxMaterialisation15.nombre = 0;
      this.form_detail.travauxMaterialisation16.nombre = 0;
      this.form_detail.travauxMaterialisation17.nombre = 0;

      let tmp = Number(this.pointsMatDiff_nombre);
      let c = 1;
      while (tmp > 0) {
        if (c <= 5) {
          // de 1 à 5 points
          this.form_detail.travauxMaterialisation14.nombre += 1;
        } else if (c <= 10) {
          // de 6 à 10 points
          this.form_detail.travauxMaterialisation15.nombre += 1;
        } else if (c <= 15) {
          // de 11 à 15 points
          this.form_detail.travauxMaterialisation16.nombre += 1;
        } else {
          // plus de 16 points
          this.form_detail.travauxMaterialisation17.nombre += 1;
        }

        tmp -= 1;
        c += 1;
      }

      this.updateMontants();
    },

    /** Set format for comptabilité: 0.00 CHF */
    setComptabiliteFormat() {
      Object.keys(this.total).forEach(x => {
        if (Array.isArray(this.total[x])) {
          for (let i=0; i<this.form_general.nb_batiments; i++) {
            this.total[x][i] = numeral(this.total[x][i]).format("0.00");
          }
        } else {
          this.total[x] = numeral(this.total[x]).format("0.00");
        }
      });
    },

    /**
     * Round numbers
     */
    round(num, multiple=0.1) {
      num = Number(num);
      multiple = Number(multiple);
      return Math.round(num / multiple) * multiple;
    },


    /**
     * postFormular (main)
     */
    async postEmolument() {
      // show progressbar
      this.showProgressBar = true;
      this.disabled = true;

      if (this.form_general.id) {
        // update form
        this.putEmolumentsGeneral().then(response => {
          if (response && response.data) {
            this.putEmolumentsDetail(this.form_general.id).then(response => {
              if (response && response.data) {
                this.showEmolumentsDialog = false;
                this.$root.$emit("ShowMessage", "Le formulaire a été enregistré correctement");
  
                this.postEmolumentAffaireRepartition(this.form_general.id);
                // refresh emoluments_general_list
                this.getEmolumentsGeneral();
                this.$root.$emit("searchAffaireFactures");
                
                // hide progressbar
                this.showProgressBar = false;
                this.disabled = false;
              }
            }).catch(err => handleException(err, this));
          }
        }).catch(err => handleException(err, this));
      } else {
        // create form
        this.postEmolumentsGeneral().then(response => {
          if (response && response.data) {
            let emolument_affaire_id = response.data.emolument_affaire_id;
            this.postEmolumentsDetail(emolument_affaire_id).then(response => {
              if (response && response.data) {
                this.showEmolumentsDialog = false;

                this.$root.$emit("ShowMessage", "Le formulaire a été enregistré correctement");
                
                this.postEmolumentAffaireRepartition(emolument_affaire_id);
                // refresh emoluments_general_list
                this.getEmolumentsGeneral();
                this.$root.$emit("searchAffaireFactures");
                
                // hide progressbar
                this.showProgressBar = false;
                this.disabled = false;
              }
            }).catch(err => {
              handleException(err, this);
              // hide progressbar
              this.showProgressBar = false;
              this.disabled = false;
            });
          }
        }).catch(err => {
          handleException(err, this);
          // hide progressbar
          this.showProgressBar = false;
          this.disabled = false;
        });
      }
    },

    async postEmolumentsGeneral() {
      let formData = new FormData();
      formData.append("data", JSON.stringify(this.form_general));

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err)); 
      });
    },

    async postEmolumentsDetail(emolument_affaire_id) {
      let form = JSON.parse(JSON.stringify(this.form_detail_batiment));
      form.push(this.form_detail)

      let formData = new FormData();
      formData.append("data", JSON.stringify(form));
      formData.append("emolument_affaire_id", emolument_affaire_id);

      return new Promise((resolve, reject) => {
        this.$http.post(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err)); 
      });
    },


    async putEmolumentsGeneral() {
      let formData = new FormData();
      formData.append("data", JSON.stringify(this.form_general));
      formData.append("emolument_affaire_id", this.form_general.id)

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err)); 
      });
    },

    async putEmolumentsDetail(emolument_affaire_id) {
      let form = JSON.parse(JSON.stringify(this.form_detail_batiment));
      form.push(this.form_detail)

      let formData = new FormData();
      formData.append("data", JSON.stringify(form));
      formData.append("emolument_affaire_id", emolument_affaire_id);

      return new Promise((resolve, reject) => {
        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err)); 
      });
    },

    /**
     * Get emoluments affaire - general
     */
    async getEmolumentsGeneral() {
      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_ENDPOINT + "?affaire_id=" + this.affaire.id,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.initForm();

          this.emolumentsGeneral_list = new Array(response.data.lenght);
          for (let j=0; j<response.data.length; j++) {
            this.emolumentsGeneral_list[j] = JSON.parse(JSON.stringify(this.form_general));
          }
          for (const [i, form_gen_i] of response.data.entries()) {
            // Parcourir les form_gen

            for (const key in this.form_general){
              // Set parameters

              if (key in form_gen_i) {
                this.emolumentsGeneral_list[i][key] = form_gen_i[key];
              }
            }
          }
          this.initForm(false); // ddd
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Get emoluments
     */
    async getEmolumentsDetail(emolument_affaire_id) {
      // set form_general
      this.form_general = this.emolumentsGeneral_list.filter(x => x.id === emolument_affaire_id)[0];
      this.disabled = this.form_general.utilise;

      this.setFormDetail();

      this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT + "?emolument_affaire_id=" + emolument_affaire_id,
        {
          withCredentials: true,
          headers: {'Accept': 'application/json'}
        }
      ).then(response => {
        if (response && response.data) {

          // Prepare divers
          for (let i=0; i<this.n_divers; i++) {
            this.form_detail["divers" + String(i+1)] = {
              tableau_emolument_id: this.indexFromDB.divers,
              nom: null,
              unite: "Heure",
              prix_unitaire: null,
              nombre: 0,
              batiment: 0,
              batiment_f: 1,
              montant: numeral(0).format("0.00"),
            }
          }

          let divers_counter = 1;
          for (const emol of response.data) {
            // iterate through response
            if (emol.batiment === 0) {
              // No building
              for (let form_emol in this.form_detail) {
                // iterate through form_detail to fill values
                if (this.form_detail[form_emol].tableau_emolument_id === emol.tableau_emolument_id) {
                  if (this.form_detail[form_emol].tableau_emolument_id === this.indexFromDB.divers) {
                    this.form_detail["divers" + String(divers_counter)]["nom"] = emol.position;
                    this.form_detail["divers" + String(divers_counter)]["prix_unitaire"] = numeral(emol.prix_unitaire).format("0.00");
                    this.form_detail["divers" + String(divers_counter)]["nombre"] = emol.nombre;
                    this.form_detail["divers" + String(divers_counter)]["montant"] = numeral(emol.montant).format("0.00");
                    divers_counter += 1;
                  } else {
                    this.form_detail[form_emol]["nom"] = emol.position;
                    this.form_detail[form_emol]["prix_unitaire"] = numeral(emol.prix_unitaire).format("0.00");
                    this.form_detail[form_emol]["nombre"] = emol.nombre;
                    this.form_detail[form_emol]["montant"] = numeral(emol.montant).format("0.00");
                  }
                  break;
                }
              }
            } else {
              // Buildings
              for (let form_emol in this.form_detail_batiment[emol.batiment-1]) {
                //update batiment_f order in form_general
                this.form_general.batiment_f[emol.batiment-1] = emol.batiment_f;

                // iterate this.form_detail_batiment to fill values
                if (this.form_detail_batiment[emol.batiment-1][form_emol].tableau_emolument_id === emol.tableau_emolument_id) {
                  this.form_detail_batiment[emol.batiment-1][form_emol]["nom"] = emol.position;
                  this.form_detail_batiment[emol.batiment-1][form_emol]["prix_unitaire"] = numeral(emol.prix_unitaire).format("0.00");
                  this.form_detail_batiment[emol.batiment-1][form_emol]["nombre"] = emol.nombre;
                  this.form_detail_batiment[emol.batiment-1][form_emol]["montant"] = numeral(emol.montant).format("0.00");
                  break;
                }
              }
            }
          }

          this.updateMontants();
          this.updateFactureRepartition();
          this.showEmolumentsDialog = true;

          // if cadastration, load numeros concerned by emoluments
          if (this.affaire.type_id === this.typesAffaires_conf.cadastration) {
            this.form_general.numeros = [];
            if (this.form_general.numeros_id.length > 0) {
              this.form_general.numeros_id.forEach(x => {
                this.form_general.numeros.push(this.numeros_references.filter(y => y.numero_id === x)[0]);
              });
            }
          }
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * Cancel formular edition
     */
    onCancel() {
      this.showEmolumentsDialog = false;
      this.getEmolumentsGeneral();
    },

    /**
     * on select BF reference (cadastration)
     */
    onSelectBFReferences(items) {
      this.form_general.numeros = items;
      this.form_general.numeros_id = [];
      items.forEach(x => {
        this.form_general.numeros_id.push(x.numero_id);
      });
    },

    /**
     * fix emolument definitively
     */
    async fixEmolumentDefinitively() {
      let formData = new FormData();
      formData.append("emolument_affaire_id", this.form_general.id);
      formData.append("utilise", true);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_FREEZE_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.getEmolumentsGeneral();
        }
      }).catch(err => handleException(err, this));
    },
    
    
    /**
     * Set prix unitaire divers format
     */
    setPrixUnitaireFormat() {
      for (let i=0; i<this.n_divers; i++) {
        if (this.form_detail["divers" + String(i+1)].prix_unitaire && Number(this.form_detail["divers" + String(i+1)].prix_unitaire) > 0) {
          this.form_detail["divers" + String(i+1)].prix_unitaire = numeral(Number(this.form_detail["divers" + String(i+1)].prix_unitaire)).format("0.00");
        } else {
          this.form_detail["divers" + String(i+1)].prix_unitaire = null;
        }
      }
    },


    /**
     * Supprimer l'émolument (général + detail !)
     */
    removeEmolumentAffaire(emolument_affaire_id) {
      this.$http.delete(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_ENDPOINT + "?emolument_affaire_id=" + emolument_affaire_id + "&affaire_id=" + this.affaire.id,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => {
        if (response && response.data) {
          this.showEmolumentsDialog = false;
          this.getEmolumentsGeneral();
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * on remove emolument
     */
    onRemoveEmolumentAffaire(emolument_affaire_id) {
      this.confirmationRemoveDialog.show = true;
      this.confirmationRemoveDialog.onConfirm = () => {
        this.deleteEmolumentAffaireRepartition(emolument_affaire_id).then(() => {
          this.removeEmolumentAffaire(emolument_affaire_id);
          this.confirmationRemoveDialog.onConfirm = () => {};
          this.confirmationRemoveDialog.onCancel = () => {};
        })
      };
      this.confirmationRemoveDialog.onCancel = () => {
        this.confirmationRemoveDialog.show = false;
        this.confirmationRemoveDialog.onConfirm = () => {};
        this.confirmationRemoveDialog.onCancel = () => {};
      };
    },


    openEmolumentDialog(emolument_affaire_id) {
      this.getEmolumentAffaireRepartition(emolument_affaire_id).then(response => {
        if (response && response.data) {
          this.initFactureRepartition(response.data);
          this.updateFactureRepartition();
        }
      }).catch(err => handleException(err, this));

      this.getEmolumentsDetail(emolument_affaire_id);
    },

    /**
     * get emolument_affaire_repartition
     */
    async getEmolumentAffaireRepartition(emolument_affaire_id) {
      return new Promise ((resolve, reject) => {
        this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_REPARTITION_ENDPOINT + "?emolument_affaire_id=" + emolument_affaire_id,
          {
            withCredentials: true,
            headers: {Accept: "appication/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      })
    },

    /**
     * save emolument_affaire_repartition
     */
    async postEmolumentAffaireRepartition(emolument_affaire_id) {
      let formData = new FormData();
      formData.append("emolument_affaire_id", emolument_affaire_id);
      formData.append("emolument_facture_repartition", JSON.stringify(this.factures_repartition));

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_REPARTITION_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {Accept: "appication/json"}
        }
      ).then(() => {})
      .catch(err => handleException(err, this));
    },

    /**
     * Delete emolument_affaire_repartition
     */
    async deleteEmolumentAffaireRepartition(emolument_affaire_id) {
      return new Promise ((resolve, reject) => {
        this.$http.delete(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_REPARTITION_ENDPOINT + "?emolument_affaire_id=" + emolument_affaire_id,
          {
            withCredentials: true,
            headers: {Accept: "appication/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },

    /**
     * init facture repartition
     */
    initFactureRepartition(emolument_facture_repartition) {
      this.factures_repartition = JSON.parse(JSON.stringify(this.affaire_factures));
      
      if (emolument_facture_repartition.length > 0) {
        // Il existe une/des relations entre l'émolument et les factures
        this.factures_repartition.forEach(x => {
          x.emolument_repartition = 0;
          emolument_facture_repartition.some(y => {
            if (y.facture_id === x.id) {
              x.emolument_repartition = y.repartition;
            }
          });
        });
      } else {
        // Il n'existe pas encore de relation entre l'émolument et les factures
        if (this.factures_repartition.length === 1) {
          this.factures_repartition[0].emolument_repartition = 100;
        } else {
          this.factures_repartition.forEach(x => {
            x.emolument_repartition = 0;
          });
        }
      }
    },

    /**
     * update facture repartition
     */
    updateFactureRepartition() {
      let somme = 0;
      let somme_ = 100;
      this.factures_repartition.forEach(x => {
        somme += Number(x.emolument_repartition);
      });

      if (Math.abs(somme - 100) >= 0.011) {
        this.emolument_facture_repartition_ctrl = true;
        } else {
        this.emolument_facture_repartition_ctrl = false;
        somme_ = somme
      }

      this.factures_repartition.forEach(x => {
        if (Number(x.emolument_repartition) > 0) {
          x.montant_mo = numeral(this.round((Number(this.total.montant_recapitulatif_somme5) * Number(x.emolument_repartition) / somme_), 0.05)).format("0.00");
          x.montant_mat_diff = numeral(this.round((Number(this.total.montant_recapitulatif_matdiff) * Number(x.emolument_repartition) / somme_), 0.05)).format("0.00");
          x.montant_rf = numeral(this.round((Number(this.total.montant_recapitulatif_registre_foncier) * Number(x.emolument_repartition) / somme_), 0.05)).format("0.00");
          x.montant_tva = numeral(this.round((Number(this.total.montant_recapitulatif_tva) * Number(x.emolument_repartition) / somme_), 0.05)).format("0.00");
          x.montant_total = numeral(this.round((Number(this.total.montant_recapitulatif_total) * Number(x.emolument_repartition) / somme_), 0.05)).format("0.00");
        } else {
          x.montant_mo = numeral(0).format("0.00");
          x.montant_mat_diff = numeral(0).format("0.00");
          x.montant_rf = numeral(0).format("0.00");
          x.montant_tva = numeral(0).format("0.00");
          x.montant_total = numeral(0).format("0.00");
        }
      });
    },

    /**
     * Save factures relative to emolument repartitions
     */
    saveToFactures() {
      let promises = [];
      let c = 0;
      let facture_;
      this.factures_repartition.forEach(x => {
        if (Number(x.emolument_repartition) > 0) {
          promises.push(this.putFacture(x));
          
          if (c === 0) {
            facture_ = x;
          }
          c += 1;
        }
      });
      
      let successMessage = "La facture a été mise à jour avec succès."
      if (promises.length > 1) {
        successMessage = "Les factures ont été mises à jour avec succès."
      }

      Promise.all(promises).then(() => {
        this.showEmolumentsDialog = false;
        this.fixEmolumentDefinitively();
        this.$root.$emit("searchAffaireFactures");
        this.$root.$emit("ShowMessage", successMessage);
        if (c === 1) {
          this.$root.$emit("openFacture", facture_);
        }
      }).catch(err => handleException(err, this));
    },

    /**
     * put facture
     */
    async putFacture(facture_data) {
      return new Promise ((resolve, reject) => {
        let montant_tva = this.round(Number(facture_data.montant_mo) * Number(this.form_general.tva_pc) / 100, 0.05) + this.round(Number(facture_data.montant_mat_diff) * Number(this.form_general.tva_pc) / 100, 0.05)
        let montant_total = this.round(Number(facture_data.montant_mo) + Number(facture_data.montant_mat_diff) + Number(facture_data.montant_rf) + Number(montant_tva), 0.05)


        let formData = new FormData();
        formData.append("id", facture_data.id);
        formData.append("montant_mo", facture_data.montant_mo);
        formData.append("montant_mat_diff", facture_data.montant_mat_diff);
        formData.append("montant_rf", facture_data.montant_rf);
        formData.append("montant_tva", montant_tva);
        formData.append("montant_total", montant_total);

        this.$http.put(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => resolve(response))
        .catch(err => reject(err));
      });
    },


    /**
     * on save emoluments repartitions
     */
    onSaveEmolumentsRepartitions() {
      this.confirmationRemoveDialog.title = "Répartition des émoluments dans les factures";
      this.confirmationRemoveDialog.msg = "En cliquant sur 'CONFIRMER', toutes les factures ayant un coefficient de répartition non nul récupéreront les valeurs de ce tableau<br>(si les factures comportaient d'anciennes valeurs, elles seront écrasées).<br>Les factures avec des coefficients nuls ne sont pas modifiées.";
      this.confirmationRemoveDialog.confirmBtn = "Confirmer";
      this.confirmationRemoveDialog.cancelBtn = "Annuler";
      this.confirmationRemoveDialog.onCancel = () => this.confirmationRemoveDialog.show = false;
      this.confirmationRemoveDialog.onConfirm = () => this.saveToFactures();
      this.confirmationRemoveDialog.show = true;
    }
  },

  mounted: function(){
    this.getEmolumentsUnit().then(() => {
      this.getEmolumentsGeneral();
    });
  }
}
</script>

