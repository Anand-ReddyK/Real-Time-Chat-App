async function getOrCreateKeyPair() {
    try {
        // Check if keys are already stored in localStorage
        const storedPublicKeyBase64 = localStorage.getItem("publicKey");
        const storedPrivateKeyBase64 = localStorage.getItem("privateKey");

        if (storedPublicKeyBase64 && storedPrivateKeyBase64) {
            // Keys are present, convert them to ArrayBuffer for importing
            const storedPublicKeyBuffer = Uint8Array.from(atob(storedPublicKeyBase64), char => char.charCodeAt(0)).buffer;
            const storedPrivateKeyBuffer = Uint8Array.from(atob(storedPrivateKeyBase64), char => char.charCodeAt(0)).buffer;

            // Import keys
            const importedPublicKey = await crypto.subtle.importKey(
                'spki',
                storedPublicKeyBuffer,
                {
                    name: 'RSA-OAEP',
                    hash: 'SHA-256',
                },
                false,
                ['encrypt']
            );

            const importedPrivateKey = await crypto.subtle.importKey(
                'pkcs8',
                storedPrivateKeyBuffer,
                {
                    name: 'RSA-OAEP',
                    hash: 'SHA-256',
                },
                false,
                ['decrypt']
            );

            return { importedPublicKey, importedPrivateKey };
        } else {
            // Keys are not present, generate a new key pair
            const keyPair = await crypto.subtle.generateKey(
                {
                    name: 'RSA-OAEP',
                    modulusLength: 2048,
                    publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
                    hash: 'SHA-256',
                },
                true,
                ['encrypt', 'decrypt']
            );

            // Export keys to store
            const publicKeyBuffer = await crypto.subtle.exportKey('spki', keyPair.publicKey);
            const privateKeyBuffer = await crypto.subtle.exportKey('pkcs8', keyPair.privateKey);

            // Convert ArrayBuffer to base64 for storage
            const publicKeyBase64 = btoa(String.fromCharCode.apply(null, new Uint8Array(publicKeyBuffer)));
            const privateKeyBase64 = btoa(String.fromCharCode.apply(null, new Uint8Array(privateKeyBuffer)));

            // Store keys
            localStorage.setItem("publicKey", publicKeyBase64);
            localStorage.setItem("privateKey", privateKeyBase64);

            return keyPair;
        }
    } catch (error) {
        console.error('Error in getOrCreateKeyPair:', error);
        throw error;
    }
}



// Example usage
(async () => {
    const keyPair = await getOrCreateKeyPair();
    console.log('Public Key:', keyPair.importedPublicKey);
    console.log('Private Key:', keyPair.importedPrivateKey);
})();



async function encryptMessage(message, recipientPublicKey) {
    // Convert the recipient's public key from Base64 to ArrayBuffer
    console.log('Recipient public key:', recipientPublicKey);
    const publicKeyBuffer = Uint8Array.from(atob(recipientPublicKey), char => char.charCodeAt(0));

    console.log('Public Key Buffer:', publicKeyBuffer);
    
    // Import the recipient's public key
    const importedPublicKey = await crypto.subtle.importKey(
        'spki',
        publicKeyBuffer,
        {
            name: 'RSA-OAEP',
            hash: 'SHA-256',
        },
        false,
        ['encrypt']
    );

    // Encode the message as UTF-8 and encrypt it with the recipient's public key
    const encoder = new TextEncoder();
    const encryptedMessageBuffer = await crypto.subtle.encrypt(
        {
            name: 'RSA-OAEP',
        },
        importedPublicKey,
        encoder.encode(message)
    );

    // Convert the encrypted message from ArrayBuffer to Base64
    const encryptedMessageBase64 = btoa(String.fromCharCode(...new Uint8Array(encryptedMessageBuffer)));

    return encryptedMessageBase64;
}


async function setupAndSendMessage() {
    const keyPair = await getOrCreateKeyPair();

    // Simulate sending the public key to the recipient (this would happen securely in a real scenario)
    console.log('Key Pair:', keyPair);
    console.log('Recipient public key:', keyPair.importedPublicKey);

    try {
        const recipientPublicKey = await crypto.subtle.exportKey('spki', keyPair.importedPublicKey);
        console.log('Successfully exported recipient public key:', recipientPublicKey);
    } catch (error) {
        console.error('Error exporting recipient public key:', error);
    }



    // Use the sender's private key to decrypt messages (not shown in this example)
    // Keep the private key secure and do not expose it to the server or other users

    // Example: Send an encrypted message
    const message = 'Hello, world!';
    const encryptedMessage = await encryptMessage(message, recipientPublicKey);

    // Now you can send the encryptedMessage to the server
    // ... (your existing code to send the message to the server)

    console.log('Sender public key:', senderKeyPair.publicKey);
    console.log('Sender private key:', senderKeyPair.privateKey);
    console.log('Recipient public key:', recipientPublicKey);
    console.log('Message:', encryptedMessage);
}

setupAndSendMessage();