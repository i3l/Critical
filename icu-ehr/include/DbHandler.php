<?php
 
class DbHandler {
 
    private $conn;
 
    function __construct() {
        require_once dirname(__FILE__) . '/DbConnect.php';

        $db = new DbConnect();
        $this->conn = $db->connect();
    }
	
	function db_bind_array($stmt, &$row)
	{
		$md = $stmt->result_metadata();
		$params = array();
		while($field = $md->fetch_field()) {
			$params[] = &$row[$field->name];
		}
		return call_user_func_array(array($stmt, 'bind_result'), $params);
	}
	
    public function getPatient($patient_id) {
       $stmt = $this->conn->prepare("SELECT * FROM pinfo WHERE id = ?");
       $stmt->bind_param("i", $patient_id);
       if($stmt->execute()) {
			$patient_info = array();
            $this->db_bind_array($stmt, $patient_info);
			$stmt->fetch();
		   
			$stmt->close();
           return $patient_info;
       } else {
           return NULL;
       }
   }
   
    public function getAllStats($patient_id) {
		$result = array();
	
        $stmt = $this->conn->prepare("SELECT time, var, value FROM vstats WHERE id = ?");
        $stmt->bind_param("i", $patient_id);
		
        if($stmt->execute()){
			
			// Retrieve the data
			$stat = array();
			$this->db_bind_array($stmt, $stat);
			
			$stats = array();
			$count = 0;
            while($stmt->fetch()) {
				$count++;
				$tmp = array();
				$tmp["time"] = $stat["time"];
				$tmp["var"] = $stat["var"];
				$tmp["value"] = $stat["value"];
				
                array_push($stats, $tmp);
            }
			
			$stmt->close();
			
			$result["count"] = $count;
			$result["stats"] = $stats;
			
			return $result;
		}else{
			return NULL;
		}
    }
   
      public function getStat($patient_id, $stat) {
		$result = array();
	  
        $stmt = $this->conn->prepare("SELECT time, var, value FROM vstats WHERE id = ? AND var = ?");
        $stmt->bind_param("is", $patient_id, $stat);
		
        if($stmt->execute()){
			
			$stat = array();
			$this->db_bind_array($stmt, $stat);
			
			$stats = array();
			$count = 0;

            while($stmt->fetch()) {
				$count++;
				$tmp = array();
				$tmp["time"] = $stat["time"];
				$tmp["var"] = $stat["var"];
				$tmp["value"] = $stat["value"];
				
                array_push($stats, $tmp);
            }
			
			$stmt->close();
			
			$result["count"] = $count;
			$result["stats"] = $stats;
			
			return $result;
		}else{
			return NULL;
		}
    }
}
	
?>