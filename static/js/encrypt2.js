const { publicKey, privateKey } = await window.crypto.subtle.generateKey(
    {
      name: "RSA-OAEP",
      modulusLength: 2048, // can be 1024, 2048, or 4096
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
      hash: { name: "SHA-256" }, // can be "SHA-1", "SHA-256", "SHA-384", or "SHA-512"
    },
    true, // whether the key is extractable (i.e. can be used in exportKey)
    ["encrypt", "decrypt"] // can be any combination of "encrypt" and "decrypt"
);

async function encryption(data, recipientPublicKey){
    const encryptedData = await window.crypto.subtle.encrypt(
        {
          name: "RSA-OAEP",
        },
        recipientPublicKey, // from generateKey or importKey above
        data // ArrayBuffer of data you want to encrypt
    );

    return encryptedData;
}

async function decryption(encryptedData){

    const decryptedData = await window.crypto.subtle.decrypt(
        {
          name: "RSA-OAEP",
        },
        privateKey, // from generateKey or importKey above
        encryptedData // ArrayBuffer of the data
    );
}