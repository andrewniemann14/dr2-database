<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$pdo = connect();

function connect() {
  // gets secure DB login information
  $db_info = parse_ini_file('/home2/niemann8/kiskis/database.ini');
  $hostname = $db_info["hostname"];
  $database = $db_info["dr2_add_database"];
  $username = $db_info["dr2_add_username"];
  $password = $db_info["dr2_add_password"];
  // $hostname = "localhost";
  // $database = "dr2";
  // $username = "root";
  // $password = "password";

  try {
    $pdo = new PDO("mysql:host=$hostname;dbname=$database", $username, $password);
    $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); // PDO uses fake prepared statements by default
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connection successful\n";
    return $pdo;
  } catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
  }
}


// FETCH ALL, CALCULATE SCORE, PREPARE FOR ALTERING
$stmt = $pdo->prepare("SELECT * FROM leaderboard");
$stmt->execute();

$all_records = array();

while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
  // id and placement are used to query and score is input
  $record = array();
  $record['challenge_id'] = $row['challenge_id'];
  $record['placement'] = $row['placement'];
  $record['score'] = get_score($row);
  array_push($all_records, $record);
}


foreach ($all_records as $record) {
  $stmt = $pdo->prepare("UPDATE leaderboard SET score = ? WHERE challenge_id = ? AND placement = ?");
  $stmt->execute(array($record['score'], $record['challenge_id'], $record['placement']));
}



function get_score($entry) {
  $time = $entry['time'];
  $time_split = explode(':', $time);
  $time = (floatval($time_split[0]) * 60) + floatval($time_split[1]);

  $diff = $entry['diff'];
  if ($diff == '--') {
    $diff = 0;
  } else {
    $diff_split = explode(':', trim($diff, '+'));
    $diff = (floatval($diff_split[0]) * 60) + floatval($diff_split[1]);
  }

  if ($diff >= ($time-$diff) ) {
    $score = 0;
  } else {
    $score = floatval(intval((1-($diff/($time-$diff))) * 10000)/100);
  }

  return $score;

}