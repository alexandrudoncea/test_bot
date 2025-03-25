const SmeeClient = require('smee-client');

const smee = new SmeeClient({
  source: 'https://smee.io/ybYJFTBTTflxvP',  // Smee URL
  target: 'http://localhost:5000/webhook',    // Flask bot endpoint
  logger: console
});

const events = smee.start();

console.log("Forwarding GitHub webhooks via Smee...");
