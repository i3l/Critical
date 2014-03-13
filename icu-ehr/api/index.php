<?php

	require_once '../include/DbHandler.php';
	require '.././libs/Slim/Slim.php';
	 
	\Slim\Slim::registerAutoloader();
	 
	$app = new \Slim\Slim();

	function echoResponse($status_code, $response) {
		$app = \Slim\Slim::getInstance();

		$app->status($status_code);
	 
		$app->contentType('application/json');
	 
		echo json_encode($response);
	}
	
	// Patient info
	$app->get('/patient/:id/', function($patient_id) {
            $response = array();
            $db = new DbHandler();
 
           $result = $db->getPatient($patient_id);
			
            if ($result != NULL) {
                echoResponse(200, $result);
            } else {
                $response["error"] = true;
                $response["message"] = "The requested resource doesn't exists";
                echoResponse(404, $response);
            }
        });
	
	$app->get('/patient/:id/stats/', function($patient_id) {
            $response = array();
            $db = new DbHandler();
 
           $result = $db->getAllStats($patient_id);
			
            if ($result != NULL) {
                echoResponse(200, $result);
            } else {
                $response["error"] = true;
                $response["message"] = "The requested resource doesn't exists";
                echoResponse(404, $response);
            }
        });
		
	$app->get('/patient/:id/stats/:stat/', function($patient_id, $stat) {
            $response = array();
            $db = new DbHandler();
 
           $result = $db->getStat($patient_id, $stat);
			
            if ($result != NULL) {
                echoResponse(200, $result);
            } else {
                $response["error"] = true;
                $response["message"] = "The requested resource doesn't exists";
                echoResponse(404, $response);
            }
        });
	
	$app->run();

?>