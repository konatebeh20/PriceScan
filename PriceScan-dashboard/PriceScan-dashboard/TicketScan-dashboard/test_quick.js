// Test rapide de l'API des magasins
console.log('🧪 Test rapide...');

// Créer un magasin de test
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

fetch('http://localhost:5000/api/stores', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(testStore)
})
.then(response => response.json())
.then(result => {
  console.log(' Magasin créé:', result);
  
  // Vérifier la liste
  return fetch('http://localhost:5000/api/stores');
})
.then(response => response.json())
.then(stores => {
  console.log(' Total magasins:', stores.length);
  stores.forEach(s => console.log('-', s.store_name, s.store_city));
})
.catch(error => console.error(' Erreur:', error));
