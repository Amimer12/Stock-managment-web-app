const wilayaToAgences = {
  'Alger': [
    'Sacré-Cœur',
    'Agence de Birkhadem',
    'Agence de Bordj El Kiffan',
    'Agence de Reghaia',
    'Agence de Aïn Benian',
    'Agence de Zeralda',
    'Agence de Cheraga',
    'Agence de Draria'
  ],
  'Bejaia': [
    'Agence de Bejaia',
    'Agence de Souk El Tenine',
    'Agence de Akbou',
    'Agence de El Kseur'
  ],
  'Tlemcen': [
    'Agence de Tlemcen',
    'Agence de Hennaya',
    'Agence de Maghnia',
    'Agence de Mansourah'
  ],
  'Oran': [
    'Cite Djamel',
    'Saint Hubert',
    'Agence Fernand Ville',
    'El Morchid',
    'Agence Arzew'
  ],
  'Biskra': [
    'Agence de Biskra',
    'Agence de Ouled Djellal',
    'Agence de Tolga'
  ],
  'Bouira': [
    'Agence de Bouira',
    'Agence de Lakhdaria',
    'Agence de Sour El Ghouzlane'
  ],
  'Setif': [
    'Agence de Ain Oulmene',
    'Agence de El Eulma',
    'Agence de Setif'
  ],
  'Tizi Ouzou': [
    'Agence de Tizi Ouzou',
    'Agence de Tizi Gheniff',
    'Agence de Azazga'
  ],
  'Adrar': [
    'Agence de Adrar',
    'Agence de Timimoun'
  ],
  'Tiaret': [
    'Agence de Frenda',
    'Agence de Tiaret'
  ],
  'Djelfa': [
    'Agence de Ain Oussara',
    'Agence de Djelfa'
  ],
  'Tamanrasset': [
    'Agence de Tamanrasset',
    'Agence de In Salah'
  ],
  'Tebessa': [
    'Agence de Tebessa',
    'Agence de Bir El Ater'
  ],
  'Chlef': [
    'Agence de Chlef',
    'Agence de Tenes'
  ],
  'Blida': [
    'Agence de Blida',
    'Agence de Boufarik'
  ],
  'Bechar': [
    'Agence de Bechar'
  ],
  'El Bayadh': [
    'Agence de El Bayadh'
  ],
  'Illizi': [
    'Agence de Illizi'
  ],
  'Touggourt': [
    'Agence de Touggourt' // Also appears under Ouargla
  ],
  'Bordj Bou Arreridj': [
    'Agence de Bordj Bou Arreridj'
  ],
  'Batna': [
    'Agence de Batna',
    'Agence de Barika'
  ],
  'Jijel': [
    'Agence de Jijel',
    'Agence de Taher'
  ],
  'Msila': [
    'Agence de Berhoum',
    'Agence de Bou Saada',
    'Agence de Msila'
  ],
  'Saida': [
    'Agence de Saida'
  ],
  'Medea': [
    'Agence de Medea'
  ],
  'Tindouf': [
    'Agence de Tindouf'
  ],
  'Khenchela': [
    'Agence de Khenchela'
  ],
  'Tipaza': [
    'Agence de Tipaza'
  ],
  'Souk Ahras': [
    'Agence de Souk Ahras'
  ],
  'Tissemsilt': [
    'Agence de Tissemsilt'
  ],
  'Mostaganem': [
    'Agence de Mostaganem'
  ],
  'Relizane': [
    'Agence de Relizane'
  ],
  'Mascara': [
    'Agence de Mascara'
  ],
  'Sidi Bel Abbes': [
    'Agence de Sidi Bel Abbes'
  ],
  'Skikda': [
    'Agence de Azzaba',
    'Agence de Collo',
    'Agence de El Harrouch',
    'Agence de Skikda'
  ],
  'Annaba': [
    'Agence de El Bouni',
    'Agence de Annaba'
  ],
  'Mila': [
    'Agence de Mila',
    'Agence de Chelghoum Laid'
  ],
  'Ain Defla': [
    'Agence de Ain Defla',
    'Agence de Khemis Miliana'
  ],
  'Naama': [
    'Agence de Naama',
    'Agence de Mecheria'
  ],
  'Guelma': [
    'Agence de Guelma',
    'Agence de Oued Zenati'
  ],
  'Constantine': [
    'Agence de Constantine',
    'Agence de El Khroub'
  ],
  'Ouargla': [
    'Agence de Ouargla',
    'Agence de Hassi Messaoud',
    'Agence de Touggourt' // Same commune name under both wilayas
  ],
  'El Oued': [
    'Agence de El Oued',
    'Agence de El M\'Ghair',
    'Agence de Djamaa'
  ],
  'Boumerdes': [
    'Agence de Boumerdes',
    'Agence de Bordj Menaiel'
  ],
  'Ghardaia': [
    'Agence de El Menia',
    'Agence de Ghardaia',
    'Agence de Metlili'
  ],
  'El Tarf': [
    'Agence de El Tarf',
    'Agence de Ben Mehidi'
  ],
  'Ain Temouchent': [
    'Agence de Ain Temouchent',
    'Agence de Hammam Bouhadjar'
  ],
  'Laghouat': [
    'Agence de Laghouat',
    'Agence de Aflou'
  ],
  'Oum El Bouaghi': [
    'Agence de Oum El Bouaghi',
    'Agence de Ain Mlila'
  ]
};
window.addEventListener('DOMContentLoaded', function () {
    const wilayaSelect = document.getElementById('id_wilaya');
    const communeSelect = document.getElementById('id_Bureau_Yalidine');
    const typeLivraison = document.getElementById('id_type_livraison');
    const adresseInput = document.getElementById('id_Adresse_livraison');
  console.log(wilayaSelect, communeSelect, typeLivraison, adresseInput);
    function updateLivraisonFields() {
    // Always keep both fields enabled and do not clear their values
    if (!typeLivraison || !communeSelect || !adresseInput) return;
    communeSelect.disabled = false;
    adresseInput.disabled = false;
}

    function updateCommunes() {
        const wilaya = wilayaSelect.value;
        const selectedCommune = communeSelect.value;

        // Clear existing options
        communeSelect.innerHTML = '<option value="">---------</option>';

        if (wilayaToAgences[wilaya]) {
            wilayaToAgences[wilaya].forEach(function (commune) {
                const opt = document.createElement('option');
                opt.value = commune;
                opt.text = commune;
                communeSelect.appendChild(opt);
            });

            // Restore selection if it existed
            communeSelect.value = selectedCommune;
        }

        // Apply disable logic again after repopulating
        updateLivraisonFields();
    }

    // Initial execution
    if (wilayaSelect && communeSelect && typeLivraison && adresseInput) {
        updateLivraisonFields(); // disable/enable appropriately
        updateCommunes();        // fill commune list and respect selection

        typeLivraison.addEventListener('change', updateLivraisonFields);
        wilayaSelect.addEventListener('change', updateCommunes);

        // If using jQuery (e.g., with Select2)
        if (window.jQuery) {
            window.jQuery(typeLivraison).on('change', updateLivraisonFields);
            window.jQuery(wilayaSelect).on('change', updateCommunes);
        }
    }
});
