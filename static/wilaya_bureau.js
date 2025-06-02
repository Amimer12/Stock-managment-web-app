const wilayaToAgences = {
  'Alger': [
    'Sacre-Coeur',
    'Agence de Birkhadem',
    'Agence de Bordj El Kiffan',
    'Agence de Reghaia',
    'Agence de Ain Benian',
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
    'Agence de Touggourt'
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
    'Agence de Touggourt'
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
    const bureauSelect = document.getElementById('id_Bureau');
    const typeLivraison = document.getElementById('id_type_livraison');
    const adresseInput = document.getElementById('id_Adresse_livraison');

    function updateLivraisonFields() {
        if (!typeLivraison || !bureauSelect || !adresseInput) return;

        const type = typeLivraison.value.toLowerCase();

        if (type === 'domicile') {
            bureauSelect.disabled = true;
            bureauSelect.value = ''; // clear selection
            adresseInput.disabled = false;
        } else if (type === 'bureau') {
            adresseInput.disabled = true;
            adresseInput.value = ''; // clear address
            bureauSelect.disabled = false;
        } else {
            bureauSelect.disabled = true;
            bureauSelect.value = '';
            adresseInput.disabled = true;
            adresseInput.value = '';
        }

        // Force redraw (for some widgets or select2)
        bureauSelect.dispatchEvent(new Event('change'));
        adresseInput.dispatchEvent(new Event('change'));
    }

    function updateBureaux() {
        const wilaya = wilayaSelect.value;
        const selectedBureau = bureauSelect.value;

        // Clear existing options
        bureauSelect.innerHTML = '<option value="">---------</option>';

        if (wilayaToAgences[wilaya]) {
            wilayaToAgences[wilaya].forEach(function (bureau) {
                const opt = document.createElement('option');
                opt.value = bureau;
                opt.text = bureau;
                bureauSelect.appendChild(opt);
            });

            // Restore selection if it existed
            bureauSelect.value = selectedBureau;
        }

        // Apply disable logic again after repopulating
        updateLivraisonFields();
    }

    // Initial execution
    if (wilayaSelect && bureauSelect && typeLivraison && adresseInput) {
        updateLivraisonFields(); // disable/enable appropriately
        updateBureaux();         // fill bureau list and respect selection

        typeLivraison.addEventListener('change', function () {
            updateLivraisonFields();
        });

        wilayaSelect.addEventListener('change', function () {
            updateBureaux();
        });

        // If using jQuery (Select2 or similar)
        if (window.jQuery) {
            window.jQuery(typeLivraison).on('change', updateLivraisonFields);
            window.jQuery(wilayaSelect).on('change', updateBureaux);
        }
    }
});
