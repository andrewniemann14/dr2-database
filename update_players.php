<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


function connect() {
  // gets secure DB login information
  $db_info = parse_ini_file('/home2/niemann8/kiskis/database.ini');
  $hostname = $db_info["hostname"];
  $database = $db_info["dr2_add_database"];
  $username = $db_info["dr2_add_username"];
  $password = $db_info["dr2_add_password"];

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
$pdo = connect();


$dir = '/home2/niemann8/dr2-data/';
foreach (scandir($dir) as $filename) {
  if (strpos($filename, "eaderboards_2")) {
    try {
      updatePlayers($pdo, $dir, $filename);
      rename($dir.$filename, $dir."backup/".$filename);
    } catch (Exception $e) {
      echo $e->getMessage();
    }
  }
}


function check_for_valid_name($element) {
  return ($element[2] != 'DiRT Player' && $element[2] != '');
}

function updatePlayers($pdo, $dir, $filename) {
  try {
    $leaderboardJson = file_get_contents($dir.$filename);
    $leaderboardData = json_decode($leaderboardJson);

    $entries_to_score = array_filter($leaderboardData, "check_for_valid_name");

    $stmt = $pdo->prepare("INSERT INTO players VALUES (?, ?, ?, 1) ON DUPLICATE KEY UPDATE points = points + ?, entries = entries + 1");
    $pdo->beginTransaction();
    // for each entry/name in yesterday's challenge results:
    foreach ($entries_to_score as $entry) {
      $name = $entry[2];
      $nationality = $entry[3];
      $points = $entry[8];

      $stmt->execute(array($name, $nationality, $points, $points));
    }
    $pdo->commit();
  } catch (Exception $e) {
    $pdo->rollBack();
    throw $e;
  }
}

?>