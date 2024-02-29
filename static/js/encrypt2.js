// Example function to encrypt a message
async function encryptMessage(message, sharedKey) {
  // Import the sharedKey as a CryptoKey object
  sharedKey = await crypto.subtle.importKey('raw', sharedKey, { name: 'AES-GCM' }, false, ['encrypt']);

  let encoder = new TextEncoder();
  let data = encoder.encode(message);
  let iv = crypto.getRandomValues(new Uint8Array(12)); // Initialization vector
  let cipher = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, sharedKey, data);
  return { iv: iv, data: new Uint8Array(cipher) }; // Return an object containing both IV and encrypted data
}

// Example function to decrypt a message
async function decryptMessage(encryptedMessage, sharedKey) {
  // Import the sharedKey as a CryptoKey object
  sharedKey = await crypto.subtle.importKey('raw', sharedKey, { name: 'AES-GCM' }, false, ['decrypt']);

  let decryptedData = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: encryptedMessage.iv }, sharedKey, encryptedMessage.data);
  let decoder = new TextDecoder();
  return decoder.decode(decryptedData);
}

// Example usage
let message = 'Hello, world!';
encryptMessage(message, sharedKey).then(encryptedMessage => {
  console.log('Encrypted message:', encryptedMessage);
  
  // Assuming encryptedMessage is received from the server
  decryptMessage(encryptedMessage, sharedKey).then(decryptedMessage => {
      console.log('Decrypted message:', decryptedMessage);
  }).catch(error => {
      console.error('Decryption error:', error);
  });
}).catch(error => {
  console.error('Encryption error:', error);
});
