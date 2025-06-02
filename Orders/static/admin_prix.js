document.addEventListener('DOMContentLoaded', function () {
    console.log('[DEBUG] Script loaded ✅');

    const produitSelect = document.getElementById('id_produit_commandé');
    const quantiteInput = document.getElementById('id_quantite_commandé');
    const typeLivraisonSelect = document.getElementById('id_type_livraison');
    const wilayaSelect = document.getElementById('id_wilaya');

    if (!produitSelect || !quantiteInput || !typeLivraisonSelect || !wilayaSelect) {
        console.warn('[DEBUG] One or more elements not found');
        return;
    }

    function getPrixLivraison(type, wilaya) {
        const isDomicile = type.toLowerCase() === 'domicile';
        const isBureau = type.toLowerCase() === 'bureau';

        if (isDomicile) {
            if (wilaya === 'Alger') return 500;
            if (['Blida', 'Tipaza', 'Boumerdes'].includes(wilaya)) return 600;
            if (['Biskra', 'Djelfa', 'Ghardaia', 'El Oued', 'El Mghair', 'El Menia', 'Ouargla', 'Ouled Djellal', 'Touggourt', 'Tebessa', 'Laghouat'].includes(wilaya)) return 900;
            if (['Bechar', 'Naama', 'El Bayadh', 'Beni Abbes', 'Adrar'].includes(wilaya)) return 1400;
            if (['Tamanrasset', 'Tindouf', 'Timimoun', 'Illizi'].includes(wilaya)) return 1600;
            return 700;
        }

        if (isBureau) {
            if (wilaya === 'Alger') return 400;
            if (['Blida', 'Tipaza', 'Boumerdes'].includes(wilaya)) return 500;
            if (['Biskra', 'Djelfa', 'Ghardaia', 'El Oued', 'El Mghair', 'El Menia', 'Ouargla', 'Ouled Djellal', 'Touggourt', 'Tebessa', 'Laghouat'].includes(wilaya)) return 650;
            if (['Bechar', 'Naama', 'El Bayadh', 'Beni Abbes', 'Adrar'].includes(wilaya)) return 1000;
            if (['Tamanrasset', 'Tindouf', 'Timimoun', 'Illizi'].includes(wilaya)) return 1400;
            return 550;
        }

        return 0;
    }

    function setDisplayValue(field, value) {
        const container = document.querySelector(`.form-group.field-${field}`);
        if (!container) {
            console.warn(`[DEBUG] Container not found for ${field}`);
            return;
        }

        const display = container.querySelector('.readonly');
        if (!display) {
            console.warn(`[DEBUG] .readonly not found in ${field}`);
            return;
        }

        display.textContent = `${value} DZD`;
        console.log(`[DEBUG] Updated ${field}: ${value} DZD`);
    }

    function getPrixProduit(callback) {
        const variantId = produitSelect.value;
        if (!variantId) {
            callback(0);
            return;
        }

        fetch(`/variants/get-product-price/${variantId}/`)
            .then(response => response.json())
            .then(data => {
                callback(parseFloat(data.price || 0));
            })
            .catch(error => {
                console.error('[DEBUG] Failed to fetch product price', error);
                callback(0);
            });
    }

    function updatePrix() {
        console.log('[DEBUG] updatePrix triggered');

        const quantite = parseInt(quantiteInput.value) || 1;
        const wilaya = wilayaSelect.value;
        const livraisonType = typeLivraisonSelect.options[typeLivraisonSelect.selectedIndex]?.text || '';

        getPrixProduit(prixProduit => {
            const prixLivraison = getPrixLivraison(livraisonType, wilaya);
            const prixTotal = quantite * prixProduit + prixLivraison;

            setDisplayValue('prix_livraison_dzd', prixLivraison);
            setDisplayValue('prix_total_dzd', prixTotal);

            console.log('[DEBUG] Prix recalculated:', { prixProduit, quantite, prixLivraison, prixTotal });
        });
    }

    // jQuery Select2-compatible and native handlers
    $(document).ready(function () {
        console.log('[DEBUG] jQuery + DOM loaded ✅');

        updatePrix(); // Initial run

        quantiteInput.addEventListener('input', updatePrix);
        produitSelect.addEventListener('change', updatePrix);
        typeLivraisonSelect.addEventListener('change', updatePrix);
        wilayaSelect.addEventListener('change', updatePrix);

        $('#id_produit_commandé').on('change.select2', updatePrix);
        $('#id_type_livraison').on('change.select2', updatePrix);
        $('#id_wilaya').on('change.select2', updatePrix);

        console.log('[DEBUG] Event listeners attached.');
    });
});
