// Test simple de l'API des magasins
console.log('🧪 Test simple de l\'API des magasins...');

// Test 1: Récupérer tous les magasins
fetch('http://localhost:5000/api/stores')
  .then(response => response.json())
  .then(stores => {
    console.log(' Magasins récupérés:', stores.length);
    stores.forEach((store, index) => {
      console.log(`${index + 1}. ${store.store_name} - ${store.store_city}`);
    });
  })
  .catch(error => {
    console.error(' Erreur:', error);
  });

// Test 2: Créer un magasin de test
const testStore = {
  store_name: 'Magasin Test ' + Date.now(),
  store_type: 'autre',
  store_address: '123 Rue Test',
  store_city: 'Abidjan',
  store_country: 'Côte d\'Ivoire',
  store_phone: '+225 27222444',
  store_email: 'test@magasin.ci',
  store_description: 'Magasin de test'
};

console.log('\n Création d\'un magasin de test...');
console.log('Données:', testStore);

fetch('http://localhost:5000/api/stores', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(testStore)
})
.then(response => response.json())
.then(result => {
  console.log(' Magasin créé:', result);
})
.catch(error => {
  console.error(' Erreur création:', error);
});
