<?php
// extract injected service details from environment
$services_json = getenv("VCAP_SERVICES");
$services = json_decode($services_json);
$service_uri = $services->{'Echo Service'}[0]->{'credentials'}->{'uri'};
var_dump($service_uri);
 
// create a message to send
$message = '{"message": "Hello CloudFoundry!"}';
 
// setup and execute the cURL call to the echo service
$curl = curl_init($service_uri);
curl_setopt($curl, CURLOPT_HEADER, false);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPHEADER, array("Content-type: application/json"));
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $message);
$response = curl_exec($curl);
 
// handle non-200 response
$status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
if ( $status != 200 ) {
    die("Error: call to URL $url failed with status $status, response $response, curl_error " . curl_error($curl) . ", curl_errno " . curl_errno($curl));
}
 
// clean up cURL connection
curl_close($curl);
 
// decode response and output
$response_as_json = json_decode($response);
var_dump($response_as_json);
?>
