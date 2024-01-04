<style src="./emoluments.css"></style>
<template src="./emoluments.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler';
// import { logAffaireEtape } from '@/services/helper';
const numeral = require("numeral");
const moment = require('moment');

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
        cadastrationFactureNumerosId_old: [],
        chapters: [],
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
        emolument_priorite: true,
        // emolumentsUnits: [],
        facture_parametres : {
          indice_application: null,
          tva_pc: null,
        },
        factures_repartition: [],
        form_general: {}, //général
        form_detail: {}, //emoluments sans bâtiment
        form_detail_batiment: [], //emoluments avec bâtiments
        n_divers: 8,
        pointsMatDiff_nombre: 0,
        showEmolumentsDialog: false,
        showProgressBar: false,
        showSendValuesToFacture: false,
        total: {
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
        },
        tableauEmolumentsNew: [],
        tableauEmolumentsNew_bk: [],
        isPageReady: false,
        id_matdiff: process.env.VUE_APP_TABLEAUEMOLUMENTS_MATDIFF_ID.split(',').map(Number),
        divers_tarif_horaire: [],
        divers_tarif_horaire_unit: {
          nom: null,
          nombre: 1,
          montant: null,
          prix: 0,
        },
        selectedHighlightRow: null,
      }
  },

  methods:{
    async initForm(form_general=true) {

      if (form_general) {
        this.form_general = {
          id: null,
          affaire_id: this.affaire.id,
          pente_pc: 0,
          diff_visibilite_pc: 0,
          trafic_pc: 0,
          zi: 1,
          nb_batiments: 0,
          indice_application: this.facture_parametres.indice_application,
          tva_pc: this.facture_parametres.tva_pc, // %
          remarque: "",
          facture_type_id: 1,
          numeros: [],
          numeros_id: [],
          utilise: false,
  
          // Bâtiments
          batiment_f: [],

        };

        this.divers_tarif_horaire = [];
        this.divers_tarif_horaire.push(JSON.parse(JSON.stringify(this.divers_tarif_horaire_unit)));

        return await this.getTableauEmolumentsNew();
      }
    },


    /**
     * Add batiment
     */
    addBatiment() {
      this.form_general.nb_batiments += 1;

      this.tableauEmolumentsNew.forEach(cat => {
        cat.forEach(scat => {
          scat.forEach(pos => {
            pos.nombre.push(0);
            pos.prix.push(0);
          })
        })
      });
      
      console.log('this.tableauEmolumentsNew', this.tableauEmolumentsNew)
      console.log('this.tableauEmolumentsNew[0][0][0].nombre', this.tableauEmolumentsNew[0][0][0].nombre)
    },

    /**
     * Remove batiment
     */
    removeBatiment(batiment_i) {
      console.log(`removeBatiment(${batiment_i})`)
      
      let tmp = JSON.parse(JSON.stringify(this.tableauEmolumentsNew));
      tmp.forEach(cat => {
        cat.forEach(scat => {
          scat.forEach(pos => {
            pos.nombre.splice(batiment_i, 1);
            pos.prix.splice(batiment_i, 1);
          })
        })
      })
      
      this.tableauEmolumentsNew = tmp;
      
      this.form_general.batiment_f.splice(batiment_i-1,1);
      this.form_general.nb_batiments -= 1;

      this.update_sommesPartielles();
    },


    /**
     * Update batimentCorrectionFactor
     */
    updateBatimentCorrectionFactor() {
      for (let i=0; i<Number(this.form_general.nb_batiments); i++) {
        console.log('updateBatimentCorrectionFactor | still need to be done')
      }

      // this.updateMontants();
    },


    // /** Autocompletion terrain-bureau */
    // terrainBureau_autocompletion(value=true) {
    //   if (this.form_general.utilise || this.disabled) {
    //     return
    //   }

    //   // 2.29 = 2.23 + ... + 2.28
    //   this.form_detail.travauxTerrain25.nombre = 
    //     Number(this.form_detail.travauxTerrain19.nombre) +
    //     Number(this.form_detail.travauxTerrain20.nombre) +
    //     Number(this.form_detail.travauxTerrain21.nombre) +
    //     Number(this.form_detail.travauxTerrain22.nombre) +
    //     Number(this.form_detail.travauxTerrain23.nombre) +
    //     Number(this.form_detail.travauxTerrain24.nombre);
     
        
    //   // 3.31 = 3.11 + 3.115
    //   this.form_detail.travauxMaterialisation9.nombre =
    //     Number(this.form_detail.travauxMaterialisation1.nombre) +
    //     Number(this.form_detail.travauxMaterialisation2.nombre);
      
    //   // 3.33 = 3.18
    //   this.form_detail.travauxMaterialisation11.nombre =
    //     Number(this.form_detail.travauxMaterialisation8.nombre);
      
    //   // 3.34 = 3.115
    //   this.form_detail.travauxMaterialisation12.nombre =
    //     Number(this.form_detail.travauxMaterialisation2.nombre);
      
    //   // 3.35 = 3.11
    //   this.form_detail.travauxMaterialisation13.nombre =
    //     Number(this.form_detail.travauxMaterialisation1.nombre);
      
    //   // 3.36 = 3.17
    //   this.form_detail.travauxMaterialisation14.nombre =
    //     Number(this.form_detail.travauxMaterialisation7.nombre);
      
   
    //   // 4.11 = 2.17 + 2.110 + 2.111 **bat
    //   this.form_detail.travauxBureau1.nombre =
    //     Number(this.form_detail.travauxTerrain9.nombre) +
    //     Number(this.form_detail.travauxTerrain12.nombre) +
    //     Number(this.form_detail.travauxTerrain13.nombre);

    //   // 4.15 = 2.110 **bat
    //   this.form_detail.travauxBureau6.nombre =
    //     Number(this.form_detail.travauxTerrain12.nombre);
      
    //   // 4.31 = 2.31 **bat
    //   if (value===true) {
    //     this.form_detail.travauxBureau13.nombre =
    //       Number(this.form_detail.travauxTerrain15.nombre);
    //   }
      
    //   // 4.32 = 2.32 **bat
    //   this.form_detail.travauxBureau14.nombre =
    //     Number(this.form_detail.travauxTerrain16.nombre);
        
    //   // 4.36 = 4.31 + 4.32 **bat
    //   this.form_detail.travauxBureau18.nombre =
    //     Number(this.form_detail.travauxBureau13.nombre) +
    //     Number(this.form_detail.travauxBureau14.nombre);
        
    //   // 4.21 = 2.23 + 2.24
    //   this.form_detail.travauxBureau28.nombre =
    //     Number(this.form_detail.travauxTerrain19.nombre) +
    //     Number(this.form_detail.travauxTerrain20.nombre);
      
    //   // 4.23 = 2.25 + 2.28
    //   this.form_detail.travauxBureau31.nombre =
    //     Number(this.form_detail.travauxTerrain21.nombre) +
    //     Number(this.form_detail.travauxTerrain24.nombre);

    //   // 4.26 = 2.27
    //   if (value===true) {
    //     this.form_detail.travauxBureau34.nombre =
    //       Number(this.form_detail.travauxTerrain23.nombre);
    //   }

    //   // 4.29 = 2.27
    //   this.form_detail.travauxBureau37.nombre =
    //     Number(this.form_detail.travauxTerrain23.nombre);

    //   // 4.210 = 2.27
    //   if (value===true) {
    //     this.form_detail.travauxBureau38.nombre =
    //       Number(this.form_detail.travauxTerrain23.nombre);
    //   }

    //   // 4.213 = 4.23 + 4.26
    //   this.form_detail.travauxBureau41.nombre =
    //     Number(this.form_detail.travauxBureau31.nombre) +
    //     Number(this.form_detail.travauxBureau34.nombre);
      


    //   // Update nombres avec bâtiments
    //   for (let j=0; j<Number(this.form_general.nb_batiments); j++) {
    //     // 4.11 = 2.17 + 2.110 + 2.111 **bat
    //     this.form_detail_batiment[j].travauxBureau1.nombre =
    //       Number(this.form_detail_batiment[j].travauxTerrain9.nombre) +
    //       Number(this.form_detail_batiment[j].travauxTerrain12.nombre) +
    //       Number(this.form_detail_batiment[j].travauxTerrain13.nombre);
        
    //     // 4.15 = 2.110 **bat
    //     this.form_detail_batiment[j].travauxBureau6.nombre =
    //       Number(this.form_detail_batiment[j].travauxTerrain12.nombre);

    //     // 4.31 = 2.31 **bat
    //     if (value===true) {
    //       this.form_detail_batiment[j].travauxBureau13.nombre =
    //         Number(this.form_detail_batiment[j].travauxTerrain15.nombre);
    //     }
        
    //     // 4.32 = 2.32 **bat
    //     this.form_detail_batiment[j].travauxBureau14.nombre =
    //       Number(this.form_detail_batiment[j].travauxTerrain16.nombre);
          
    //     // 4.36 = 2.31 + 2.32 **bat
    //     this.form_detail_batiment[j].travauxBureau18.nombre =
    //       Number(this.form_detail_batiment[j].travauxBureau13.nombre) +
    //       Number(this.form_detail_batiment[j].travauxBureau14.nombre);
    //   }
      
    // },



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
      
      console.log('postEmolument | ')
      this.showProgressBar = true;

      let formData = new FormData();
      formData.append('form_general', JSON.stringify(this.form_general));
      formData.append('emoluments', JSON.stringify(this.tableauEmolumentsNew));
      formData.append('divers_tarifhoraire', JSON.stringify(this.divers_tarif_horaire));

      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(response => console.log('postEmolument | success ', response))
      .catch(err => handleException(err, this))
      .finally(() => this.showProgressBar = false);
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
          return
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


      // get facture id and check if there are other BF in facture
      let factures = [];
      let numeros_id = [];
      let numeros_id_arr = [];
      this.factures_repartition.filter(x => {
        if (x.numeros_id.some(y => this.form_general.numeros_id.includes(y))) {
          factures.push(x);
          numeros_id_arr.push(x.numeros_id);
          numeros_id.push(...x.numeros_id);
        }
      });
      
      
      // rajouter/retirer les numéros des biens-fonds
      let disappear = this.cadastrationFactureNumerosId_old.filter(y => !this.form_general.numeros_id.includes(y)); // left comparison, shows what disappears
      if (disappear.length > 0) {
        let tmp = [];
        numeros_id_arr.filter(y => {
          if (!y.includes(disappear[0])) {
            tmp.push(...y);
          }
        });

        // update form_general.numeros and form_general.numeros_id
        this.form_general.numeros = [];
        tmp.forEach(y => {
          if (this.numeros_references.length > 0) {
            this.form_general.numeros.push(this.numeros_references.filter(z => z.numero_id === y)[0]);
          }
        });
        this.form_general.numeros_id = tmp;
        numeros_id = tmp;

        // update factures
        factures = factures.filter(y => !y.numeros_id.includes(disappear[0]));
      }
      
      let appear = this.form_general.numeros_id.filter(y => !this.cadastrationFactureNumerosId_old.includes(y)); // left comparison, shows what appears
      if (appear.length > 0) {
        let tmp = [];
        if (this.numeros_references.length > 0) {
          numeros_id.forEach(x => tmp.push(this.numeros_references.filter(y => y.numero_id === x)[0]));
        }
        this.form_general.numeros = tmp;
      }


      // update numeros_id_old
      this.cadastrationFactureNumerosId_old = numeros_id;


      // if only one facture selected, set emolument_repartition 100% automatically
      if (factures.length === 1) {
        let facture = factures[0];
        
        // set facture repartition to 100%
        this.factures_repartition.forEach(x => {
          if (x.numeros_id === facture.numeros_id) {
            x.emolument_repartition = 100;
          } else {
            x.emolument_repartition = 0;
          }
        });

      } else {
        // get facture repartitions if existing
        let sum_check = 0;
        this.factures_repartition.forEach(x => sum_check += x.emolument_repartition);
        if (sum_check <= 0){
          // set all facture repartitions to 0, it should be entered manually
          this.factures_repartition.forEach(x => x.emolument_repartition = 0);
        }
      }

    },

    /**
     * fix emolument definitively
     */
    async fixEmolumentDefinitively(emolument_affaire_id, status=true) {
      let formData = new FormData();
      formData.append("emolument_affaire_id", emolument_affaire_id);
      formData.append("utilise", status);

      this.$http.put(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_AFFAIRE_FREEZE_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"}
        }
      ).then(() => {})
      .catch(err => handleException(err, this));
    },
    
    





    


    async openEmolumentDialog(emolument_affaire_id) {
      console.log('openEmolumentDialog | emolument_affaire_id', emolument_affaire_id)
      await this.getEmolument(emolument_affaire_id);
      this.emolument_priorite = true;
      console.log('openEmolumentDialog | do something with getEmolumentAffaireRepartition')
      // this.getEmolumentAffaireRepartition(emolument_affaire_id).then(response => {
      //   if (response && response.data) {
      //     this.initFactureRepartition(response.data);
      //     this.updateFactureRepartition();
      //   }
      // }).catch(err => handleException(err, this));

      // this.getEmolumentsDetail(emolument_affaire_id);
      this.showEmolumentsDialog = true;
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
    async saveToFactures() {
      this.postEmolument().then((response_id) => {
        this.form_general.id = response_id;

        let promises = [];
        this.factures_repartition.forEach(x => {
          if (Number(x.emolument_repartition) > 0) {
            promises.push(this.putFacture(x));
          }
        });
        
        let successMessage = "La facture a été mise à jour avec succès."
        if (promises.length > 1) {
          successMessage = "Les factures ont été mises à jour avec succès."
        }
  
        Promise.all(promises).then(() => {
          this.showEmolumentsDialog = false;
          this.fixEmolumentDefinitively(response_id, true);
          this.$root.$emit("searchAffaireFactures");
          this.$root.$emit("ShowMessage", successMessage);
          this.getEmolumentsGeneral();
        }).catch(err => handleException(err, this));
      });
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
        formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));
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
    },

    /**
     * Download emoluments pdf
     */
    async downloadEmoluments() {
      // show the entire table
      let last_emolument_priorite = false;
      if (this.emolument_priorite === true) {
        last_emolument_priorite = true;
        this.emolument_priorite = false;
      }

      // tableau emoluments
      let tableau_emoluments_html = JSON.parse(JSON.stringify(document.getElementById("tableau_emoluments").outerHTML));
      let inputs = tableau_emoluments_html.matchAll(/(md-input-)\w+/g);
      let value = 0;
      for (const input of inputs) {
        value = document.getElementById(input[0]).value;
        if (Number(value) === 0) {
          tableau_emoluments_html = tableau_emoluments_html.replaceAll(new RegExp(`<input.*(${input[0]}).*?>`, 'g'), '<div class="alignCenter"></div>');
        } else {
          tableau_emoluments_html = tableau_emoluments_html.replaceAll(new RegExp(`<input.*(${input[0]}).*?>`, 'g'), '<div class="alignCenter">' + value + '</div>');
        }
      }
      // remove 1st column with chapter name, adapt colspan of headers and correct display when 'CHF' is located after end of div
      tableau_emoluments_html = tableau_emoluments_html.replaceAll(/<(t[dh][^<>]+?chapter.*?)>*<\/t[dh]>/g, "");
      tableau_emoluments_html = tableau_emoluments_html.replaceAll('colspan="7"', 'colspan="6"');
      tableau_emoluments_html = tableau_emoluments_html.replaceAll(/<\/div>CHF/g, "CHF</div>");
      tableau_emoluments_html = tableau_emoluments_html.replaceAll('<div class="alignCenter">CHF</div>', '<div class="alignCenter"></div>');
      tableau_emoluments_html = tableau_emoluments_html.replaceAll('Nombre', 'Qté');
      
      
      // tableau recapitulatif
      let tableau_recapitulatif_html = JSON.parse(JSON.stringify(document.getElementById("tableau_recapitulatif_form").outerHTML));
      inputs = tableau_recapitulatif_html.matchAll(/(md-input-)\w+/g);
      for (const input of inputs) {
        tableau_recapitulatif_html = tableau_recapitulatif_html.replaceAll(new RegExp(`<input.*(${input[0]}).*?>`, 'g'), '<div class="alignCenter">' + document.getElementById(input[0]).value + '</div>');
      }
      tableau_recapitulatif_html = tableau_recapitulatif_html.replaceAll(/<\/div>%/g, " %</div>");
      
      let formData = new FormData();
      formData.append('tableau_emoluments_id', this.form_general.id);
      formData.append('affaire_id', this.affaire.id);
      formData.append('tableau_emoluments_html', tableau_emoluments_html);
      formData.append('tableau_recapitulatif_html', tableau_recapitulatif_html);
      
      this.$http.post(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_EXPORT_EMOLUMENTS_PDF_ENDPOINT,
        formData,
        {
          withCredentials: true,
          headers: {"Accept": "application/json"},
          responseType: "blob"
        }
        ).then((response) => {
        let fileURL = window.URL.createObjectURL(new Blob([response.data]));
        let fileLink = document.createElement('a');
      
        fileLink.href = fileURL;
        let header_content_type = response.headers['content-type'];
        let filename = undefined;
        for (let item of header_content_type.split(';')){
          item = item.trim(); 
          if (item.startsWith('filename=')) {
            filename = item.replace('filename=', '').replaceAll('"', '');
            break
          }
        }
        fileLink.setAttribute('download', filename);
        document.body.appendChild(fileLink);
        fileLink.click();
      }).catch(err => {
        handleException(err, this);
      }).finally(() => {
        this.emolument_priorite = last_emolument_priorite;
      });
    },
    
    /**
     * update emolument_affaire used
     */
    updateUsed() {
      this.fixEmolumentDefinitively(this.form_general.id, this.form_general.utilise);
      this.disabled = this.form_general.utilise;
    },


// ================================================================================================================================================
// ================================================================================================================================================
//                  NEW EMOLUMENTS
// ================================================================================================================================================
// ================================================================================================================================================



   /**
    * Get facture parametres
    */
   async getFactureParametres() {
     this.$http.get(
       process.env.VUE_APP_API_URL + process.env.VUE_APP_FACTURE_PARAMETRES_ENDPOINT,
       {
         withCredentials: true,
         headers: {"Accept": "application/json"}
        }
        ).then(response => {
          if(response && response.data) {
            this.facture_parametres  = response.data.facture_parametres;
            this.isPageReady = true;
          }
        })
        .catch(err => handleException(err, this)); 
      },

    /**
     * Get empty table of emoluments
     */
    async getTableauEmolumentsNew() {
       return this.$http.get(
         process.env.VUE_APP_API_URL + "/tableau_emoluments_new",
         {
           withCredentials: true,
           headers: {"Accept": "application/json"}
          }
          ).then(response => {
            if(response && response.data) {
              let tmp = response.data;
              tmp.forEach(cat => {
                cat.forEach(scat => {
                  scat.forEach(pos => {
                    pos.prix = [0];
                    pos.nombre = [0];
                  })
                })
            });
              
            this.tableauEmolumentsNew_bk = tmp;
            this.tableauEmolumentsNew = JSON.parse(JSON.stringify(this.tableauEmolumentsNew_bk));
            
          }
      })
      .catch(err => handleException(err, this)); 
    },

    /**
     * Get emoluments
     */
    async getEmolument(emolument_affaire_id) {
       return this.$http.get(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT + '?emolument_affaire_id=' + emolument_affaire_id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            
            this.form_general = JSON.parse(response.data.form_general);
            this.tableauEmolumentsNew_bk = JSON.parse(response.data.emoluments);
            this.tableauEmolumentsNew = JSON.parse(JSON.stringify(this.tableauEmolumentsNew_bk));
            this.divers_tarif_horaire = JSON.parse(response.data.divers_tarifhoraire);

            // this.initFactureRepartition(response.data);
            // this.updateFactureRepartition();

            console.log('getEmoluments | this.tableauEmolumentsNew', this.tableauEmolumentsNew)

            this.update_sommesPartielles();
          }
      })
      .catch(err => handleException(err, this));
    },

    confirmDelete(emolument_affaire_id) {
      this.confirmationRemoveDialog.show = true;
      this.confirmationRemoveDialog.onConfirm = () => this.deleteEmolument(emolument_affaire_id);
    },

    async deleteEmolument(emolument_affaire_id) {
      return this.$http.delete(
          process.env.VUE_APP_API_URL + process.env.VUE_APP_EMOLUMENT_ENDPOINT + '?emolument_affaire_id=' + emolument_affaire_id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        ).then(response => {
          if (response && response.data) {
            this.getEmolumentsGeneral();
            this.showEmolumentsDialog = false;
          }
        })
        .catch(err => handleException(err, this));
    },

    handleUpdateEmolument(position, idx) {
      this.updateMontant(position, idx);
      this.automaticUpdateNombres();
      this.update_sommesPartielles();
    },


    updateMontant(position, idx) {
      let f = 1;
      if (idx > 0) {
        f = Number(this.form_general.batiment_f[idx-1]);
      }
      position.prix[idx] = this.round(f * Number(position.nombre[idx]) * Number(position.montant), 0.05);
    },

    automaticUpdateNombres() {
      let base = [];
      let tmp = JSON.parse(JSON.stringify(this.tableauEmolumentsNew));
      this.tableauEmolumentsNew.forEach(cat=> {
        cat.forEach(scat => {
          scat.forEach(pos => {
            if (pos.calcul_auto) {
              base = pos.calcul_auto.split('+');
              for (let i=0; i<this.form_general.nb_batiments+1; i++) {
                pos.nombre[i] = tmp.reduce((partialSum, a) => partialSum + a.reduce((partialSum, a) => partialSum + a.reduce((partialSum, a) => partialSum + (base.includes(a.id_html)? Number(a.nombre[i]): 0), 0), 0), 0);
                this.updateMontant(pos, i);
              }
            }
          })
        })
      })
    },

    update_sommesPartielles() {
      //sommes partielles du tableau récapitulatif
      this.total.montant_recapitulatif_mandat = 0;
      this.total.montant_recapitulatif_somme1 = 0;
      this.total.montant_recapitulatif_terrain_materialisation_deplacements = 0;
      this.total.montant_recapitulatif_somme2 = 0;
      this.total.montant_recapitulatif_bureau = 0;
      this.total.montant_recapitulatif_somme3 = 0;
      this.total.montant_recapitulatif_indice_application = 0;
      this.total.montant_recapitulatif_somme4 = 0;
      this.total.montant_recapitulatif_materiel_divers = 0;
      this.total.montant_recapitulatif_somme5 = 0;
      this.total.montant_recapitulatif_matdiff = 0;
      this.total.montant_recapitulatif_somme6 = 0;
      this.total.montant_recapitulatif_tva = 0;
      this.total.montant_recapitulatif_somme7 = 0;
      this.total.montant_recapitulatif_registre_foncier = 0;

      // let pos_cat_scat = ''
      this.tableauEmolumentsNew.forEach(cat => {
        cat.forEach(scat => {
          scat.forEach(pos => {
            // mandat (cat 1)
            if (pos.categorie_id === 1) {
              this.total.montant_recapitulatif_mandat += pos.prix.reduce((partialSum, a) => partialSum + a, 0);
              return;
            }

            // travaux terrain (cat 2 + cat 3.1, 3.2, 3.5)
            if ([2, 5].includes(pos.categorie_id) || (pos.categorie_id === 3 && [1, 2, 5].includes(pos.sous_categorie_id))) {
              this.total.montant_recapitulatif_terrain_materialisation_deplacements += pos.prix.reduce((partialSum, a) => partialSum + a, 0);
              return;
            }

            // travaux bureau (cat 4)
            if (pos.categorie_id === 4) {
              this.total.montant_recapitulatif_bureau += pos.prix.reduce((partialSum, a) => partialSum + a, 0);
              return;
            }

            // matériel (cat 3.3)
            if ((pos.categorie_id === 3 && pos.sous_categorie_id === 3) || pos.categorie_id === 6) {
              this.total.montant_recapitulatif_materiel_divers += pos.prix.reduce((partialSum, a) => partialSum + a, 0);
              return;
            }

            // mat diff (cat 3.4)
            if (pos.categorie_id === 3 && pos.sous_categorie_id === 4) {
              this.total.montant_recapitulatif_matdiff += pos.prix.reduce((partialSum, a) => partialSum + a, 0);
              return;
            }

            // RF (cat 7)
            if (pos.categorie_id === 7) {
              this.total.montant_recapitulatif_registre_foncier += pos.prix.reduce((partialSum, a) => partialSum + a, 0);
              return;
            }

            // pos not used if any ?
            console.error(` ${pos.id} - ${pos.id_html} - ${pos.nom} /!\\  update_sommesPartielles | not used position: pos=`, pos);
          })
        })
      });

      // add divers_tarif_horaire to corresponding sum
      this.total.montant_recapitulatif_materiel_divers += this.divers_tarif_horaire.reduce((partialSum, a) => partialSum + a.prix, 0);
      this.total.montant_recapitulatif_somme1 = this.total.montant_recapitulatif_mandat;
      this.total.montant_recapitulatif_somme2 = this.total.montant_recapitulatif_somme1 + this.total.montant_recapitulatif_terrain_materialisation_deplacements;
      this.total.montant_recapitulatif_somme3 = this.total.montant_recapitulatif_somme2 + this.total.montant_recapitulatif_bureau;
      this.total.montant_recapitulatif_indice_application = this.round(this.total.montant_recapitulatif_somme3 * (this.form_general.indice_application-1), 0.05);
      this.total.montant_recapitulatif_somme4 = this.total.montant_recapitulatif_somme3 + this.total.montant_recapitulatif_indice_application;
      this.total.montant_recapitulatif_somme5 = this.total.montant_recapitulatif_somme4 + this.total.montant_recapitulatif_materiel_divers;
      this.total.montant_recapitulatif_somme6 = this.total.montant_recapitulatif_somme5 + this.total.montant_recapitulatif_matdiff;
      this.total.montant_recapitulatif_tva = this.round(this.total.montant_recapitulatif_somme6 * this.form_general.tva_pc/100, 0.05);
      this.total.montant_recapitulatif_somme7 = this.total.montant_recapitulatif_somme6 + this.total.montant_recapitulatif_tva;
      this.total.montant_recapitulatif_total = this.total.montant_recapitulatif_somme7 + this.total.montant_recapitulatif_registre_foncier;

    },

    addDivers() {
      this.divers_tarif_horaire.push(JSON.parse(JSON.stringify(this.divers_tarif_horaire_unit)));
    },

    updateMatDiffNumber(position) {
      console.log('updateMatDiffNumber | position', position)
      if (position.id == this.id_matdiff[0]) {
        console.log('updateMatDiffNumber | position is matdiff', position)
        let tmp = Number(position.nombre[0]);
        console.log('tmp', tmp)

        let tmp_5 = 0;
        let tmp_10 = 0;
        let tmp_15 = 0;
        let tmp_gt15 = 0;
        let c = 1;
        while (tmp > 0) {
          if (c <= 5) {
            // de 1 à 5 points
            tmp_5 += 1;
          } else if (c <= 10) {
            // de 6 à 10 points
            tmp_10 += 1;
          } else if (c <= 15) {
            // de 11 à 15 points
            tmp_15 += 1;
          } else {
            // plus de 16 points
            tmp_gt15 += 1;
          }

          tmp -= 1;
          c += 1;
        }

        console.log('matdiff | tmp_5', tmp_5, 'tmp_10', tmp_10, 'tmp_15', tmp_15, 'tmp_gt15', tmp_gt15)

        this.tableauEmolumentsNew.forEach(cat => {
          cat.forEach(scat => {
            scat.forEach(pos => {
              if (pos.id === this.id_matdiff[0]) {pos.nombre[0] = tmp_5; this.updateMontant(pos, 0)}
              if (pos.id === this.id_matdiff[1]) {pos.nombre[0] = tmp_10; this.updateMontant(pos, 0)}
              if (pos.id === this.id_matdiff[2]) {pos.nombre[0] = tmp_15; this.updateMontant(pos, 0)}
              if (pos.id === this.id_matdiff[3]) {pos.nombre[0] = tmp_gt15; this.updateMontant(pos, 0)}
            })
          })
        });
      }
    },
    
    highlithtSelectedRow(position_id) {
      this.selectedHighlightRow = position_id;
    }
  },

  mounted: function(){
    this.getEmolumentsGeneral();
    this.getTableauEmolumentsNew();
    this.getFactureParametres();

    this.addDivers();
    
    // this.getEmolumentsUnit().then(() => {
    //   this.getEmolumentsGeneral();
    // });

    this.$root.$on("getEmolumentsGeneral", () => this.getEmolumentsGeneral());
  }
}
</script>

